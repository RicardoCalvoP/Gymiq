# api_service/main.py
from fastapi import FastAPI

from .routes.router_logs import router as logs_router
from .routes.router_auth import router as auth_router
from .routes.router_users import router as users_router

app = FastAPI(title="Gymiq Core API")

# Logs RL
app.include_router(logs_router)

# Auth + usuarios
app.include_router(auth_router)
app.include_router(users_router)
