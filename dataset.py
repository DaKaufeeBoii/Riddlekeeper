"""
Riddlekeeper Dataset Generator.
Synthesizes procedural grid puzzle instances, oracle optimal actions,
valid move masks, and ground-truth distance maps for Bellman-Ford value alignment.
"""

import random
from typing import Dict, List, Optional, Tuple
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from riddlekeeper.environment import GridWorldEnv


class GridNavigationDataset(Dataset):
    """
    In-memory dataset of procedurally generated Grid Navigation instances.
    Each sample contains:
    - state_tensor: (4, H, W)
    - action_mask: (4,) boolean
    - oracle_action: int in {0, 1, 2, 3}
    - distance_map: (1, H, W) BFS distance in unit moves
    - distance_mask: reachable traversable cells used for value supervision
    """

    def __init__(
        self,
        num_samples: int = 1000,
        grid_size: int = 5,
        obstacle_density: float = 0.15,
        seed: Optional[int] = None
    ):
        self.num_samples = num_samples
        self.grid_size = grid_size
        self.obstacle_density = obstacle_density
        self.seed = seed

        self.samples: List[Dict[str, torch.Tensor]] = []
        self._generate_dataset()

    def _generate_dataset(self):
        rng = random.Random(self.seed)
        env = GridWorldEnv(
            height=self.grid_size,
            width=self.grid_size,
            obstacle_density=self.obstacle_density,
            seed=self.seed
        )

        count = 0
        while count < self.num_samples:
            env.reset(new_layout=True)
            # Traverse a few steps or use current configuration
            optimal_action = env.get_optimal_action()
            if optimal_action is None:
                # A no-op state has no policy label and cannot train a 4-way
                # action classifier. Regenerate rather than spin forever on
                # tiny grids or unusual obstacle settings.
                continue

            # Record sample
            state_tensor = env.get_symbolic_tensor()
            action_mask = env.get_valid_action_mask()
            
            # Keep oracle distances in the same unit scale as Bellman-Ford
            # propagation (one per move).
            dist_map = env.distance_map.copy()
            # Walls and unreachable cells are excluded from value supervision.
            valid = dist_map >= 0
            dist_map[~valid] = 0.0
            distance_map = torch.from_numpy(dist_map).unsqueeze(0).float()
            distance_mask = torch.from_numpy(valid).unsqueeze(0)

            self.samples.append({
                "state": state_tensor,
                "action_mask": action_mask,
                "action": torch.tensor(optimal_action, dtype=torch.long),
                "distance_map": distance_map,
                "distance_mask": distance_mask
            })
            count += 1

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, idx: int) -> Dict[str, torch.Tensor]:
        return self.samples[idx]


def get_dataloaders(
    train_size: int = 1000,
    val_size: int = 200,
    grid_size: int = 5,
    obstacle_density: float = 0.15,
    batch_size: int = 32,
    seed: int = 42
) -> Tuple[DataLoader, DataLoader]:
    """Creates training and validation dataloaders for grid navigation."""
    train_ds = GridNavigationDataset(
        num_samples=train_size,
        grid_size=grid_size,
        obstacle_density=obstacle_density,
        seed=seed
    )
    val_ds = GridNavigationDataset(
        num_samples=val_size,
        grid_size=grid_size,
        obstacle_density=obstacle_density,
        seed=seed + 1000
    )
    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False)
    return train_loader, val_loader
