"""Puzzle solver interfaces and built-in exact solvers."""

from riddlekeeper.puzzles.base import Puzzle, PuzzleSolver, SolveResult
from riddlekeeper.puzzles.registry import PuzzleRegistry, default_registry

__all__ = ["Puzzle", "PuzzleSolver", "SolveResult", "PuzzleRegistry", "default_registry"]
