# src/training/simple_env.py

from dataclasses import dataclass
from typing import Dict, Tuple
import random

from ..rl_engine.action_space import ACTION_SPACE_KG
from .compute_functions import compute_reward


@dataclass
class SimpleStrengthEnv:
    """
    Entorno simplificado para entrenamiento RL.

    Usa un 'state_raw' como los del backend:
      - peso_kg_actual
      - rpe_objetivo
      - rpe_real (será actualizado)
      - historial_lesion_tipo
      - historial_lesion_tiempo_semanas
      - dolor_actual
    """

    user_profile: Dict
    current_state: Dict
    max_steps: int = 10

    def __post_init__(self):
        self.step_count = 0

    def reset(self) -> Dict:
        """Reinicia el episodio."""
        self.step_count = 0
        return self.current_state

    def step(self, action_idx: int) -> Tuple[Dict, float, bool, Dict]:

        self.step_count += 1

        delta_kg = ACTION_SPACE_KG[action_idx]

        prev_peso = self.current_state["peso_kg_actual"]
        new_peso = max(0.0, prev_peso + delta_kg)

        rpe_obj = self.current_state["rpe_objetivo"]

        # Subir peso aumenta RPE, bajar lo reduce
        base_effect = (delta_kg / 2.5) * 0.5
        rpe_real = rpe_obj + base_effect

        # Ruido para que no sea determinista
        rpe_real += random.uniform(-0.3, 0.3)
        rpe_real = max(1.0, min(10.0, rpe_real))

        # ===== Simulación de dolor =====
        # Basada en:
        #   historial_lesion_tipo
        #   historial_lesion_tiempo_semanas
        #   dolor_actual
        #   rpe_real

        dolor_actual = self.current_state.get("dolor_actual", "no_dolor")
        lesion_tipo = self.current_state["historial_lesion_tipo"]

        # Lesiones:
        pain_prob = 0.01
        if lesion_tipo in ("moderada", "grave"):
            pain_prob += 0.10
        elif lesion_tipo == "leve":
            pain_prob += 0.05

        # Dolor previo:
        if dolor_actual != "no_dolor":
            pain_prob += 0.10

        # RPE muy alto:
        if rpe_real > 9:
            pain_prob += 0.25
        elif rpe_real > 8:
            pain_prob += 0.15
        elif rpe_real < 6:
            pain_prob -= 0.02

        # Subir peso aumenta riesgo
        if delta_kg > 0:
            pain_prob += 0.05

        # Clamp final
        pain_prob = max(0.0, min(1.0, pain_prob))
        hubo_dolor = random.random() < pain_prob

        # ===== Calcular recompensa =====

        reward = compute_reward(
            rpe_objetivo=rpe_obj,
            rpe_real=rpe_real,
            hubo_dolor=hubo_dolor,
            progreso_kg=(new_peso - prev_peso),
        )

        # ===== Actualizar estado =====
        self.current_state = {
            **self.current_state,
            "peso_kg_actual": new_peso,
            "rpe_real": rpe_real,
            # Si quieres, podrías actualizar dolor_actual
            # "dolor_actual": "dolor" if hubo_dolor else "no_dolor"
        }

        done = self.step_count >= self.max_steps

        info = {
            "delta_kg": delta_kg,
            "hubo_dolor": hubo_dolor,
            "pain_prob": pain_prob,
        }

        return self.current_state, reward, done, info
