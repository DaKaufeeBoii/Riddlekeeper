"""Solver for word and Wend puzzles (letter grid path finding and dictionary matching)."""

from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple

from riddlekeeper.puzzles.base import SolveResult

Position = Tuple[int, int]
WordPath = Tuple[Position, ...]
WordsState = Tuple[Optional[WordPath], ...]  # Path for each target word in puzzle.words


@dataclass(frozen=True)
class WordGrid:
    width: int
    height: int
    grid: Tuple[Tuple[str, ...], ...]

    @classmethod
    def from_list(cls, rows: List[List[str]]) -> "WordGrid":
        if not rows:
            raise ValueError("Word grid must not be empty")
        width = len(rows[0])
        if width == 0 or any(len(r) != width for r in rows):
            raise ValueError("Word grid must be rectangular")
        height = len(rows)
        # Store as uppercase characters
        grid_tuple = tuple(tuple(rows[r][c].upper() for c in range(width)) for r in range(height))
        return cls(width=width, height=height, grid=grid_tuple)


class WordsPuzzle:
    puzzle_type = "words"

    def __init__(self, grid: WordGrid, words: List[str], allow_diagonal: bool = True, disallow_overlap: bool = False):
        if not words:
            raise ValueError("Word list must not be empty")
        self.grid = grid
        self.words = [w.strip().upper() for w in words]
        self.allow_diagonal = allow_diagonal
        self.disallow_overlap = disallow_overlap

    def initial_state(self) -> WordsState:
        return tuple(None for _ in self.words)

    def _neighbors(self, r: int, c: int) -> List[Position]:
        deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        if self.allow_diagonal:
            deltas += [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        res = []
        for dr, dc in deltas:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.grid.height and 0 <= nc < self.grid.width:
                res.append((nr, nc))
        return res

    def legal_actions(self, state: WordsState) -> List[Tuple[int, WordPath]]:
        # Find next unplaced word
        next_idx = -1
        for i, p in enumerate(state):
            if p is None:
                next_idx = i
                break
        if next_idx == -1:
            return []

        word = self.words[next_idx]
        used_cells: Set[Position] = set()
        if self.disallow_overlap:
            for p in state:
                if p is not None:
                    used_cells.update(p)

        valid_paths = self._find_paths_for_word(word, used_cells)
        return [(next_idx, p) for p in valid_paths]

    def _find_paths_for_word(self, word: str, forbidden: Set[Position]) -> List[WordPath]:
        if not word:
            return []
        h, w = self.grid.height, self.grid.width
        results: List[WordPath] = []

        def dfs(idx: int, curr_pos: Position, path: List[Position]):
            if idx == len(word):
                results.append(tuple(path))
                return
            for nr, nc in self._neighbors(curr_pos[0], curr_pos[1]):
                npos = (nr, nc)
                if npos not in forbidden and npos not in path:
                    if self.grid.grid[nr][nc] == word[idx]:
                        dfs(idx + 1, npos, path + [npos])

        first_char = word[0]
        for r in range(h):
            for c in range(w):
                pos = (r, c)
                if pos not in forbidden and self.grid.grid[r][c] == first_char:
                    dfs(1, pos, [pos])

        return results

    def apply(self, state: WordsState, action: Tuple[int, WordPath]) -> WordsState:
        idx, path = action
        lst = list(state)
        lst[idx] = path
        return tuple(lst)

    def is_solved(self, state: WordsState) -> bool:
        if len(state) != len(self.words):
            return False
        if any(p is None for p in state):
            return False

        used_cells: Set[Position] = set()
        for i, word in enumerate(self.words):
            path = state[i]
            if path is None or len(path) != len(word):
                return False
            # Verify letters match
            for char_idx, pos in enumerate(path):
                r, c = pos
                if not (0 <= r < self.grid.height and 0 <= c < self.grid.width):
                    return False
                if self.grid.grid[r][c] != word[char_idx]:
                    return False

            # Verify consecutive steps are neighbors
            for step_idx in range(len(path) - 1):
                p1, p2 = path[step_idx], path[step_idx + 1]
                dr = abs(p1[0] - p2[0])
                dc = abs(p1[1] - p2[1])
                max_d = max(dr, dc)
                if max_d != 1 or (not self.allow_diagonal and dr + dc != 1):
                    return False

            if self.disallow_overlap:
                for pos in path:
                    if pos in used_cells:
                        return False
                    used_cells.add(pos)

        return True

    def state_key(self, state: WordsState):
        return state


class WordsSolver:
    name = "words-search"

    def supports(self, puzzle_type: str) -> bool:
        return puzzle_type in ("words", "wend", "wordsearch")

    def solve(self, puzzle: WordsPuzzle, max_states: int = 100000) -> SolveResult[Tuple[int, WordPath]]:
        explored = 0

        def search(state: WordsState, actions: List[Tuple[int, WordPath]]) -> Optional[Tuple[WordsState, List[Tuple[int, WordPath]]]]:
            nonlocal explored
            explored += 1
            if explored > max_states:
                return None

            if puzzle.is_solved(state):
                return state, actions

            legal = puzzle.legal_actions(state)
            if not legal:
                return None

            for act in legal:
                nxt = puzzle.apply(state, act)
                res = search(nxt, actions + [act])
                if res is not None:
                    return res

            return None

        init_st = puzzle.initial_state()
        if puzzle.is_solved(init_st):
            return SolveResult(
                solved=True,
                actions=[],
                final_state=init_st,
                explored_states=1,
                solver=self.name,
                message="Already solved",
            )

        ans = search(init_st, [])
        if ans is not None:
            final_st, actions = ans
            return SolveResult(
                solved=True,
                actions=actions,
                final_state=final_st,
                explored_states=explored,
                solver=self.name,
                message="Solved",
            )

        return SolveResult(
            solved=False,
            actions=[],
            final_state=None,
            explored_states=explored,
            solver=self.name,
            message="No solution found",
        )
