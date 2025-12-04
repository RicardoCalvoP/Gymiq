from dataclasses import dataclass
from typing import Dict, Tuple, Set
import random

from ..rl_engine.action_space import ACTION_SPACE_KG
from .compute_functions import compute_reward


DOLOR_CATS = ["no_dolor", "molestia", "dolor"]


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

    En este entorno SOLO varían explícitamente:
      - peso_kg_actual      (peso levantado por set)
      - reps_real           (repeticiones por set)
      - dolor_actual        (no_dolor, molestia, dolor)

    Todo lo demás es constante o derivado de esas variables.
    """

    user_profile: Dict
    current_state: Dict
    max_steps: int = 50
    # Límite de variaciones distintas (peso, rango de reps, categoría de dolor)
    num_explorations: int = 500

    def __post_init__(self):
        self.step_count = 0
        # Conjunto de variaciones visitadas: (peso_bucket, reps_bucket, dolor_idx)
        self.visited_variations: Set[Tuple[int, int, int]] = set()

        # Aseguramos algunos campos básicos en el estado
        if "dolor_actual" not in self.current_state:
            self.current_state["dolor_actual"] = "no_dolor"

        # Repeticiones objetivo por set (constante del plan)
        if "reps_objetivo" not in self.current_state:
            # Default razonable si no viene del backend
            self.current_state["reps_objetivo"] = 8

        # Volumen objetivo opcional, si no viene lo derivamos cuando haga falta
        if "volumen_objetivo" not in self.current_state:
            peso_kg = self.current_state.get("peso_kg_actual", 0.0)
            reps_obj = self.current_state["reps_objetivo"]
            self.current_state["volumen_objetivo"] = peso_kg * reps_obj

    def reset(self) -> Dict:
        """Reinicia el episodio."""
        self.step_count = 0
        self.visited_variations.clear()
        return self.current_state

    # ----------------- Helpers internos -----------------

    def _simulate_reps(self, new_peso: float) -> int:
        """
        Simula reps_real en función del peso y reps_objetivo.

        Objetivo: cubrir muchas combinaciones:
          - muchas reps / mucho peso
          - muchas reps / poco peso
          - pocas reps / mucho peso
          - pocas reps / poco peso
        """
        reps_obj = self.current_state["reps_objetivo"]
        # Peso "base" del plan para este set (si no viene, usamos el peso previo)
        peso_base_plan = self.current_state.get(
            "peso_base_plan", self.current_state.get(
                "peso_kg_actual", new_peso)
        )

        # Carga relativa vs el plan
        carga_rel = (new_peso - peso_base_plan) / max(1.0, peso_base_plan)

        # Ruido discreto amplio para forzar exploración
        ruido = random.randint(-3, 3)

        # Regla simple:
        # - Si estás muy por encima del plan, tendemos a menos reps,
        #   pero con algo de probabilidad de muchas reps (para explorar).
        # - Si estás muy por debajo, tendemos a más reps.
        if carga_rel > 0.30:
            if random.random() < 0.7:
                reps_real = max(1, reps_obj - random.randint(2, 6) + ruido)
            else:
                reps_real = max(1, reps_obj + random.randint(0, 4) + ruido)
        elif carga_rel < -0.30:
            if random.random() < 0.7:
                reps_real = max(1, reps_obj + random.randint(2, 6) + ruido)
            else:
                reps_real = max(1, reps_obj - random.randint(0, 3) + ruido)
        else:
            # Zona intermedia ⇒ reps alrededor del objetivo con ruido fuerte
            reps_real = max(1, reps_obj + ruido)

        # Cota razonable de reps
        reps_real = max(1, min(25, reps_real))
        return reps_real

    def _compute_rpe_real(self, new_peso: float, reps_real: int) -> float:
        """
        Calcula RPE real en función de peso y reps, más ruido.
        """
        rpe_obj = self.current_state["rpe_objetivo"]
        reps_obj = self.current_state["reps_objetivo"]
        prev_peso = self.current_state["peso_kg_actual"]

        # Carga relativa vs peso previo
        carga_rel_peso = (new_peso - prev_peso) / max(1.0, prev_peso)
        # Fatiga por reps vs objetivo
        fatiga_reps = (reps_real - reps_obj) / max(1, reps_obj)

        rpe_real = (
            rpe_obj
            + 1.0 * carga_rel_peso   # peso más alto ⇒ más RPE
            + 0.7 * fatiga_reps      # más reps que el objetivo ⇒ más RPE
        )

        # Ruido continuo para romper determinismo
        rpe_real += random.uniform(-0.5, 0.5)
        rpe_real = max(4.0, min(10.0, rpe_real))
        return rpe_real

    def _simulate_dolor_cat(self, new_peso: float, reps_real: int, rpe_real: float) -> Tuple[str, float]:
        """
        Simula categoría de dolor (no_dolor, molestia, dolor) y devuelve también pain_prob.
        """
        lesion_tipo = self.current_state["historial_lesion_tipo"]
        dolor_prev = self.current_state.get("dolor_actual", "no_dolor")
        reps_obj = self.current_state["reps_objetivo"]
        prev_peso = self.current_state["peso_kg_actual"]

        # Riesgo base
        pain_prob = 0.02

        # Lesión
        if lesion_tipo == "leve":
            pain_prob += 0.05
        elif lesion_tipo == "moderada":
            pain_prob += 0.12
        elif lesion_tipo == "grave":
            pain_prob += 0.20

        # Dolor previo
        if dolor_prev == "molestia":
            pain_prob += 0.10
        elif dolor_prev == "dolor":
            pain_prob += 0.25

        # RPE alto
        if rpe_real > 9:
            pain_prob += 0.25
        elif rpe_real > 8:
            pain_prob += 0.15
        elif rpe_real < 6:
            pain_prob -= 0.02

        # Carga relativa vs peso previo
        carga_rel_peso = (new_peso - prev_peso) / max(1.0, prev_peso)
        if carga_rel_peso > 0.30:
            pain_prob += 0.10
        elif carga_rel_peso < -0.30:
            pain_prob -= 0.02

        # Muchas reps también aportan riesgo
        if reps_real > reps_obj + 3:
            pain_prob += 0.10

        # Clamp
        pain_prob = max(0.0, min(1.0, pain_prob))

        u = random.random()
        if u < pain_prob * 0.5:
            dolor_cat = "molestia"
        elif u < pain_prob:
            dolor_cat = "dolor"
        else:
            dolor_cat = "no_dolor"

        return dolor_cat, pain_prob

    def _bucket_variation(self, peso_kg: float, reps_real: int, dolor_cat: str) -> Tuple[int, int, int]:
        """
        Discretiza (peso, reps, dolor) para contar variaciones únicas.

        - peso_bucket: pasos de ~2.5 kg
        - reps_bucket: rangos de reps
        - dolor_idx: índice en DOLOR_CATS
        """
        # Peso en "bloques" de 2.5 kg (redondeado)
        peso_bucket = int(round(peso_kg / 2.5))

        # Rangos de reps (0-4, 5-8, 9-12, 13+)
        if reps_real <= 4:
            reps_bucket = 0
        elif reps_real <= 8:
            reps_bucket = 1
        elif reps_real <= 12:
            reps_bucket = 2
        else:
            reps_bucket = 3

        try:
            dolor_idx = DOLOR_CATS.index(dolor_cat)
        except ValueError:
            dolor_idx = 0  # fallback a "no_dolor"

        return peso_bucket, reps_bucket, dolor_idx

    # ----------------- Paso principal del entorno -----------------

    def step(self, action_idx: int) -> Tuple[Dict, float, bool, Dict]:
        """
        Ejecuta un paso del entorno dado un índice de acción.
        La acción decide delta_kg, el entorno simula reps y dolor.
        """

        self.step_count += 1

        # ----- Acción → peso -----
        delta_kg = ACTION_SPACE_KG[action_idx]

        prev_peso = self.current_state["peso_kg_actual"]
        new_peso = max(0.0, prev_peso + delta_kg)

        # ----- Simular reps -----
        reps_real = self._simulate_reps(new_peso)

        # ----- Calcular RPE real -----
        rpe_real = self._compute_rpe_real(new_peso, reps_real)
        rpe_obj = self.current_state["rpe_objetivo"]

        # ----- Simular dolor categórico -----
        dolor_cat, pain_prob = self._simulate_dolor_cat(
            new_peso, reps_real, rpe_real)
        hubo_dolor = dolor_cat != "no_dolor"

        # ----- Volumen y ratios -----
        reps_obj = self.current_state["reps_objetivo"]
        volumen_real = new_peso * reps_real
        volumen_obj = self.current_state.get(
            "volumen_objetivo", prev_peso * reps_obj)

        ratio_volumen = volumen_real / max(1.0, volumen_obj)
        ratio_reps = reps_real / max(1, reps_obj)

        lesion_tipo = self.current_state["historial_lesion_tipo"]

        # ----- Recompensa -----
        reward = compute_reward(
            rpe_objetivo=rpe_obj,
            rpe_real=rpe_real,
            hubo_dolor=hubo_dolor,
            progreso_kg=(new_peso - prev_peso),
            ratio_volumen=ratio_volumen,
            ratio_reps=ratio_reps,
            lesion_tipo=lesion_tipo,
        )

        # ----- Actualizar estado -----
        self.current_state = {
            **self.current_state,
            "peso_kg_actual": new_peso,
            "rpe_real": rpe_real,
            "reps_real": reps_real,
            "ratio_volumen": ratio_volumen,
            "ratio_reps": ratio_reps,
            "dolor_actual": dolor_cat,
        }

        # ----- Registrar variación explorada -----
        variation_id = self._bucket_variation(new_peso, reps_real, dolor_cat)
        self.visited_variations.add(variation_id)

        # Terminar por pasos o por número de variaciones distintas alcanzadas
        done = (
            self.step_count >= self.max_steps
            or len(self.visited_variations) >= self.num_explorations
        )

        info = {
            "delta_kg": delta_kg,
            "hubo_dolor": hubo_dolor,
            "pain_prob": pain_prob,
            "reps_real": reps_real,
            "dolor_cat": dolor_cat,
            "visited_variations": len(self.visited_variations),
        }

        return self.current_state, reward, done, info
