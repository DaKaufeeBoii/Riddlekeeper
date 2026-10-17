"""Common request/result API for agent interaction."""

from dataclasses import dataclass, field
from typing import Any, Callable, List, Optional

from riddlekeeper.agent.orchestrator import AgentRequest, AgentResult, RiddlekeeperAgent
from riddlekeeper.puzzles.registry import PuzzleRegistry


@dataclass
class Request:
    puzzle_type: str
    data: Any
    time_limit_ms: Optional[int] = None
    state_limit: Optional[int] = None


@dataclass
class Result:
    success: bool
    solver: str = ""
    actions: List = field(default_factory=list)
    final_state: Any = None
    explored_states: int = 0
    runtime_ms: float = 0.0
    message: str = ""
    trace: List[str] = field(default_factory=list)
    validated: bool = False


class Agent:
    def __init__(self, registry: Optional[PuzzleRegistry] = None):
        self._agent = RiddlekeeperAgent(registry=registry)

    def handle(self, request: Request) -> Result:
        puzzle = request.data
        res = self._agent.solve(
            AgentRequest(request.puzzle_type, request.data, request.time_limit_ms, request.state_limit),
            puzzle,
        )
        return Result(
            success=res.success,
            solver=res.solver,
            actions=res.actions,
            final_state=res.final_state,
            explored_states=res.explored_states,
            runtime_ms=res.runtime_ms,
            message=res.message,
            trace=res.trace.events,
            validated=res.validated,
        )

    def replan_execute(
        self,
        puzzle_env: Any,
        puzzle_factory: Callable[[Any], Any],
        puzzle_type: str,
        max_steps: int = 50,
        time_limit_ms: Optional[int] = 5000,
    ) -> Result:
        res = self._agent.replan_execute(
            puzzle_env=puzzle_env,
            puzzle_factory=puzzle_factory,
            puzzle_type=puzzle_type,
            max_steps=max_steps,
            time_limit_ms=time_limit_ms,
        )
        return Result(
            success=res.success,
            solver=res.solver,
            actions=res.actions,
            final_state=res.final_state,
            explored_states=res.explored_states,
            runtime_ms=res.runtime_ms,
            message=res.message,
            trace=res.trace.events,
            validated=res.validated,
        )
