from typing import Any  # si arriba ya tienes Any en los imports, omite esta línea
from typing import Dict, Any, List
import torch

# ================================
# Categóricos (one-hot)
# ================================

SEXO_CATS = ["M", "F"]

# Lo dejo aunque en este encoder solo usamos un flag de historial_lesiones;
# puede servir para otros módulos.
LESION_TIPO_CATS = ["ninguna", "leve", "moderada", "grave"]

DOLOR_CATS = ["no_dolor", "molestia", "dolor"]

# Ajusta estas listas a los IDs reales de tu backend
EJERCICIOS_MAP = {
    # =======================
    # PECHO (1)
    # =======================
    "Press banca con barra": {"id": 101, "grupo_muscular_id": 1},
    "Press banca inclinado con barra": {"id": 102, "grupo_muscular_id": 1},
    "Press banca declinado con barra": {"id": 103, "grupo_muscular_id": 1},
    "Press banca con mancuernas": {"id": 104, "grupo_muscular_id": 1},
    "Press inclinado con mancuernas": {"id": 105, "grupo_muscular_id": 1},
    "Aperturas con mancuernas en banco plano": {"id": 106, "grupo_muscular_id": 1},
    "Aperturas en banco inclinado": {"id": 107, "grupo_muscular_id": 1},
    "Fondos en paralelas": {"id": 108, "grupo_muscular_id": 1},
    "Fondos en paralelas asistidos": {"id": 109, "grupo_muscular_id": 1},
    "Peck deck": {"id": 110, "grupo_muscular_id": 1},
    "Crossover en polea alta": {"id": 111, "grupo_muscular_id": 1},

    # =======================
    # ESPALDA (2)
    # =======================
    "Jalón en polea alta agarre cerrado": {"id": 201, "grupo_muscular_id": 2},
    "Jalón en polea alta agarre abierto": {"id": 202, "grupo_muscular_id": 2},
    "Remo con barra": {"id": 203, "grupo_muscular_id": 2},
    "Remo con mancuernas": {"id": 204, "grupo_muscular_id": 2},
    "Remo sentado en polea baja": {"id": 205, "grupo_muscular_id": 2},
    "Remo T-Bar": {"id": 206, "grupo_muscular_id": 2},
    "Peso muerto": {"id": 207, "grupo_muscular_id": 2},
    "Peso muerto rumano": {"id": 208, "grupo_muscular_id": 2},
    "Pull-over en polea": {"id": 209, "grupo_muscular_id": 2},

    # =======================
    # PIERNAS (3)
    # =======================
    "Sentadilla con barra": {"id": 301, "grupo_muscular_id": 3},
    "Sentadilla barra alta": {"id": 302, "grupo_muscular_id": 3},
    "Sentadilla frontal": {"id": 303, "grupo_muscular_id": 3},
    "Prensa de piernas": {"id": 304, "grupo_muscular_id": 3},
    "Desplantes": {"id": 305, "grupo_muscular_id": 3},
    "Elevación de talones de pie (pantorrilla)": {"id": 306, "grupo_muscular_id": 3},
    "Elevación de talones sentado": {"id": 307, "grupo_muscular_id": 3},
    "Extensión de cuádriceps": {"id": 308, "grupo_muscular_id": 3},
    "Curl femoral sentado": {"id": 309, "grupo_muscular_id": 3},
    "Curl femoral acostado": {"id": 310, "grupo_muscular_id": 3},

    # =======================
    # HOMBROS (4)
    # =======================
    "Press militar con barra": {"id": 401, "grupo_muscular_id": 4},
    "Press militar con mancuernas": {"id": 402, "grupo_muscular_id": 4},
    "Elevaciones laterales": {"id": 403, "grupo_muscular_id": 4},
    "Elevaciones frontales": {"id": 404, "grupo_muscular_id": 4},
    "Pájaros con mancuernas": {"id": 405, "grupo_muscular_id": 4},
    "Remo al mentón": {"id": 406, "grupo_muscular_id": 4},

    # =======================
    # BÍCEPS (5)
    # =======================
    "Curl con barra": {"id": 501, "grupo_muscular_id": 5},
    "Curl con mancuernas": {"id": 502, "grupo_muscular_id": 5},
    "Curl martillo": {"id": 503, "grupo_muscular_id": 5},
    "Curl en banco scott": {"id": 504, "grupo_muscular_id": 5},
    "Curl en polea baja": {"id": 505, "grupo_muscular_id": 5},

    # =======================
    # TRÍCEPS (6)
    # =======================
    "Extensión de tríceps en polea": {"id": 601, "grupo_muscular_id": 6},
    "Extensión de tríceps con cuerda": {"id": 602, "grupo_muscular_id": 6},
    "Press francés con barra": {"id": 603, "grupo_muscular_id": 6},
    "Press francés con mancuernas": {"id": 604, "grupo_muscular_id": 6},
    "Patada de tríceps": {"id": 605, "grupo_muscular_id": 6},

    # =======================
    # GLÚTEOS (7)
    # =======================
    "Hip thrust": {"id": 701, "grupo_muscular_id": 7},
    "Puente de glúteos": {"id": 702, "grupo_muscular_id": 7},
    "Patada de glúteo en polea": {"id": 703, "grupo_muscular_id": 7},
    "Abducción de cadera en máquina": {"id": 704, "grupo_muscular_id": 7},

    # =======================
    # CORE (8)
    # =======================
    "Crunch": {"id": 801, "grupo_muscular_id": 8},
    "Plancha": {"id": 802, "grupo_muscular_id": 8},
    "Elevación de piernas": {"id": 803, "grupo_muscular_id": 8},
    "Crunch en máquina": {"id": 804, "grupo_muscular_id": 8},
}

