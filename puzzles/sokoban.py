"""Exact solver for Sokoban puzzles."""

from collections import deque
from dataclasses import dataclass
from typing import List, Optional, Sequence, Set, Tuple

from riddlekeeper.puzzles.base import SolveResult

Position = Tuple[int, int]
SokobanState = Tuple[int, int, Tuple[Position, ...]]  # (pr, pc, boxes_tuple)


@dataclass(frozen=True)
class SokobanBoard:
    width: int
    height: int
    walls: Tuple[Position, ...]
    goals: Tuple[Position, ...]
    player_start: Position
    boxes_start: Tuple[Position, ...]

    @classmethod
    def from_string(cls, grid: str) -> "SokobanBoard":
        lines = [line for line in grid.splitlines()]
        # remove trailing empty lines that don't affect board
        while lines and lines[-1] == "":
            lines.pop()
        if not lines:
            raise ValueError("Empty Sokoban grid")
        height = len(lines)
        width = max(len(line) for line in lines) if height else 0
        walls: List[Position] = []
        goals: List[Position] = []
        player_start: Optional[Position] = None
        boxes_start: List[Position] = []
        for r, line in enumerate(lines):
            for c in range(width):
                if c < len(line):
                    ch = line[c]
                else:
                    ch = " "
                if ch == "#":
                    walls.append((r, c))
                elif ch == "@":
                    player_start = (r, c)
                elif ch == "+":
                    player_start = (r, c)
                    goals.append((r, c))
                elif ch == "$":
                    boxes_start.append((r, c))
                elif ch == "*":
                    boxes_start.append((r, c))
                    goals.append((r, c))
                elif ch == ".":
                    goals.append((r, c))
                elif ch == " ":
                    pass
                else:
                    # treat unknown as empty space
                    pass
        if player_start is None:
            raise ValueError("Sokoban grid missing player start")
        return cls(
            width=width,
            height=height,
            walls=tuple(walls),
            goals=tuple(goals),
            player_start=player_start,
            boxes_start=tuple(sorted(boxes_start)),
        )


class SokobanPuzzle:
    puzzle_type = "sokoban"

    def __init__(self, board: SokobanBoard):
        self.board = board
        self._initial_boxes = tuple(sorted(board.boxes_start))

    def initial_state(self) -> SokobanState:
        pr, pc = self.board.player_start
        return (pr, pc, self._initial_boxes)

    def _is_wall(self, r: int, c: int) -> bool:
        return (r, c) in self.board.walls

    def legal_actions(self, state: SokobanState) -> List[str]:
        pr, pc, boxes = state
        box_set: Set[Position] = set(boxes)
        actions: List[str] = []
        dirs_map = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}
        # Moves
        for name, (dr, dc) in dirs_map.items():
            nr, nc = pr + dr, pc + dc
            if nr < 0 or nr >= self.board.height or nc < 0 or nc >= self.board.width:
                continue
            if self._is_wall(nr, nc) or (nr, nc) in box_set:
                continue
            actions.append(name)
        # Pushes
        for name, (dr, dc) in dirs_map.items():
            nr, nc = pr + dr, pc + dc
            if (nr, nc) not in box_set:
                continue
            bn_r, bn_c = nr + dr, nc + dc
            if bn_r < 0 or bn_r >= self.board.height or bn_c < 0 or bn_c >= self.board.width:
                continue
            if self._is_wall(bn_r, bn_c) or (bn_r, bn_c) in box_set:
                continue
            actions.append(f"push_{name}")
        return actions

    def apply(self, state: SokobanState, action: str) -> SokobanState:
        if action not in self.legal_actions(state):
            raise ValueError("Illegal Sokoban move")
        pr, pc, boxes = state
        dirs_map = {
            "up": (-1, 0),
            "down": (1, 0),
            "left": (0, -1),
            "right": (0, 1),
            "push_up": (-1, 0),
            "push_down": (1, 0),
            "push_left": (0, -1),
            "push_right": (0, 1),
        }
        dr, dc = dirs_map[action]
        if action.startswith("push_"):
            nr, nc = pr + dr, pc + dc
            bn_r, bn_c = nr + dr, nc + dc
            new_boxes = tuple(sorted(b for b in boxes if b != (nr, nc)) + [(bn_r, bn_c)])
            return (nr, nc, new_boxes)
        else:
            nr, nc = pr + dr, pc + dc
            return (nr, nc, boxes)

    def is_solved(self, state: SokobanState) -> bool:
        _, _, boxes = state
        goals_set = set(self.board.goals)
        return all(b in goals_set for b in boxes)

    def state_key(self, state: SokobanState) -> SokobanState:
        return state


    def is_deadlock(self, state: SokobanState, deadlock_corners: Set[Position]) -> bool:
        _, _, boxes = state
        return any(b in deadlock_corners for b in boxes)


