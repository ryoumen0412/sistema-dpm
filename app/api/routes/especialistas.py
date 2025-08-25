from fastapi import APIRouter, Depends, HTTPException, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional

from app.api.deps import get_db, get_current_user
from app.crud import especialistas
from app.schemas.especialistas import EspecialistaCreate, EspecialistaUpdate
from app.models.user import User

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
    current_user: User = Depends(get_current_user)
):
    """Formulario para crear nuevo especialista."""
    return templates.TemplateResponse("especialistas/formulario.html", {
        "request": request,
        "user": current_user,
        "action": "crear"
    })


@router.post("/crear")
async def crear_especialista(
    request: Request,
    esp_nombre: str = Form(...),
    esp_apellido: str = Form(...),
    esp_especialidad: str = Form(...),
    esp_telefono: Optional[str] = Form(None),
    esp_email: Optional[str] = Form(None),
    esp_direccion: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Crear nuevo especialista."""
    try:
        especialista_data = EspecialistaCreate(
            esp_nombre=esp_nombre,
            esp_apellido=esp_apellido,
            esp_especialidad=esp_especialidad,
            esp_telefono=esp_telefono,
            esp_email=esp_email,
            esp_direccion=esp_direccion
        )
        especialistas.create_especialista(db, especialista_data)
        return RedirectResponse(url="/especialistas/", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        return templates.TemplateResponse("especialistas/formulario.html", {
            "request": request,
            "user": current_user,
            "action": "crear",
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
    
    return templates.TemplateResponse("especialistas/formulario.html", {
        "request": request,
        "user": current_user,
        "especialista": especialista,
        "action": "editar"
    })


@router.post("/{especialista_id}/editar")
async def editar_especialista(
    especialista_id: int,
    request: Request,
    esp_nombre: str = Form(...),
    esp_apellido: str = Form(...),
    esp_especialidad: str = Form(...),
    esp_telefono: Optional[str] = Form(None),
    esp_email: Optional[str] = Form(None),
    esp_direccion: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Actualizar especialista."""
    try:
        especialista_update = EspecialistaUpdate(
            esp_nombre=esp_nombre,
            esp_apellido=esp_apellido,
            esp_especialidad=esp_especialidad,
            esp_telefono=esp_telefono,
            esp_email=esp_email,
            esp_direccion=esp_direccion
        )
        especialistas.update_especialista(db, especialista_id, especialista_update)
        return RedirectResponse(url="/especialistas/", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        especialista = especialistas.get_especialista(db, especialista_id)
        return templates.TemplateResponse("especialistas/formulario.html", {
            "request": request,
            "user": current_user,
            "especialista": especialista,
            "action": "editar",
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
