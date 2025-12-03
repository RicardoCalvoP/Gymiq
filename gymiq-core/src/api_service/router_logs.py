from fastapi import APIRouter
from .schemas import WorkoutLogRL
from ..rl_engine import ingest_log_entry
from pprint import pprint
import os
router = APIRouter(prefix="/log", tags=["logs"])


@router.post("/")
async def receive_log(entry: WorkoutLogRL):
    payload = entry.model_dump(by_alias=False)
    os.system('cls')
    print("\n===================================================== \n")
    print("BACKEND PAYLOAD:")
    pprint(payload, width=80, sort_dicts=False)
    print("\n===================================================== \n")
    ingest_log_entry(payload)
    return {"status": "ok"}