class SokobanSolver:
    name = "sokoban-astar"

    def supports(self, puzzle_type: str) -> bool:
        return puzzle_type == "sokoban"

    def _precompute_deadlocks(self, puzzle: SokobanPuzzle) -> Set[Position]:
        deadlocks: Set[Position] = set()
        goals_set = set(puzzle.board.goals)
        h, w = puzzle.board.height, puzzle.board.width

        for r in range(h):
            for c in range(w):
                pos = (r, c)
                if puzzle._is_wall(r, c) or pos in goals_set:
                    continue
                # Check 4 corner combinations
                up_wall = puzzle._is_wall(r - 1, c) or (r == 0)
                down_wall = puzzle._is_wall(r + 1, c) or (r == h - 1)
                left_wall = puzzle._is_wall(r, c - 1) or (c == 0)
                right_wall = puzzle._is_wall(r, c + 1) or (c == w - 1)

                if (up_wall and left_wall) or (up_wall and right_wall) or (down_wall and left_wall) or (down_wall and right_wall):
                    deadlocks.add(pos)
        return deadlocks

    def _heuristic(self, boxes: Tuple[Position, ...], goals: Tuple[Position, ...]) -> int:
        total = 0
        for br, bc in boxes:
            min_d = min(abs(br - gr) + abs(bc - gc) for gr, gc in goals) if goals else 0
            total += min_d
        return total

    def solve(self, puzzle: SokobanPuzzle, max_states: int = 200000) -> SolveResult[str]:
        import heapq
        explored = 0
        start = puzzle.initial_state()
        if puzzle.is_solved(start):
            return SolveResult(
                solved=True,
                actions=[],
                final_state=start,
                explored_states=0,
                solver=self.name,
                message="Solved",
            )

        deadlocks = self._precompute_deadlocks(puzzle)
        goals = puzzle.board.goals

        visited = {puzzle.state_key(start)}
        # Heap item: (f_score, g_cost, counter, state, path)
        counter = 0
        h_start = self._heuristic(start[2], goals)
        heap = [(h_start, 0, counter, start, [])]

        while heap and explored < max_states:
            _, g_cost, _, current, path = heapq.heappop(heap)
            explored += 1

            for move in puzzle.legal_actions(current):
                nxt = puzzle.apply(current, move)
                k = puzzle.state_key(nxt)
                if k in visited:
                    continue

                # Prune corner deadlocks
                if any(b in deadlocks for b in nxt[2]):
                    continue

                new_path = path + [move]
                if puzzle.is_solved(nxt):
                    return SolveResult(
                        solved=True,
                        actions=new_path,
                        final_state=nxt,
                        explored_states=explored,
                        solver=self.name,
                        message="Solved",
                    )
                visited.add(k)
                counter += 1
                nxt_h = self._heuristic(nxt[2], goals)
                heapq.heappush(heap, (g_cost + 1 + nxt_h, g_cost + 1, counter, nxt, new_path))

        return SolveResult(
            solved=False,
            actions=[],
            final_state=None,
            explored_states=explored,
            solver=self.name,
            message="No solution found within state limit",
        )
