from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.services.user_service import UserService
from app.models.schemas import UserRegisterRequest, UserLoginRequest, UserResponse
from typing import List

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=UserResponse, status_code=201)
async def register(
    user_data: UserRegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Registra un nuevo usuario en el sistema.
    
    - **username**: Nombre de usuario único
    - **email**: Correo electrónico único
    - **password**: Contraseña del usuario
    
    Retorna el usuario creado junto con su API key para autenticación.
    """
    service = UserService(db)
    return service.register(user_data.username, user_data.email, user_data.password)

@router.post("/login", response_model=UserResponse)
async def login(
    login_data: UserLoginRequest,
    db: Session = Depends(get_db)
):
    """
    Inicia sesión de un usuario existente.
    
    - **email**: Correo electrónico del usuario
    - **password**: Contraseña del usuario
    
    Retorna la información del usuario y su API key para autenticación.
    Si las credenciales son inválidas, retorna un error 401.
    """
    service = UserService(db)
    return service.login(login_data.email, login_data.password) 