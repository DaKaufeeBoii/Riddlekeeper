# Riddlekeeper User & Execution Guide

Riddlekeeper is a neuro-symbolic visual puzzle-solving system that combines:
1. **Algorithmic Alignment**: A Bellman-Ford Graph Neural Network (GNN) trained on small grids ($5\times 5$) that extrapolates zero-shot to large grids ($8\times 8, 10\times 10$).
2. **Multi-Puzzle Symbolic Constraint Engine**: Exact deterministic solvers for Sudoku (MRV backtracking), $N$-Queens (bitmask conflict search), Sokoban ($\text{A}^*$ search with Hungarian heuristics and corner deadlock pruning), Flow Free (full-board coverage backtracking with dead-end checks), Pipes (rotational CSP), and Words (letter grid DFS).
3. **Decoupled Visual Perception & Annotation Pipeline**: Translates puzzle screenshots into structured symbolic representations and renders pixel-perfect visual solution overlays.

---

## 1. Prerequisites & Environment Setup

### System Requirements
* **Python 3.9+** (Python 3.10, 3.11, 3.12, 3.14 supported).
* Standard libraries: The symbolic solvers and agent orchestration use only the Python standard library.
* External libraries required for vision and neural models:
  ```powershell
  pip install pillow numpy torch
  ```

Check your Python environment:
```powershell
python --version
```

---

## 2. Exact Steps to Execute the Program