# Categorías para one-hot de ejercicio y grupo muscular
EXERCISE_ID_CATS = sorted({v["id"] for v in EJERCICIOS_MAP.values()})
MUSCLE_GROUP_CATS = sorted({v["grupo_muscular_id"]
                           for v in EJERCICIOS_MAP.values()})


def one_hot(value: str, categories: List[str]) -> List[float]:
    return [1.0 if value == c else 0.0 for c in categories]


# ================================
# Encoder de estado
# ================================

def encode_state(state_raw: Dict) -> torch.Tensor:
    """
    Encoder para 1 estado = 1 ejercicio (agregado sobre la sesión).

    Espera un state_raw con, al menos:

      Perfil:
        - edad: int
        - imc: float
        - sexo: "M" | "F"
        - historial_lesiones: bool
        - dolor_actual: en DOLOR_CATS

      Ejercicio:
        - exercise_id: en EXERCISE_ID_CATS
        - muscle_group: en MUSCLE_GROUP_CATS
        - sesion_num: int

      Objetivos (de ese ejercicio en la sesión):
        - sets_objetivo: int
        - reps_objetivo: float/int (promedio target)
        - rpe_objetivo: float
        - volumen_objetivo: float (kg * reps * sets objetivo)

      Resultados agregados:
        - reps_real: float
        - rpe_real: float
        - volumen_real_total: float
        - ratio_volumen: float
        - ratio_reps: float
        - delta_rpe: float (rpe_real_prom - rpe_objetivo)

      Peso:
        - peso_kg_actual: float (peso típico de trabajo actual)
    """

    # --- Perfil ---
    edad_norm = state_raw["edad"] / 100.0          # 0–1 aprox
    imc_norm = state_raw["imc"] / 40.0             # asumiendo IMC < 40
    sexo_oh = one_hot(state_raw["sexo"], SEXO_CATS)
    peso_usuario_norm = state_raw["peso_usuario"] / 200.0

    lesion_tipo_oh = one_hot(
        state_raw["historial_lesion_tipo"], LESION_TIPO_CATS)
    lesion_tiempo_norm = state_raw["historial_lesion_tiempo_semanas"] / 520.0
    dolor_oh = one_hot(state_raw["dolor_actual"], DOLOR_CATS)

    # --- Ejercicio ---
    exercise_id_oh = one_hot(state_raw["exercise_id"], EXERCISE_ID_CATS)
    muscle_group_oh = one_hot(state_raw["muscle_group"], MUSCLE_GROUP_CATS)
    sesion_norm = state_raw["sesion_num"] / 52.0   # típicamente semanas/año

    # --- Objetivos ---
    sets_obj_norm = state_raw["sets_objetivo"] / 5.0       # hasta ~10 series
    reps_obj_norm = state_raw["reps_objetivo"] / 30.0       # hasta ~30 reps
    rpe_obj_norm = state_raw["rpe_objetivo"] / 10.0         # 1–10
    volumen_obj_norm = state_raw["volumen_objetivo"] / 50000.0
    peso_norm = state_raw["peso_kg_actual"] / 300.0  # suponiendo < 300 kg

    # --- Resultados reales agregados ---
    reps_real_norm = state_raw["reps_real"] / 30.0
    rpe_real_norm = state_raw["rpe_real"] / 10.0

    volumen_real_norm = state_raw["volumen_real_total"] / 50000.0

    # ratios; capamos a [0, 2] y normalizamos a [0,1]
    ratio_vol = state_raw["ratio_volumen"]
    ratio_reps = state_raw["ratio_reps"]

    ratio_vol_clamped = min(max(ratio_vol, 0.0), 2.0)
    ratio_reps_clamped = min(max(ratio_reps, 0.0), 2.0)

    ratio_vol_norm = ratio_vol_clamped / 2.0
    ratio_reps_norm = ratio_reps_clamped / 2.0

    delta_rpe = state_raw["delta_rpe"]
    delta_rpe_norm = delta_rpe / 5.0   # -5 a +5 aprox → -1 a +1

    features = [
        # Perfil
        edad_norm,
        imc_norm,
        peso_usuario_norm,
        *lesion_tipo_oh,
        lesion_tiempo_norm,
        *sexo_oh,
        *dolor_oh,

        # Ejercicio
        *exercise_id_oh,
        *muscle_group_oh,
        sesion_norm,

        # Objetivos
        sets_obj_norm,
        reps_obj_norm,
        rpe_obj_norm,
        volumen_obj_norm,
        peso_norm,

        # Resultados agregados
        reps_real_norm,
        rpe_real_norm,
        volumen_real_norm,

        # Ratios
        ratio_vol_norm,
        ratio_reps_norm,
        delta_rpe_norm,

    ]

    return torch.tensor(features, dtype=torch.float32)


