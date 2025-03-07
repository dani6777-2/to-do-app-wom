from sqlalchemy.orm import Session
from app.models.models import User, APIKey
from .base_repository import BaseRepository
from typing import Optional

class UserRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, User)

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()

    def create_user(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def create_api_key(self, api_key: APIKey) -> APIKey:
        self.db.add(api_key)
        self.db.commit()
        self.db.refresh(api_key)
        return api_key

    def get_api_key(self, user_id: int) -> Optional[APIKey]:
        return self.db.query(APIKey).filter(APIKey.user_id == user_id).first()

    def delete_api_key(self, api_key: APIKey) -> None:
        self.db.delete(api_key)
        self.db.commit() 