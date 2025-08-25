from fastapi import APIRouter, Depends, HTTPException, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from app.database import get_db
from app.crud import viajes
from app.schemas.viajes import ViajeCreate, ViajeUpdate
from app.models.user import User
from .auth import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def lista_viajes(
    request: Request, 
    page: int = 1, 
    search: str = "",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lista de viajes con paginación y búsqueda."""
    per_page = 10
    skip = (page - 1) * per_page
    
    viajes_list = viajes.get_viajes(db, skip=skip, limit=per_page, search=search if search else None)
    total = viajes.count_viajes(db, search=search if search else None)
    total_pages = (total + per_page - 1) // per_page
    
    return templates.TemplateResponse("viajes/lista.html", {
        "request": request,
        "viajes": viajes_list,
        "current_page": page,
        "total_pages": total_pages,
        "search": search,
        "total": total,
        "user": current_user
    })


@router.get("/crear", response_class=HTMLResponse)
async def crear_viaje_form(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Formulario para crear nuevo viaje."""
    return templates.TemplateResponse("viajes/formulario.html", {
        "request": request,
        "user": current_user,
        "action": "crear"
    })


@router.post("/crear")
async def crear_viaje(
    request: Request,
    via_viaje: str = Form(...),
    via_destino: str = Form(...),
    via_fecha: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Crear nuevo viaje."""
    try:
        # Convert date string to date object
        from datetime import datetime
        fecha_obj = datetime.strptime(via_fecha, '%Y-%m-%d').date()
        
        viaje_data = ViajeCreate(
            via_viaje=via_viaje,
            via_destino=via_destino,
            via_fecha=fecha_obj
        )
        viajes.create_viaje(db, viaje_data)
        return RedirectResponse(url="/viajes/", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        return templates.TemplateResponse("viajes/formulario.html", {
            "request": request,
            "user": current_user,
            "action": "crear",
            "error": f"Error al crear viaje: {str(e)}"
        })


@router.get("/{viaje_id}/editar", response_class=HTMLResponse)
async def editar_viaje_form(
    viaje_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Formulario para editar viaje."""
    viaje = viajes.get_viaje(db, viaje_id)
    if not viaje:
        raise HTTPException(status_code=404, detail="Viaje no encontrado")
    
    return templates.TemplateResponse("viajes/formulario.html", {
        "request": request,
        "user": current_user,
        "viaje": viaje,
        "action": "editar"
    })


@router.post("/editar/{viaje_id}")
async def editar_viaje(
    viaje_id: int,
    request: Request,
    via_viaje: str = Form(...),
    via_destino: str = Form(...),
    via_fecha: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Editar viaje existente."""
    try:
        # Convert date string to date object
        from datetime import datetime
        fecha_obj = datetime.strptime(via_fecha, '%Y-%m-%d').date()
        
        viaje_data = ViajeUpdate(
            via_viaje=via_viaje,
            via_destino=via_destino,
            via_fecha=fecha_obj
        )
        viajes.update_viaje(db, viaje_id, viaje_data)
        return RedirectResponse(url="/viajes/", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        return templates.TemplateResponse("viajes/formulario.html", {
            "request": request,
            "user": current_user,
            "action": "editar",
            "viaje_id": viaje_id,
            "error": f"Error al editar viaje: {str(e)}"
        })


@router.post("/{viaje_id}/eliminar")
async def eliminar_viaje(
    viaje_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Eliminar viaje."""
    viajes.delete_viaje(db, viaje_id)
    return RedirectResponse(url="/viajes/", status_code=status.HTTP_303_SEE_OTHER)
