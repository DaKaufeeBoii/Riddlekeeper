"""Exact backtracking solver for standard 9x9 Sudoku."""

from typing import List, Optional, Sequence, Tuple

from riddlekeeper.puzzles.base import SolveResult

SudokuState = Tuple[int, ...]


class SudokuPuzzle:
    puzzle_type = "sudoku"

    def __init__(self, rows: Sequence[Sequence[int]]):
        if len(rows) != 9 or any(len(row) != 9 for row in rows):
            raise ValueError("Sudoku board must be 9x9")
        if any(value not in range(10) for row in rows for value in row):
            raise ValueError("Sudoku cells must be integers from 0 to 9")
        self._initial = tuple(value for row in rows for value in row)
        self._validate_givens(self._initial)

    @staticmethod
    def _validate_givens(board: SudokuState) -> None:
        for i, value in enumerate(board):
            if not value:
                continue
            row, col = divmod(i, 9)
            peers = {row * 9 + c for c in range(9)} | {r * 9 + col for r in range(9)}
            br, bc = (row // 3) * 3, (col // 3) * 3
            peers |= {r * 9 + c for r in range(br, br + 3) for c in range(bc, bc + 3)}
            if any(j != i and board[j] == value for j in peers):
                raise ValueError("Sudoku givens contain a row, column, or box conflict")

    def initial_state(self) -> SudokuState:
        return self._initial

    def legal_actions(self, state: SudokuState) -> List[Tuple[int, int]]:
        best = None
        best_values = None
        for i, value in enumerate(state):
            if value:
                continue
            row, col = divmod(i, 9)
            used = set(state[row * 9:(row + 1) * 9])
            used.update(state[r * 9 + col] for r in range(9))
            br, bc = (row // 3) * 3, (col // 3) * 3
            used.update(state[r * 9 + c] for r in range(br, br + 3) for c in range(bc, bc + 3))
            candidates = [v for v in range(1, 10) if v not in used]
            if not candidates:
                return []
            if best_values is None or len(candidates) < len(best_values):
                best, best_values = i, candidates
                if len(candidates) == 1:
                    break
        return [(best, value) for value in best_values] if best is not None else []

    def apply(self, state: SudokuState, action: Tuple[int, int]) -> SudokuState:
        index, value = action
        if state[index] != 0 or action not in self.legal_actions(state):
            raise ValueError("Illegal Sudoku move")
        board = list(state)
        board[index] = value
        return tuple(board)

    def is_solved(self, state: SudokuState) -> bool:
        return 0 not in state and all(set(state[r * 9:(r + 1) * 9]) == set(range(1, 10)) for r in range(9))

    def state_key(self, state: SudokuState):
        return state

    @staticmethod
    def format(state: SudokuState) -> str:
        lines = []
        for r in range(9):
            row = state[r * 9:(r + 1) * 9]
            lines.append(" ".join(str(v) if v else "." for v in row[:3]) + " | " +
                         " ".join(str(v) if v else "." for v in row[3:6]) + " | " +
                         " ".join(str(v) if v else "." for v in row[6:]))
            if r in (2, 5):
                lines.append("------+-------+------")
        return "\n".join(lines)


class SudokuSolver:
    name = "sudoku-backtracking-mrv"

    def supports(self, puzzle_type: str) -> bool:
        return puzzle_type == "sudoku"

    def solve(self, puzzle: SudokuPuzzle) -> SolveResult[Tuple[int, int]]:
        explored = 0

        def search(state: SudokuState) -> Optional[SudokuState]:
            nonlocal explored
            explored += 1
            if puzzle.is_solved(state):
                return state
            moves = puzzle.legal_actions(state)
            if not moves:
                return None
            for move in moves:
                answer = search(puzzle.apply(state, move))
                if answer is not None:
                    return answer
            return None

        initial = puzzle.initial_state()
        solved = search(initial)
        return SolveResult(solved is not None, final_state=solved, explored_states=explored,
                           solver=self.name, message="Solved" if solved is not None else "No solution")
