from __future__ import annotations

from typing import List, Tuple, Dict, Any
import json

import torch
import torch.optim as optim

from ..rl_engine.config import MODELS_DIR, DUMMY_FILE
from ..rl_engine.state_builder import build_state_raw_from_exercise, encode_state
from ..rl_engine.policy_net import PolicyNetwork
from ..rl_engine.action_space import ACTION_SPACE_KG
from .compute_functions import rule_based_delta_from_meta
from .train_from_teacher import train_policy_from_teacher
from .simple_env import SimpleStrengthEnv
from .train_reinforce import train_policy_gradient


def load_logs(path) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict):
        return [data]
    if isinstance(data, list):
        return data
    raise ValueError("Formato de logs inválido: debe ser dict o list.")


def _delta_to_action_idx(delta_kg: float) -> int:
    """
    Mapea un delta_kg continuo al índice más cercano en ACTION_SPACE_KG.
    """
    for i, d in enumerate(ACTION_SPACE_KG):
        if abs(d - delta_kg) < 1e-6:
            return i
    diffs = [abs(delta_kg - d) for d in ACTION_SPACE_KG]
    return int(min(range(len(ACTION_SPACE_KG)), key=lambda i: diffs[i]))


def build_states_and_targets(
    logs: List[Dict[str, Any]],
) -> List[Tuple[torch.Tensor, int]]:
    """
    Logs reales → lista (state_tensor, target_idx) para el Maestro.
    El Maestro usa rule_based_delta_from_meta(state_raw, user_profile).

    IMPORTANTE: ahora recorre TODOS los ejercicios de TODOS los logs
    (se quitó el return dentro del primer ejercicio).
    """
    states_and_targets: List[Tuple[torch.Tensor, int]] = []

    for log_entry in logs:
        user_profile = log_entry["perfil"]
        sesion_num = log_entry.get(
            "sesion_num", log_entry.get("sessionNum", 1))

        ejercicios = log_entry.get("ejercicios", [])
        if not ejercicios:
            continue

        for ex in ejercicios:
            state_raw = build_state_raw_from_exercise(
                user_profile=user_profile,
                exercise=ex,
                sesion_num=sesion_num,
            )
            state_tensor = encode_state(state_raw)

            # Maestro basado en state_raw + user_profile
            delta_teacher = rule_based_delta_from_meta(state_raw, user_profile)
            target_idx = _delta_to_action_idx(delta_teacher)

            print(
                "TEACHER(real):", delta_teacher,
                "vol:", state_raw["ratio_volumen"],
                "reps:", state_raw["ratio_reps"],
                "rpe_real:", state_raw["rpe_real"],
            )

            states_and_targets.append((state_tensor, target_idx))

    return states_and_targets


def build_synthetic_teacher_dataset(
    logs: List[Dict[str, Any]],
    episodes_per_exercise: int = 20,
    max_steps_per_episode: int = 250,
    num_explorations: int = 1000,
) -> List[Tuple[torch.Tensor, int]]:
    """
    Usa SimpleStrengthEnv + rule_based_delta_from_meta para generar
    un dataset grande (state_tensor, target_idx) para el Maestro.

    Política que actúa en el entorno: el Maestro de reglas.
    """
    synthetic_data: List[Tuple[torch.Tensor, int]] = []

    for log_entry in logs:
        user_profile = log_entry["perfil"]
        sesion_num = log_entry.get(
            "sesion_num", log_entry.get("sessionNum", 1))

        ejercicios = log_entry.get("ejercicios", [])
        if not ejercicios:
            continue

        for ex in ejercicios:
            # Estado inicial realista basado en el log
            initial_state_raw = build_state_raw_from_exercise(
                user_profile=user_profile,
                exercise=ex,
                sesion_num=sesion_num,
            )

            env = SimpleStrengthEnv(
                user_profile=user_profile,
                current_state=initial_state_raw,
                max_steps=max_steps_per_episode,
                num_explorations=num_explorations,
            )

            for ep in range(episodes_per_exercise):
                state_raw = env.reset()
                done = False
                steps = 0

                while not done and steps < max_steps_per_episode:
                    # Estado → tensor
                    state_tensor = encode_state(state_raw)

                    # Maestro de reglas decide delta de peso
                    delta_teacher = rule_based_delta_from_meta(
                        state_raw, user_profile)
                    target_idx = _delta_to_action_idx(delta_teacher)

                    # Guardamos (estado, acción del teacher)
                    synthetic_data.append((state_tensor, target_idx))

                    # Avanzamos el entorno con la acción del teacher
                    next_state_raw, _, done, info = env.step(target_idx)

                    state_raw = next_state_raw
                    steps += 1

            print(
                f"[SyntheticTeacher] Ejercicio '{ex.get('name', '')}': "
                f"{episodes_per_exercise} episodios simulados"
            )

    print(
        f"[SyntheticTeacher] Dataset sintético generado: "
        f"{len(synthetic_data)} muestras"
    )
    return synthetic_data


