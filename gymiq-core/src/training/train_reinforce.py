# src/training/train_reinforce.py

from typing import List

import torch
import torch.optim as optim

from ..rl_engine.state_builder import (
    encode_state,
    build_state_raw_from_exercise,
)
from ..rl_engine.policy_net import PolicyNetwork
from ..rl_engine.action_space import N_ACTIONS
from ..rl_engine.config import MODELS_DIR

from .simple_env import SimpleStrengthEnv


def train_policy_gradient(
    env: SimpleStrengthEnv,
    policy: PolicyNetwork,
    optimizer: optim.Optimizer,
    n_episodes: int = 1000,
    gamma: float = 0.99,
) -> None:
    """
    Entrenamiento básico REINFORCE:
      - Recolecta episodios completos
      - Calcula retornos G_t
      - Actualiza la política con -E[ G_t * logπ(a_t|s_t) ]
    """
    for episode in range(n_episodes):
        state_raw = env.reset()
        log_probs: List[torch.Tensor] = []
        rewards: List[float] = []

        done = False
        while not done:
            # Estado → tensor
            state_tensor = encode_state(state_raw)  # [D_STATE]

            # Forward de la policy (con gradiente)
            probs = policy(state_tensor)           # [1, n_actions]
            dist = torch.distributions.Categorical(probs=probs)
            action = dist.sample()                 # tensor con el índice

            log_prob = dist.log_prob(action)       # tensor con grad_fn

            action_idx = int(action.item())

            # Paso en el entorno
            next_state_raw, reward, done, info = env.step(action_idx)

            log_probs.append(log_prob)             # ya es tensor con grad
            rewards.append(float(reward))

            state_raw = next_state_raw

        total_reward = sum(rewards)
        steps = len(rewards)

        # 1) Retornos descontados
        returns: List[float] = []
        G = 0.0
        for r in reversed(rewards):
            G = r + gamma * G
            returns.insert(0, G)

        returns_t = torch.tensor(returns, dtype=torch.float32)

        # 2) Normalizar retornos
        if returns_t.std() > 1e-8:
            returns_t = (returns_t - returns_t.mean()) / \
                (returns_t.std() + 1e-8)

        # 3) Loss de política
        policy_loss = []
        for log_prob, Gt in zip(log_probs, returns_t):
            policy_loss.append(-log_prob * Gt)

        loss = torch.stack(policy_loss).sum()
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if (episode + 1) % 100 == 0:
            avg_reward = total_reward / max(1, steps)
            print(
                f"Episodio {episode+1}/{n_episodes} | "
                f"Recompensa media: {avg_reward:.3f} | Loss: {loss.item():.3f}"
            )


def main():
    # 1) Definir un perfil real (ejemplo, aquí hardcodeado)
    user_profile = {
        "edad": 24,
        "imc": 25.0,
        "peso_usuario": 78.0,
        "sexo": "M",
        "historial_lesion_tipo": "ninguna",
        "historial_lesion_tiempo_semanas": 0,
        "dolor_actual": "no_dolor",
    }

    # 2) Definir un ejercicio realista (como lo manda tu frontend)
    exercise = {
        "name": "Press banca con barra",
        "reps_objetivo": 8,
        "rpe_objetivo": 8.0,
        "sets": [
            {"reps": 8, "rpe": 8.0, "peso_kg": 60.0},
            {"reps": 8, "rpe": 8.0, "peso_kg": 60.0},
            {"reps": 8, "rpe": 8.0, "peso_kg": 60.0},
        ],
    }

    # 3) Construimos el estado inicial raw
    initial_state_raw = build_state_raw_from_exercise(
        user_profile=user_profile,
        exercise=exercise,
        sesion_num=1,
    )

    # 4) Creamos el entorno RL
    env = SimpleStrengthEnv(
        user_profile=user_profile,
        current_state=initial_state_raw,
        max_steps=5,
    )

    # 5) Policy: puedes inicializarla desde cero...
    policy = PolicyNetwork()

    #    ...o, si ya tienes pesos del Maestro, cargarlos aquí:
    # weights_teacher = MODELS_DIR / "policy_teacher.pt"
    # policy.load_state_dict(torch.load(weights_teacher, map_location="cpu"))

    optimizer = optim.Adam(policy.parameters(), lr=1e-3)

    # 6) Entrenamiento REINFORCE
    train_policy_gradient(
        env=env,
        policy=policy,
        optimizer=optimizer,
        n_episodes=500,
        gamma=0.99,
    )

    # 7) Guardar modelo
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    weights_path = MODELS_DIR / "policy_reinforce.pt"
    torch.save(policy.state_dict(), weights_path)
    print(f"\nModelo RL guardado en: {weights_path}")


if __name__ == "__main__":
    main()
