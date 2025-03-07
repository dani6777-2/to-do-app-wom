from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers.task_controller import router as task_router
from app.controllers.user_controller import router as user_router
from app.controllers.list_controller import router as list_router

app = FastAPI(
    title="To-Do App API",
    description="API RESTful para gestión de tareas con autenticación mediante API keys",
    version="1.0.0"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos
    allow_headers=["*"],  # Permite todos los headers
    expose_headers=["*"]  # Expone todos los headers
)

# Incluir routers
app.include_router(user_router)
app.include_router(list_router)
app.include_router(task_router)

@app.get("/")
async def root():
    return {
        "message": "Bienvenido a la API de gestión de tareas",
        "docs": "/docs",
        "redoc": "/redoc"
    } 