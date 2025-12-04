# update_workout_data.py
import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, List

# Ruta al archivo JS que quieres reescribir
# ajusta a tu estructura real

BASE_PATH = Path(__file__).resolve().parent  # .../gymiq-core/src/api_service
EXERCISE_JS_PATH = (
    BASE_PATH / "../../../gymiq-app/app/lib/exerciseData.js").resolve()


def load_workout_data_from_js(path: Path) -> List[Dict[str, Any]]:
    """
    Lee exerciseData.js y devuelve el array interno como estructura Python.
    Asume formato:
      export const WORKOUT_DATA = [ ... ];
    y puede haber más código JS después.
    """
    text = path.read_text(encoding="utf-8")

    prefix = "export const WORKOUT_DATA"
    if prefix not in text:
        raise ValueError(
            "No se encontró 'export const WORKOUT_DATA' en el archivo JS.")

    # 1) Buscar el inicio del array: primer "[" después del prefix
    prefix_pos = text.index(prefix)
    start_bracket = text.index("[", prefix_pos)

    # 2) Buscar el final del array: la secuencia "];" que cierra WORKOUT_DATA
    end_marker = "];"
    end_pos = text.index(end_marker, start_bracket)

    # 3) Extraer SOLO el contenido "[ ... ]"
    json_str = text[start_bracket: end_pos + 1]  # incluye el ']'
    json_str = json_str.strip()

    # 4) Parsear como JSON
    data = json.loads(json_str)
    return data


def save_workout_data_to_js(path: Path, data: List[Dict[str, Any]]) -> None:
    """
    Escribe la estructura Python como módulo JS:
      export const WORKOUT_DATA = <json pretty>;
    """
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    content = f"export const WORKOUT_DATA = {json_str};//n"
    path.write_text(content, encoding="utf-8")


def apply_backend_recommendations_to_workout_data(
    workout_data: List[Dict[str, Any]],
    backend_response: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Aplica las recomendaciones de peso del backend sobre workout_data.
    SOLO toca:
      - el usuario dueño del workout (por workout_id: "w_u1_0" -> "u1")
      - el workout con ese workout_id
      - los campos 'weight' y 'peso_kg_actual' de los sets.
    """

    if not backend_response:
        return workout_data

    workout_id = backend_response.get("workout_id")
    ejercicios = backend_response.get("ejercicios")

    if not workout_id or not isinstance(ejercicios, list):
        return workout_data

    # workout_id: "w_u1_0" -> ["w", "u1", "0"]
    parts = workout_id.split("_")
    if len(parts) < 3:
        return workout_data

    _, user_id, _ = parts  # user_id = "u1"

    # Mapa: nombre ejercicio -> { index -> peso_kg }
    recomendaciones_por_ejercicio: Dict[str, Dict[int, float]] = {}

    for ej in ejercicios:
        name = ej.get("name")
        sets_recomendados = ej.get("sets_recomendados", [])
        if not name or not isinstance(sets_recomendados, list):
            continue

        by_index: Dict[int, float] = {}
        for s in sets_recomendados:
            idx = s.get("index")
            peso = s.get("peso_kg")
            if isinstance(idx, int) and isinstance(peso, (int, float)):
                by_index[idx] = float(peso)

        recomendaciones_por_ejercicio[name] = by_index

    # Trabajamos sobre una copia profunda para no mutar el original
    new_data = deepcopy(workout_data)

    for block in new_data:
        usuarios = block.get("usuarios", [])
        for usuario in usuarios:
            # Sólo el usuario dueño del workout
            if usuario.get("id") != user_id:
                continue

            workouts = usuario.get("workouts", [])
            for workout in workouts:
                # Sólo el workout con ese workout_id
                if workout.get("id") != workout_id:
                    continue

                exercises = workout.get("exercises", [])
                for exercise in exercises:
                    name = exercise.get("name")
                    rec_set_por_index = recomendaciones_por_ejercicio.get(name)
                    if not rec_set_por_index:
                        continue

                    sets = exercise.get("sets", [])
                    for s in sets:
                        idx = s.get("index")
                        if idx in rec_set_por_index:
                            nuevo_peso = rec_set_por_index[idx]
                            # Actualizamos solo peso
                            s["weight"] = nuevo_peso
                            s["peso_kg_actual"] = nuevo_peso

    return new_data


def update_exercise_js_file(backend_response: Dict[str, Any]) -> None:
    """
    Función de alto nivel:
      - lee exerciseData.js
      - aplica recomendaciones
      - rescribe exerciseData.js
    """
    data = load_workout_data_from_js(EXERCISE_JS_PATH)
    updated = apply_backend_recommendations_to_workout_data(
        data, backend_response)
    save_workout_data_to_js(EXERCISE_JS_PATH, updated)
