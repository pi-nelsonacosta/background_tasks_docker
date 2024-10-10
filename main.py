# Archivo: main.py
from fastapi import FastAPI
from app.api.routers import background_tasks_router

app = FastAPI()

# Registrar el router de /send-log/
app.include_router(background_tasks_router.router, prefix="/api/v1", tags=["background_tasks"])

# Para correr la aplicación
# uvicorn main:app --reload
