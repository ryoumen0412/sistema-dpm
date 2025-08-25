from fastapi import APIRouter, Depends, HTTPException, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from app.database import get_db
from app.crud import actividades
from app.schemas.actividades import ActividadCreate, ActividadUpdate
from app.models.user import User
from .auth import get_current_user

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
        "limit": per_page,
        "skip": skip,
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
    act_actividad: str = Form(...),
    act_fecha: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Crear nueva actividad."""
    try:
        # Convert date string to date object
        from datetime import datetime
        fecha_obj = datetime.strptime(act_fecha, '%Y-%m-%d').date()
        
        actividad_data = ActividadCreate(
            act_actividad=act_actividad,
            act_fecha=fecha_obj
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


@router.post("/editar/{actividad_id}")
async def editar_actividad(
    actividad_id: int,
    request: Request,
    act_actividad: str = Form(...),
    act_fecha: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Editar actividad existente."""
    try:
        # Convert date string to date object
        from datetime import datetime
        fecha_obj = datetime.strptime(act_fecha, '%Y-%m-%d').date()
        
        actividad_data = ActividadUpdate(
            act_actividad=act_actividad,
            act_fecha=fecha_obj
        )
        actividades.update_actividad(db, actividad_id, actividad_data)
        return RedirectResponse(url="/actividades/", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        return templates.TemplateResponse("actividades/formulario.html", {
            "request": request,
            "user": current_user,
            "action": "editar",
            "actividad_id": actividad_id,
            "error": f"Error al editar actividad: {str(e)}"
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
