from typing import List, Tuple
import torch
import torch.optim as optim

from ..rl_engine.policy_net import PolicyNetwork


def train_policy_from_teacher(
    states_and_targets: List[Tuple[torch.Tensor, int]],
    n_epochs: int = 50,
    lr: float = 1e-3,
    device: torch.device | None = None,
) -> PolicyNetwork:
    if device is None:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    policy = PolicyNetwork().to(device)
    optimizer = optim.Adam(policy.parameters(), lr=lr)
    loss_fn = torch.nn.CrossEntropyLoss()

    for epoch in range(n_epochs):
        total_loss = 0.0

        for state_tensor, target_idx in states_and_targets:
            # mover cada sample a la GPU
            state_tensor = state_tensor.to(device)
            target = torch.tensor(
                [target_idx], dtype=torch.long, device=device)

            logits = policy(state_tensor.unsqueeze(0))  # [1, n_actions]
            loss = loss_fn(logits, target)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            total_loss += float(loss.item())

        avg_loss = total_loss / max(1, len(states_and_targets))
        if (epoch + 1) % 10 == 0:
            print(
                f"[Teacher] Epoch {epoch+1}/{n_epochs} | Loss media: {avg_loss:.6f}"
            )

    policy.eval()
    return policy.to("cpu")
