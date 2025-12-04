from fastapi import APIRouter
from pprint import pprint
import os

from src.api_service.update_workout_data import update_exercise_js_file

from .schemas import WorkoutLogRL
from ..rl_engine import ingest_log_entry

router = APIRouter(prefix="/log", tags=["logs"])


@router.post("/")
async def receive_log(entry: WorkoutLogRL):
    os.system('cls')

    payload = entry.model_dump(by_alias=False)
    print("\n===================================================== \n")
    print("BACKEND PAYLOAD:")
    pprint(payload, width=80, sort_dicts=False)
    print("\n===================================================== \n")

    response = ingest_log_entry(payload)
    print("\n===================================================== \n")
    print("BACKEND RESPONSE:")
    pprint(response, width=80, sort_dicts=False)
    print("\n===================================================== \n")

    update_exercise_js_file(response)

    return response