# ================================
# Label de progresión (n saltos)
# ================================

def compute_progression_label_from_state(state_raw: Dict) -> int:
    """
    Usa el estado agregado de un ejercicio para generar un 'label' n
    (n saltos de 2.5 kg) a partir de volumen, reps y RPE.

    Basado en:
      score = 0.5*(ratio_volumen - 1) + 0.3*(ratio_reps - 1) - 0.2*delta_rpe
      n = función escalonada del score
    """

    ratio_volumen = state_raw["ratio_volumen"]
    ratio_reps = state_raw["ratio_reps"]
    delta_rpe = state_raw["delta_rpe"]

    score = 0.5 * (ratio_volumen - 1.0) + 0.3 * \
        (ratio_reps - 1.0) - 0.2 * delta_rpe

    if score > 0.8:
        n = 10
    elif score > 0.5:
        n = 6
    elif score > 0.2:
        n = 3
    elif score > -0.2:
        n = 1
    elif score > -0.5:
        n = 0
    elif score > -1.0:
        n = -1
    else:
        n = -3

    return n


# EJERCICIOS_MAP, SEXO_CATS, LESION_TIPO_CATS, DOLOR_CATS ya existen en tu archivo


def _validate_profile(user_profile: Dict[str, Any]) -> None:
    required_fields = [
        "edad",
        "imc",
        "peso_usuario",
        "sexo",
        "historial_lesion_tipo",
        "historial_lesion_tiempo_semanas",
        "dolor_actual",
    ]

    for field in required_fields:
        if field not in user_profile:
            raise ValueError(f"Perfil incompleto: falta '{field}'")

    if user_profile["sexo"] not in SEXO_CATS:
        raise ValueError(f"Valor inválido en 'sexo': {user_profile['sexo']}")

    if user_profile["historial_lesion_tipo"] not in LESION_TIPO_CATS:
        raise ValueError(
            f"Valor inválido en 'historial_lesion_tipo': {user_profile['historial_lesion_tipo']}"
        )

    if user_profile["dolor_actual"] not in DOLOR_CATS:
        raise ValueError(
            f"Valor inválido en 'dolor_actual': {user_profile['dolor_actual']}"
        )


def _aggregate_sets(exercise: Dict[str, Any]) -> Dict[str, float]:
    sets = exercise.get("sets", [])
    if not isinstance(sets, list):
        raise ValueError("'sets' debe ser una lista")

    reps_list = []
    rpe_list = []
    peso_list = []

    for s in sets:
        reps_list.append(float(s["reps"]))
        rpe_list.append(float(s["rpe"]))
        peso_list.append(float(s["peso_kg"]))

    reps_real = sum(reps_list) if reps_list else 0.0
    rpe_real = (sum(rpe_list) / len(rpe_list)) if rpe_list else 0.0
    volumen_real_total = sum(p * r for p, r in zip(peso_list, reps_list))

    # Peso típico de trabajo: último peso usado (más lógico)
    peso_kg_actual = peso_list[-1] if peso_list else 0.0

    return {
        "reps_real": reps_real,
        "rpe_real": rpe_real,
        "peso_kg_actual": peso_kg_actual,
        "volumen_real_total": volumen_real_total,
    }


