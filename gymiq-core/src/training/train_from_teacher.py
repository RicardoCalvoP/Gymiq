from typing import List, Tuple
import torch
import torch.optim as optim

from ..rl_engine.policy_net import PolicyNetwork


def train_policy_from_teacher(
    states_and_targets: List[Tuple[torch.Tensor, int]],
    n_epochs: int = 50,
    lr: float = 1e-3,
) -> PolicyNetwork:
    """
    Entrena una PolicyNetwork para imitar al Maestro.

    states_and_targets:
      lista de (state_tensor, target_idx) donde:
        - state_tensor: salida de encode_state(state_raw) [D_STATE]
        - target_idx: índice de acción en ACTION_SPACE_KG
    """
    if not states_and_targets:
        raise ValueError(
            "train_policy_from_teacher: states_and_targets vacío.")

    policy = PolicyNetwork()
    optimizer = optim.Adam(policy.parameters(), lr=lr)

    policy.train()

    for epoch in range(n_epochs):
        total_loss = 0.0

        for state_tensor, target_idx in states_and_targets:
            probs = policy(state_tensor)          # [1, n_actions]
            probs = probs.squeeze(0)              # [n_actions]

            log_prob = torch.log(probs[target_idx] + 1e-8)
            loss = -log_prob

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
    return policy
