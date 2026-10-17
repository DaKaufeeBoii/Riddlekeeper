"""Exact backtracking solver for the N-Queens puzzle."""

from typing import List, Optional, Tuple

from riddlekeeper.puzzles.base import SolveResult

QueensState = Tuple[int, ...]  # queen column for each filled row


class QueensPuzzle:
    puzzle_type = "queens"

    def __init__(self, size: int = 8):
        if size < 1:
            raise ValueError("Board size must be positive")
        self.size = size

    def initial_state(self) -> QueensState:
        return ()

    def legal_actions(self, state: QueensState) -> List[int]:
        row = len(state)
        if row >= self.size:
            return []
        return [col for col in range(self.size)
                if all(col != old_col and abs(col - old_col) != row - old_row
                       for old_row, old_col in enumerate(state))]

    def apply(self, state: QueensState, action: int) -> QueensState:
        if action not in self.legal_actions(state):
            raise ValueError("Illegal queen placement")
        return state + (action,)

    def is_solved(self, state: QueensState) -> bool:
        return len(state) == self.size

    def state_key(self, state: QueensState):
        return state


class QueensSolver:
    name = "queens-backtracking"

    def supports(self, puzzle_type: str) -> bool:
        return puzzle_type == "queens"

    def solve(self, puzzle: QueensPuzzle) -> SolveResult[int]:
        explored = 0

        def search(state: QueensState) -> Optional[QueensState]:
            nonlocal explored
            explored += 1
            if puzzle.is_solved(state):
                return state
            for col in puzzle.legal_actions(state):
                answer = search(puzzle.apply(state, col))
                if answer is not None:
                    return answer
            return None

        answer = search(puzzle.initial_state())
        return SolveResult(answer is not None, final_state=answer, explored_states=explored,
                           solver=self.name, message="Solved" if answer is not None else "No solution")
