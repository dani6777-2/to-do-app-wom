from sqlalchemy.orm import Session
from app.models.models import List
from app.repositories.list_repository import ListRepository
from fastapi import HTTPException

class ListService:
    def __init__(self, db: Session):
        self.repository = ListRepository(db)
        self.db = db

    def get_user_lists(self, user_id: int):
        return self.repository.get_lists_by_user(user_id)

    def get_list(self, list_id: int, user_id: int):
        list_obj = self.repository.get_list_by_id(list_id)
        if not list_obj:
            raise HTTPException(status_code=404, detail="List not found")
        
        if list_obj.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to access this list")
        
        return list_obj

    def create_list(self, user_id: int, list_name: str):
        list_obj = List(
            user_id=user_id,
            list_name=list_name
        )
        return self.repository.create_list(list_obj)

    def update_list(self, list_id: int, user_id: int, list_data: dict):
        # Verificar que la lista existe y pertenece al usuario
        list_obj = self.get_list(list_id, user_id)
        
        # Actualizar solo el nombre de la lista
        if "list_name" not in list_data:
            raise HTTPException(status_code=400, detail="list_name is required")
        
        return self.repository.update_list(list_id, {"list_name": list_data["list_name"]})

    def delete_list(self, list_id: int, user_id: int) -> bool:
        # Verificar que la lista existe y pertenece al usuario
        list_obj = self.get_list(list_id, user_id)
        
        return self.repository.delete_list(list_id) 