### Step 1: Solve Puzzles via Command Line (Text & Logic)
Run [`solve.py`](file:///d:/Kaufee/padhai/7th-sem/PBA/riddlekeeper/solve.py) with the target puzzle name:

```powershell
# 1. Sudoku (9x9 standard grid with MRV backtracking)
python solve.py sudoku

# 2. N-Queens (specify any N, default N=8)
python solve.py queens --size 8

# 3. Sokoban Push-Box (Tactical 2-box puzzle with A* & deadlock avoidance)
python solve.py sokoban

# 4. Flow Free (5x5 5-color puzzle with full-board winding coverage)
python solve.py flow

# 5. Pipes / Net (2x2 rotational network connectivity)
python solve.py pipes

# 6. Words / Wend (3x3 letter grid dictionary path search)
python solve.py words
```

> **Automated Solution Storage**:  
> Every solve command outputs the step-by-step actions to the terminal and saves the solution to:  
> [`puzzles/solutions/<puzzle>_solution.txt`](file:///d:/Kaufee/padhai/7th-sem/PBA/riddlekeeper/puzzles/solutions/)

---

### Step 2: Solve Puzzle Images (Visual Perception & Solution Overlays)
Riddlekeeper can process puzzle images directly, solve them, and draw the solution onto the original image:

```powershell
# 1. Solve a Maze image (draws glowing cyan-pink shortest path)
python vision/pipeline.py puzzles/puzzle.png

# 2. Solve an 8-Queens chessboard image (places centered ruby queen badges)
python vision/pipeline.py puzzles/queens_puzzle.png

# 3. Solve a Sudoku image (overlays royal blue digits in light blue cells)
python vision/pipeline.py puzzles/sudoku_puzzle.png

# 4. Solve a Flow Free image (draws smooth, rounded multi-colored pipes)
python vision/pipeline.py puzzles/flow_puzzle.png

# 5. Solve a Sokoban warehouse image (draws player path, push vectors, & OK badges)
python vision/pipeline.py puzzles/sokoban_puzzle.png
```

> **Visual Solution Output**:  
> Annotated solution images are automatically saved to:  
> [`puzzles/solutions/<image_name>_solution.png`](file:///d:/Kaufee/padhai/7th-sem/PBA/riddlekeeper/puzzles/solutions/)

---

### Step 3: Run the Unit Test Suite
To verify that all 32 unit tests across all puzzle types pass:

```powershell
python puzzles/tests.py
```

Expected output:
```text
Ran 32 tests in 2.600s
OK
```

---

### Step 4: Run Neural GNN Size Extrapolation Experiments
To evaluate the Bellman-Ford GNN vs. standard CNN policies on out-of-distribution (OOD) grid sizes:

```powershell
# Run size extrapolation benchmark across 5x5, 8x8, and 10x10 grids
python evaluate.py

# Run an interactive demonstration with step-by-step rollouts
python demo.py

# Train the GNN model from scratch on 5x5 configurations
python train.py
```

---

## 3. How to Share Your Own Picture to Get Solutions

You can supply your own puzzle screenshot or photo in any of the following three ways:

---

### Method A: Run via the Vision Pipeline CLI (Recommended for Local Files)

1. **Place your puzzle image** anywhere on your system (e.g., `C:\Users\user\Downloads\my_puzzle.png` or in the `puzzles/` directory).
2. **Execute the pipeline** pointing to your image path:
   ```powershell
   python vision/pipeline.py "path/to/my_puzzle.png"
   ```
3. To specify a custom output path for the annotated solution:
   ```powershell
   python vision/pipeline.py "path/to/my_puzzle.png" --output "path/to/solved_overlay.png"
   ```

#### How the Pipeline Processes Your Image:
- **Fast Local Computer Vision**: For clean grid screenshots (Mazes, Chessboards, Sudokus), the built-in parser automatically isolates the grid boundaries using corner-background estimation and extracts board elements in $< 0.05\text{ seconds}$.
- **Local Vision-Language Model (Ollama)**: For unstandardized screenshots or photos, Riddlekeeper connects to a locally running Ollama instance (e.g., `qwen2.5vl:3b` or `moondream`) to transcribe the board into a structured JSON representation:
  ```powershell
  # Step 1: Ensure Ollama is running with a vision model
  ollama run qwen2.5vl:3b

  # Step 2: Run the pipeline with forced VLM transcription
  python vision/pipeline.py "path/to/my_puzzle.png" --force-ollama
  ```
  *(If running on a CPU-only laptop, use `moondream` for 3–5 second transcription: `--model moondream`)*.

---

### Method B: Upload Directly in Chat (Interactive Pair-Programming)

If working within the Antigravity assistant:
1. **Drag and drop** or paste your puzzle screenshot directly into this conversation chat.
2. Tell the assistant: *"Solve this puzzle for me."*
3. The assistant will:
   - Read the image pixels directly.
   - Transcribe the grid layout and entities (start, goal, walls, clues, numbers).
   - Execute Riddlekeeper's exact symbolic solver on the transcribed configuration.
   - Return both the text action sequence and render an annotated solution overlay image for you.

---

### Method C: Define Custom Board States via Python API

If you have a puzzle configuration from an app, newspaper, or website and prefer feeding the board state directly in code:

#### 1. Custom Sudoku ($9\times 9$)
```python
from riddlekeeper.puzzles.sudoku import SudokuPuzzle
from riddlekeeper.puzzles.registry import default_registry

my_grid = [
    [0, 0, 0, 2, 6, 0, 7, 0, 1],
    [6, 8, 0, 0, 7, 0, 0, 9, 0],
    [1, 9, 0, 0, 0, 4, 5, 0, 0],
    [8, 2, 0, 1, 0, 0, 0, 4, 0],
    [0, 0, 4, 6, 0, 2, 9, 0, 0],
    [0, 5, 0, 0, 0, 3, 0, 2, 8],
    [0, 0, 9, 3, 0, 0, 0, 7, 4],
    [0, 4, 0, 0, 5, 0, 0, 3, 6],
    [7, 0, 3, 0, 1, 8, 0, 0, 0]
]

puzzle = SudokuPuzzle(my_grid)
result = default_registry().solve(puzzle)

if result.solved:
    print(SudokuPuzzle.format(result.final_state))
```

#### 2. Custom Flow Free ($N\times N$)
```python
from riddlekeeper.puzzles.flow import FlowBoard, FlowPuzzle, FlowSolver

# 0 = empty cell; 1, 2, 3... = color endpoint pairs
my_flow_grid = [
    [1, 2, 0, 0, 0],
    [0, 3, 4, 5, 2],
    [0, 0, 0, 0, 5],
    [0, 0, 0, 0, 0],
    [1, 0, 0, 3, 4]
]

board = FlowBoard.from_list(my_flow_grid)
puzzle = FlowPuzzle(board)
result = FlowSolver().solve(puzzle)

if result.solved:
    for color_idx, path in enumerate(result.final_state):
        print(f"Color {color_idx + 1} path: {' -> '.join(str(p) for p in path)}")
```

#### 3. Custom Sokoban Level
```python
from riddlekeeper.puzzles.sokoban import SokobanBoard, SokobanPuzzle, SokobanSolver

# Standard Sokoban ASCII notation:
# # = Wall, @ = Player, $ = Box, . = Goal, * = Box on Goal
my_sokoban_level = """
######
#  . #
# $$ #
# .# #
#  @ #
######
"""

board = SokobanBoard.from_string(my_sokoban_level.strip())
puzzle = SokobanPuzzle(board)
result = SokobanSolver().solve(puzzle)

if result.solved:
    print(f"Solved in {len(result.actions)} steps!")
    print("Action sequence:", " -> ".join(result.actions))
```

---

## 4. Supported Puzzle Formats & Schema Reference

When transcribing an image or writing an input file, Riddlekeeper uses these standard formats:

| Puzzle | Input Format | Key Symbols / Values | Solution Output |
| :--- | :--- | :--- | :--- |
| **Maze** | JSON / Coordinates | Walls `[r, c]`, Start `[r, c]`, Goal `[r, c]` | Discrete moves: `UP`, `DOWN`, `LEFT`, `RIGHT` |
| **$N$-Queens** | Board size $N$ | Integer $N \ge 4$ | Queen columns per row: `(c_0, c_1, ..., c_{N-1})` |
| **Sudoku** | 2D list ($9\times 9$) | `0` = Empty, `1–9` = Given digits | Completed $9\times 9$ numerical grid |
| **Flow Free** | 2D square list | `0` = Empty, `1, 2, 3...` = Color terminal pairs | Orthogonal coordinate paths covering 100% of grid |
| **Sokoban** | ASCII multi-line string | `#` Wall, `@` Player, `$` Box, `.` Goal | Moves (`up`, `down`...) and Pushes (`push_up`...) |
| **Pipes** | 2D list of strings | `"L"` Corner, `"I"` Line, `"T"` T-pipe, `"+"` Cross | Clockwise rotation steps `(0, 1, 2, 3)` per cell |
| **Words** | 2D character matrix + list | Letter grid + list of uppercase search words | Ordered coordinate paths spelling each word |

---

## 5. Frequently Asked Questions (FAQ)

#### Q1: "Where do the generated solution images go?"
By default, the pipeline writes directly to:
```text
riddlekeeper/puzzles/solutions/<image_filename>_solution.png
```
You can also specify any custom destination with `--output custom_name.png`.

#### Q2: "Can the solver handle images with margins, title text, or coordinates?"
**Yes.** The adaptive grid detector in `vision/pipeline.py` uses corner-background sampling and contiguous cell chunking to crop out headers, rank/file coordinate labels (like `A–H`, `1–8` on chessboards), and background borders before solving and annotating.

#### Q3: "What happens if a puzzle has no solution or is invalid?"
Because Riddlekeeper uses exact search and constraint satisfaction rather than probabilistic text generation, it will **never hallucinate an impossible answer**. If no valid sequence exists, the solver returns `solved=False` with the number of explored states and an informative termination message.
