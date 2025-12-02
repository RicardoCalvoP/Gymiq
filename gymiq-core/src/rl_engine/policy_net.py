from typing import Tuple

import torch
import torch.nn as nn

from .state_builder import D_STATE
from .action_space import ACTION_SPACE_KG, N_ACTIONS


class PolicyNetwork(nn.Module):
    def __init__(self, state_dim: int = D_STATE, n_actions: int = N_ACTIONS) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(state_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, n_actions),  # logits para cada acción
        )

    def forward(self, state: torch.Tensor) -> torch.Tensor:
        """
        state: tensor [D_STATE] o [batch, D_STATE]
        return: tensor [batch, n_actions] con probabilidades sobre acciones.
        """
        if state.dim() == 1:
            state = state.unsqueeze(0)  # [D_STATE] -> [1, D_STATE]

        logits = self.net(state)       # [batch, n_actions]
        probs = torch.softmax(logits, dim=-1)
        return probs

    def act(self, state: torch.Tensor) -> Tuple[int, float]:
        """
        Escoge una acción según la política actual.

        Devuelve:
          - action_idx: índice en ACTION_SPACE_KG
          - log_prob: logπ(a|s) como escalar float (para REINFORCE)
        """
        probs = self.forward(state)        # [1, n_actions]
        dist = torch.distributions.Categorical(probs=probs)
        action_idx = dist.sample()         # tensor [1]
        log_prob = dist.log_prob(action_idx)  # [1]
        return int(action_idx.item()), float(log_prob.item())


# ============================================================
# Validación de la red de política (solo modo debug)
# ============================================================

if __name__ == "__main__":
    from .state_builder import D_STATE  # redundante pero explícito

    print("\n========================")
    print("VALIDANDO RED DE POLÍTICA")
    print("========================\n")

    # Instancia de la red de política para depuración
    policy_debug = PolicyNetwork(state_dim=D_STATE, n_actions=N_ACTIONS)

    print("Estructura de la red de política:")
    print(policy_debug)

    # Vector de entrada dummy (todo ceros) para probar shapes
    dummy_state = torch.zeros(D_STATE, dtype=torch.float32)
    print("\nVector de estado dummy (solo para probar shapes):")
    print("Valor:", dummy_state)
    print("Shape:", dummy_state.shape)

    # Pasamos el dummy por la red
    probs_debug = policy_debug(dummy_state)

    print("\nSalida de la red (probabilidades de acciones):")
    print("Probabilidades:", probs_debug.detach().numpy())
    print("Suma de probabilidades (debe ≈ 1.0):", probs_debug.sum().item())

    # Probamos el método act() para ver qué acción samplea
    action_idx_debug, logp_debug = policy_debug.act(dummy_state)

    print("\nAcción sampleada por la política (modo debug):")
    print("Índice de acción:", action_idx_debug)
    print("Δ kg asociado:", ACTION_SPACE_KG[action_idx_debug])
    print("log_prob de la acción:", logp_debug)

    print("\n========================\n")
