from fastapi import APIRouter
from .schemas import WorkoutLog
from ..rl_engine import ingest_log_entry

router = APIRouter(prefix="/log", tags=["logs"])


@router.post("/")
async def receive_log(entry: WorkoutLog):
    # entry.model_dump(by_alias=False) devuelve con nombres snake_case
    ingest_log_entry(entry.model_dump(by_alias=False))
    return {"status": "ok"}
