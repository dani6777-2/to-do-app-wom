from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.config.database import get_db
from app.services.list_service import ListService
from app.utils.auth import get_current_user
from app.models.models import User
from app.models.schemas import ListCreateRequest, ListResponse

router = APIRouter(prefix="/lists", tags=["lists"])

@router.get("/", response_model=List[ListResponse])
async def get_lists(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtiene todas las listas de tareas del usuario autenticado.
    
    Requiere autenticación mediante API key en el header 'X-API-Key'.
    """
    service = ListService(db)
    return service.get_user_lists(current_user.user_id)

@router.get("/{list_id}", response_model=ListResponse)
async def get_list(
    list_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtiene una lista de tareas específica por su ID.
    
    - **list_id**: ID de la lista a obtener
    
    Requiere autenticación mediante API key en el header 'X-API-Key'.
    Solo puede acceder a las listas propias del usuario.
    """
    service = ListService(db)
    return service.get_list(list_id, current_user.user_id)

@router.post("/", response_model=ListResponse, status_code=201)
async def create_list(
    list_data: ListCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Crea una nueva lista de tareas.
    
    - **list_name**: Nombre de la lista
    
    Requiere autenticación mediante API key en el header 'X-API-Key'.
    La lista se asociará automáticamente al usuario autenticado.
    """
    service = ListService(db)
    return service.create_list(current_user.user_id, list_data.list_name)

@router.put("/{list_id}", response_model=ListResponse)
async def update_list(
    list_id: int,
    list_data: ListCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Actualiza una lista de tareas existente.
    
    - **list_id**: ID de la lista a actualizar
    - **list_name**: Nuevo nombre de la lista
    
    Requiere autenticación mediante API key en el header 'X-API-Key'.
    Solo puede modificar las listas propias del usuario.
    """
    service = ListService(db)
    return service.update_list(list_id, current_user.user_id, {"list_name": list_data.list_name})

@router.delete("/{list_id}")
async def delete_list(
    list_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Elimina una lista de tareas.
    
    - **list_id**: ID de la lista a eliminar
    
    Requiere autenticación mediante API key en el header 'X-API-Key'.
    Solo puede eliminar las listas propias del usuario.
    Al eliminar una lista, se eliminarán también todas las tareas asociadas.
    """
    service = ListService(db)
    if service.delete_list(list_id, current_user.user_id):
        return {"message": "List deleted successfully"}
    raise HTTPException(status_code=404, detail="List not found") 