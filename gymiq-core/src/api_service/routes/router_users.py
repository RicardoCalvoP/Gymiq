# api_service/routes/router_users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..db.db import get_db
from ..db.models.user import User, UserProfile
from ..schemas import UserProfileRead, UserProfileUpdate, UserRead
from ..security import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserRead)
async def read_current_user(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return current_user


@router.put("/me/profile", response_model=UserProfileRead)
async def upsert_profile(
    payload: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    - Si el usuario no tiene perfil todavía: lo crea (requiere username).
    - Si ya tiene perfil: actualiza solo los campos enviados.
    """
    profile = current_user.profile

    # Crear nuevo perfil si no existe
    if profile is None:
        if payload.username is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="username is required to create profile",
            )

        profile = UserProfile(
            user_id=current_user.id,
            username=payload.username,
            gender=payload.gender,
            birth_date=payload.birth_date,
            height=payload.height,
            weight=payload.weight,
            experience_level=payload.experience_level,
            goal=payload.goal,
        )
        db.add(profile)
    else:
        # Actualizar solo campos enviados (parcial)
        if payload.username is not None:
            profile.username = payload.username
        if payload.gender is not None:
            profile.gender = payload.gender
        if payload.birth_date is not None:
            profile.birth_date = payload.birth_date
        if payload.height is not None:
            profile.height = payload.height
        if payload.weight is not None:
            profile.weight = payload.weight
        if payload.experience_level is not None:
            profile.experience_level = payload.experience_level
        if payload.goal is not None:
            profile.goal = payload.goal

    db.commit()
    db.refresh(profile)
    return profile
