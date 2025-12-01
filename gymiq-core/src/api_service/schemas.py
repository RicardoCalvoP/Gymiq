from typing import List
from pydantic import BaseModel, Field


class WorkoutSet(BaseModel):
    weight: float
    reps: int


class WorkoutExercise(BaseModel):
    exercise_id: str = Field(alias="exerciseId")
    sets: List[WorkoutSet]


class WorkoutLog(BaseModel):
    workout_id: str = Field(alias="workoutId")
    date: str
    exercises: List[WorkoutExercise]

    class Config:
        populate_by_name = True  # por si luego quieres usar los nombres snake_case
