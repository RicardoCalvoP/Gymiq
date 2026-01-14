# src/api_service/schemas.py
from typing import List, Literal, Optional
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field, EmailStr


# ========================
# RL / workout log schemas
# ========================

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


# ========================
# Auth / user schemas
# ========================

class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserLogin(UserBase):
    password: str


class UserProfileBase(BaseModel):
    gender: Optional[str] = None  # "male", "female"
    birth_date: Optional[date] = None
    height: Optional[Decimal] = None
    weight: Optional[Decimal] = None
    # "beginner", "intermediate", "advanced"
    experience_level: Optional[str] = None
    goal: Optional[str] = None  # "strength", "hypertrophy", "fat_loss"


class UserProfileUpdate(UserProfileBase):
    # username para crear; opcional para actualizar
    username: Optional[str] = None


class UserProfileRead(UserProfileBase):
    id: int
    user_id: int
    username: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # antes orm_mode = True


class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    profile: Optional[UserProfileRead] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
