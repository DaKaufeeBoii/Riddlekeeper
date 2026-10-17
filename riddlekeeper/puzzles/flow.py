"""Solver for Flow Free puzzles (grid with color endpoints and full-board coverage)."""

from collections import deque
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple

from riddlekeeper.puzzles.base import SolveResult

Position = Tuple[int, int]
Color = int
FlowAction = Tuple[int, Position]  # (color_index, next_position)
FlowState = Tuple[Tuple[Position, ...], ...]  # tuple of paths for all_colors


@dataclass(frozen=True)
class FlowBoard:
    size: int
    endpoints: Dict[Color, Tuple[Position, Position]]
    grid_colors: Dict[Position, Color]
    all_colors: Tuple[Color, ...]

    @classmethod
    def from_list(cls, rows: List[List[int]]) -> "FlowBoard":
        if not rows or any(len(r) != len(rows) for r in rows):
            raise ValueError("Flow board must be square")
        size = len(rows)
        endpoints: Dict[Color, List[Position]] = {}
        for r in range(size):
            for c in range(size):
                v = rows[r][c]
                if v != 0:
                    endpoints.setdefault(v, []).append((r, c))
        for color, positions in endpoints.items():
            if len(positions) != 2:
                raise ValueError(f"Flow color {color} must have exactly 2 endpoints")
        all_colors = tuple(sorted(endpoints.keys()))
        return cls(
            size=size,
            endpoints={c: (endpoints[c][0], endpoints[c][1]) for c in all_colors},
            grid_colors={(r, c): rows[r][c] for r in range(size) for c in range(size) if rows[r][c] != 0},
            all_colors=all_colors,
        )


class FlowPuzzle:
    puzzle_type = "flow"

    def __init__(self, board: FlowBoard):
        self.board = board

    def initial_state(self) -> FlowState:
        return tuple((self.board.endpoints[c][0],) for c in self.board.all_colors)

    def _neighbors(self, r: int, c: int) -> List[Position]:
        res = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.board.size and 0 <= nc < self.board.size:
                res.append((nr, nc))
        return res

    def legal_actions(self, state: FlowState) -> List[FlowAction]:
        # Find the first color whose path has not reached its target endpoint
        active_idx = -1
        for i, color in enumerate(self.board.all_colors):
            target = self.board.endpoints[color][1]
            if state[i][-1] != target:
                active_idx = i
                break

        if active_idx == -1:
            return []

        color = self.board.all_colors[active_idx]
        target = self.board.endpoints[color][1]
        head = state[active_idx][-1]

        # Occupied cells by any path so far
        occupied: Set[Position] = {p for path in state for p in path}
        # Other endpoints that cannot be stepped on
        other_endpoints: Set[Position] = set()
        for c, (e1, e2) in self.board.endpoints.items():
            if c != color:
                other_endpoints.add(e1)
                other_endpoints.add(e2)

        actions: List[FlowAction] = []
        for nr, nc in self._neighbors(head[0], head[1]):
            pos = (nr, nc)
            if pos == target:
                actions.append((active_idx, pos))
            elif pos not in occupied and pos not in other_endpoints:
                actions.append((active_idx, pos))

        return actions

    def apply(self, state: FlowState, action: FlowAction) -> FlowState:
        color_idx, pos = action
        paths = list(state)
        paths[color_idx] = paths[color_idx] + (pos,)
        return tuple(paths)

    def is_solved(self, state: FlowState) -> bool:
        used: Set[Position] = set()
        for i, color in enumerate(self.board.all_colors):
            path = state[i]
            if not path:
                return False
            e1, e2 = self.board.endpoints[color]
            # Must connect e1 and e2
            if not ((path[0] == e1 and path[-1] == e2) or (path[0] == e2 and path[-1] == e1)):
                return False
            # Verify connectivity step by step
            for idx in range(len(path) - 1):
                p1, p2 = path[idx], path[idx + 1]
                if abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) != 1:
                    return False
            for pos in path:
                if pos in used:
                    return False
                used.add(pos)
        # All cells must be covered
        return len(used) == self.board.size * self.board.size

    def state_key(self, state: FlowState):
        return state


class FlowSolver:
    name = "flow-search"

    def supports(self, puzzle_type: str) -> bool:
        return puzzle_type == "flow"

    def solve(self, puzzle: FlowPuzzle, max_states: int = 100000) -> SolveResult[FlowAction]:
        explored = 0

        # Precompute endpoint sets
        board = puzzle.board
        endpoints_set = set()
        for e1, e2 in board.endpoints.values():
            endpoints_set.add(e1)
            endpoints_set.add(e2)

        def has_dead_ends(occupied: Set[Position], current_head: Position, unreached_heads: Set[Position]) -> bool:
            # Quick dead end check: an unvisited cell must have >= 2 available neighbors (or >= 1 if it is an unreached endpoint)
            for r in range(board.size):
                for c in range(board.size):
                    pos = (r, c)
                    if pos in occupied:
                        continue
                    is_endpoint = (pos in endpoints_set)
                    req = 1 if is_endpoint else 2
                    avail = 0
                    for nr, nc in puzzle._neighbors(r, c):
                        npos = (nr, nc)
                        if npos not in occupied or npos == current_head or npos in unreached_heads:
                            avail += 1
                    if avail < req:
                        return True
            return False

        def search(state: FlowState, actions_so_far: List[FlowAction]) -> Optional[Tuple[FlowState, List[FlowAction]]]:
            nonlocal explored
            explored += 1
            if explored > max_states:
                return None

            if puzzle.is_solved(state):
                return state, actions_so_far

            legal = puzzle.legal_actions(state)
            if not legal:
                return None

            occupied: Set[Position] = {p for path in state for p in path}
            active_idx = legal[0][0]
            color = board.all_colors[active_idx]
            target = board.endpoints[color][1]

            unreached_heads = {
                state[i][-1]
                for i, col in enumerate(board.all_colors)
                if state[i][-1] != board.endpoints[col][1]
            }

            for act in legal:
                nxt = puzzle.apply(state, act)
                new_head = act[1]
                # Prune if this move created isolated empty cells
                if new_head != target:
                    new_occupied = occupied | {new_head}
                    if has_dead_ends(new_occupied, new_head, unreached_heads):
                        continue

                ans = search(nxt, actions_so_far + [act])
                if ans is not None:
                    return ans

            return None

        start = puzzle.initial_state()
        if puzzle.is_solved(start):
            return SolveResult(
                solved=True,
                actions=[],
                final_state=start,
                explored_states=1,
                solver=self.name,
                message="Already solved",
            )

        res = search(start, [])
        if res is not None:
            final_st, actions = res
            return SolveResult(
                solved=True,
                actions=actions,
                final_state=final_st,
                explored_states=explored,
                solver=self.name,
                message="Solved",
            )
        return SolveResult(
            solved=False,
            actions=[],
            final_state=None,
            explored_states=explored,
            solver=self.name,
            message="No solution found",
        )
