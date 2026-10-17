# Riddlekeeper

Riddlekeeper is a modular puzzle-solving agent and neural reasoning system. It provides exact, constraint-satisfaction and search-based solvers for diverse puzzle families, an agent orchestration layer with time/state budgets, and an algorithmically-aligned neural solver for out-of-distribution grid navigation.

## Quick start

Use Python 3.9 or later. The symbolic logic solvers use only the Python standard library, so PyTorch is not needed for them. From the directory containing the `riddlekeeper` package, run:

```powershell
# Logic puzzle solvers
python -m riddlekeeper.solve sudoku
python -m riddlekeeper.solve queens --size 8
python -m riddlekeeper.solve sokoban
python -m riddlekeeper.solve flow
python -m riddlekeeper.solve pipes
python -m riddlekeeper.solve words

# Run full regression test suite (30 tests)
python -m riddlekeeper.puzzles.tests

# Transcribe and solve a maze image (requires Ollama + Pillow)
ollama pull qwen2.5vl:3b
python -m riddlekeeper.vision.pipeline riddlekeeper\puzzles\puzzle.png
```

The image pipeline first reads clean, color-coded 8x8 maze images locally, so
those do not need a running vision model. Other images are resized to at most
768 px on the longest side and sent to Ollama for JSON board transcription;
Riddlekeeper then solves with exact BFS and writes an annotated image next to
the input. Set `RIDDLEKEEPER_VISION_MODEL` or pass `--model` to choose another
locally available Ollama vision model.

## Project structure

- `puzzles/`: Symbolic solver implementations and input benchmark puzzle images (`puzzle.png`, `queens_puzzle.png`, `sudoku_puzzle.png`, `flow_puzzle.png`, `sokoban_puzzle.png`).
- `puzzles/base.py`: Defines the shared puzzle, solver, and `SolveResult` contracts.
- `puzzles/registry.py`: Extensible solver registry with duplicate checks and auto-discovery.
- `puzzles/sudoku.py`: Backtracking solver with minimum-remaining-values (MRV) cell selection.
- `puzzles/queens.py`: Row-wise backtracking solver for arbitrary N-Queens boards.
- `puzzles/sokoban.py`: A* push-based search with corner-deadlock pruning.
- `puzzles/flow.py`: Flow Free path search with dead-end neighbor pruning and full-board constraints.
- `puzzles/pipes.py`: Rotational constraint satisfaction and connectivity verification for pipe networks.
- `puzzles/words.py`: Grid path search for words and Wend letter-path puzzles.
- `puzzles/solutions/`: Central output directory where all generated solutions (annotated images and formatted solution texts) are automatically saved.
- `agent/`: Orchestration layer (`RiddlekeeperAgent`, `Agent`, `Request`, `Result`) with state/time budgets, execution traces, independent validation, and dynamic replanning.
- `environment.py`, `models.py`, `train.py`, `evaluate.py`, and `demo.py`: Exact Bellman-Ford grid solver and a learned CNN policy baseline for grid navigation.
- `puzzles/tests.py`: Dependency-free 30-test regression suite covering valid, invalid, and unsatisfiable inputs across all puzzle modules.
- `.gitignore`: Repository hygiene configuration ignoring research papers (`*.pdf`), `Project/` folder, bytecode (`__pycache__`), virtual environments (`.venv`), temporary logs, OS artifacts, and presentation binaries.

## Implementation roadmap status

### Phase 1 — Reliable solver framework [COMPLETE]
- [x] Stable puzzle contract: type, initial state, legal actions, transition, solved check, state key.
- [x] Registry checks and clear errors for unknown puzzle types and duplicate solver names.
- [x] Puzzle logic fully independent from ML/PyTorch dependencies.
- [x] Regression tests for invalid, unsatisfiable, and already-solved inputs.

### Phase 2 — Broaden symbolic puzzle coverage [COMPLETE]
- [x] **Sokoban**: Box/goal representation, corner-deadlock detection, and bounded A* search.
- [x] **Flow Free**: Multi-color path search with dead-end neighbor pruning and full-board coverage validation.
- [x] **Pipes**: Model pipe orientations, rotational constraints, boundary checks, and single-component connectivity.
- [x] **Word/Wend puzzles**: Rectangular letter grid extraction, multi-word path finding, and adjacency constraints.

### Phase 3 — Agent orchestration [COMPLETE]
- [x] Common `AgentRequest` / `AgentResult` API reporting solver selection, execution trace, and elapsed runtime.
- [x] Time and state budget enforcement with informative failure reasons.
- [x] Independent solution validation prior to returning success.
- [x] Iterative replanning loop (`replan_execute`) for environments where actions are executed step-by-step.