def eval_teacher(policy, states_and_targets):
    correct = 0
    total = 0
    with torch.no_grad():
        for state_tensor, target_idx in states_and_targets:
            probs = policy(state_tensor)      # [1, n_actions]
            pred = probs.argmax(dim=1).item()  # índice acción
            if pred == target_idx:
                correct += 1
            total += 1
    acc = correct / max(1, total)
    print(f"[Teacher] Accuracy: {acc*100:.2f}% ({correct}/{total})")


def main():
    # 1) Cargar logs y armar dataset del Maestro (real + sintético)
    logs_path = DUMMY_FILE
    if not logs_path.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo de logs: {logs_path}\n"
            "Crea exerciseData.json con el formato de tu frontend."
        )

    print(f"[FullPipeline] Cargando logs desde: {logs_path}")
    logs = load_logs(logs_path)

    # Datos reales del teacher (pocos pero exactos)
    real_states_and_targets = build_states_and_targets(logs)

    if not real_states_and_targets:
        raise ValueError(
            "No se generaron estados reales para el Maestro. "
            "Revisa que tus logs tengan 'perfil' y 'ejercicios' válidos."
        )

    # Datos sintéticos usando el entorno (miles de estados)
    synthetic_states_and_targets = build_synthetic_teacher_dataset(
        logs=logs,
        episodes_per_exercise=20,
        max_steps_per_episode=20,
        num_explorations=250,
    )

    states_and_targets = real_states_and_targets + synthetic_states_and_targets

    print(
        f"[FullPipeline] Dataset total del Maestro listo: "
        f"{len(states_and_targets)} muestras "
        f"({len(real_states_and_targets)} reales, "
        f"{len(synthetic_states_and_targets)} sintéticas)"
    )

    # 2) Entrenar política desde Maestro (reglas) con TODO el dataset
    policy_teacher = train_policy_from_teacher(
        states_and_targets=states_and_targets,
        n_epochs=100,
        lr=1e-3,
        device=DEVICE,
    )
    eval_teacher(policy_teacher, states_and_targets)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    teacher_path = MODELS_DIR / "policy_teacher.pt"
    torch.save(policy_teacher.state_dict(), teacher_path)
    print(f"[FullPipeline] Pesos del Maestro guardados en: {teacher_path}")

    # 3) Inicializar policy RL desde el Maestro UNA sola vez
    policy_rl = PolicyNetwork().to(DEVICE)
    policy_rl.load_state_dict(policy_teacher.state_dict())
    optimizer = optim.Adam(policy_rl.parameters(), lr=1e-3)

    # 4) Afinar con REINFORCE en el entorno simulado
    #    Recorremos todos los logs y ejercicios; el mismo policy_rl se
    #    sigue entrenando en todos los entornos.
    for log_entry in logs:
        user_profile = log_entry["perfil"]
        sesion_num = log_entry.get(
            "sesion_num", log_entry.get("sessionNum", 1))

        ejercicios = log_entry.get("ejercicios", [])
        if not ejercicios:
            continue

        for ex in ejercicios:
            print(f"***************first_exercise***********{ex}")

            initial_state_raw = build_state_raw_from_exercise(
                user_profile=user_profile,
                exercise=ex,
                sesion_num=sesion_num,
            )

            env = SimpleStrengthEnv(
                user_profile=user_profile,
                current_state=initial_state_raw,
                max_steps=200,        # suficientemente grande
                num_explorations=250,
            )

            # Afinar con REINFORCE en este ejercicio/perfil
            train_policy_gradient(
                env=env,
                policy=policy_rl,
                optimizer=optimizer,
                n_episodes=50,
                gamma=0.98,
                device=DEVICE,
            )

    # 5) Guardar pesos finales (para backend)
    rl_path = MODELS_DIR / "policy_reinforce.pt"
    latest_path = MODELS_DIR / "policy_latest.pt"

    torch.save(policy_rl.state_dict(), rl_path)
    torch.save(policy_rl.state_dict(), latest_path)

    print(f"[FullPipeline] Modelo RL guardado en: {rl_path}")
    print(f"[FullPipeline] Modelo para backend actualizado en: {latest_path}")


if __name__ == "__main__":
    DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[FullPipeline] Usando device: {DEVICE}")
    main()
