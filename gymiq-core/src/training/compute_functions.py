from typing import Dict

from ..rl_engine.action_space import ACTION_SPACE_KG


def compute_reward(
    rpe_objetivo: float,
    rpe_real: float,
    hubo_dolor: bool,
    progreso_kg: float,
    ratio_volumen: float,
    ratio_reps: float,
    lesion_tipo: str,
) -> float:
    # 1) Termino de performance (volumen/reps vs objetivo)
    # -----------------------------------------
    # score_perf > 0 si cumples/superas, < 0 si no alcanzas
    avg_ratio = 0.5 * (ratio_volumen + ratio_reps)

    if avg_ratio >= 1.0:
        # Cumple/supera objetivo -> base positivo
        # cuanto más por encima, más reward, pero cap.
        score_perf = min(avg_ratio - 1.0, 1.0)  # [0, 1]
        base_reward = 0.5 + 0.5 * score_perf    # en [0.5, 1.0]
    else:
        # No llega al objetivo -> base negativo
        deficit = min(1.0 - avg_ratio, 1.0)     # [0, 1]
        base_reward = -deficit                  # en [-1.0, 0)

    # 2) Ajuste por salud (lesión/dolor)
    # -----------------------------------------
    # Factor de salud que baja el reward si hay lesión
    if lesion_tipo in ("ninguna", "leve"):
        health_factor = 1.0
    elif lesion_tipo == "moderada":
        health_factor = 0.6
    else:  # severa / crónica
        health_factor = 0.3

    # Dolor actual: baja aún más
    if hubo_dolor:
        health_factor *= 0.3

    reward_health = base_reward * health_factor

    # 3) RPE como freno de seguridad
    # -----------------------------------------
    # Penalizar alejarse del objetivo
    diff_rpe = abs(rpe_real - rpe_objetivo)
    reward_rpe = -diff_rpe  # 0 si clavas RPE, negativo si te vas

    # Penalización fuerte si te pasas mucho
    if rpe_real > rpe_objetivo + 1.0:
        reward_rpe -= 1.0

    # 4) Bonus suave por progresar en kg (si todo lo demás no está mal)
    # -----------------------------------------
    reward_prog = 0.0
    if progreso_kg > 0 and base_reward > 0 and not hubo_dolor:
        reward_prog = min(progreso_kg / 2.5, 1.0) * 0.5  # cap y factor suave

    # 5) Reward total
    # -----------------------------------------
    reward = reward_health + reward_rpe + reward_prog
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


def rule_based_delta_from_meta(state_raw: Dict, user_profile: Dict) -> float:
    """
    Maestro basado en los mismos features que construye state_builder:
    usa ratios, delta_rpe + RPE + perfil (edad, lesión).
    """

    # 1) Leer lo que ya construye el state_builder
    rpe_real = state_raw["rpe_real"]
    rpe_obj = state_raw["rpe_objetivo"]
    ratio_vol = state_raw.get("ratio_volumen", 1.0)
    ratio_reps = state_raw.get("ratio_reps", 1.0)
    delta_rpe = state_raw.get("delta_rpe", 0.0)

    # 2) Heurística de progresión: mezcla ratios y delta_rpe
    score = 0.5 * (ratio_vol - 1.0) + 0.3 * \
        (ratio_reps - 1.0) - 0.2 * delta_rpe

    if score > 0.8:
        base_delta = 2.5
    elif score > 0.5:
        base_delta = 1.0
    elif score > 0.2:
        base_delta = 1.0
    elif score > -0.2:
        base_delta = 0.0
    elif score > -0.5:
        base_delta = -1.0
    else:
        base_delta = -2.5

    # 3) Ajustar con RPE para no hacer locuras
    if rpe_real > rpe_obj + 0.3 and base_delta > 0:
        base_delta = 0.0
    if rpe_real < rpe_obj - 0.3 and base_delta < 0:
        base_delta = 0.0

    # 4) Modulación por edad / lesión
    edad = user_profile["edad"]
    lesion_tipo = user_profile["historial_lesion_tipo"]
    lesion_tiempo = user_profile["historial_lesion_tiempo_semanas"]
    dolor_actual = user_profile["dolor_actual"]

    age_factor = compute_age_factor(edad)
    injury_factor = compute_injury_factor(
        lesion_tipo, lesion_tiempo, dolor_actual)

    delta_continuo = base_delta * age_factor * injury_factor

    # 5) Ajuste al ACTION_SPACE_KG
    delta_discreto = snap_to_action_space(delta_continuo)
    return delta_discreto
