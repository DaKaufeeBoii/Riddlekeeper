"""Puzzle solver interfaces and built-in exact solvers."""

import sys
from pathlib import Path

_repo_dir = Path(__file__).resolve().parents[1]
if str(_repo_dir.parent) not in sys.path:
    sys.path.insert(0, str(_repo_dir.parent))
if str(_repo_dir) not in sys.path:
    sys.path.insert(0, str(_repo_dir))

from riddlekeeper.puzzles.base import Puzzle, PuzzleSolver, SolveResult
from riddlekeeper.puzzles.registry import PuzzleRegistry, default_registry

__all__ = ["Puzzle", "PuzzleSolver", "SolveResult", "PuzzleRegistry", "default_registry"]
