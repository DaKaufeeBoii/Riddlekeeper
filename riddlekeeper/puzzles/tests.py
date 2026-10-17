"""Comprehensive dependency-free regression test suite for Riddlekeeper.

Run with: python -m riddlekeeper.puzzles.tests
"""

import unittest

from riddlekeeper.agent.api import Agent, Request
from riddlekeeper.agent.orchestrator import AgentRequest, RiddlekeeperAgent
from riddlekeeper.puzzles.base import NoSolverFound
from riddlekeeper.puzzles.flow import FlowBoard, FlowPuzzle
from riddlekeeper.puzzles.pipes import PipesBoard, PipesPuzzle
from riddlekeeper.puzzles.queens import QueensPuzzle
from riddlekeeper.puzzles.registry import PuzzleRegistry, default_registry
from riddlekeeper.puzzles.sokoban import SokobanBoard, SokobanPuzzle
from riddlekeeper.puzzles.sudoku import SudokuPuzzle
from riddlekeeper.puzzles.words import WordGrid, WordsPuzzle
from riddlekeeper.solve import SAMPLE_SUDOKU


class PuzzleSolverTests(unittest.TestCase):
    # ==========================
    # Queens Tests
    # ==========================
    def test_eight_queens_solution_is_valid(self):
        puzzle = QueensPuzzle(8)
        result = default_registry().solve(puzzle)
        self.assertTrue(result.solved)
        self.assertEqual(len(result.final_state), 8)
        self.assertTrue(puzzle.is_solved(result.final_state))

    def test_four_queens_solution_is_valid(self):
        puzzle = QueensPuzzle(4)
        result = default_registry().solve(puzzle)
        self.assertTrue(result.solved)
        self.assertTrue(puzzle.is_solved(result.final_state))

    def test_two_queens_is_unsatisfiable(self):
        result = default_registry().solve(QueensPuzzle(2))
        self.assertFalse(result.solved)

    def test_queens_size_one_is_solved(self):
        puzzle = QueensPuzzle(1)
        result = default_registry().solve(puzzle)
        self.assertTrue(result.solved)
        self.assertTrue(puzzle.is_solved(result.final_state))

    def test_queens_invalid_size_rejected(self):
        with self.assertRaises(ValueError):
            QueensPuzzle(0)

    # ==========================
    # Sudoku Tests
    # ==========================
    def test_sample_sudoku_solution_is_valid(self):
        puzzle = SudokuPuzzle(SAMPLE_SUDOKU)
        result = default_registry().solve(puzzle)
        self.assertTrue(result.solved)
        self.assertTrue(puzzle.is_solved(result.final_state))

    def test_conflicting_sudoku_givens_are_rejected(self):
        bad = [row[:] for row in SAMPLE_SUDOKU]
        bad[0][2] = 5
        with self.assertRaises(ValueError):
            SudokuPuzzle(bad)

    def test_sudoku_invalid_dimensions_rejected(self):
        with self.assertRaises(ValueError):
            SudokuPuzzle([[1] * 9] * 8)
        with self.assertRaises(ValueError):
            SudokuPuzzle([[1] * 8] * 9)

    def test_sudoku_invalid_values_rejected(self):
        bad = [row[:] for row in SAMPLE_SUDOKU]
        bad[0][0] = 10
        with self.assertRaises(ValueError):
            SudokuPuzzle(bad)
        bad = [row[:] for row in SAMPLE_SUDOKU]
        bad[0][0] = -1
        with self.assertRaises(ValueError):
            SudokuPuzzle(bad)

    def test_sudoku_already_solved_returns_solved(self):
        solved_board = [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 9],
        ]
        puzzle = SudokuPuzzle(solved_board)
        result = default_registry().solve(puzzle)
        self.assertTrue(result.solved)
        self.assertTrue(puzzle.is_solved(result.final_state))

    # ==========================
    # Sokoban Tests
    # ==========================
    def test_sokoban_simple_solved(self):
        grid = """
#####
#@$.#
#####
"""
        b = SokobanBoard.from_string(grid)
        p = SokobanPuzzle(b)
        res = default_registry().solve(p)
        self.assertTrue(res.solved)
        self.assertTrue(p.is_solved(res.final_state))

    def test_sokoban_unsatisfiable_empty_path(self):
        grid = """
####
#@.$
####
"""
        b = SokobanBoard.from_string(grid)
        p = SokobanPuzzle(b)
        res = default_registry().solve(p)
        self.assertFalse(res.solved)

    def test_sokoban_already_solved_returns_solved(self):
        grid = """
#####
#@* #
#####
"""
        b = SokobanBoard.from_string(grid)
        p = SokobanPuzzle(b)
        res = default_registry().solve(p)
        self.assertTrue(res.solved)

    def test_sokoban_invalid_grid_rejected(self):
        with self.assertRaises(ValueError):
            SokobanBoard.from_string("")
        # Missing player
        with self.assertRaises(ValueError):
            SokobanBoard.from_string("#####\n# $.#\n#####")

    # ==========================
    # Flow Free Tests
    # ==========================
    def test_flow_simple_solved(self):
        board_list = [
            [1, 2, 3],
            [0, 0, 0],
            [1, 2, 3],
        ]
        board = FlowBoard.from_list(board_list)
        p = FlowPuzzle(board)
        res = default_registry().solve(p)
        self.assertTrue(res.solved)
        self.assertTrue(p.is_solved(res.final_state))

    def test_flow_already_solved(self):
        board_list = [
            [1, 2],
            [1, 2],
        ]
        board = FlowBoard.from_list(board_list)
        p = FlowPuzzle(board)
        res = default_registry().solve(p)
        self.assertTrue(res.solved)

    def test_flow_unsatisfiable(self):
        # Crossing colors in 2x2 grid cannot connect without intersection
        board_list = [
            [1, 2],
            [2, 1],
        ]
        board = FlowBoard.from_list(board_list)
        p = FlowPuzzle(board)
        res = default_registry().solve(p)
        self.assertFalse(res.solved)

    def test_flow_invalid_dimensions_rejected(self):
        with self.assertRaises(ValueError):
            FlowBoard.from_list([])
        with self.assertRaises(ValueError):
            FlowBoard.from_list([[1, 2], [1]])

    # ==========================
    # Pipes Tests
    # ==========================
    def test_pipes_simple_solved(self):
        rows = [
            ["L", "L"],
            ["L", "L"],
        ]
        b = PipesBoard.from_list(rows)
        p = PipesPuzzle(b)
        res = default_registry().solve(p)
        self.assertTrue(res.solved)
        self.assertTrue(p.is_solved(res.final_state))

    def test_pipes_already_solved(self):
        # Solved loop with exact orientations: (0, 1, 1, 0), (0, 0, 1, 1), (1, 1, 0, 0), (1, 0, 0, 1)
        rows = [
            ["RD", "DL"],
            ["UR", "UL"],
        ]
        b = PipesBoard.from_list(rows)
        p = PipesPuzzle(b)
        res = default_registry().solve(p)
        self.assertTrue(res.solved)

    def test_pipes_unsatisfiable(self):
        # Incompatible tiles (e.g. cross in corner that cannot satisfy boundary constraints)
        rows = [
            ["+", "L"],
            ["L", "L"],
        ]
        b = PipesBoard.from_list(rows)
        p = PipesPuzzle(b)
        res = default_registry().solve(p)
        self.assertFalse(res.solved)

    def test_pipes_invalid_board_rejected(self):
        with self.assertRaises(ValueError):
            PipesBoard.from_list([])
        with self.assertRaises(ValueError):
            PipesBoard.from_list([["L", "L"], ["L"]])

    # ==========================
    # Words Tests
    # ==========================
    def test_words_simple_solved(self):
        rows = [
            ["C", "A", "T"],
            ["D", "O", "G"],
            ["F", "O", "X"],
        ]
        grid = WordGrid.from_list(rows)
        p = WordsPuzzle(grid, ["CAT", "DOG", "FOX"])
        res = default_registry().solve(p)
        self.assertTrue(res.solved)
        self.assertTrue(p.is_solved(res.final_state))

    def test_words_already_solved(self):
        rows = [
            ["C", "A", "T"],
        ]
        grid = WordGrid.from_list(rows)
        p = WordsPuzzle(grid, ["CAT"])
        res = default_registry().solve(p)
        self.assertTrue(res.solved)

    def test_words_unsatisfiable_missing_word(self):
        rows = [
            ["C", "A", "T"],
        ]
        grid = WordGrid.from_list(rows)
        p = WordsPuzzle(grid, ["ZEBRA"])
        res = default_registry().solve(p)
        self.assertFalse(res.solved)

    def test_words_invalid_dimensions_rejected(self):
        with self.assertRaises(ValueError):
            WordGrid.from_list([])
        with self.assertRaises(ValueError):
            WordGrid.from_list([["A", "B"], ["A"]])
        with self.assertRaises(ValueError):
            WordsPuzzle(WordGrid.from_list([["A"]]), [])

    # ==========================
    # Registry & Agent Tests
    # ==========================
    def test_registry_unknown_puzzle_type_raises(self):
        registry = default_registry()

        class Dummy:
            puzzle_type = "nonexistent"

        with self.assertRaises(NoSolverFound):
            registry.solve(Dummy())

    def test_registry_duplicate_name_rejected(self):
        class DummySolver:
            name = "sudoku-backtracking-mrv"

            def supports(self, t):
                return False

            def solve(self, p):
                return None

        reg = PuzzleRegistry()
        reg.register(DummySolver())
        with self.assertRaises(ValueError):
            reg.register(DummySolver())

    def test_agent_orchestrator_state_limit(self):
        agent = RiddlekeeperAgent()
        puzzle = QueensPuzzle(8)
        req = AgentRequest("queens", puzzle, state_limit=5)
        res = agent.solve(req, puzzle)
        self.assertFalse(res.success)
        self.assertIn("State limit exceeded", res.message)

    def test_agent_orchestrator_successful_solve(self):
        agent = Agent()
        puzzle = QueensPuzzle(4)
        req = Request("queens", puzzle)
        res = agent.handle(req)
        self.assertTrue(res.success)
        self.assertTrue(res.validated)
        self.assertGreater(res.runtime_ms, 0.0)
        self.assertIn("Solution validated", res.trace)


if __name__ == "__main__":
    unittest.main()
