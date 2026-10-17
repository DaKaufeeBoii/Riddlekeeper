"""Exact Bellman-Ford grid solver and a learned CNN policy baseline."""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Tuple, Optional


class BellmanFordLayer(nn.Module):
    """
    One exact unit-cost Bellman-Ford relaxation over four-neighbor grids.
    """
    def __init__(self, channels: int = 16):
        super().__init__()
        # Keep the public constructor compatible; the exact shortest-path
        # relaxation below has one shared unit edge cost and no learned weights.
        self.channels = channels

    def forward(self, h: torch.Tensor, walls: torch.Tensor) -> torch.Tensor:
        """
        h: (B, C, H, W) current distance / potential field
        walls: (B, 1, H, W) 1.0 for walls, 0.0 for free space
        """
        b, c, h_dim, w_dim = h.shape
        # Use a large boundary value instead of replicate padding: an edge must
        # not accidentally inherit the value of the border cell itself.
        padded_h = F.pad(h, (1, 1, 1, 1), mode="constant", value=1e6)
        padded_walls = F.pad(walls, (1, 1, 1, 1), mode="constant", value=1.0)

        neighbor_values = []
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            r0, c0 = 1 + dr, 1 + dc
            values = padded_h[:, :, r0:r0 + h_dim, c0:c0 + w_dim]
            blocked = padded_walls[:, :, r0:r0 + h_dim, c0:c0 + w_dim] > 0.5
            neighbor_values.append(values.masked_fill(blocked, 1e6))

        min_neighbor = torch.stack(neighbor_values, dim=0).amin(dim=0)
        updated_h = torch.minimum(h, min_neighbor + 1.0)
        return updated_h.masked_fill(walls > 0.5, 1e6)


class BellmanFordGNN(nn.Module):
    """
    Algorithmic Reasoner:
    Propagates shortest-path distance field from goal, then selects the neighbor
    minimizing distance to goal.
    """

    def __init__(self, in_channels: int = 4, hidden_dim: int = 16, default_k: int = 12):
        super().__init__()
        self.in_channels = in_channels
        self.hidden_dim = hidden_dim
        self.default_k = default_k

        # The recurrence is an exact, parameter-free Bellman-Ford relaxation.
        self.bf_layer = BellmanFordLayer(channels=hidden_dim)

    def forward(
        self,
        x: torch.Tensor,
        num_steps: Optional[int] = None,
        action_mask: Optional[torch.Tensor] = None
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Args:
            x: (B, 4, H, W) [walls, agent, goal, free]
            num_steps: Recurrent message passing depth
            action_mask: (B, 4) boolean mask of valid moves
        """
        b, c, h, w = x.shape
        if num_steps is None:
            num_steps = max(self.default_k, 2 * (h + w))

        walls = x[:, 0:1, :, :]  # (B, 1, H, W)
        agent = x[:, 1, :, :]    # (B, H, W)
        goal = x[:, 2:3, :, :]   # (B, 1, H, W)

        # Initialize distance field: 0.0 at goal, infinity elsewhere.
        init_dist = torch.where(goal > 0.5, torch.zeros_like(goal), torch.full_like(goal, 1e6))
        h_field = init_dist.repeat(1, self.hidden_dim, 1, 1)

        # Iterative message passing (Bellman-Ford update)
        # Bellman-Ford needs at most V-1 relaxations for a simple shortest path.
        # Honor a caller's smaller depth for experiments but never exceed the
        # useful bound (and allow explicit num_steps=0).
        steps = min(max(0, num_steps), max(0, h * w - 1))
        for _ in range(steps):
            h_field = self.bf_layer(h_field, walls)

        # All repeated channels carry the same exact distance values.
        val_map = h_field[:, :1]
        # Goal cell is strictly 0
        val_map = torch.where(goal > 0.5, torch.zeros_like(val_map), val_map)

        # Action prediction: Extract neighbor values around the agent
        padded = F.pad(val_map, (1, 1, 1, 1), mode="constant", value=1e6)
        neighbor_maps = torch.stack([
            padded[:, :, 0:h, 1:w + 1], padded[:, :, 2:h + 2, 1:w + 1],
            padded[:, :, 1:h + 1, 0:w], padded[:, :, 1:h + 1, 2:w + 2]
        ], dim=1)  # (B, 4, 1, H, W)
        # Gather each action's neighboring value at the agent's cell.
        action_logits = -(neighbor_maps[:, :, 0] * agent[:, None]).sum(dim=(-1, -2))

        if action_mask is not None:
            action_logits = action_logits.masked_fill(~action_mask, -1e9)

        return action_logits, val_map


class BaselineCNNPolicy(nn.Module):
    """
    Standard Baseline CNN + Global Pooling + MLP Policy.
    """
    def __init__(self, in_channels: int = 4, hidden_dim: int = 32):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(in_channels, hidden_dim, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(hidden_dim, hidden_dim, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(hidden_dim, hidden_dim, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d((1, 1))
        )
        self.fc = nn.Sequential(
            nn.Linear(hidden_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 4)
        )

    def forward(
        self,
        x: torch.Tensor,
        action_mask: Optional[torch.Tensor] = None
    ) -> Tuple[torch.Tensor, None]:
        b = x.shape[0]
        feat = self.conv(x).view(b, -1)
        logits = self.fc(feat)
        if action_mask is not None:
            logits = logits.masked_fill(~action_mask, -1e9)
        return logits, None
