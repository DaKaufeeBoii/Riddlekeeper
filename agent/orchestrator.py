"""Agent orchestration: common request/result API with budgets, validation, and replanning."""

from dataclasses import dataclass, field
import time
from typing import Any, Callable, List, Optional

from riddlekeeper.puzzles.base import NoSolverFound, Puzzle, SolveResult
from riddlekeeper.puzzles.registry import PuzzleRegistry, default_registry


@dataclass
class AgentRequest:
    puzzle_type: str
    puzzle_data: Any
    time_limit_ms: Optional[int] = None
    state_limit: Optional[int] = None


@dataclass
class AgentTrace:
    events: List[str] = field(default_factory=list)


@dataclass
class AgentResult:
    success: bool
    solver: str = ""
    actions: List = field(default_factory=list)
    final_state: Any = None
    explored_states: int = 0
    runtime_ms: float = 0.0
    message: str = ""
    trace: AgentTrace = field(default_factory=AgentTrace)
    validated: bool = False


class RiddlekeeperAgent:
    def __init__(self, registry: Optional[PuzzleRegistry] = None):
        self.registry = registry or default_registry()

    def solve(self, request: AgentRequest, puzzle: Puzzle) -> AgentResult:
        trace = AgentTrace(events=[])
        start_time = time.perf_counter()
        try:
            solver = self.registry.for_type(request.puzzle_type)
            trace.events.append(f"Selected solver: {solver.name}")

            if request.time_limit_ms is not None and request.time_limit_ms <= 0:
                return AgentResult(success=False, solver=solver.name,
                                   message="Time limit exceeded before solving",
                                   trace=trace)
            if request.state_limit is not None and request.state_limit <= 0:
                return AgentResult(success=False, solver=solver.name,
                                   message="State limit exceeded before solving",
                                   trace=trace)

            result = solver.solve(puzzle)
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0

            if request.time_limit_ms is not None and elapsed_ms > request.time_limit_ms:
                trace.events.append(f"Time limit exceeded: {elapsed_ms:.2f}ms > {request.time_limit_ms}ms")
                return AgentResult(
                    success=False,
                    solver=result.solver,
                    actions=[],
                    final_state=None,
                    explored_states=result.explored_states,
                    runtime_ms=elapsed_ms,
                    message="Time limit exceeded",
                    trace=trace,
                )

            if request.state_limit is not None and result.explored_states > request.state_limit:
                trace.events.append(f"State limit exceeded: {result.explored_states} > {request.state_limit}")
                return AgentResult(
                    success=False,
                    solver=result.solver,
                    actions=[],
                    final_state=None,
                    explored_states=result.explored_states,
                    runtime_ms=elapsed_ms,
                    message="State limit exceeded",
                    trace=trace,
                )

            trace.events.append("Solution computed")

            # Validate solution independently
            validated = False
            if result.solved and result.final_state is not None:
                try:
                    validated = puzzle.is_solved(result.final_state)
                    trace.events.append("Solution validated")
                except Exception as ex:
                    validated = False
                    trace.events.append(f"Validation error: {ex}")

            return AgentResult(
                success=result.solved and validated,
                solver=result.solver,
                actions=result.actions,
                final_state=result.final_state,
                explored_states=result.explored_states,
                runtime_ms=elapsed_ms,
                message=result.message,
                trace=trace,
                validated=validated,
            )
        except NoSolverFound:
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            trace.events.append("No solver found")
            return AgentResult(success=False, runtime_ms=elapsed_ms, message="No solver found", trace=trace)
        except Exception as e:
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            trace.events.append(f"Error: {e}")
            return AgentResult(success=False, runtime_ms=elapsed_ms, message=str(e), trace=trace)

    def replan_execute(
        self,
        puzzle_env: Any,
        puzzle_factory: Callable[[Any], Puzzle],
        puzzle_type: str,
        max_steps: int = 50,
        time_limit_ms: Optional[int] = 5000,
    ) -> AgentResult:
        """Iterative replanning loop for environments where actions are executed step-by-step.

        If a step fails or is blocked, re-solves from current environment state.
        """
        trace = AgentTrace(events=["Starting replan execution loop"])
        total_actions_executed = []
        start_time = time.perf_counter()

        step_count = 0
        while step_count < max_steps:
            step_count += 1
            # Check if environment is already at goal
            if hasattr(puzzle_env, "agent_pos") and hasattr(puzzle_env, "goal_pos"):
                if puzzle_env.agent_pos == puzzle_env.goal_pos:
                    elapsed_ms = (time.perf_counter() - start_time) * 1000.0
                    trace.events.append(f"Goal reached in {step_count - 1} steps")
                    return AgentResult(
                        success=True,
                        actions=total_actions_executed,
                        final_state=puzzle_env.agent_pos,
                        runtime_ms=elapsed_ms,
                        message="Goal reached successfully via replanning",
                        trace=trace,
                        validated=True,
                    )

            # Build puzzle from current env state
            current_puzzle = puzzle_factory(puzzle_env)
            req = AgentRequest(puzzle_type=puzzle_type, puzzle_data=current_puzzle, time_limit_ms=time_limit_ms)
            res = self.solve(req, current_puzzle)

            if not res.success or not res.actions:
                elapsed_ms = (time.perf_counter() - start_time) * 1000.0
                trace.events.append(f"Failed to find plan at step {step_count}")
                return AgentResult(
                    success=False,
                    actions=total_actions_executed,
                    runtime_ms=elapsed_ms,
                    message="Replanning failed to find path",
                    trace=trace,
                )

            # Execute the next action in the plan
            next_action = res.actions[0]
            total_actions_executed.append(next_action)
            _, _, done, info = puzzle_env.step(next_action)
            trace.events.append(f"Step {step_count}: executed action {next_action}")

            if done:
                elapsed_ms = (time.perf_counter() - start_time) * 1000.0
                trace.events.append("Environment finished")
                return AgentResult(
                    success=True,
                    actions=total_actions_executed,
                    final_state=getattr(puzzle_env, "agent_pos", None),
                    runtime_ms=elapsed_ms,
                    message="Environment goal reached",
                    trace=trace,
                    validated=True,
                )

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        trace.events.append("Max step limit reached")
        return AgentResult(
            success=False,
            actions=total_actions_executed,
            runtime_ms=elapsed_ms,
            message="Max steps exceeded without reaching goal",
            trace=trace,
        )
