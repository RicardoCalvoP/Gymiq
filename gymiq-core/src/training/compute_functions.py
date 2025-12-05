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
    """
    Reward para RL alineado con la misma metodología que rule_based_delta_from_meta.

    Idea:
      - A partir de ratio_reps aproximamos cuántas reps de más/de menos hizo
        (diff_reps_aprox) asumiendo un objetivo típico de 8 reps.
      - En función de diff_reps_aprox definimos qué *debería* hacer el agente:
          * diff_reps_aprox <= -2        → bajar peso
          * -2 < diff_reps_aprox < 1     → mantener
          * 1 <= diff_reps_aprox < 2     → subir poco
          * diff_reps_aprox >= 2         → subir más
      - Comparamos eso con lo que realmente hizo (progreso_kg):
          * progreso_kg > 0  → acción "subir"
          * progreso_kg ≈ 0  → "mantener"
          * progreso_kg < 0  → "bajar"
      - Recompensamos si la dirección de la acción coincide con la esperada
        según las reps, y penalizamos si hace lo contrario.
      - Ajustamos por RPE, lesión y dolor.
    """

    # -----------------------------------------
    # 1) Aproximar diff_reps a partir de ratio_reps
    # -----------------------------------------
    # Tomamos reps_objetivo "típico" = 8 para mapear ratio_reps → reps de más/menos.
    # Para objetivos de 6–12 reps esto es una aproximación razonable.
    reps_obj_aprox = 8.0
    diff_reps_aprox = (ratio_reps - 1.0) * reps_obj_aprox  # +2 ≈ 2 reps extra, -2 ≈ 2 reps menos

    # -----------------------------------------
    # 2) Dirección DESEADA según reps/volumen
    # -----------------------------------------
    # Bandas similares a rule_based_delta_from_meta, pero en modo "dirección":
    #   - "down"        si va claramente corto
    #   - "hold"        si está cerca del objetivo
    #   - "up_small"    si excede un poco
    #   - "up_big"      si excede bastante
    if diff_reps_aprox >= 2.0:
        desired = "up_big"
    elif diff_reps_aprox >= 1.0:
        desired = "up_small"
    elif diff_reps_aprox <= -2.0:
        desired = "down"
    else:
        desired = "hold"

    # Ajuste suave con volumen: si el volumen está claramente alto o bajo,
    # refuerza la dirección.
    if ratio_volumen > 1.2 and desired.startswith("up"):
        desired = "up_big"
    elif ratio_volumen < 0.8 and desired == "hold":
        desired = "down"

    # -----------------------------------------
    # 3) Dirección REAL de la acción del agente
    # -----------------------------------------
    # progreso_kg > 0  → subir
    # progreso_kg < 0  → bajar
    # |progreso_kg| muy pequeño (ej. 0 en espacio discreto) → mantener
    if progreso_kg > 0.5:
        action_dir = "up"
    elif progreso_kg < -0.5:
        action_dir = "down"
    else:
        action_dir = "hold"

    # -----------------------------------------
    # 4) Recompensa por concordancia acción vs. desired
    # -----------------------------------------
    reward_choice = 0.0

    if desired == "hold":
        if action_dir == "hold":
            reward_choice = 1.0
        else:
            reward_choice = -0.5  # penaliza mover peso cuando deberías mantener
    elif desired in ("up_small", "up_big"):
        if action_dir == "up":
            # Subir cuando toca subir
            reward_choice = 1.0 if desired == "up_small" else 1.3
        elif action_dir == "hold":
            # Mantener cuando deberías subir → penalización suave
            reward_choice = -0.3
        else:
            # bajar cuando deberías subir
            reward_choice = -1.0
    elif desired == "down":
        if action_dir == "down":
            reward_choice = 1.0
        elif action_dir == "hold":
            reward_choice = -0.3
        else:
            reward_choice = -1.0

    # -----------------------------------------
    # 5) Salud: lesión y dolor modulan reward_choice
    # -----------------------------------------
    # Factor de salud basado en tipo de lesión
    if lesion_tipo in ("ninguna", "leve"):
        health_factor = 1.0
    elif lesion_tipo == "moderada":
        health_factor = 0.7
    else:  # severa / cronica
        health_factor = 0.4

    # Dolor actual: reduce aún más la recompensa por subir
    if hubo_dolor and action_dir == "up":
        # castigamos subir con dolor
        reward_choice -= 1.0

    reward_choice *= health_factor

    # -----------------------------------------
    # 6) RPE como freno adicional
    # -----------------------------------------
    diff_rpe = abs(rpe_real - rpe_objetivo)
    # Clavar el RPE = 0, desviarse resta
    reward_rpe = -diff_rpe  # en [-∞, 0]

    # Penalización extra si se pasa mucho de RPE objetivo
    if rpe_real > rpe_objetivo + 1.0:
        reward_rpe -= 1.0

    # Si viene MUY por encima de RPE y aún así la acción fue "up",
    # penaliza adicionalmente.
    if rpe_real > rpe_objetivo + 1.0 and action_dir == "up":
        reward_choice -= 0.5

    # -----------------------------------------
    # 7) Bonus suave por progresar en la dirección correcta
    # -----------------------------------------
    reward_prog = 0.0
    if action_dir == "up" and desired.startswith("up") and not hubo_dolor:
        # más kilos, más bonus, pero cap
        reward_prog = min(abs(progreso_kg) / 5.0, 1.0) * 0.3
    elif action_dir == "down" and desired == "down":
        # bonus más pequeño por bajar cuando toca
        reward_prog = 0.1

    # -----------------------------------------
    # 8) Reward total
    # -----------------------------------------
    reward = reward_choice + reward_rpe + reward_prog
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
    Regla basada en el contexto completo del ejercicio (promedio de reps y peso).

    Idea:
      - reps_mean = reps promedio por set (ratio_reps * reps_obj).
      - diff_reps = reps_mean - reps_obj.

      Reglas de reps:
        * diff_reps <= -2           → bajar (más reps faltan, más baja).
        * -2 < diff_reps < 1        → mantener (no subir).
        * 1 <= diff_reps < 2        → subir poco (+2.5).
        * diff_reps >= 2            → subir más, por bandas (5, 7.5, 10...).

    Luego se ajusta por RPE, edad/lesión/dolor y se encaja en ACTION_SPACE_KG.
    """

    # -----------------------------
    # 1) Contexto del ejercicio
    # -----------------------------
    rpe_real = state_raw["rpe_real"]
    rpe_obj = state_raw["rpe_objetivo"]
    ratio_reps = state_raw.get("ratio_reps", 1.0)
    ratio_vol = state_raw.get("ratio_volumen", 1.0)

    reps_obj = float(state_raw.get("reps_objetivo", 0.0))
    delta_rpe = rpe_real - rpe_obj

    # reps promedio por set según el ratio
    if reps_obj > 0:
        reps_mean = ratio_reps * reps_obj
    else:
        reps_mean = reps_obj

    diff_reps = reps_mean - reps_obj  # +2 => 2 reps de más por set; -2 => 2 de menos

    base_delta = 0.0

    # -----------------------------
    # 2) Base_delta según diff_reps
    # -----------------------------
    if diff_reps >= 2.0:
        # Muy por encima del objetivo. Más reps extra => más kg.
        if diff_reps < 4.0:
            base_delta = 5.0       # +2..+3 reps extra → salto alto pero razonable
        elif diff_reps < 6.0:
            base_delta = 7.5       # +4..+5 reps extra → más agresivo
        else:
            base_delta = 10.0      # +6 reps extra o más → muy agresivo (modulado luego)
    elif diff_reps >= 1.0:
        # Entre +1 y +2 reps por set: ya se pasó del objetivo → subir poco
        base_delta = 2.5
    elif diff_reps <= -2.0:
        # Bastante por debajo del objetivo.
        if diff_reps > -4.0:
            base_delta = -2.5      # -2..-3 reps menos → baja poco
        elif diff_reps > -6.0:
            base_delta = -5.0      # -4..-5 → baja más
        else:
            base_delta = -7.5      # -6 o más → baja fuerte
    else:
        # Entre (obj_reps - 2, obj_reps + 1) → mantener
        base_delta = 0.0

    # Ajuste suave con volumen
    if base_delta > 0 and ratio_vol > 1.2 and diff_reps >= 2.0:
        base_delta += 2.5
    elif base_delta < 0 and ratio_vol < 0.8:
        base_delta -= 2.5

    # -----------------------------
    # 3) Freno por RPE
    # -----------------------------
    if delta_rpe > 0.5 and base_delta > 0:
        # Vino más pesado de lo esperado: como mucho un salto pequeño.
        base_delta = min(base_delta, 2.5)

    if delta_rpe > 1.0:
        # Muy por arriba de RPE objetivo: mejor bajar algo.
        if base_delta >= 0:
            base_delta = -2.5
        else:
            base_delta = min(base_delta, -2.5)

    if delta_rpe < -0.5 and diff_reps >= 2.0 and base_delta > 0:
        # Muy fácil y con reps de sobra → permite un escalón más.
        if base_delta == 5.0:
            base_delta = 7.5
        elif base_delta == 7.5:
            base_delta = 10.0

    # -----------------------------
    # 4) Modulación por edad / lesión / dolor
    # -----------------------------
    edad = user_profile["edad"]
    lesion_tipo = user_profile["historial_lesion_tipo"]
    lesion_tiempo = user_profile["historial_lesion_tiempo_semanas"]
    dolor_actual = user_profile["dolor_actual"]

    age_factor = compute_age_factor(edad)
    injury_factor = compute_injury_factor(lesion_tipo, lesion_tiempo, dolor_actual)

    delta_continuo = base_delta * age_factor * injury_factor

    # Dolor actual: aún más conservador
    if dolor_actual == "molestia":
        if delta_continuo > 5.0:
            delta_continuo = 5.0
    elif dolor_actual == "dolor":
        if delta_continuo > 0:
            delta_continuo = 0.0
        else:
            delta_continuo = max(delta_continuo, -5.0)

    # -----------------------------
    # 5) Clamp al rango de ACTION_SPACE_KG
    # -----------------------------
    max_pos = max(a for a in ACTION_SPACE_KG if a > 0)
    min_neg = min(a for a in ACTION_SPACE_KG if a < 0)

    if delta_continuo > max_pos:
        delta_continuo = max_pos
    if delta_continuo < min_neg:
        delta_continuo = min_neg

    # -----------------------------
    # 6) Snap al action space
    # -----------------------------
    delta_discreto = snap_to_action_space(delta_continuo)
    return delta_discreto
