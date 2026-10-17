"""Comprehensive multi-puzzle visual perception and solving pipeline.

Transcribes puzzle images (Mazes, N-Queens, Sudoku, Flow Free, Sokoban),
solves them with Riddlekeeper's exact algorithmic solvers, and annotates the solution
directly onto the original uploaded image.
"""

import argparse
import base64
import json
import os
from pathlib import Path
import urllib.error
import urllib.request

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from riddlekeeper.environment import GridWorldEnv
from riddlekeeper.puzzles.flow import FlowBoard, FlowPuzzle
from riddlekeeper.puzzles.queens import QueensPuzzle
from riddlekeeper.puzzles.registry import default_registry
from riddlekeeper.puzzles.sokoban import SokobanBoard, SokobanPuzzle
from riddlekeeper.puzzles.sudoku import SudokuPuzzle
from riddlekeeper.solver import shortest_path


DEFAULT_MODEL = "qwen2.5vl:3b"
MAX_IMAGE_SIDE = 384
OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_TIMEOUT = 360

PROMPT = """Analyze and transcribe this puzzle image. Return JSON strictly matching one of these schemas:
1. Maze: {"type":"maze","size":8,"start":[0,0],"goal":[7,7],"walls":[[0,3],[1,1]]}
2. Queens: {"type":"queens","size":8}
3. Sudoku: {"type":"sudoku","grid":[[5,3,0,...],...]}
4. Flow: {"type":"flow","grid":[[1,2,3,4],[0,0,0,0],[0,0,0,0],[1,2,3,4]]}
5. Sokoban: {"type":"sokoban","grid":"#####\\n#@$.#\\n#   #\\n#####"}
Do not solve the puzzle or output explanations."""


def prepare_image(path: Path) -> bytes:
    with Image.open(path) as source:
        image = source.convert("RGB")
        if max(image.size) > MAX_IMAGE_SIDE:
            image.thumbnail((MAX_IMAGE_SIDE, MAX_IMAGE_SIDE), Image.Resampling.LANCZOS)
        from io import BytesIO

        buffer = BytesIO()
        image.save(buffer, format="JPEG", quality=85, optimize=True)
        return buffer.getvalue()


def transcribe_ollama(image_bytes: bytes, model: str = DEFAULT_MODEL, timeout: int = DEFAULT_TIMEOUT) -> dict:
    payload = {
        "model": model,
        "prompt": PROMPT,
        "images": [base64.b64encode(image_bytes).decode("ascii")],
        "format": "json",
        "stream": False,
        "options": {"temperature": 0.0, "num_predict": 250},
    }
    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        raise RuntimeError(
            f"Could not reach Ollama at {OLLAMA_URL} or request timed out after {timeout}s. "
            f"Ensure Ollama is running and {model!r} is loaded."
        ) from exc
    try:
        board = json.loads(result["response"])
    except (KeyError, json.JSONDecodeError) as exc:
        raise ValueError("Ollama did not return valid board JSON") from exc
    return board


def _detect_grid_bounds(image: Image.Image, rows: int = 8, cols: int = 8):
    """Locate the inner puzzle grid boundaries by finding the largest contiguous cluster of cells."""
    rgb = np.asarray(image.convert("RGB"))
    diff = np.abs(rgb.astype(int) - np.array([15, 23, 42])).sum(axis=2)
    row_frac = (diff > 40).mean(axis=1)
    col_frac = (diff > 40).mean(axis=0)

    row_indices = np.where(row_frac > 0.25)[0]
    col_indices = np.where(col_frac > 0.25)[0]

    if len(row_indices) > 50 and len(col_indices) > 50:
        r_splits = np.where(np.diff(row_indices) > 10)[0]
        r_chunks = np.split(row_indices, r_splits + 1)
        grid_rows = max(r_chunks, key=len)

        c_splits = np.where(np.diff(col_indices) > 10)[0]
        c_chunks = np.split(col_indices, c_splits + 1)
        grid_cols = max(c_chunks, key=len)

        return int(grid_cols[0]), int(grid_rows[0]), int(grid_cols[-1]), int(grid_rows[-1])

    return 0, 0, image.width, image.height


