from typing import List, Tuple, Dict, Any
import json

import torch
import torch.nn as nn
import torch.optim as optim

from ..rl_engine.state_builder import build_state_raw_from_exercise, encode_state
from ..rl_engine.policy_net import PolicyNetwork
from ..rl_engine.action_space import ACTION_SPACE_KG
from .compute_functions import rule_based_delta_from_meta


def build_states_and_meta_from_logs(logs_path: str) -> List[Tuple[torch.Tensor, Dict[str, Any]]]:
    """
    Carga logs en formato frontend y construye:
      - state_tensor: encode_state(state_raw)
      - meta: dict con la info que necesita rule_based_delta_from_meta
    """
    with open(logs_path, "r", encoding="utf-8") as f:
        logs = json.load(f)

    # Permite tanto {"...": ...} como [ {...}, {...} ]
    if isinstance(logs, dict):
        logs = [logs]

    states_and_meta: List[Tuple[torch.Tensor, Dict[str, Any]]] = []

    for log_entry in logs:
        user_profile = log_entry["perfil"]
        sesion_num = log_entry.get(
            "sesion_num", log_entry.get("sessionNum", 1))

        for ex in log_entry["ejercicios"]:
            # 1) state_raw (como en producción)
            state_raw = build_state_raw_from_exercise(
                user_profile=user_profile,
                exercise=ex,
                sesion_num=sesion_num,
            )

            # 2) tensor de estado
            state_tensor = encode_state(state_raw)

            # 3) meta para el Maestro
            meta: Dict[str, Any] = {
                "rpe_real": state_raw["rpe_real"],
                "rpe_objetivo": state_raw["rpe_objetivo"],
                "edad": user_profile["edad"],
                "historial_lesion_tipo": user_profile["historial_lesion_tipo"],
                "historial_lesion_tiempo_semanas": user_profile["historial_lesion_tiempo_semanas"],
                "lesion_dolor_actual": user_profile["dolor_actual"],
            }

            states_and_meta.append((state_tensor, meta))

    return states_and_meta


def _delta_to_action_idx(delta_kg: float) -> int:
    """
    Convierte el delta continuo del Maestro al índice discreto en ACTION_SPACE_KG.
    Si el delta no cae exactamente, elige el más cercano.
    """
    # Intentar match exacto primero
    for i, d in enumerate(ACTION_SPACE_KG):
        if abs(d - delta_kg) < 1e-6:
            return i

    # Si no hay match exacto, mapeamos al más cercano
    diffs = [abs(delta_kg - d) for d in ACTION_SPACE_KG]
    return int(min(range(len(ACTION_SPACE_KG)), key=lambda i: diffs[i]))


def train_policy_from_teacher(
    states_and_meta: List[Tuple[torch.Tensor, Dict[str, Any]]],
    n_epochs: int = 50,
    lr: float = 1e-3,
) -> PolicyNetwork:
    """
    Entrena una PolicyNetwork para imitar al Maestro (rule_based_delta_from_meta).

    states_and_meta:
      lista de (state_tensor, meta) donde:
        - state_tensor: salida de encode_state(state_raw) [D_STATE]
        - meta: dict con campos para rule_based_delta_from_meta(meta)
    """
    if not states_and_meta:
        raise ValueError("train_policy_from_teacher: states_and_meta vacío.")

    policy = PolicyNetwork()
    optimizer = optim.Adam(policy.parameters(), lr=lr)

    policy.train()

    for epoch in range(n_epochs):
        total_loss = 0.0

        # (opcional) podrías barajear aquí:
        # random.shuffle(states_and_meta)

        for state_tensor, meta in states_and_meta:
            # Teacher: delta sugerido por Maestro
            delta_teacher = rule_based_delta_from_meta(meta)
            target_idx = _delta_to_action_idx(delta_teacher)

            # Forward de la policy
            probs = policy(state_tensor)          # [1, n_actions]
            probs = probs.squeeze(0)              # [n_actions]

            # Log-prob de la acción del Maestro
            log_prob = torch.log(probs[target_idx] + 1e-8)

            loss = -log_prob  # maximizar log_prob = minimizar -log_prob

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            total_loss += float(loss.item())

        avg_loss = total_loss / max(1, len(states_and_meta))
        if (epoch + 1) % 10 == 0:
            print(
                f"[Teacher] Epoch {epoch+1}/{n_epochs} | Loss media: {avg_loss:.6f}")

    policy.eval()
    return policy
