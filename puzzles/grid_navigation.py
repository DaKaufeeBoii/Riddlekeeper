"""Adapter that exposes the existing Riddlekeeper grid as a puzzle plugin."""

from riddlekeeper.puzzles.base import SolveResult
from riddlekeeper.solver import shortest_path


class GridNavigationSolver:
    name = "grid-navigation-bfs"

    def supports(self, puzzle_type: str) -> bool:
        return puzzle_type == "grid_navigation"

    def solve(self, puzzle) -> SolveResult[int]:
        path = shortest_path(puzzle)
        if path is None:
            return SolveResult(False, solver=self.name, message="No path to goal")
        return SolveResult(True, actions=path, solver=self.name,
                           explored_states=0, message="Solved optimally")
