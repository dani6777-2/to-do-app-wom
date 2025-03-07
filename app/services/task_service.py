from sqlalchemy.orm import Session
from app.models.models import Task, List
from app.repositories.task_repository import TaskRepository
from fastapi import HTTPException

class TaskService:
    def __init__(self, db: Session):
        self.repository = TaskRepository(db)
        self.db = db

    def get_user_tasks(self, user_id: int):
        return self.repository.get_user_tasks(user_id)

    def get_task(self, task_id: int, user_id: int):
        task = self.repository.get_task_by_id(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        # Verificar que la tarea pertenece al usuario
        list_owner = self.db.query(List).filter(List.list_id == task.list_id).first()
        if not list_owner or list_owner.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to access this task")
        
        return task

    def create_task(self, list_id: int, user_id: int, task_data: dict):
        # Verificar que la lista pertenece al usuario
        list_obj = self.db.query(List).filter(List.list_id == list_id).first()
        if not list_obj or list_obj.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to create tasks in this list")

        task = Task(
            list_id=list_id,
            task_name=task_data["task_name"],
            description=task_data.get("description"),
            is_completed=task_data.get("is_completed", False)
        )
        return self.repository.create_task(task)

    def update_task(self, task_id: int, user_id: int, task_data: dict):
        task = self.get_task(task_id, user_id)  # This will handle authorization
        updated_task = self.repository.update_task(task_id, task_data)
        if not updated_task:
            raise HTTPException(status_code=404, detail="Task not found")
        return updated_task

    def delete_task(self, task_id: int, user_id: int) -> bool:
        task = self.get_task(task_id, user_id)  # This will handle authorization
        return self.repository.delete_task(task_id) 