from sqlalchemy.orm import Session
from app.models.models import User, APIKey
from app.repositories.user_repository import UserRepository
from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta
import secrets

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)
        self.db = db

    def register(self, username: str, email: str, password: str):
        # Verificar si el usuario ya existe
        if self.repository.get_user_by_email(email):
            raise HTTPException(status_code=400, detail="Email already registered")
        
        if self.repository.get_user_by_username(username):
            raise HTTPException(status_code=400, detail="Username already taken")

        # Crear el usuario
        hashed_password = pwd_context.hash(password)
        user = User(
            username=username,
            email=email,
            password_hash=hashed_password,
            created_at=datetime.utcnow()
        )
        
        user = self.repository.create_user(user)
        
        # Crear API key
        api_key = APIKey(
            user_id=user.user_id,
            api_key=secrets.token_urlsafe(32)
        )
        api_key = self.repository.create_api_key(api_key)
        
        return {
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email,
            "api_key": api_key.api_key,
            "created_at": user.created_at
        }

    def login(self, email: str, password: str):
        user = self.repository.get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        if not pwd_context.verify(password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        # Crear nueva API key
        api_key = APIKey(
            user_id=user.user_id,
            api_key=secrets.token_urlsafe(32)
        )
        api_key = self.repository.create_api_key(api_key)
        
        return {
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email,
            "api_key": api_key.api_key,
            "created_at": user.created_at
        } 