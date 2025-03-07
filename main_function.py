from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from functions_framework import logging

from app.controllers.user_controller import router as user_router
from app.controllers.list_controller import router as list_router
from app.controllers.task_controller import router as task_router

app = FastAPI(
    title="Todo List API",
    description="API para gestionar listas de tareas",
    version="1.0.0"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir los routers
app.include_router(user_router, prefix="/auth", tags=["Authentication"])
app.include_router(list_router, prefix="/lists", tags=["Lists"])
app.include_router(task_router, prefix="/tasks", tags=["Tasks"])

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de Todo List"}

def handle_request(request: Request):
    """
    Función principal que maneja las solicitudes HTTP en Cloud Functions
    """
    return app(request) 