### Phase 4 — Visual perception and interaction [IN PROGRESS]
- [x] Multi-puzzle visual perception and annotation pipeline (`riddlekeeper.vision.pipeline`).
- [x] Fast local CV detection for clean screenshots (Mazes, N-Queens, Sudoku, Flow Free, Sokoban).
- [x] Ollama VLM integration (`qwen2.5vl:3b`, `moondream`) for unformatted screenshots.
- [x] Pixel-perfect visual overlays (glowing paths, royal queen badges, highlighted sudoku digits, colored pipes, push vectors).
- [ ] Incorporate PoNG (Normalized Group Conv) visual grounding for raw pixel inputs.
- [ ] Confidence reporting and human-in-the-loop correction when perception is ambiguous.

### Phase 5 — Evaluation and generalization [IN PROGRESS]
- [x] Exact Bellman-Ford reference solver and learned CNN baseline evaluated on out-of-distribution grid navigation ($5 \times 5 \to 10 \times 10$).
- [x] Benchmark suite reporting success rate, path optimality ratio, and explored states.
- [ ] Extend empirical size-extrapolation evaluation to Sokoban push-distance complexity.

## Frequently Asked Questions (FAQ)

### 1. Are puzzle images or solutions generated using cloud models (like Gemini)?
**No.** Riddlekeeper is 100% local and offline:
* Input puzzle images are rendered locally using Python (`matplotlib` / `PIL`).
* Board perception is performed locally (instant CV heuristics or local Ollama VLMs).
* Solvers are exact Python algorithms running on your CPU with zero external API calls.
* Solution images are annotated and saved locally using Pillow (`PIL.ImageDraw`).

### 2. Can Ollama models edit or paint pixels onto an existing input image?
**No.** Ollama is a Large Language Model and Vision-Language Model (VLM) runtime. Models in Ollama (such as `qwen2.5vl:3b`, `moondream`, or `llava`) accept images + text as input, but **only output text/JSON tokens**. They cannot generate or modify image pixels. Riddlekeeper uses Ollama strictly for transcription (translating pixels into a structured JSON grid), and then uses Pillow to draw the solution directly onto the image.

### 3. Why not use a generative image model (like Stable Diffusion or DALL-E) to draw the solution?
Generative diffusion models hallucinate pixels. Asking an image generator to "paint the solution" on a Sudoku or Maze results in smudged digits, duplicate numbers, and broken paths. Industry standard systems (e.g., Photomath, Google Lens, Chess.com) strictly decouple **Perception** (reading the board), **Logic** (exact mathematical solving with 0% error), and **Rendering** (deterministic pixel overlays).

### 4. Why does Ollama take 2–4 minutes per image on my machine?
If your computer does not have a dedicated NVIDIA GPU (CUDA), Ollama runs in CPU mode. Processing thousands of image tokens on a CPU is memory-bandwidth intensive.
* **Instant (< 0.05s)**: Riddlekeeper automatically uses local computer vision (`transcribe_local`) for clean screenshots.
* **Fast Ollama CPU Alternative**: Pull `moondream` (`ollama pull moondream`), a 1.8B parameter vision model designed for edge CPUs that runs in ~3–8 seconds.

### 5. Does Riddlekeeper only solve fixed-size puzzles (like 8x8 or 9x9)?
**No.** The symbolic algorithms are mathematically size-invariant:
* **N-Queens**: Solves for arbitrary $N$ (e.g., $N=4, 8, 16, 25$).
* **Sudoku**: Solves standard $9 \times 9$, extensible to custom block shapes.
* **Maze, Flow Free, Pipes, Words**: Solve arbitrary dimensions up to configured search budgets.
* The visual pipeline dynamically calculates grid boundaries and cell ratios regardless of image dimensions.

### 6. What happens if a puzzle has no solution or is unsolvable?
Because Riddlekeeper uses exact constraint satisfaction and search, impossible puzzles will **never** output hallucinated solutions. The solver searches up to the state budget, returns `solved=False`, and reports the exact failure reason without drawing a false path.

## Development checks

From the package parent directory:

```powershell
python -m riddlekeeper.puzzles.tests
python -m py_compile riddlekeeper\puzzles\*.py riddlekeeper\agent\*.py riddlekeeper\solve.py
```

See [guide.md](guide.md) for detailed Python API usage and examples.
