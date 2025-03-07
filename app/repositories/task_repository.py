from sqlalchemy.orm import Session
from app.models.models import Task, List
from .base_repository import BaseRepository

class TaskRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, Task)

    def get_tasks_by_list_id(self, list_id: int):
        return self.db.query(Task).filter(Task.list_id == list_id).all()

    def get_task_by_id(self, task_id: int):
        return self.db.query(Task).filter(Task.task_id == task_id).first()

    def get_user_tasks(self, user_id: int):
        return (
            self.db.query(Task)
            .join(List)
            .filter(List.user_id == user_id)
            .all()
        )

    def create_task(self, task):
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def update_task(self, task_id: int, task_data: dict):
        task = self.get_task_by_id(task_id)
        if task:
            for key, value in task_data.items():
                setattr(task, key, value)
            self.db.commit()
            self.db.refresh(task)
        return task

    def delete_task(self, task_id: int) -> bool:
        task = self.get_task_by_id(task_id)
        if task:
            self.db.delete(task)
            self.db.commit()
            return True
        return False 