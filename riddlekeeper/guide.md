# Riddlekeeper User Guide

This guide explains how to use Riddlekeeper to solve structured puzzles using exact search and constraint satisfaction, orchestrate solutions with budgets and execution traces, and run neural reasoning experiments.

---

## 1. Requirements

* **Python 3.9 or newer**.
* The symbolic logic solvers (`puzzles/`) and orchestration agent (`agent/`) use only the Python standard library. No external dependencies are required.
* **PyTorch** is needed only if you wish to run the learned neural grid-navigation models (`train.py`, `evaluate.py`, `demo.py`).

Check your Python version:
```powershell
python --version
```

---

## 2. CLI Quick Start

Run any supported puzzle directly from your terminal:

```powershell
# Standard 9x9 Sudoku
python -m riddlekeeper.solve sudoku

# N-Queens (specify custom size N)
python -m riddlekeeper.solve queens --size 8

# Sokoban push-box puzzle (A* with deadlock pruning)
python -m riddlekeeper.solve sokoban

# Flow Free (path search with full-board constraints)
python -m riddlekeeper.solve flow

# Pipes / Net (rotational constraint satisfaction)
python -m riddlekeeper.solve pipes

# Word / Wend search (letter grid path finding)
python -m riddlekeeper.solve words
```

> **Automatic Solution Persistence**:  
> Every CLI solve command automatically outputs and saves its formatted solution into the centralized directory:  
> [`riddlekeeper/puzzles/solutions/<puzzle>_solution.txt`](file:///d:/Kaufee/padhai/7th-sem/PBA/riddlekeeper/puzzles/solutions)

---

## 3. Python API Examples

### 3.1 Flow Free
Connect color pairs across the board so that all cells are filled without paths crossing:

```python
from riddlekeeper.puzzles.flow import FlowBoard, FlowPuzzle
from riddlekeeper.puzzles.registry import default_registry

board = FlowBoard.from_list([
    [1, 2, 3],
    [0, 0, 0],
    [1, 2, 3],
])
puzzle = FlowPuzzle(board)
result = default_registry().solve(puzzle)

if result.solved:
    for color_idx, path in enumerate(result.final_state):
        color = puzzle.board.all_colors[color_idx]
        print(f"Color {color}: {path}")
```

### 3.2 Pipes / Net
Rotate tiles (0, 90, 180, or 270 degrees) so that all pipe connections align and form a single connected network:

```python
from riddlekeeper.puzzles.pipes import PipesBoard, PipesPuzzle
from riddlekeeper.puzzles.registry import default_registry

# Pipe types: 'L' (corner), 'I' (line), 'T' (T-junction), '+' (cross), 'C' (end)
board = PipesBoard.from_list([
    ["L", "L"],
    ["L", "L"],
])
puzzle = PipesPuzzle(board)
result = default_registry().solve(puzzle)

if result.solved:
    print("Required clockwise rotations:", result.final_state)
```

### 3.3 Word / Wend Search
Find continuous letter paths for given target words:

```python
from riddlekeeper.puzzles.words import WordGrid, WordsPuzzle
from riddlekeeper.puzzles.registry import default_registry

grid = WordGrid.from_list([
    ["C", "A", "T"],
    ["D", "O", "G"],
    ["F", "O", "X"],
])
puzzle = WordsPuzzle(grid, ["CAT", "DOG", "FOX"], allow_diagonal=True)
result = default_registry().solve(puzzle)

if result.solved:
    for word_idx, path in enumerate(result.final_state):
        print(f"{puzzle.words[word_idx]}: {path}")
```

### 3.4 Agent Orchestration with Budgets
Use the high-level `Agent` API to enforce search state limits, time limits, and inspect execution traces:

```python
from riddlekeeper.agent.api import Agent, Request
from riddlekeeper.puzzles.queens import QueensPuzzle

agent = Agent()
puzzle = QueensPuzzle(8)

# Enforce a maximum explored state budget
req = Request("queens", puzzle, state_limit=5000, time_limit_ms=1000)
res = agent.handle(req)

print(f"Success: {res.success}")
print(f"Solver used: {res.solver}")
print(f"Runtime: {res.runtime_ms:.2f} ms")
print(f"Trace events: {res.trace}")
```

---

## 4. Running Verification Tests

Run the complete 30-test regression suite:
```powershell
python -m riddlekeeper.puzzles.tests
```

---

## 5. Visual Perception Pipeline & Common Doubts (FAQ)

Riddlekeeper includes an end-to-end multimodal perception pipeline ([pipeline.py](file:///d:/Kaufee/padhai/7th-sem/PBA/riddlekeeper/vision/pipeline.py)) that takes an uploaded puzzle screenshot, recognizes the board state, runs the exact algorithmic solver, and annotates the solution path/steps directly onto the original image.

### 5.1 Running the Visual Pipeline

```powershell
# Solve a Grid Maze image (draws glowing navigation path)
python -m riddlekeeper.vision.pipeline Project\puzzle.png

# Solve an 8-Queens chessboard image (places ruby badges on ranks)
python -m riddlekeeper.vision.pipeline Project\queens_puzzle.png

# Solve a Sudoku puzzle image (fills solved numbers in highlighted blue cells)
python -m riddlekeeper.vision.pipeline Project\sudoku_puzzle.png

# Solve a Flow Free image (draws continuous, non-overlapping colored pipes)
python -m riddlekeeper.vision.pipeline Project\flow_puzzle.png

# Solve a Sokoban box-pushing image (draws push vectors and step banners)
python -m riddlekeeper.vision.pipeline Project\sokoban_puzzle.png
```

Each command automatically archives the annotated solution image directly into:
[`riddlekeeper/puzzles/solutions/<image_stem>_solution.png`](file:///d:/Kaufee/padhai/7th-sem/PBA/riddlekeeper/puzzles/solutions)
while keeping a convenient copy next to the input file (e.g., `Project/sudoku_puzzle_solution.png`). Custom destinations can also be specified using the `--output` flag.

---

### 5.2 Frequently Asked Questions & Common Doubts

#### Q1: "Are the images being generated or edited using Gemini or cloud models in Antigravity?"
**No, absolutely not.**
* **Input generation**: The benchmark puzzle images in `Project/` are generated locally by Python scripts using `matplotlib` and `PIL`.
* **Solving**: The solvers are pure Python algorithms running on your local machine.
* **Image editing / annotation**: The solution paths, numbers, badges, and markers are drawn directly onto the original image pixels locally using `Pillow` (`PIL.ImageDraw`).
* **Zero cloud calls**: The pipeline works completely offline without touching Gemini, Antigravity cloud services, or any external API.

#### Q2: "Can Ollama models edit existing input images directly?"
**No.** Ollama cannot edit or generate images.
* Ollama is an LLM and Vision-Language Model (VLM) runtime.
* Models in Ollama (like `qwen2.5vl:3b`, `moondream`, `llava`) only accept images/prompts as input and output **text or JSON**. They do not possess image-generation or pixel-rendering heads.
* In Riddlekeeper, Ollama is used exclusively as a **visual transcriber** (converting pixels into a JSON grid representation). The actual image editing is then handled deterministically by Pillow.

#### Q3: "Why not use a Generative Image AI (like Stable Diffusion / Flux / DALL-E) to draw the solutions?"
Generative diffusion models hallucinate pixels. If you prompt an image generator to "draw the solution" on a Sudoku or Maze:
* Numbers get duplicated or distorted.
* Maze paths pass through solid walls or break continuity.
* Grid geometry becomes crooked.

Production visual intelligence systems (such as Photomath, Google Lens, and Chess.com) use a **decoupled 3-stage architecture**:
1. **Perception**: Vision model or computer vision reads the image into structured data.
2. **Reasoning**: Exact mathematical algorithms solve the puzzle with 100% accuracy and 0 hallucination.
3. **Rendering**: Deterministic graphics engine overlays the solution with sub-pixel precision.

#### Q4: "Why does Ollama take 2–4 minutes per image on my computer?"
If your PC lacks a dedicated NVIDIA GPU (running on CPU), Ollama must compute billions of floating-point operations across CPU threads for high-resolution visual tokens.
* **Instant local perception (< 0.05s)**: Riddlekeeper includes `transcribe_local`, which detects clean puzzle layouts instantly without needing an LLM.
* **Fastest CPU Vision Model**: Install **Moondream2** (`ollama pull moondream`). At 1.8B parameters, it runs in ~3–8 seconds on standard CPUs.

#### Q5: "Can Riddlekeeper handle different image sizes and board dimensions?"
**Yes.** 
* The visual pipeline features an adaptive grid detector (`_detect_grid_bounds`) that separates puzzle grids from title banners and margins across any resolution.
* The algorithmic solvers are size-invariant: N-Queens solves for any $N$, Sudoku solves standard and custom grids, and Mazes/Flow Free/Sokoban solve arbitrary row and column counts up to specified state budgets.

#### Q6: "What happens if a user uploads an impossible or broken puzzle?"
Because Riddlekeeper uses exact search and constraint satisfaction rather than probabilistic text generation, it will **never invent a false solution**. If a puzzle cannot be solved, the engine returns `solved=False` with the number of explored states and explains why no path exists.

