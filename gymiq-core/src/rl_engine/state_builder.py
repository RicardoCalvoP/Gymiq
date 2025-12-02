from typing import Dict, List

import torch

# Categorical encodings (one-hot)
SEXO_CATS = ["M", "F"]
LESION_TIPO_CATS = ["ninguna", "leve", "moderada", "grave"]
DOLOR_CATS = ["no_dolor", "molestia", "dolor"]


def one_hot(value: str, categories: List[str]) -> List[float]:
    return [1.0 if value == c else 0.0 for c in categories]


def encode_state(state_raw: Dict) -> torch.Tensor:
    """
    Convierte el estado crudo del usuario/serie en un vector numérico normalizado.
    Normalizaciones clave:
      - peso_kg_actual_normalizado = peso_kg_actual / 200
      - reps_*_normalizado = reps / 20
      - edad_normalizada = edad / 100
      - historial_lesion_tiempo_normalizado = semanas / 52
    """
    edad_norm = state_raw["edad"] / 100.0               # 0–1 aprox

    # IMC típico 15–45 → normalizamos para que ~[0,1]
    imc = state_raw["imc"]
    imc_norm = (imc - 15.0) / 30.0                      # (15→0, 45→1)

    sexo_oh = one_hot(state_raw["sexo"], SEXO_CATS)

    lesion_tipo_oh = one_hot(
        state_raw["historial_lesion_tipo"],
        LESION_TIPO_CATS,
    )

    lesion_tiempo_weeks = state_raw["historial_lesion_tiempo_semanas"]
    lesion_tiempo_norm = lesion_tiempo_weeks / 52.0     # 0–1 año

    dolor_oh = one_hot(state_raw["lesion_dolor_actual"], DOLOR_CATS)

    peso_norm = state_raw["peso_kg_actual"] / 200.0     # suponiendo máximo 200 kg
    reps_obj_norm = state_raw["reps_objetivo"] / 20.0   # máximo 20 reps
    reps_real_norm = state_raw["reps_realizadas"] / 20.0

    rpe_obj_norm = state_raw["rpe_objetivo"] / 10.0     # 1–10 → 0.1–1
    rpe_real_norm = state_raw["rpe_real"] / 10.0

    sesion_norm = state_raw["sesion_num"] / 52.0        # ej. semanas en el año

    features = [
        edad_norm,
        imc_norm,
        lesion_tiempo_norm,
        peso_norm,
        reps_obj_norm,
        reps_real_norm,
        rpe_obj_norm,
        rpe_real_norm,
        sesion_norm,
        # one-hot:
        *sexo_oh,
        *lesion_tipo_oh,
        *dolor_oh,
    ]

    return torch.tensor(features, dtype=torch.float32)


# Dimensión del vector de estado
D_STATE = len(
    encode_state(
        {
            "edad": 52,
            "imc": 27.5,
            "sexo": "F",
            "historial_lesion_tipo": "leve",
            "historial_lesion_tiempo_semanas": 6,
            "lesion_dolor_actual": "no_dolor",
            "peso_kg_actual": 100.0,
            "reps_objetivo": 6,
            "reps_realizadas": 6,
            "rpe_objetivo": 8.0,
            "rpe_real": 7.5,
            "sesion_num": 10,
        }
    )
)

if __name__ == "__main__":
    # Bloque de debug, solo si corres este archivo directamente.
    debug_state_raw = {
        "edad": 52,
        "imc": 27.5,
        "sexo": "F",
        "historial_lesion_tipo": "leve",
        "historial_lesion_tiempo_semanas": 6,
        "lesion_dolor_actual": "no_dolor",
        "peso_kg_actual": 100.0,
        "reps_objetivo": 6,
        "reps_realizadas": 6,
        "rpe_objetivo": 8.0,
        "rpe_real": 7.5,
        "sesion_num": 10,
    }

    print("\n========================")
    print("VALIDANDO NORMALIZACIÓN DEL ESTADO")
    print("========================\n")

    print("Estado CRUDO recibido:")
    for k, v in debug_state_raw.items():
        print(f"  {k}: {v}")

    debug_vec = encode_state(debug_state_raw)

    print("\nEstado NORMALIZADO (vector):")
    print(debug_vec)

    print("\nDimensión del vector:", debug_vec.shape)

    print("\nOne-hot encoding:")
    print(f"Sexo (M,F):              {debug_vec[9:11].tolist()}")
    print(f"Lesión tipo (4 clases):  {debug_vec[11:15].tolist()}")
    print(f"Dolor actual (3 clases): {debug_vec[15:18].tolist()}")
    print("\n========================\n")
