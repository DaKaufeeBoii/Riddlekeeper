"""Dependency-free contracts shared by puzzle parsers and solvers."""

from dataclasses import dataclass, field
from typing import Any, Generic, List, Optional, Protocol, TypeVar

StateT = TypeVar("StateT")
ActionT = TypeVar("ActionT")


class Puzzle(Protocol[StateT, ActionT]):
    """A structured puzzle instance with explicit rules and legal actions."""

    @property
    def puzzle_type(self) -> str: ...

    def initial_state(self) -> StateT: ...

    def legal_actions(self, state: StateT) -> List[ActionT]: ...

    def apply(self, state: StateT, action: ActionT) -> StateT: ...

    def is_solved(self, state: StateT) -> bool: ...

    def state_key(self, state: StateT) -> Any: ...


class PuzzleSolver(Protocol[StateT, ActionT]):
    """Solver plugin for one or more puzzle types."""

    @property
    def name(self) -> str: ...

    def supports(self, puzzle_type: str) -> bool: ...

    def solve(self, puzzle: Puzzle[StateT, ActionT]) -> "SolveResult[ActionT]": ...


@dataclass
class SolveResult(Generic[ActionT]):
    solved: bool
    actions: List[ActionT] = field(default_factory=list)
    final_state: Any = None
    explored_states: int = 0
    solver: str = ""
    message: str = ""


class NoSolverFound(LookupError):
    """Raised when no registered solver claims a puzzle type."""

