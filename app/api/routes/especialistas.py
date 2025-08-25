from fastapi import APIRouter, Depends, HTTPException, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.crud import especialistas
from app.schemas.especialistas import EspecialistaCreate, EspecialistaUpdate
from app.models.user import User
from .auth import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def lista_especialistas(
    request: Request, 
    page: int = 1, 
    search: str = "",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lista de especialistas con paginación y búsqueda."""
    per_page = 10
    skip = (page - 1) * per_page
    
    especialistas_list = especialistas.get_especialistas(db, skip=skip, limit=per_page, search=search if search else None)
    total = especialistas.count_especialistas(db, search=search if search else None)
    total_pages = (total + per_page - 1) // per_page
    
    return templates.TemplateResponse("especialistas/lista.html", {
        "request": request,
        "especialistas": especialistas_list,
        "current_page": page,
        "total_pages": total_pages,
        "search": search,
        "total": total,
        "user": current_user
    })


@router.get("/crear", response_class=HTMLResponse)
async def crear_especialista_form(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Formulario para crear nuevo especialista."""
    from app.crud import especialidades
    especialidades_list = especialidades.get_especialidades(db, skip=0, limit=100)
    
    return templates.TemplateResponse("especialistas/formulario.html", {
        "request": request,
        "user": current_user,
        "action": "crear",
        "especialidades": especialidades_list
    })


@router.post("/crear")
async def crear_especialista(
    request: Request,
    esp_rut: str = Form(...),
    esp_nombre: str = Form(...),
    esp_apellido: str = Form(...),
    esp_espeid: Optional[int] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Crear nuevo especialista."""
    try:
        especialista_data = EspecialistaCreate(
            esp_rut=esp_rut,
            esp_nombre=esp_nombre,
            esp_apellido=esp_apellido,
            esp_espeid=esp_espeid
        )
        especialistas.create_especialista(db, especialista_data)
        return RedirectResponse(url="/especialistas/", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        from app.crud import especialidades
        especialidades_list = especialidades.get_especialidades(db, skip=0, limit=100)
        
        return templates.TemplateResponse("especialistas/formulario.html", {
            "request": request,
            "user": current_user,
            "action": "crear",
            "especialidades": especialidades_list,
            "error": f"Error al crear especialista: {str(e)}"
        })


@router.get("/{especialista_id}/editar", response_class=HTMLResponse)
async def editar_especialista_form(
    especialista_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Formulario para editar especialista."""
    especialista = especialistas.get_especialista(db, especialista_id)
    if not especialista:
        raise HTTPException(status_code=404, detail="Especialista no encontrado")
    
    from app.crud.especialidades import get_especialidades
    especialidades_list = get_especialidades(db)
    return templates.TemplateResponse("especialistas/formulario.html", {
        "request": request,
        "user": current_user,
        "especialista": especialista,
        "action": "editar",
        "especialidades": especialidades_list
    })


@router.post("/{especialista_id}/editar")
async def editar_especialista(
    especialista_id: int,
    request: Request,
    esp_rut: str = Form(...),
    esp_nombre: str = Form(...),
    esp_apellido: str = Form(...),
    esp_espeid: Optional[int] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Actualizar especialista."""
    try:
        especialista_update = EspecialistaUpdate(
            esp_rut=esp_rut,
            esp_nombre=esp_nombre,
            esp_apellido=esp_apellido,
            esp_espeid=esp_espeid
        )
        especialistas.update_especialista(db, especialista_id, especialista_update)
        return RedirectResponse(url="/especialistas/", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        especialista = especialistas.get_especialista(db, especialista_id)
        from app.crud.especialidades import get_especialidades
        especialidades_list = get_especialidades(db)
        return templates.TemplateResponse("especialistas/formulario.html", {
            "request": request,
            "user": current_user,
            "especialista": especialista,
            "action": "editar",
            "especialidades": especialidades_list,
            "error": f"Error al actualizar especialista: {str(e)}"
        })


@router.post("/{especialista_id}/eliminar")
async def eliminar_especialista(
    especialista_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Eliminar especialista."""
    especialistas.delete_especialista(db, especialista_id)
    return RedirectResponse(url="/especialistas/", status_code=status.HTTP_303_SEE_OTHER)
