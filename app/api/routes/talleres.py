from fastapi import APIRouter, Depends, HTTPException, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from app.database import get_db
from app.crud import talleres
from app.schemas.talleres import TallerCreate, TallerUpdate
from app.models.user import User
from .auth import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def lista_talleres(
    request: Request, 
    page: int = 1, 
    search: str = "",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lista de talleres con paginación y búsqueda."""
    per_page = 10
    skip = (page - 1) * per_page
    
    talleres_list = talleres.get_talleres(db, skip=skip, limit=per_page, search=search if search else None)
    total = talleres.count_talleres(db, search=search if search else None)
    total_pages = (total + per_page - 1) // per_page
    
    return templates.TemplateResponse("talleres/lista.html", {
        "request": request,
        "talleres": talleres_list,
        "current_page": page,
        "total_pages": total_pages,
        "search": search,
        "total": total,
        "user": current_user
    })


@router.get("/crear", response_class=HTMLResponse)
async def crear_taller_form(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Formulario para crear nuevo taller."""
    return templates.TemplateResponse("talleres/formulario.html", {
        "request": request,
        "user": current_user,
        "action": "crear"
    })


@router.post("/crear")
async def crear_taller(
    request: Request,
    tal_taller: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Crear nuevo taller."""
    try:
        taller_data = TallerCreate(tal_taller=tal_taller)
        talleres.create_taller(db, taller_data)
        return RedirectResponse(url="/talleres/", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        return templates.TemplateResponse("talleres/formulario.html", {
            "request": request,
            "user": current_user,
            "action": "crear",
            "error": f"Error al crear taller: {str(e)}"
        })


@router.get("/{taller_id}/editar", response_class=HTMLResponse)
async def editar_taller_form(
    taller_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Formulario para editar taller."""
    taller = talleres.get_taller(db, taller_id)
    if not taller:
        raise HTTPException(status_code=404, detail="Taller no encontrado")
    
    return templates.TemplateResponse("talleres/formulario.html", {
        "request": request,
        "user": current_user,
        "taller": taller,
        "action": "editar"
    })


@router.post("/{taller_id}/editar")
async def editar_taller(
    taller_id: int,
    request: Request,
    tal_taller: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Actualizar taller."""
    try:
        taller_update = TallerUpdate(tal_taller=tal_taller)
        talleres.update_taller(db, taller_id, taller_update)
        return RedirectResponse(url="/talleres/", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        taller = talleres.get_taller(db, taller_id)
        return templates.TemplateResponse("talleres/formulario.html", {
            "request": request,
            "user": current_user,
            "taller": taller,
            "action": "editar",
            "error": f"Error al actualizar taller: {str(e)}"
        })


@router.post("/{taller_id}/eliminar")
async def eliminar_taller(
    taller_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Eliminar taller."""
    talleres.delete_taller(db, taller_id)
    return RedirectResponse(url="/talleres/", status_code=status.HTTP_303_SEE_OTHER)
