import argparse
import sys
from pathlib import Path

# Ensure parent directory is on sys.path so 'riddlekeeper' package can always be imported
_repo_dir = Path(__file__).resolve().parent
if str(_repo_dir.parent) not in sys.path:
    sys.path.insert(0, str(_repo_dir.parent))
if str(_repo_dir) not in sys.path:
    sys.path.insert(0, str(_repo_dir))

from riddlekeeper.puzzles.flow import FlowBoard, FlowPuzzle
from riddlekeeper.puzzles.pipes import PipesBoard, PipesPuzzle
from riddlekeeper.puzzles.queens import QueensPuzzle
from riddlekeeper.puzzles.registry import default_registry
from riddlekeeper.puzzles.sokoban import SokobanBoard, SokobanPuzzle
from riddlekeeper.puzzles.sudoku import SudokuPuzzle
from riddlekeeper.puzzles.words import WordGrid, WordsPuzzle

SOLUTIONS_DIR = Path(__file__).resolve().parent / "puzzles" / "solutions"


SAMPLE_SUDOKU = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]


SAMPLE_SOKOBAN = """
######
#  . #
# $$ #
# .# #
#  @ #
######
""".strip()

SAMPLE_FLOW = [
    [1, 2, 0, 0, 0],
    [0, 3, 4, 5, 2],
    [0, 0, 0, 0, 5],
    [0, 0, 0, 0, 0],
    [1, 0, 0, 3, 4],
]

SAMPLE_PIPES = [
    ["L", "L"],
    ["L", "L"],
]

SAMPLE_WORDS_GRID = [
    ["C", "A", "T"],
    ["D", "O", "G"],
    ["F", "O", "X"],
]
SAMPLE_WORDS_LIST = ["CAT", "DOG", "FOX"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve a supported Riddlekeeper puzzle")
    parser.add_argument("puzzle", choices=("sudoku", "queens", "sokoban", "flow", "pipes", "words"))
    parser.add_argument("--size", type=int, default=8, help="N for N-Queens")
    args = parser.parse_args()

    if args.puzzle == "sudoku":
        puzzle = SudokuPuzzle(SAMPLE_SUDOKU)
    elif args.puzzle == "queens":
        puzzle = QueensPuzzle(args.size)
    elif args.puzzle == "sokoban":
        board = SokobanBoard.from_string(SAMPLE_SOKOBAN)
        puzzle = SokobanPuzzle(board)
    elif args.puzzle == "flow":
        board = FlowBoard.from_list(SAMPLE_FLOW)
        puzzle = FlowPuzzle(board)
    elif args.puzzle == "pipes":
        board = PipesBoard.from_list(SAMPLE_PIPES)
        puzzle = PipesPuzzle(board)
    elif args.puzzle == "words":
        grid = WordGrid.from_list(SAMPLE_WORDS_GRID)
        puzzle = WordsPuzzle(grid, SAMPLE_WORDS_LIST)
    else:
        raise ValueError("Unknown puzzle type")

    result = default_registry().solve(puzzle)
    print(f"Puzzle: {puzzle.puzzle_type}")
    print(f"Solver: {result.solver}")
    print(f"Result: {result.message}; explored {result.explored_states} states")

    lines = []
    lines.append(f"Puzzle: {puzzle.puzzle_type}")
    lines.append(f"Solver: {result.solver}")
    lines.append(f"Result: {result.message}; explored {result.explored_states} states")

    if result.solved and puzzle.puzzle_type == "sudoku":
        formatted = SudokuPuzzle.format(result.final_state)
        print(formatted)
        lines.append(formatted)
    elif result.solved and puzzle.puzzle_type == "queens":
        for row, col in enumerate(result.final_state):
            row_str = "." * col + "Q" + "." * (puzzle.size - col - 1)
            print(row_str)
            lines.append(row_str)
    elif result.solved and puzzle.puzzle_type == "sokoban":
        print(f"Actions: {len(result.actions)}")
        lines.append(f"Actions: {len(result.actions)}")
        if result.actions:
            act_str = " ".join(result.actions)
            print(act_str)
            lines.append(act_str)
    elif result.solved and puzzle.puzzle_type == "flow":
        for color_idx, path in enumerate(result.final_state):
            color = puzzle.board.all_colors[color_idx]
            p_str = f"Color {color} path: {' -> '.join(str(p) for p in path)}"
            print(p_str)
            lines.append(p_str)
    elif result.solved and puzzle.puzzle_type == "pipes":
        rot_str = f"Solved rotations (clock-wise 90 deg): {result.final_state}"
        print(rot_str)
        lines.append(rot_str)
    elif result.solved and puzzle.puzzle_type == "words":
        for word_idx, path in enumerate(result.final_state):
            w_str = f"Word '{puzzle.words[word_idx]}': {' -> '.join(str(p) for p in path)}"
            print(w_str)
            lines.append(w_str)

    if result.solved:
        SOLUTIONS_DIR.mkdir(parents=True, exist_ok=True)
        sol_file = SOLUTIONS_DIR / f"{puzzle.puzzle_type}_solution.txt"
        sol_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"[+] Solution stored in: {sol_file}")


if __name__ == "__main__":
    main()
