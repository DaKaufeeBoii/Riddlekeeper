"""
Riddlekeeper GridWorld Environment.
Defines procedural grid navigation with symbolic tensor representations,
deterministic state transitions, and BFS-based optimal oracle computation.
"""

from collections import deque
import random
from typing import Dict, List, Optional, Tuple
import numpy as np
import torch

# Action Definitions
ACTION_UP = 0
ACTION_DOWN = 1
ACTION_LEFT = 2
ACTION_RIGHT = 3

ACTION_NAMES = {
    ACTION_UP: "UP",
    ACTION_DOWN: "DOWN",
    ACTION_LEFT: "LEFT",
    ACTION_RIGHT: "RIGHT",
}

ACTION_DELTAS = {
    ACTION_UP: (-1, 0),
    ACTION_DOWN: (1, 0),
    ACTION_LEFT: (0, -1),
    ACTION_RIGHT: (0, 1),
}


class GridWorldEnv:
    """Configurable 2D Grid Navigation Environment for Riddlekeeper.

    Provides symbolic multi-channel tensor representations and BFS oracle paths.
    """

    def __init__(
        self,
        height: int = 5,
        width: int = 5,
        obstacle_density: float = 0.15,
        max_steps: Optional[int] = None,
        seed: Optional[int] = None,
    ):
        self.height = height
        self.width = width
        self.obstacle_density = obstacle_density
        self.max_steps = max_steps or (height * width * 2)
        self.rng = random.Random(seed)

        self.grid = np.zeros((self.height, self.width), dtype=np.int32)
        # 0: Free, 1: Wall
        self.agent_pos = (0, 0)
        self.goal_pos = (height - 1, width - 1)
        self.step_count = 0
        self.distance_map = np.full((self.height, self.width), -1.0, dtype=np.float32)

        self.reset()

    def reset(self, new_layout: bool = True) -> torch.Tensor:
        """Resets the environment.

        If new_layout is True, generates a new solvable maze/grid.
        """
        self.step_count = 0
        if new_layout:
            self._generate_solvable_grid()
        self._compute_distance_map()
        return self.get_symbolic_tensor()

    def _generate_solvable_grid(self, max_attempts: int = 100):
        """Generates a random grid with guaranteed path from agent to goal."""
        for _ in range(max_attempts):
            grid = np.zeros((self.height, self.width), dtype=np.int32)
            num_cells = self.height * self.width
            num_walls = int(num_cells * self.obstacle_density)

            all_coords = [(r, c) for r in range(self.height) for c in range(self.width)]
            self.rng.shuffle(all_coords)

            agent = all_coords[0]
            goal = all_coords[1]

            # Remaining coords can be walls
            candidate_walls = all_coords[2:]
            wall_indices = candidate_walls[:num_walls]
            for r, c in wall_indices:
                grid[r, c] = 1

            # Check reachability via BFS
            dist_map = self._bfs(grid, goal)
            if dist_map[agent] != -1:
                self.grid = grid
                self.agent_pos = agent
                self.goal_pos = goal
                return

        # Fallback to an empty grid with agent at (0,0) and goal at (H-1, W-1)
        self.grid = np.zeros((self.height, self.width), dtype=np.int32)
        self.agent_pos = (0, 0)
        self.goal_pos = (self.height - 1, self.width - 1)

    def _bfs(self, grid: np.ndarray, target: Tuple[int, int]) -> np.ndarray:
        """Computes shortest distance from every cell to target using BFS."""
        h, w = grid.shape
        dist = np.full((h, w), -1.0, dtype=np.float32)
        if grid[target] == 1:
            return dist

        queue = deque([target])
        dist[target] = 0.0

        while queue:
            cr, cc = queue.popleft()
            d = dist[cr, cc]
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = cr + dr, cc + dc
                if 0 <= nr < h and 0 <= nc < w:
                    if grid[nr, nc] == 0 and dist[nr, nc] == -1:
                        dist[nr, nc] = d + 1.0
                        queue.append((nr, nc))
        return dist

    def _compute_distance_map(self):
        """Calculates distance map from all cells to the goal position."""
        self.distance_map = self._bfs(self.grid, self.goal_pos)

    def get_symbolic_tensor(self) -> torch.Tensor:
        """Generates a 4-channel symbolic grid tensor of shape (4, H, W).

        Channel 0: Walls / Obstacles (1 if wall, 0 otherwise)
        Channel 1: Agent Position (1 at agent, 0 elsewhere)
        Channel 2: Goal Position (1 at goal, 0 elsewhere)
        Channel 3: Free Traversable Space (1 if free, 0 if wall)
        """
        walls = (self.grid == 1).astype(np.float32)
        agent = np.zeros((self.height, self.width), dtype=np.float32)
        agent[self.agent_pos] = 1.0
        goal = np.zeros((self.height, self.width), dtype=np.float32)
        goal[self.goal_pos] = 1.0
        free_space = (self.grid == 0).astype(np.float32)

        stacked = np.stack([walls, agent, goal, free_space], axis=0)
        return torch.from_numpy(stacked)

    def get_valid_action_mask(self, pos: Optional[Tuple[int, int]] = None) -> torch.Tensor:
        """Returns a 4-element boolean tensor indicating valid non-wall moves."""
        r, c = pos if pos is not None else self.agent_pos
        mask = [False, False, False, False]
        for a in [ACTION_UP, ACTION_DOWN, ACTION_LEFT, ACTION_RIGHT]:
            dr, dc = ACTION_DELTAS[a]
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.height and 0 <= nc < self.width:
                if self.grid[nr, nc] == 0:
                    mask[a] = True
        return torch.tensor(mask, dtype=torch.bool)

    def get_optimal_action(self) -> Optional[int]:
        """Oracle: Determines the optimal next action via BFS distance gradient."""
        if self.agent_pos == self.goal_pos:
            return None

        r, c = self.agent_pos
        current_dist = self.distance_map[r, c]
        if current_dist <= 0:
            return None

        best_action = None
        best_dist = float("inf")

        for a in [ACTION_UP, ACTION_DOWN, ACTION_LEFT, ACTION_RIGHT]:
            dr, dc = ACTION_DELTAS[a]
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.height and 0 <= nc < self.width:
                if self.grid[nr, nc] == 0:
                    d = self.distance_map[nr, nc]
                    if 0 <= d < best_dist:
                        best_dist = d
                        best_action = a

        return best_action

    def get_oracle_trajectory(self) -> List[int]:
        """Computes the complete optimal sequence of actions from agent to goal."""
        trajectory = []
        curr = self.agent_pos
        visited = {curr}

        while curr != self.goal_pos:
            r, c = curr
            best_a = None
            best_dist = float("inf")
            next_pos = None

            for a in [ACTION_UP, ACTION_DOWN, ACTION_LEFT, ACTION_RIGHT]:
                dr, dc = ACTION_DELTAS[a]
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.height and 0 <= nc < self.width and self.grid[nr, nc] == 0:
                    d = self.distance_map[nr, nc]
                    if 0 <= d < best_dist and (nr, nc) not in visited:
                        best_dist = d
                        best_a = a
                        next_pos = (nr, nc)

            if best_a is None or next_pos is None:
                break
            trajectory.append(best_a)
            visited.add(next_pos)
            curr = next_pos

        return trajectory

    def step(self, action: int) -> Tuple[torch.Tensor, float, bool, Dict]:
        """Applies action, updates agent position, and returns step information."""
        self.step_count += 1
        dr, dc = ACTION_DELTAS[action]
        nr, nc = self.agent_pos[0] + dr, self.agent_pos[1] + dc

        info = {"hit_wall": False, "out_of_bounds": False}

        if 0 <= nr < self.height and 0 <= nc < self.width:
            if self.grid[nr, nc] == 0:
                self.agent_pos = (nr, nc)
            else:
                info["hit_wall"] = True
        else:
            info["out_of_bounds"] = True

        done = (self.agent_pos == self.goal_pos) or (self.step_count >= self.max_steps)
        reward = 10.0 if (self.agent_pos == self.goal_pos) else -0.1

        return self.get_symbolic_tensor(), reward, done, info

    def render_ascii(self) -> str:
        """Returns an ASCII visual representation of the grid state."""
        chars = []
        for r in range(self.height):
            row_str = []
            for c in range(self.width):
                if (r, c) == self.agent_pos and (r, c) == self.goal_pos:
                    row_str.append(" * ")
                elif (r, c) == self.agent_pos:
                    row_str.append(" A ")
                elif (r, c) == self.goal_pos:
                    row_str.append(" G ")
                elif self.grid[r, c] == 1:
                    row_str.append("###")
                else:
                    row_str.append(" . ")
            chars.append("".join(row_str))
        return "\n".join(chars)
