from datetime import datetime
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from app.models.models import APIKey, User
from app.config.database import get_db

api_key_header = APIKeyHeader(name="X-API-Key")

async def get_current_user(
    api_key: str = Depends(api_key_header),
    db: Session = Depends(get_db)
) -> User:
    # Buscar la API key en la base de datos
    api_key_record = db.query(APIKey).filter(
        APIKey.api_key == api_key
    ).first()
    
    if not api_key_record:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
    
    # Obtener el usuario asociado a la API key
    user = db.query(User).filter(User.user_id == api_key_record.user_id).first()
    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )
    
    return user 