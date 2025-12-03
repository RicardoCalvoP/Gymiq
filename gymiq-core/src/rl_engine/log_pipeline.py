from typing import Dict, Any, List

from .inference import PolicyService
from .state_builder import build_state_raw_from_exercise

# Instancia global de la policy (carga pesos si existen)
POLICY_SERVICE = PolicyService()


def _get_user_profile_from_log(log_entry: Dict[str, Any]) -> Dict[str, Any]:
    """
    Espera SIEMPRE un objeto 'perfil' enviado por el frontend.
    """
    perfil = log_entry.get("perfil")
    if not isinstance(perfil, dict):
        raise ValueError(
            "El payload /log/ debe incluir un objeto 'perfil' (dict).")
    return perfil


def _get_exercises_from_log(log_entry: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Espera SIEMPRE una lista 'ejercicios' enviada por el frontend.
    Cada ejercicio debe incluir al menos:
      - name: str
      - reps_objetivo: number
      - rpe_objetivo: number
      - sets: lista de { reps, rpe, peso_kg }
    """
    ejercicios = log_entry.get("ejercicios")
    if not isinstance(ejercicios, list) or not ejercicios:
        raise ValueError(
            "El payload /log/ debe incluir una lista 'ejercicios' no vacía."
        )
    return ejercicios


def ingest_log_entry(log_entry: Dict[str, Any]) -> None:
    """
    Entry point llamado por el endpoint /log/.

    Flujo esperado (formato final del frontend):
      1) log_entry.perfil: dict con datos del usuario.
      2) log_entry.ejercicios: lista de ejercicios con sets.
      3) Para cada ejercicio:
         - construir state_raw con build_state_raw_from_exercise,
         - pedir recomendación a la policy,
         - loguear current / delta / recommended.
    """

    workout_id = (
        log_entry.get("workout_id")
        or log_entry.get("workoutId")
        or "unknown_workout"
    )

    assert "sesion_num" in log_entry, "sesion_num debe existir después del modelo Pydantic"

    sesion_num = log_entry["sesion_num"]   # ya es int, Pydantic lo garantiza

    if sesion_num is None:
        raise ValueError("El payload /log/ debe incluir 'sesion_num' (int).")

    user_profile = _get_user_profile_from_log(log_entry)
    exercises = _get_exercises_from_log(log_entry)

    print(
        f"[RL_ENGINE] Workout log received: {workout_id} "
        f"({len(exercises)} ejercicios, sesion_num={sesion_num})"
    )

    for idx, ex in enumerate(exercises, start=1):
        # 1) Construir state_raw a partir de perfil + ejercicio
        state_raw = build_state_raw_from_exercise(
            user_profile=user_profile,
            exercise=ex,
            sesion_num=sesion_num,
        )

        # 2) Pedir recomendación de delta de peso a la policy
        result = POLICY_SERVICE.recommend_weight_delta(state_raw)
        delta_kg = result["delta_kg"]
        action_idx = result["action_index"]

        current_w = state_raw["peso_kg_actual"]
        recommended_w = current_w + delta_kg

        exercise_name = ex.get("name", "Ejercicio sin nombre")

        print(
            "\n******************************************************* \n"
            f"[RL_ENGINE] ex#{idx} '{exercise_name}': \n"
            f"current={current_w:.1f} kg, \n"
            f"delta={delta_kg:+.1f} kg (action {action_idx}), \n"
            f"recommended={recommended_w:.1f} kg, \n"
            f"rpe_obj={state_raw['rpe_objetivo']:.1f}, \n"
            f"rpe_real={state_raw['rpe_real']:.2f}, \n"
            f"ratio_vol={state_raw['ratio_volumen']:.2f}, \n"
            f"ratio_reps={state_raw['ratio_reps']:.2f}\n"
            "\n******************************************************* \n"
        )

        result = POLICY_SERVICE.recommend_weight_delta(state_raw)

        delta_kg = result["delta_kg"]
        action_idx = result["action_index"]
        action_probs = result["action_probs"]

        print("action_probs:", action_probs)
