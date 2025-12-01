from fastapi import FastAPI
from .router_logs import router as logs_router

app = FastAPI(title="Gymiq Core API")

app.include_router(logs_router)
