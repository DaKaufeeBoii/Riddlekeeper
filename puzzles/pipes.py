"""Solver for Pipes puzzles (pipe network connectivity and rotation)."""

from collections import deque
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple

from riddlekeeper.puzzles.base import SolveResult

# Directions: 0: Up, 1: Right, 2: Down, 3: Left
Connection = Tuple[int, int, int, int]  # (up, right, down, left), each 0 or 1
PipesState = Tuple[int, ...]  # Rotation (0, 1, 2, 3) for each cell index r * width + c


def rotate_connection(conn: Connection, steps: int) -> Connection:
    """Rotates connection 90 degrees clockwise 'steps' times."""
    steps = steps % 4
    u, r, d, l = conn
    for _ in range(steps):
        u, r, d, l = l, u, r, d
    return (u, r, d, l)


def parse_pipe_str(pipe: str) -> Connection:
    """Parses a string token into a base (up, right, down, left) connection tuple."""
    p = pipe.strip().upper()
    if p in ("", "E", "EMPTY", "."):
        return (0, 0, 0, 0)
    if p in ("+", "CROSS"):
        return (1, 1, 1, 1)
    if p in ("I", "LINE", "|"):
        return (1, 0, 1, 0)
    if p in ("-",):
        return (0, 1, 0, 1)
    if p in ("L", "CORNER"):
        return (1, 1, 0, 0)
    if p in ("T",):
        return (1, 1, 1, 0)
    if p in ("C", "END", "O"):
        return (1, 0, 0, 0)

    # Direction-based string e.g. "UR", "DL", "URD"
    u = 1 if "U" in p else 0
    r = 1 if "R" in p else 0
    d = 1 if "D" in p else 0
    l = 1 if "L" in p else 0
    return (u, r, d, l)


@dataclass(frozen=True)
class PipesBoard:
    width: int
    height: int
    grid: Tuple[Tuple[str, ...], ...]
    initial_connections: Tuple[Connection, ...]

    @classmethod
    def from_list(cls, rows: List[List[str]]) -> "PipesBoard":
        if not rows:
            raise ValueError("Pipes board must not be empty")
        height = len(rows)
        width = len(rows[0]) if height else 0
        for r in rows:
            if len(r) != width:
                raise ValueError("Pipes board must be rectangular")

        grid_tuple = tuple(tuple(rows[r][c] for c in range(width)) for r in range(height))
        conns: List[Connection] = []
        for r in range(height):
            for c in range(width):
                conns.append(parse_pipe_str(grid_tuple[r][c]))

        return cls(
            width=width,
            height=height,
            grid=grid_tuple,
            initial_connections=tuple(conns)
        )


class PipesPuzzle:
    puzzle_type = "pipes"

    def __init__(self, board: PipesBoard):
        self.board = board

    def initial_state(self) -> PipesState:
        # Default starting state: 0 rotations applied to every cell
        return tuple(0 for _ in range(self.board.height * self.board.width))

    def legal_actions(self, state: PipesState) -> List[Tuple[int, int]]:
        # Actions for the next unplaced cell index
        # Find first cell with non-empty options, or cell-by-cell placement
        return [(idx, rot) for idx in range(len(state)) for rot in (1, 2, 3)]

    def apply(self, state: PipesState, action: Tuple[int, int]) -> PipesState:
        idx, rot = action
        lst = list(state)
        lst[idx] = (lst[idx] + rot) % 4
        return tuple(lst)

    def is_solved(self, state: PipesState) -> bool:
        h, w = self.board.height, self.board.width
        conns: List[Connection] = []
        non_empty = []

        for idx, rot in enumerate(state):
            c = rotate_connection(self.board.initial_connections[idx], rot)
            conns.append(c)
            if any(c):
                non_empty.append(idx)

        # 1. Boundary and neighbor alignment checks
        for r in range(h):
            for c in range(w):
                idx = r * w + c
                u, right, d, l = conns[idx]

                # Boundary: cannot connect outside
                if r == 0 and u == 1:
                    return False
                if r == h - 1 and d == 1:
                    return False
                if c == 0 and l == 1:
                    return False
                if c == w - 1 and right == 1:
                    return False

                # Neighbor connectivity: outgoing connection must be met with incoming
                if r > 0 and u != conns[(r - 1) * w + c][2]:
                    return False
                if c > 0 and l != conns[r * w + c - 1][1]:
                    return False

        if not non_empty:
            return True

        # 2. Single connected component check for non-empty pipes
        start_node = non_empty[0]
        visited: Set[int] = {start_node}
        queue = deque([start_node])

        while queue:
            curr = queue.popleft()
            r, c = divmod(curr, w)
            u, right, d, l = conns[curr]

            neighbors = []
            if u and r > 0:
                neighbors.append((r - 1) * w + c)
            if right and c < w - 1:
                neighbors.append(r * w + c + 1)
            if d and r < h - 1:
                neighbors.append((r + 1) * w + c)
            if l and c > 0:
                neighbors.append(r * w + c - 1)

            for n in neighbors:
                if n not in visited:
                    visited.add(n)
                    queue.append(n)

        return len(visited) == len(non_empty)

    def state_key(self, state: PipesState):
        return state


