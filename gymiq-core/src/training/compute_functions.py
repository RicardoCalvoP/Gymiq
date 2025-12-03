from typing import Dict

from ..rl_engine.action_space import ACTION_SPACE_KG


def compute_reward(
    rpe_objetivo: float,
    rpe_real: float,
    hubo_dolor: bool,
    progreso_kg: float,
) -> float:
    """
    Función de recompensa para una serie.

    Parámetros:
        rpe_objetivo: RPE target de la serie (p.ej. 8.0)
        rpe_real: RPE reportado / estimado (p.ej. 7.5)
        hubo_dolor: True si el usuario reportó dolor relevante
        progreso_kg: cambio de peso respecto a la referencia (kg),
                     típicamente el delta aplicado en la recomendación.

    Devuelve:
        reward (float): recompensa escalar para usar en el update de la policy.
    """
    # 1) Término principal: acercarse al RPE objetivo
    diff = abs(rpe_real - rpe_objetivo)
    reward_rpe = -diff  # máximo en 0 cuando rpe_real == rpe_objetivo

    # 2) Penalización fuerte si se pasa mucho del objetivo (sobre-esfuerzo)
    if rpe_real > rpe_objetivo + 1.0:
        reward_rpe -= 1.0

    # 3) Penalización por dolor
    reward_dolor = -2.0 if hubo_dolor else 0.0

    # 4) Incentivo leve si progresó un poquito (no loco)
    reward_prog = 0.0
    if progreso_kg > 0:
        # cap a +1.0 para que no incentive saltos enormes
        reward_prog = min(progreso_kg / 2.5, 1.0)

    reward = reward_rpe + reward_dolor + reward_prog
    return float(reward)


def compute_age_factor(edad: int) -> float:
    if edad < 30:
        return 1.0
    elif edad < 40:
        return 0.9
    elif edad < 50:
        return 0.85
    elif edad < 60:
        return 0.8
    else:
        return 0.7


def compute_injury_factor(
    lesion_tipo: str,
    lesion_tiempo_semanas: int,
    dolor_actual: str,
) -> float:
    tipo_base = {
        "ninguna": 1.0,
        "leve": 0.9,
        "moderada": 0.8,
        "severa": 0.7,
        "cronica": 0.6,
    }
    f = tipo_base.get(lesion_tipo, 0.8)

    if lesion_tiempo_semanas < 12:
        f *= 0.9

    if dolor_actual != "no_dolor":
        f *= 0.9

    return f


def snap_to_action_space(delta: float) -> float:
    return min(ACTION_SPACE_KG, key=lambda a: abs(a - delta))


def rule_based_delta_from_meta(meta: Dict) -> float:
    """
    Regla tal cual lo que definiste:

    - Si RPE_real < RPE_obj -> progresar (+)
    - Si RPE_real > RPE_obj -> reducir (-)
    - Si RPE_real == RPE_obj -> mantener (0)

    Luego modulamos el tamaño con edad y lesión, y ajustamos
    al salto más cercano de ACTION_SPACE_KG.
    """
    rpe_real = meta["rpe_real"]
    rpe_obj = meta["rpe_objetivo"]

    # 1) SOLO regla directa de comparación
    if rpe_real < rpe_obj:
        sign = +1
    elif rpe_real > rpe_obj:
        sign = -1
    else:
        return 0.0  # igual → mantener

    # 2) Factores personales
    edad = meta["edad"]
    lesion_tipo = meta["historial_lesion_tipo"]
    lesion_tiempo = meta["historial_lesion_tiempo_semanas"]
    dolor_actual = meta["lesion_dolor_actual"]

    age_factor = compute_age_factor(edad)
    injury_factor = compute_injury_factor(
        lesion_tipo, lesion_tiempo, dolor_actual)

    incremento_base = 2.5  # como en tu doc
    delta_continuo = sign * incremento_base * age_factor * injury_factor

    # 3) Ajustar al salto más cercano de ACTION_SPACE_KG
    delta_discreto = snap_to_action_space(delta_continuo)
    return delta_discreto
