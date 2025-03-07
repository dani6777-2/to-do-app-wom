from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.config.database import get_db
from app.services.task_service import TaskService
from app.utils.auth import get_current_user
from app.models.models import User
from app.models.schemas import TaskCreateRequest, TaskUpdateRequest, TaskResponse

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtiene todas las tareas del usuario autenticado.
    
    Requiere autenticación mediante API key en el header 'X-API-Key'.
    Las tareas se obtienen de todas las listas del usuario.
    """
    service = TaskService(db)
    return service.get_user_tasks(current_user.user_id)

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtiene una tarea específica por su ID.
    
    - **task_id**: ID de la tarea a obtener
    
    Requiere autenticación mediante API key en el header 'X-API-Key'.
    Solo puede acceder a las tareas de las listas propias del usuario.
    """
    service = TaskService(db)
    return service.get_task(task_id, current_user.user_id)

@router.post("/", response_model=TaskResponse, status_code=201)
async def create_task(
    task_data: TaskCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Crea una nueva tarea.
    
    - **list_id**: ID de la lista donde se creará la tarea
    - **task_name**: Nombre de la tarea
    - **description**: Descripción detallada de la tarea (opcional)
    - **is_completed**: Estado de completitud de la tarea (opcional, default: false)
    
    Requiere autenticación mediante API key en el header 'X-API-Key'.
    Solo puede crear tareas en listas propias del usuario.
    """
    service = TaskService(db)
    return service.create_task(task_data.list_id, current_user.user_id, task_data.dict())

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Actualiza una tarea existente.
    
    - **task_id**: ID de la tarea a actualizar
    - **task_name**: Nuevo nombre de la tarea (opcional)
    - **description**: Nueva descripción de la tarea (opcional)
    - **is_completed**: Nuevo estado de completitud (opcional)
    
    Requiere autenticación mediante API key en el header 'X-API-Key'.
    Solo puede modificar tareas de las listas propias del usuario.
    """
    service = TaskService(db)
    return service.update_task(task_id, current_user.user_id, task_data.dict(exclude_unset=True))

@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Elimina una tarea.
    
    - **task_id**: ID de la tarea a eliminar
    
    Requiere autenticación mediante API key en el header 'X-API-Key'.
    Solo puede eliminar tareas de las listas propias del usuario.
    """
    service = TaskService(db)
    if service.delete_task(task_id, current_user.user_id):
        return {"message": "Task deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found") 