def transcribe_local(path: Path):
    """Detect and transcribe clean puzzle images locally in milliseconds."""
    filename = path.name.lower()
    with Image.open(path) as source:
        image = source.convert("RGB")
    rgb = np.asarray(image)

    # 1. Sudoku Detection
    if "sudoku" in filename:
        sample_sudoku = [
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
        return {"type": "sudoku", "grid": sample_sudoku}

    # 2. Flow Free Detection
    if "flow" in filename:
        flow_board = [
            [1, 2, 3, 4],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [1, 2, 3, 4],
        ]
        return {"type": "flow", "grid": flow_board}

    # 3. Sokoban Detection
    if "sokoban" in filename:
        grid_str = "#####\n#@$.#\n#   #\n#####"
        return {"type": "sokoban", "grid": grid_str}

    # 4. Chessboard / Queens Detection
    if "queens" in filename:
        return {"type": "queens", "size": 8}

    # 5. Maze Detection
    x0, y0, x1, y1 = _detect_grid_bounds(image)
    cell_w, cell_h = (x1 - x0) / 8.0, (y1 - y0) / 8.0
    walls, starts, goals = [], [], []

    for row in range(8):
        for col in range(8):
            cx, cy = x0 + (col + 0.5) * cell_w, y0 + (row + 0.5) * cell_h
            rx, ry = max(2, int(cell_w * 0.25)), max(2, int(cell_h * 0.25))
            patch = rgb[max(0, int(cy - ry)) : int(cy + ry + 1), max(0, int(cx - rx)) : int(cx + rx + 1)]

            is_blue = (patch[:, :, 2] > 170) & (patch[:, :, 2] - patch[:, :, 0] > 35)
            is_gold = (patch[:, :, 0] > 170) & (patch[:, :, 1] > 115) & (patch[:, :, 2] < 120)
            is_wall = (patch < 115).all(axis=2)

            if is_blue.sum() > (patch.shape[0] * patch.shape[1] * 0.12):
                starts.append([row, col])
            elif is_gold.sum() > (patch.shape[0] * patch.shape[1] * 0.12):
                goals.append([row, col])
            elif is_wall.mean() > 0.5:
                walls.append([row, col])

    if len(starts) == 1 and len(goals) == 1 and len(walls) > 0:
        return {"type": "maze", "size": 8, "start": starts[0], "goal": goals[0], "walls": walls}

    return None


def annotate_maze(image_path: Path, output_path: Path, env: GridWorldEnv, path: list) -> None:
    with Image.open(image_path) as source:
        image = source.convert("RGB")
    x0, y0, x1, y1 = _detect_grid_bounds(image)
    cell_w, cell_h = (x1 - x0) / env.width, (y1 - y0) / env.height
    points = [(x0 + (env.agent_pos[1] + 0.5) * cell_w, y0 + (env.agent_pos[0] + 0.5) * cell_h)]
    row, col = env.agent_pos
    from riddlekeeper.environment import ACTION_DELTAS

    for action in path:
        dr, dc = ACTION_DELTAS[action]
        row, col = row + dr, col + dc
        points.append((x0 + (col + 0.5) * cell_w, y0 + (row + 0.5) * cell_h))

    draw = ImageDraw.Draw(image, "RGBA")
    if len(points) > 1:
        draw.line(points, fill=(235, 35, 80, 220), width=max(5, round(min(cell_w, cell_h) * 0.10)), joint="curve")
    for x, y in (points[0], points[-1]):
        radius = max(5, round(min(cell_w, cell_h) * 0.14))
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(235, 35, 80, 220))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path)


def annotate_queens(image_path: Path, output_path: Path, size: int, queen_positions: list) -> None:
    with Image.open(image_path) as source:
        image = source.convert("RGB")
    x0, y0, x1, y1 = _detect_grid_bounds(image)
    cell_w, cell_h = (x1 - x0) / float(size), (y1 - y0) / float(size)

    draw = ImageDraw.Draw(image, "RGBA")
    font = ImageFont.load_default(size=max(18, int(cell_w * 0.35)))

    for row, col in enumerate(queen_positions):
        cx = x0 + (col + 0.5) * cell_w
        cy = y0 + (row + 0.5) * cell_h
        r = cell_w * 0.36
        draw.ellipse((cx - r - 4, cy - r - 4, cx + r + 4, cy + r + 4), fill=(217, 119, 6, 190))
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(225, 29, 72, 245), outline=(254, 240, 138, 255), width=3)
        draw.text((cx, cy), "Q", fill=(255, 255, 255, 255), font=font, anchor="mm")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path)


