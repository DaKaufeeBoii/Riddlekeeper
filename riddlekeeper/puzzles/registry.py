"""Solver registry and first-pass puzzle routing."""

from typing import List

from riddlekeeper.puzzles.base import NoSolverFound, PuzzleSolver


class PuzzleRegistry:
    def __init__(self) -> None:
        self._solvers: List[PuzzleSolver] = []

    def register(self, solver: PuzzleSolver) -> None:
        if any(existing.name == solver.name for existing in self._solvers):
            raise ValueError(f"Solver already registered: {solver.name}")
        self._solvers.append(solver)

    def for_type(self, puzzle_type: str) -> PuzzleSolver:
        for solver in self._solvers:
            if solver.supports(puzzle_type):
                return solver
        raise NoSolverFound(f"No solver registered for puzzle type: {puzzle_type}")

    def solve(self, puzzle):
        return self.for_type(puzzle.puzzle_type).solve(puzzle)

    @property
    def solver_names(self) -> List[str]:
        return [solver.name for solver in self._solvers]


def default_registry() -> PuzzleRegistry:
    """Create registry with the currently implemented logic puzzle solvers."""
    from riddlekeeper.puzzles.queens import QueensSolver
    from riddlekeeper.puzzles.sudoku import SudokuSolver
    try:
        from riddlekeeper.puzzles.sokoban import SokobanSolver
    except Exception:  # pragma: no cover
        SokobanSolver = None
    try:
        from riddlekeeper.puzzles.flow import FlowSolver
    except Exception:  # pragma: no cover
        FlowSolver = None
    try:
        from riddlekeeper.puzzles.pipes import PipesSolver
    except Exception:  # pragma: no cover
        PipesSolver = None
    try:
        from riddlekeeper.puzzles.words import WordsSolver
    except Exception:  # pragma: no cover
        WordsSolver = None
    try:
        from riddlekeeper.puzzles.grid_navigation import GridNavigationSolver
    except Exception:  # pragma: no cover
        GridNavigationSolver = None

    registry = PuzzleRegistry()
    registry.register(SudokuSolver())
    registry.register(QueensSolver())
    if SokobanSolver is not None:
        registry.register(SokobanSolver())
    if FlowSolver is not None:
        registry.register(FlowSolver())
    if PipesSolver is not None:
        registry.register(PipesSolver())
    if WordsSolver is not None:
        registry.register(WordsSolver())
    if GridNavigationSolver is not None:
        registry.register(GridNavigationSolver())
    return registry