def build_state_raw_from_exercise(
    user_profile: Dict[str, Any],
    exercise: Dict[str, Any],
    sesion_num: int,
) -> Dict[str, Any]:

    _validate_profile(user_profile)

    # -------- Ejercicio: ID y grupo muscular --------
    exercise_name = exercise["name"]
    if exercise_name not in EJERCICIOS_MAP:
        raise ValueError(f"Ejercicio no reconocido: '{exercise_name}'")

    meta = EJERCICIOS_MAP[exercise_name]
    exercise_id = meta["id"]
    muscle_group = meta["grupo_muscular_id"]

    # -------- Objetivos --------
    reps_objetivo = float(exercise["reps_objetivo"])
    rpe_objetivo = float(exercise["rpe_objetivo"])

    sets = exercise["sets"]
    sets_objetivo = len(sets)
    if sets_objetivo == 0:
        raise ValueError(f"Ejercicio '{exercise_name}' no tiene sets")

    # -------- Agregados reales --------
    agg = _aggregate_sets(exercise)
    reps_real = agg["reps_real"]
    rpe_real = agg["rpe_real"]
    peso_kg_actual = agg["peso_kg_actual"]
    volumen_real_total = agg["volumen_real_total"]

    volumen_objetivo = sets_objetivo * reps_objetivo * peso_kg_actual

    ratio_volumen = (
        volumen_real_total / volumen_objetivo if volumen_objetivo > 0 else 1.0
    )
    ratio_reps = (
        reps_real / (sets_objetivo *
                     reps_objetivo) if reps_objetivo > 0 else 1.0
    )
    delta_rpe = rpe_real - rpe_objetivo

    # -------- Construcción final del estado bruto --------
    state_raw = {
        # PERFIL
        "edad": int(user_profile["edad"]),
        "imc": float(user_profile["imc"]),
        "peso_usuario": float(user_profile["peso_usuario"]),
        "sexo": user_profile["sexo"],
        "historial_lesion_tipo": user_profile["historial_lesion_tipo"],
        "historial_lesion_tiempo_semanas": int(
            user_profile["historial_lesion_tiempo_semanas"]
        ),
        "dolor_actual": user_profile["dolor_actual"],

        # EJERCICIO
        "exercise_id": exercise_id,
        "muscle_group": muscle_group,
        "sesion_num": int(sesion_num),

        # OBJETIVOS
        "sets_objetivo": sets_objetivo,
        "reps_objetivo": reps_objetivo,
        "rpe_objetivo": rpe_objetivo,
        "volumen_objetivo": volumen_objetivo,
        "peso_kg_actual": peso_kg_actual,

        # RESULTADOS (AGREGADOS DE SETS)
        "reps_real": reps_real,
        "rpe_real": rpe_real,
        "volumen_real_total": volumen_real_total,
        "ratio_volumen": ratio_volumen,
        "ratio_reps": ratio_reps,
        "delta_rpe": delta_rpe,
    }

    return state_raw

# ================================
# Dimensión del vector de estado
# ================================
# Se calcula pasando un state_raw sintético por encode_state.
# Solo sirve para que la PolicyNetwork sepa cuántas features tiene la entrada.


def _build_dummy_state_raw_for_dim() -> Dict[str, Any]:
    return {
        # Perfil
        "edad": 30,
        "imc": 25.0,
        "peso_usuario": 80.0,
        "sexo": "M",
        "historial_lesion_tipo": "ninguna",
        "historial_lesion_tiempo_semanas": 0,
        "dolor_actual": "no_dolor",

        # Ejercicio (usamos el primer id/grupo válidos)
        "exercise_id": EXERCISE_ID_CATS[0],
        "muscle_group": MUSCLE_GROUP_CATS[0],
        "sesion_num": 1,

        # Objetivos
        "sets_objetivo": 3,
        "reps_objetivo": 8.0,
        "rpe_objetivo": 8.0,
        "volumen_objetivo": 1000.0,
        "peso_kg_actual": 60.0,

        # Resultados reales agregados
        "reps_real": 24.0,
        "rpe_real": 8.0,
        "volumen_real_total": 1440.0,

        # Ratios
        "ratio_volumen": 1.0,
        "ratio_reps": 1.0,
        "delta_rpe": 0.0,
    }


D_STATE = encode_state(_build_dummy_state_raw_for_dim()).shape[0]