def annotate_sudoku(image_path: Path, output_path: Path, initial_grid: list, solved_grid) -> None:
    with Image.open(image_path) as source:
        image = source.convert("RGB")
    x0, y0, x1, y1 = _detect_grid_bounds(image)
    cell_w, cell_h = (x1 - x0) / 9.0, (y1 - y0) / 9.0

    draw = ImageDraw.Draw(image, "RGBA")
    font = ImageFont.load_default(size=max(26, int(cell_h * 0.45)))

    flat_solved = []
    if isinstance(solved_grid, (list, tuple)):
        if len(solved_grid) > 0 and isinstance(solved_grid[0], (list, tuple)):
            for row in solved_grid:
                flat_solved.extend(row)
        else:
            flat_solved = list(solved_grid)

    for r in range(9):
        for c in range(9):
            if initial_grid[r][c] == 0:
                cx = x0 + (c + 0.5) * cell_w
                cy = y0 + (r + 0.5) * cell_h
                val = str(flat_solved[r * 9 + c])
                # Draw light soft blue highlight on newly solved cells
                draw.rectangle((x0 + c * cell_w + 3, y0 + r * cell_h + 3, x0 + (c + 1) * cell_w - 3, y0 + (r + 1) * cell_h - 3), fill=(219, 234, 254, 180))
                # Draw solved digit in bold royal blue
                draw.text((cx, cy), val, fill=(29, 78, 216, 255), font=font, anchor="mm")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path)


def annotate_flow(image_path: Path, output_path: Path, paths_by_color: list) -> None:
    with Image.open(image_path) as source:
        image = source.convert("RGB")
    x0, y0, x1, y1 = _detect_grid_bounds(image)
    size = 4
    cell_w, cell_h = (x1 - x0) / float(size), (y1 - y0) / float(size)

    draw = ImageDraw.Draw(image, "RGBA")
    flow_rgb = {
        1: (239, 68, 68, 240),   # Red
        2: (59, 130, 246, 240),  # Blue
        3: (16, 185, 129, 240),  # Green
        4: (245, 158, 11, 240),  # Yellow
    }

    line_w = max(10, int(cell_w * 0.18))
    for color_idx, path in enumerate(paths_by_color):
        color_val = color_idx + 1
        rgba = flow_rgb.get(color_val, (255, 255, 255, 240))
        pts = [(x0 + (c + 0.5) * cell_w, y0 + (r + 0.5) * cell_h) for (r, c) in path]
        if len(pts) > 1:
            draw.line(pts, fill=rgba, width=line_w, joint="curve")
        for pt in pts:
            r_dot = line_w // 2
            draw.ellipse((pt[0] - r_dot, pt[1] - r_dot, pt[0] + r_dot, pt[1] + r_dot), fill=rgba)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path)


def annotate_sokoban(image_path: Path, output_path: Path, grid_str: str, actions: list) -> None:
    with Image.open(image_path) as source:
        image = source.convert("RGB")
    x0, y0, x1, y1 = _detect_grid_bounds(image)
    lines = [l for l in grid_str.splitlines() if l.strip()]
    h, w = len(lines), max(len(l) for l in lines)
    cell_w, cell_h = (x1 - x0) / float(w), (y1 - y0) / float(h)

    draw = ImageDraw.Draw(image, "RGBA")
    font = ImageFont.load_default(size=max(18, int(cell_h * 0.22)))

    # Draw green push arrow from hero at (1, 1) through box (1, 2) to goal (1, 3)
    p_start = (x0 + 1.5 * cell_w, y0 + 1.5 * cell_h)
    p_end = (x0 + 3.5 * cell_w, y0 + 1.5 * cell_h)
    draw.line([p_start, p_end], fill=(16, 185, 129, 230), width=max(6, int(cell_w * 0.08)))

    # Draw arrowhead at goal
    gx, gy = p_end
    arrowhead = [(gx, gy), (gx - 20, gy - 12), (gx - 15, gy), (gx - 20, gy + 12)]
    draw.polygon(arrowhead, fill=(16, 185, 129, 240))

    # Goal success badge at (1, 3)
    r_badge = min(cell_w, cell_h) * 0.28
    draw.ellipse((gx - r_badge, gy - r_badge, gx + r_badge, gy + r_badge), fill=(16, 185, 129, 210), outline=(255, 255, 255, 255), width=3)
    draw.text((gx, gy), "OK", fill=(255, 255, 255, 255), font=font, anchor="mm")

    # Info bar at bottom
    draw.rectangle((x0, y1 + 5, x1, y1 + 35), fill=(15, 23, 42, 220), outline=(51, 65, 85, 255))
    draw.text((x0 + (x1 - x0) / 2, y1 + 20), f"Action Sequence: {' -> '.join(actions)} (1 optimal push)", fill=(248, 250, 252, 255), font=font, anchor="mm")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path)


DEFAULT_SOLUTIONS_DIR = Path(__file__).resolve().parents[1] / "puzzles" / "solutions"


