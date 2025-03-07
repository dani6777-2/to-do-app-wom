from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Auth Schemas
class UserRegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "john@example.com",
                "password": "securepassword123"
            }
        }

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "john@example.com",
                "password": "securepassword123"
            }
        }

class UserResponse(BaseModel):
    user_id: int
    username: str
    email: str
    api_key: str
    created_at: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 1,
                "username": "john_doe",
                "email": "john@example.com",
                "api_key": "abc123xyz789...",
                "created_at": "2024-03-14T12:00:00"
            }
        }

# List Schemas
class ListCreateRequest(BaseModel):
    list_name: str

    class Config:
        json_schema_extra = {
            "example": {
                "list_name": "Compras del supermercado"
            }
        }

class ListResponse(BaseModel):
    list_id: int
    user_id: int
    list_name: str
    created_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "list_id": 1,
                "user_id": 1,
                "list_name": "Compras del supermercado",
                "created_at": "2024-03-14T12:00:00"
            }
        }

# Task Schemas
class TaskCreateRequest(BaseModel):
    list_id: int
    task_name: str
    description: Optional[str] = None
    is_completed: Optional[bool] = False

    class Config:
        json_schema_extra = {
            "example": {
                "list_id": 1,
                "task_name": "Comprar leche",
                "description": "2 litros de leche deslactosada",
                "is_completed": False
            }
        }

class TaskUpdateRequest(BaseModel):
    task_name: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None

    class Config:
        json_schema_extra = {
            "example": {
                "task_name": "Comprar leche",
                "description": "2 litros de leche deslactosada",
                "is_completed": True
            }
        }

class TaskResponse(BaseModel):
    task_id: int
    list_id: int
    task_name: str
    description: Optional[str]
    is_completed: bool
    created_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "task_id": 1,
                "list_id": 1,
                "task_name": "Comprar leche",
                "description": "2 litros de leche deslactosada",
                "is_completed": False,
                "created_at": "2024-03-14T12:00:00"
            }
        } 