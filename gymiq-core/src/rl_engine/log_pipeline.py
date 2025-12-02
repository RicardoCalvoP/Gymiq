from dataclasses import dataclass
from typing import Any, Dict, List

import torch

from .state_builder import encode_state


@dataclass
class SetRecord:
    exercise_id: str
    weight: float
    reps: int


@dataclass
class WorkoutRecord:
    workout_id: str
    date: str
    sets: List[SetRecord]


# Simple in-memory buffers for now
WORKOUT_LOG_BUFFER: List[WorkoutRecord] = []
STATE_BUFFER: List[torch.Tensor] = []


def _parse_workout_log(raw_log: Dict[str, Any]) -> WorkoutRecord:
    """
    Transform the raw workout log dict coming from the API
    into a structured WorkoutRecord.

    Expected raw_log shape (snake_case from Pydantic):
    {
        "workout_id": str,
        "date": str,
        "exercises": [
            {
                "exercise_id": str,
                "sets": [
                    {"weight": float, "reps": int},
                    ...
                ]
            },
            ...
        ]
    }
    """
    workout_id = raw_log["workout_id"]
    date = raw_log["date"]
    sets: List[SetRecord] = []

    for ex in raw_log.get("exercises", []):
        exercise_id = ex["exercise_id"]
        for s in ex.get("sets", []):
            sets.append(
                SetRecord(
                    exercise_id=exercise_id,
                    weight=float(s["weight"]),
                    reps=int(s["reps"]),
                )
            )

    return WorkoutRecord(
        workout_id=workout_id,
        date=date,
        sets=sets,
    )


def _build_state_raw_for_set(
    set_record: SetRecord,
    session_index: int,
    user_profile: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Build the raw state dict for ONE set, combining:
    - user profile info (age, bmi, sex, injury, etc.)
    - set info (weight, reps)
    """

    age = user_profile["edad"]
    bmi = user_profile["imc"]
    sex = user_profile["sexo"]
    injury_type = user_profile["historial_lesion_tipo"]
    injury_weeks = user_profile["historial_lesion_tiempo_semanas"]
    pain_now = user_profile["lesion_dolor_actual"]

    # For now we assume reps_target == reps_performed
    reps_target = set_record.reps
    reps_done = set_record.reps

    rpe_target = user_profile.get("rpe_objetivo", 8.0)
    rpe_real = user_profile.get("rpe_real", 7.5)

    state_raw = {
        "edad": age,
        "imc": bmi,
        "sexo": sex,
        "historial_lesion_tipo": injury_type,
        "historial_lesion_tiempo_semanas": injury_weeks,
        "lesion_dolor_actual": pain_now,
        "peso_kg_actual": set_record.weight,
        "reps_objetivo": reps_target,
        "reps_realizadas": reps_done,
        "rpe_objetivo": rpe_target,
        "rpe_real": rpe_real,
        "sesion_num": session_index,
    }

    return state_raw


def ingest_log_entry(log_entry: Dict[str, Any]) -> None:
    """
    Entry point called by the API when a workout log is received.

    For now:
      1) parse the raw dict into WorkoutRecord
      2) store it in an in-memory buffer
      3) build a normalized state vector for each set
         and store it in STATE_BUFFER

    Later:
      - transform into full RL trajectories
      - write to disk / DB
      - trigger training jobs
    """
    workout_record = _parse_workout_log(log_entry)
    WORKOUT_LOG_BUFFER.append(workout_record)

    print(
        "[RL_ENGINE] Workout log stored:",
        workout_record.workout_id,
        "| total stored:",
        len(WORKOUT_LOG_BUFFER),
    )

    # TODO: replace this dummy profile with real user profile info
    dummy_user_profile: Dict[str, Any] = {
        "edad": 30,
        "imc": 24.0,
        "sexo": "M",
        "historial_lesion_tipo": "ninguna",
        "historial_lesion_tiempo_semanas": 0,
        "lesion_dolor_actual": "no_dolor",
        "rpe_objetivo": 8.0,
        "rpe_real": 7.5,
    }

    session_index = 0
    for set_record in workout_record.sets:
        session_index += 1
        state_raw = _build_state_raw_for_set(
            set_record=set_record,
            session_index=session_index,
            user_profile=dummy_user_profile,
        )
        state_vec = encode_state(state_raw)
        STATE_BUFFER.append(state_vec)

    print(
        "[RL_ENGINE] States built from workout:",
        len(workout_record.sets),
        "| total states in buffer:",
        len(STATE_BUFFER),
    )
    print("[DEBUG] state vec:", state_vec.tolist())
