"""Train the grid-navigation CNN baseline; evaluate Bellman-Ford as an exact solver."""

import os
import argparse
import torch
import torch.nn.functional as F
import torch.optim as optim
from riddlekeeper.dataset import get_dataloaders
from riddlekeeper.models import BaselineCNNPolicy


def train_epoch(model, loader, optimizer, device):
    model.train()
    total_loss = 0.0
    correct = 0
    total = 0

    for batch in loader:
        state = batch["state"].to(device)
        mask = batch["action_mask"].to(device)
        target_a = batch["action"].to(device)

        optimizer.zero_grad()

        logits, _ = model(state, action_mask=mask)
        loss = F.cross_entropy(logits, target_a)

        loss.backward()
        optimizer.step()

        total_loss += loss.item() * state.size(0)
        preds = logits.argmax(dim=-1)
        correct += (preds == target_a).sum().item()
        total += state.size(0)

    return total_loss / total, correct / total


@torch.no_grad()
def evaluate_epoch(model, loader, device):
    model.eval()
    total_loss = 0.0
    correct = 0
    total = 0

    for batch in loader:
        state = batch["state"].to(device)
        mask = batch["action_mask"].to(device)
        target_a = batch["action"].to(device)

        logits, _ = model(state, action_mask=mask)

        loss = F.cross_entropy(logits, target_a)
        total_loss += loss.item() * state.size(0)
        preds = logits.argmax(dim=-1)
        correct += (preds == target_a).sum().item()
        total += state.size(0)

    return total_loss / total, correct / total


def main():
    parser = argparse.ArgumentParser(description="Train Riddlekeeper Solvers")
    parser.add_argument("--epochs", type=int, default=15, help="Number of training epochs")
    parser.add_argument("--batch_size", type=int, default=32, help="Batch size")
    parser.add_argument("--lr", type=float, default=1e-3, help="Learning rate")
    parser.add_argument("--train_size", type=int, default=1200, help="Number of training configurations")
    parser.add_argument("--val_size", type=int, default=300, help="Number of validation configurations")
    parser.add_argument("--grid_size", type=int, default=5, help="Training grid dimensions (e.g., 5 for 5x5)")
    parser.add_argument("--checkpoint_dir", type=str, default="riddlekeeper/checkpoints", help="Output directory")
    args = parser.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[*] Training on device: {device}")
    print(f"[*] Configuration: Grid Size = {args.grid_size}x{args.grid_size}, Epochs = {args.epochs}")

    os.makedirs(args.checkpoint_dir, exist_ok=True)

    print("[*] Generating procedural datasets...")
    train_loader, val_loader = get_dataloaders(
        train_size=args.train_size,
        val_size=args.val_size,
        grid_size=args.grid_size,
        batch_size=args.batch_size,
        seed=42
    )

    # Bellman-Ford is an exact, parameter-free reference solver; train only
    # the learned policy baseline.
    print("\n" + "="*50)
    print(">>> Training Baseline CNN Policy (Standard Deep Learning)")
    print("="*50)
    cnn_model = BaselineCNNPolicy(in_channels=4, hidden_dim=32).to(device)
    cnn_optimizer = optim.Adam(cnn_model.parameters(), lr=args.lr)

    best_cnn_acc = 0.0
    for epoch in range(1, args.epochs + 1):
        tr_loss, tr_acc = train_epoch(cnn_model, train_loader, cnn_optimizer, device)
        val_loss, val_acc = evaluate_epoch(cnn_model, val_loader, device)
        print(f"CNN Epoch {epoch:02d}/{args.epochs:02d} | Train Loss: {tr_loss:.4f}, Acc: {tr_acc*100:.1f}% | Val Acc: {val_acc*100:.1f}%")

        if val_acc > best_cnn_acc:
            best_cnn_acc = val_acc
            torch.save(cnn_model.state_dict(), os.path.join(args.checkpoint_dir, "baseline_best.pt"))

    print("\n[+] Training Complete!")
    print(f"[+] Saved models to: {args.checkpoint_dir}")


if __name__ == "__main__":
    main()
