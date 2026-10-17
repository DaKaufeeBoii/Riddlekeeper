"""
Riddlekeeper Generalization Evaluation Suite.
Assesses closed-loop sequential puzzle-solving performance on:
1. In-Distribution (IID): 5x5 grids
2. Out-of-Distribution (OOD): 8x8 and 10x10 grids
Measures Success Rate (SR) and Path Optimality Ratio (POR).
"""

import os
import argparse
import torch
from riddlekeeper.environment import GridWorldEnv
from riddlekeeper.models import BellmanFordGNN, BaselineCNNPolicy
from riddlekeeper.solver import shortest_path


def evaluate_closed_loop(
    model,
    grid_size: int,
    num_episodes: int = 50,
    obstacle_density: float = 0.15,
    is_gnn: bool = True,
    device: str = "cpu",
    seed_offset: int = 5000
):
    model.eval()
    successes = 0
    evaluated = 0
    episode_ratios = []

    for ep in range(num_episodes):
        env = GridWorldEnv(
            height=grid_size,
            width=grid_size,
            obstacle_density=obstacle_density,
            seed=seed_offset + ep
        )
        oracle_traj = env.get_oracle_trajectory()
        optimal_len = len(oracle_traj)
        if optimal_len == 0:
            continue
        evaluated += 1

        done = False
        steps = 0
        max_allowed_steps = grid_size * grid_size * 2

        while not done and steps < max_allowed_steps:
            state_tensor = env.get_symbolic_tensor().unsqueeze(0).to(device)
            mask = env.get_valid_action_mask().unsqueeze(0).to(device)

            with torch.no_grad():
                if is_gnn:
                    # Dynamically scale message passing depth to graph diameter
                    k_steps = max(12, 2 * (grid_size + grid_size))
                    logits, _ = model(state_tensor, num_steps=k_steps, action_mask=mask)
                else:
                    logits, _ = model(state_tensor, action_mask=mask)

            action = logits.argmax(dim=-1).item()
            _, _, done, _ = env.step(action)
            steps += 1

        if env.agent_pos == env.goal_pos:
            successes += 1
            episode_ratios.append(steps / max(1, optimal_len))
        else:
            episode_ratios.append(max_allowed_steps / max(1, optimal_len))

    sr = (successes / evaluated * 100.0) if evaluated else 0.0
    # Include failures at the step cap so the mean cannot hide failed episodes.
    mean_por = sum(episode_ratios) / len(episode_ratios) if episode_ratios else 0.0
    return sr, mean_por


def evaluate_bfs(grid_size: int, num_episodes: int, obstacle_density: float = 0.15, seed_offset: int = 5000):
    """Evaluate exact search on the reproducible layouts used by learned policies."""
    successes = 0
    evaluated = 0
    for ep in range(num_episodes):
        env = GridWorldEnv(height=grid_size, width=grid_size,
                           obstacle_density=obstacle_density, seed=seed_offset + ep)
        path = shortest_path(env)
        if path is None or not path:
            continue
        evaluated += 1
        for action in path:
            env.step(action)
        successes += int(env.agent_pos == env.goal_pos)
    return (successes / evaluated * 100.0 if evaluated else 0.0), 1.0 if successes else 0.0, evaluated


def main():
    parser = argparse.ArgumentParser(description="Evaluate Riddlekeeper Generalization")
    parser.add_argument("--checkpoint_dir", type=str, default="riddlekeeper/checkpoints")
    parser.add_argument("--episodes", type=int, default=50, help="Episodes per evaluation size")
    args = parser.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[*] Evaluating closed-loop generalization on {device}...")

    gnn_path = os.path.join(args.checkpoint_dir, "gnn_best.pt")
    cnn_path = os.path.join(args.checkpoint_dir, "baseline_best.pt")

    gnn = None
    cnn = None
    if os.path.exists(gnn_path):
        gnn = BellmanFordGNN(in_channels=4, hidden_dim=32).to(device)
        gnn.load_state_dict(torch.load(gnn_path, map_location=device), strict=False)
    if os.path.exists(cnn_path):
        cnn = BaselineCNNPolicy(in_channels=4, hidden_dim=32).to(device)
        cnn.load_state_dict(torch.load(cnn_path, map_location=device))

    test_sizes = [5, 8, 10]
    results = {"BFS": {}, "GNN": {}, "Baseline_CNN": {}}

    print("\n" + "="*70)
    print("RIDDLEKEEPER CLOSED-LOOP GENERALIZATION BENCHMARK")
    print("="*70)

    for sz in test_sizes:
        is_iid = (sz == 5)
        tag = "I.I.D." if is_iid else "O.O.D. (Size Extrapolation)"
        print(f"\n[*] Evaluating on Grid Size: {sz}x{sz} [{tag}] ({args.episodes} episodes)...")

        bfs_sr, bfs_por, evaluated = evaluate_bfs(sz, args.episodes)
        results["BFS"][sz] = (bfs_sr, bfs_por)
        print(f"    --> BFS reference    : Success Rate = {bfs_sr:5.1f}% | Optimality Ratio = {bfs_por:.2f}x ({evaluated} solvable)")
        if gnn is not None:
            gnn_sr, gnn_por = evaluate_closed_loop(gnn, grid_size=sz, num_episodes=args.episodes, is_gnn=True, device=device)
            results["GNN"][sz] = (gnn_sr, gnn_por)
            print(f"    --> Bellman-Ford GNN : Success Rate = {gnn_sr:5.1f}% | Optimality Ratio = {gnn_por:.2f}x")
        if cnn is not None:
            cnn_sr, cnn_por = evaluate_closed_loop(cnn, grid_size=sz, num_episodes=args.episodes, is_gnn=False, device=device)
            results["Baseline_CNN"][sz] = (cnn_sr, cnn_por)
            print(f"    --> Baseline CNN     : Success Rate = {cnn_sr:5.1f}% | Optimality Ratio = {cnn_por:.2f}x")

    print("\n" + "="*70)
    print(f"{'Model':<20} | {'5x5 (IID)':<12} | {'8x8 (OOD)':<12} | {'10x10 (OOD)':<12}")
    print("-"*70)
    for model_name in [name for name in results if results[name]]:
        s5 = f"{results[model_name][5][0]:.1f}%" if 5 in results[model_name] else "N/A"
        s8 = f"{results[model_name][8][0]:.1f}%" if 8 in results[model_name] else "N/A"
        s10 = f"{results[model_name][10][0]:.1f}%" if 10 in results[model_name] else "N/A"
        print(f"{model_name:<20} | {s5:<12} | {s8:<12} | {s10:<12}")
    print("="*70)


if __name__ == "__main__":
    main()
