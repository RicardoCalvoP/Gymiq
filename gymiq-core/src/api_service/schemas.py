from typing import List, Literal
from pydantic import BaseModel, Field


class PerfilRL(BaseModel):
    edad: int
    imc: float
    peso_usuario: float
    sexo: Literal["M", "F"]
    historial_lesion_tipo: Literal["ninguna", "leve", "moderada", "grave"]
    historial_lesion_tiempo_semanas: int
    dolor_actual: Literal["no_dolor", "molestia", "dolor"]


class WorkoutSetRL(BaseModel):
    reps: int
    rpe: float
    peso_kg: float


class WorkoutExerciseRL(BaseModel):
    name: str
    reps_objetivo: float
    rpe_objetivo: float
    sets: List[WorkoutSetRL]


class WorkoutLogRL(BaseModel):
    workout_id: str = Field(alias="workoutId")
    sesion_num: int
    perfil: PerfilRL
    ejercicios: List[WorkoutExerciseRL]

    class Config:
        populate_by_name = True
