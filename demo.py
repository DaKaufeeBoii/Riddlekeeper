"""
Riddlekeeper Interactive Rollout Demo.
Visualizes step-by-step puzzle solving on an unseen test grid (e.g., 8x8 or 10x10)
demonstrating out-of-distribution generalization.
"""

import os
import argparse
import time
import torch
from riddlekeeper.environment import GridWorldEnv, ACTION_NAMES
from riddlekeeper.models import BellmanFordGNN
from riddlekeeper.solver import shortest_path


def run_demo(grid_size: int = 8, obstacle_density: float = 0.15, checkpoint: str = "riddlekeeper/checkpoints/gnn_best.pt", seed: int = 42):
    env = GridWorldEnv(
        height=grid_size,
        width=grid_size,
        obstacle_density=obstacle_density,
        seed=seed
    )
    oracle_path = shortest_path(env)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if not os.path.exists(checkpoint):
        if oracle_path is None:
            print("[-] No path exists for this puzzle.")
            return
        print(f"[!] Checkpoint {checkpoint} not found; demonstrating the exact BFS reference solver.")
        print(env.render_ascii())
        for step, action in enumerate(oracle_path, start=1):
            _, _, _, _ = env.step(action)
            print(f"Step {step:02d}: BFS chose [{ACTION_NAMES[action]}] | Agent at: {env.agent_pos}")
            print(env.render_ascii())
            print("-" * 40)
        print(f"[+] SUCCESS in {len(oracle_path)} optimal steps.")
        return

    print("="*60)
    print(f" RIDDLEKEEPER OOD INFERENCE DEMO (Trained on 5x5 -> Testing on {grid_size}x{grid_size})")
    print("="*60)

    model = BellmanFordGNN(in_channels=4, hidden_dim=32).to(device)
    model.load_state_dict(torch.load(checkpoint, map_location=device))
    model.eval()

    oracle_traj = env.get_oracle_trajectory()
    print(f"[*] Initial Agent Pos : {env.agent_pos}")
    print(f"[*] Goal Pos          : {env.goal_pos}")
    print(f"[*] Oracle Min Steps  : {len(oracle_traj)} moves")
    print("\nInitial Grid:")
    print(env.render_ascii())
    print("-" * 40)

    done = False
    step = 0
    max_steps = grid_size * grid_size * 2

    while not done and step < max_steps:
        step += 1
        state_tensor = env.get_symbolic_tensor().unsqueeze(0).to(device)
        mask = env.get_valid_action_mask().unsqueeze(0).to(device)

        k_steps = max(12, 2 * (grid_size + grid_size))
        with torch.no_grad():
            logits, val_map = model(state_tensor, num_steps=k_steps, action_mask=mask)

        action = logits.argmax(dim=-1).item()
        action_name = ACTION_NAMES[action]
        oracle_action = env.get_optimal_action()
        oracle_name = ACTION_NAMES[oracle_action] if oracle_action is not None else "GOAL"

        _, _, done, _ = env.step(action)

        print(f"Step {step:02d}: Model Chose [{action_name}] | Oracle: [{oracle_name}] | Agent at: {env.agent_pos}")
        print(env.render_ascii())
        print("-" * 40)

    if env.agent_pos == env.goal_pos:
        print(f"\n[+] SUCCESS! Puzzle solved in {step} steps (Oracle: {len(oracle_traj)} steps).")
        print(f"[+] Optimality: {step / max(1, len(oracle_traj)):.2f}x")
    else:
        print(f"\n[-] Failed to reach goal within {max_steps} steps.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--grid_size", type=int, default=8, help="Test grid size (e.g., 8 or 10)")
    parser.add_argument("--seed", type=int, default=123, help="Random seed for procedural layout")
    args = parser.parse_args()
    run_demo(grid_size=args.grid_size, seed=args.seed)
