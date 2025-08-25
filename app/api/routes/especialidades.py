from fastapi import APIRouter, Depends, HTTPException, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.crud import especialidades
from app.schemas.especialidades import EspecialidadCreate, EspecialidadUpdate
from app.models.user import User
from .auth import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def lista_especialidades(
    request: Request, 
    page: int = 1, 
    per_page: int = 20,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lista de especialidades con paginación."""
    skip = (page - 1) * per_page
    especialidades_list = especialidades.get_especialidades(db, skip=skip, limit=per_page, search=search)
    total = especialidades.count_especialidades(db, search=search if search else None)
    total_pages = (total + per_page - 1) // per_page
    
    return templates.TemplateResponse("especialidades/lista.html", {
        "request": request,
        "especialidades": especialidades_list,
        "current_page": page,
        "total_pages": total_pages,
        "search": search,
        "total": total,
        "user": current_user
    })


@router.get("/crear", response_class=HTMLResponse)
async def crear_especialidad_form(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Formulario para crear nueva especialidad."""
    return templates.TemplateResponse("especialidades/formulario.html", {
        "request": request,
        "user": current_user,
        "action": "crear"
    })


@router.post("/crear")
async def crear_especialidad(
    request: Request,
    espe_especialidad: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Crear nueva especialidad."""
    try:
        especialidad_data = EspecialidadCreate(espe_especialidad=espe_especialidad)
        especialidades.create_especialidad(db, especialidad_data)
        return RedirectResponse(url="/especialidades/", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        return templates.TemplateResponse("especialidades/formulario.html", {
            "request": request,
            "user": current_user,
            "action": "crear",
            "error": f"Error al crear especialidad: {str(e)}"
        })


@router.get("/{especialidad_id}/editar", response_class=HTMLResponse)
async def editar_especialidad_form(
    especialidad_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Formulario para editar especialidad."""
    especialidad = especialidades.get_especialidad(db, especialidad_id)
    if not especialidad:
        raise HTTPException(status_code=404, detail="Especialidad no encontrada")
    
    return templates.TemplateResponse("especialidades/formulario.html", {
        "request": request,
        "user": current_user,
        "especialidad": especialidad,
        "action": "editar"
    })


@router.post("/{especialidad_id}/editar")
async def editar_especialidad(
    especialidad_id: int,
    request: Request,
    espe_especialidad: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Actualizar especialidad."""
    try:
        especialidad_update = EspecialidadUpdate(espe_especialidad=espe_especialidad)
        especialidades.update_especialidad(db, especialidad_id, especialidad_update)
        return RedirectResponse(url="/especialidades/", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        especialidad = especialidades.get_especialidad(db, especialidad_id)
        return templates.TemplateResponse("especialidades/formulario.html", {
            "request": request,
            "user": current_user,
            "especialidad": especialidad,
            "action": "editar",
            "error": f"Error al actualizar especialidad: {str(e)}"
        })


@router.post("/{especialidad_id}/eliminar")
async def eliminar_especialidad(
    especialidad_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Eliminar especialidad."""
    especialidades.delete_especialidad(db, especialidad_id)
    return RedirectResponse(url="/especialidades/", status_code=status.HTTP_303_SEE_OTHER)