class PipesSolver:
    name = "pipes-search"

    def supports(self, puzzle_type: str) -> bool:
        return puzzle_type == "pipes"

    def solve(self, puzzle: PipesPuzzle, max_states: int = 100000) -> SolveResult[Tuple[int, int]]:
        explored = 0
        h, w = puzzle.board.height, puzzle.board.width
        num_cells = h * w
        initial_conns = puzzle.board.initial_connections

        current_rotations = [0] * num_cells

        def backtrack(cell_idx: int) -> Optional[PipesState]:
            nonlocal explored
            explored += 1
            if explored > max_states:
                return None

            if cell_idx == num_cells:
                st = tuple(current_rotations)
                if puzzle.is_solved(st):
                    return st
                return None

            r, c = divmod(cell_idx, w)
            base_conn = initial_conns[cell_idx]

            # If empty cell, rotation doesn't matter (0 is enough)
            if not any(base_conn):
                current_rotations[cell_idx] = 0
                res = backtrack(cell_idx + 1)
                if res is not None:
                    return res
                return None

            # Distinct rotations for symmetric tiles
            # Cross: 1 distinct orientation; Line: 2 distinct orientations; others: 4
            if base_conn == (1, 1, 1, 1):
                allowed_rotations = [0]
            elif base_conn in ((1, 0, 1, 0), (0, 1, 0, 1)):
                allowed_rotations = [0, 1]
            else:
                allowed_rotations = [0, 1, 2, 3]

            for rot in allowed_rotations:
                conn = rotate_connection(base_conn, rot)
                u, right, d, l = conn

                # Boundary constraints
                if r == 0 and u != 0:
                    continue
                if r == h - 1 and d != 0:
                    continue
                if c == 0 and l != 0:
                    continue
                if c == w - 1 and right != 0:
                    continue

                # Match with top neighbor
                if r > 0:
                    top_conn = rotate_connection(initial_conns[(r - 1) * w + c], current_rotations[(r - 1) * w + c])
                    if u != top_conn[2]:
                        continue

                # Match with left neighbor
                if c > 0:
                    left_conn = rotate_connection(initial_conns[r * w + c - 1], current_rotations[r * w + c - 1])
                    if l != left_conn[1]:
                        continue

                current_rotations[cell_idx] = rot
                res = backtrack(cell_idx + 1)
                if res is not None:
                    return res

            return None

        # Check if initial state is already solved
        init_st = puzzle.initial_state()
        if puzzle.is_solved(init_st):
            return SolveResult(
                solved=True,
                actions=[],
                final_state=init_st,
                explored_states=1,
                solver=self.name,
                message="Already solved",
            )

        sol = backtrack(0)
        if sol is not None:
            # Action list: rotations needed for each cell
            actions = [(i, sol[i]) for i in range(num_cells) if sol[i] != 0]
            return SolveResult(
                solved=True,
                actions=actions,
                final_state=sol,
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
