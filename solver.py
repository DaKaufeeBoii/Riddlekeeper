"""Exact reference solver for Riddlekeeper grid puzzles.

The search is deliberately independent of PyTorch, so it can serve as a
reliable baseline and keep the interactive demo usable without model weights.
"""

from collections import deque
from typing import List, Optional, Tuple

from riddlekeeper.environment import ACTION_DELTAS, GridWorldEnv


def shortest_path(env: GridWorldEnv) -> Optional[List[int]]:
    """Return an optimal action sequence for the current grid, or None."""
    start = env.agent_pos
    goal = env.goal_pos
    if start == goal:
        return []

    queue = deque([start])
    parent = {start: (None, None)}
    while queue:
        pos = queue.popleft()
        for action, (dr, dc) in ACTION_DELTAS.items():
            nxt = (pos[0] + dr, pos[1] + dc)
            if not (0 <= nxt[0] < env.height and 0 <= nxt[1] < env.width):
                continue
            if env.grid[nxt] != 0 or nxt in parent:
                continue
            parent[nxt] = (pos, action)
            if nxt == goal:
                path = []
                cursor = goal
                while cursor != start:
                    previous, step = parent[cursor]
                    path.append(step)
                    cursor = previous
                return list(reversed(path))
            queue.append(nxt)
    return None


def run_shortest_path(env: GridWorldEnv) -> Tuple[bool, int, Optional[int]]:
    """Execute an optimal path; return (success, steps, optimal_length)."""
    path = shortest_path(env)
    if path is None:
        return False, 0, None
    for action in path:
        _, _, done, _ = env.step(action)
        if done:
            break
    return env.agent_pos == env.goal_pos, len(path), len(path)
