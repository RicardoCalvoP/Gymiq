# src/training/train_full_pipeline.py

from __future__ import annotations

from typing import List, Tuple, Dict, Any
import json

import torch
import torch.optim as optim

from ..rl_engine.config import MODELS_DIR, DUMMY_FILE
from ..rl_engine.state_builder import build_state_raw_from_exercise, encode_state
from ..rl_engine.policy_net import PolicyNetwork
from .train_from_teacher import train_policy_from_teacher
from .simple_env import SimpleStrengthEnv
from .train_reinforce import train_policy_gradient


def load_logs(path) -> List[Dict[str, Any]]:
    """
    Carga exerciseData.json o logs históricos.

    Espera formato tipo frontend:

    [
      {
        "perfil": {...},
        "sesion_num": 17,
        "ejercicios": [
          {
            "name": "...",
            "reps_objetivo": 8,
            "rpe_objetivo": 8.0,
            "sets": [
              {"reps": 8, "rpe": 8.0, "peso_kg": 60.0},
              ...
            ]
          },
          ...
        ]
      },
      ...
    ]
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict):
        return [data]
    if isinstance(data, list):
        return data
    raise ValueError("Formato de logs inválido: debe ser dict o list.")


def build_states_and_meta(
    logs: List[Dict[str, Any]],
) -> List[Tuple[torch.Tensor, Dict[str, Any]]]:
    """
    Convierte logs reales → lista (state_tensor, meta) para el Maestro.

    meta tiene exactamente los campos que necesita rule_based_delta_from_meta:
      - rpe_real
      - rpe_objetivo
      - edad
      - historial_lesion_tipo
      - historial_lesion_tiempo_semanas
      - lesion_dolor_actual
    """
    states_and_meta: List[Tuple[torch.Tensor, Dict[str, Any]]] = []

    for entry in logs:
        user_profile = entry["perfil"]
        sesion_num = entry.get("sesion_num", entry.get("sessionNum", 1))

        ejercicios = entry.get("ejercicios", [])
        if not ejercicios:
            continue

        for ex in ejercicios:
            # 1) state_raw tal como en producción
            state_raw = build_state_raw_from_exercise(
                user_profile=user_profile,
                exercise=ex,
                sesion_num=sesion_num,
            )

            # 2) tensor de estado [D_STATE]
            state_tensor = encode_state(state_raw)

            # 3) meta para el Maestro (reglas)
            meta = {
                "rpe_real": state_raw["rpe_real"],
                "rpe_objetivo": state_raw["rpe_objetivo"],
                "edad": user_profile["edad"],
                "historial_lesion_tipo": user_profile["historial_lesion_tipo"],
                "historial_lesion_tiempo_semanas": user_profile[
                    "historial_lesion_tiempo_semanas"
                ],
                # rule_based_delta_from_meta espera esta key exacta:
                # meta["lesion_dolor_actual"]
                "lesion_dolor_actual": user_profile["dolor_actual"],
            }

            states_and_meta.append((state_tensor, meta))

    return states_and_meta


def main():
    # ============================
    # 1) Cargar logs y armar dataset del Maestro
    # ============================
    logs_path = DUMMY_FILE
    if not logs_path.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo de logs: {logs_path}\n"
            "Crea exerciseData.json con el formato de tu frontend."
        )

    print(f"[FullPipeline] Cargando logs desde: {logs_path}")
    logs = load_logs(logs_path)

    states_and_meta = build_states_and_meta(logs)
    if not states_and_meta:
        raise ValueError(
            "No se generaron estados para el Maestro. "
            "Revisa que tus logs tengan 'perfil' y 'ejercicios' válidos."
        )

    print(
        f"[FullPipeline] Dataset del Maestro listo: {len(states_and_meta)} muestras")

    # ============================
    # 2) Entrenar política desde Maestro (reglas)
    # ============================
    policy_teacher = train_policy_from_teacher(
        states_and_meta=states_and_meta,
        n_epochs=50,
        lr=1e-3,
    )

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    teacher_path = MODELS_DIR / "policy_teacher.pt"
    torch.save(policy_teacher.state_dict(), teacher_path)
    print(f"[FullPipeline] Pesos del Maestro guardados en: {teacher_path}")

    # ============================
    # 3) Preparar entorno RL (SimpleStrengthEnv) con un caso real
    # ============================
    # Tomamos el primer log y primer ejercicio como estado inicial de ejemplo
    first_log = logs[0]
    user_profile = first_log["perfil"]
    sesion_num = first_log.get("sesion_num", first_log.get("sessionNum", 1))
    first_exercise = first_log["ejercicios"][0]

    initial_state_raw = build_state_raw_from_exercise(
        user_profile=user_profile,
        exercise=first_exercise,
        sesion_num=sesion_num,
    )

    env = SimpleStrengthEnv(
        user_profile=user_profile,
        current_state=initial_state_raw,
        max_steps=5,
    )

    # ============================
    # 4) Inicializar policy RL desde el Maestro
    # ============================
    policy_rl = PolicyNetwork()
    policy_rl.load_state_dict(policy_teacher.state_dict())

    optimizer = optim.Adam(policy_rl.parameters(), lr=1e-3)

    # ============================
    # 5) Afinar con REINFORCE en el entorno simulado
    # ============================
    train_policy_gradient(
        env=env,
        policy=policy_rl,
        optimizer=optimizer,
        n_episodes=500,
        gamma=0.99,
    )

    # ============================
    # 6) Guardar pesos finales (para backend)
    # ============================
    rl_path = MODELS_DIR / "policy_reinforce.pt"
    latest_path = MODELS_DIR / "policy_latest.pt"

    torch.save(policy_rl.state_dict(), rl_path)
    torch.save(policy_rl.state_dict(), latest_path)

    print(f"[FullPipeline] Modelo RL guardado en: {rl_path}")
    print(f"[FullPipeline] Modelo para backend actualizado en: {latest_path}")


if __name__ == "__main__":
    main()
