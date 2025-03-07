from sqlalchemy.orm import Session
from app.models.models import List
from .base_repository import BaseRepository

class ListRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, List)

    def get_lists_by_user(self, user_id: int):
        return self.db.query(List).filter(List.user_id == user_id).all()

    def get_list_by_id(self, list_id: int):
        return self.db.query(List).filter(List.list_id == list_id).first()

    def create_list(self, list_obj: List):
        self.db.add(list_obj)
        self.db.commit()
        self.db.refresh(list_obj)
        return list_obj

    def update_list(self, list_id: int, list_data: dict):
        list_obj = self.get_list_by_id(list_id)
        if list_obj:
            for key, value in list_data.items():
                setattr(list_obj, key, value)
            self.db.commit()
            self.db.refresh(list_obj)
        return list_obj

    def delete_list(self, list_id: int) -> bool:
        list_obj = self.get_list_by_id(list_id)
        if list_obj:
            self.db.delete(list_obj)
            self.db.commit()
            return True
        return False 