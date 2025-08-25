from fastapi import APIRouter, Depends, HTTPException, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from app.api.deps import get_db, get_current_user
from app.crud import actividades
from app.schemas.actividades import ActividadCreate, ActividadUpdate
from app.models.user import User

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def lista_actividades(
    request: Request, 
    page: int = 1, 
    search: str = "",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lista de actividades con paginación y búsqueda."""
    per_page = 10
    skip = (page - 1) * per_page
    
    actividades_list = actividades.get_actividades(db, skip=skip, limit=per_page, search=search if search else None)
    total = actividades.count_actividades(db, search=search if search else None)
    total_pages = (total + per_page - 1) // per_page
    
    return templates.TemplateResponse("actividades/lista.html", {
        "request": request,
        "actividades": actividades_list,
        "current_page": page,
        "total_pages": total_pages,
        "search": search,
        "total": total,
        "user": current_user
    })


@router.get("/crear", response_class=HTMLResponse)
async def crear_actividad_form(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Formulario para crear nueva actividad."""
    return templates.TemplateResponse("actividades/formulario.html", {
        "request": request,
        "user": current_user,
        "action": "crear"
    })


@router.post("/crear")
async def crear_actividad(
    request: Request,
    act_nombre: str = Form(...),
    act_descripcion: Optional[str] = Form(None),
    act_fecha: Optional[str] = Form(None),
    act_lugar: Optional[str] = Form(None),
    act_tipo: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Crear nueva actividad."""
    try:
        # Convert date string to datetime object
        fecha = None
        if act_fecha:
            fecha = datetime.strptime(act_fecha, "%Y-%m-%d")
        
        actividad_data = ActividadCreate(
            act_nombre=act_nombre,
            act_descripcion=act_descripcion,
            act_fecha=fecha,
            act_lugar=act_lugar,
            act_tipo=act_tipo
        )
        actividades.create_actividad(db, actividad_data)
        return RedirectResponse(url="/actividades/", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        return templates.TemplateResponse("actividades/formulario.html", {
            "request": request,
            "user": current_user,
            "action": "crear",
            "error": f"Error al crear actividad: {str(e)}"
        })


@router.get("/{actividad_id}/editar", response_class=HTMLResponse)
async def editar_actividad_form(
    actividad_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Formulario para editar actividad."""
    actividad = actividades.get_actividad(db, actividad_id)
    if not actividad:
        raise HTTPException(status_code=404, detail="Actividad no encontrada")
    
    return templates.TemplateResponse("actividades/formulario.html", {
        "request": request,
        "user": current_user,
        "actividad": actividad,
        "action": "editar"
    })


@router.post("/{actividad_id}/editar")
async def editar_actividad(
    actividad_id: int,
    request: Request,
    act_nombre: str = Form(...),
    act_descripcion: Optional[str] = Form(None),
    act_fecha: Optional[str] = Form(None),
    act_lugar: Optional[str] = Form(None),
    act_tipo: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Actualizar actividad."""
    try:
        # Convert date string to datetime object
        fecha = None
        if act_fecha:
            fecha = datetime.strptime(act_fecha, "%Y-%m-%d")
        
        actividad_update = ActividadUpdate(
            act_nombre=act_nombre,
            act_descripcion=act_descripcion,
            act_fecha=fecha,
            act_lugar=act_lugar,
            act_tipo=act_tipo
        )
        actividades.update_actividad(db, actividad_id, actividad_update)
        return RedirectResponse(url="/actividades/", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        actividad = actividades.get_actividad(db, actividad_id)
        return templates.TemplateResponse("actividades/formulario.html", {
            "request": request,
            "user": current_user,
            "actividad": actividad,
            "action": "editar",
            "error": f"Error al actualizar actividad: {str(e)}"
        })


@router.post("/{actividad_id}/eliminar")
async def eliminar_actividad(
    actividad_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Eliminar actividad."""
    actividades.delete_actividad(db, actividad_id)
    return RedirectResponse(url="/actividades/", status_code=status.HTTP_303_SEE_OTHER)