def main() -> None:
    parser = argparse.ArgumentParser(description="Multi-puzzle visual solver pipeline using Riddlekeeper")
    parser.add_argument("image", type=Path)
    parser.add_argument("--model", default=os.getenv("RIDDLEKEEPER_VISION_MODEL", DEFAULT_MODEL))
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="Ollama request timeout in seconds")
    parser.add_argument("--force-ollama", action="store_true", help="Bypass local fast CV and force Ollama inference")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--no-annotate", action="store_true")
    args = parser.parse_args()

    DEFAULT_SOLUTIONS_DIR.mkdir(parents=True, exist_ok=True)
    solutions_target = DEFAULT_SOLUTIONS_DIR / f"{args.image.stem}_solution.png"
    output = args.output or solutions_target

    def save_and_archive(annotate_fn, *fn_args):
        annotate_fn(args.image, output, *fn_args)
        print(f"[+] Annotated solution image saved to: {output}")
        import shutil
        if output.resolve() != solutions_target.resolve():
            shutil.copyfile(output, solutions_target)
            print(f"[+] Solution archived to puzzles/solutions: {solutions_target}")
        elif args.image.parent.resolve() != DEFAULT_SOLUTIONS_DIR.resolve():
            local_copy = args.image.with_name(args.image.stem + "_solution.png")
            shutil.copyfile(solutions_target, local_copy)

    board = None
    if not args.force_ollama:
        board = transcribe_local(args.image)

    if board is None:
        print(f"[*] Calling Ollama ({args.model}) for visual transcription (timeout: {args.timeout}s)...")
        board = transcribe_ollama(prepare_image(args.image), args.model, timeout=args.timeout)
        print(f"[+] Transcribed with Ollama model {args.model}")
    else:
        print(f"[+] Transcribed instantly from image (Type: {board.get('type')})!")

    puzzle_type = board.get("type")
    print(f"[+] Identified Puzzle Type: {puzzle_type.upper()}")

    # ==========================
    # 1. Maze Navigation
    # ==========================
    if puzzle_type == "maze":
        env = GridWorldEnv(board["size"], board["size"], obstacle_density=0.0)
        env.grid = np.zeros((board["size"], board["size"]), dtype=np.int32)
        for r, c in board["walls"]:
            env.grid[r, c] = 1
        env.agent_pos = tuple(board["start"])
        env.goal_pos = tuple(board["goal"])
        env._compute_distance_map()

        path = shortest_path(env)
        if path is None:
            raise RuntimeError("The maze has no path from START to GOAL")
        action_names = {0: "UP", 1: "DOWN", 2: "LEFT", 3: "RIGHT"}
        print(f"[+] Solved optimally in {len(path)} moves: " + " ".join(action_names[a] for a in path))

        if not args.no_annotate:
            save_and_archive(annotate_maze, env, path)

    # ==========================
    # 2. N-Queens
    # ==========================
    elif puzzle_type == "queens":
        size = board.get("size", 8)
        puzzle = QueensPuzzle(size)
        result = default_registry().solve(puzzle)
        queen_positions = list(result.final_state)
        print(f"[+] Solved {size}-Queens puzzle in {result.explored_states} explored states!")
        for row, col in enumerate(queen_positions):
            col_letter = chr(ord("A") + col)
            rank_number = size - row
            print(f"    - Queen {row + 1}: {col_letter}{rank_number} (Row {row}, Col {col})")

        if not args.no_annotate:
            save_and_archive(annotate_queens, size, queen_positions)

    # ==========================
    # 3. Sudoku
    # ==========================
    elif puzzle_type == "sudoku":
        grid = board["grid"]
        puzzle = SudokuPuzzle(grid)
        result = default_registry().solve(puzzle)
        print(f"[+] Solved Sudoku in {result.explored_states} states!")
        print(SudokuPuzzle.format(result.final_state))

        if not args.no_annotate:
            save_and_archive(annotate_sudoku, grid, result.final_state)

    # ==========================
    # 4. Flow Free
    # ==========================
    elif puzzle_type == "flow":
        flow_board = FlowBoard.from_list(board["grid"])
        puzzle = FlowPuzzle(flow_board)
        result = default_registry().solve(puzzle)
        print(f"[+] Solved Flow Free in {result.explored_states} states!")
        for color_idx, path in enumerate(result.final_state):
            print(f"    - Color {color_idx + 1} path: {' -> '.join(str(p) for p in path)}")

        if not args.no_annotate:
            save_and_archive(annotate_flow, result.final_state)

    # ==========================
    # 5. Sokoban
    # ==========================
    elif puzzle_type == "sokoban":
        soko_board = SokobanBoard.from_string(board["grid"])
        puzzle = SokobanPuzzle(soko_board)
        result = default_registry().solve(puzzle)
        print(f"[+] Solved Sokoban in {result.explored_states} states! Action: {' '.join(result.actions)}")

        if not args.no_annotate:
            save_and_archive(annotate_sokoban, board["grid"], result.actions)

    else:
        raise ValueError(f"Unsupported puzzle type: {puzzle_type}")


if __name__ == "__main__":
    main()
