from fastapi import APIRouter, Depends, HTTPException, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional

from app.api.deps import get_db, get_current_user
from app.crud import organizaciones
from app.schemas.organizaciones import OrganizacionCreate, OrganizacionUpdate
from app.models.user import User

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def lista_organizaciones(
    request: Request, 
    page: int = 1, 
    search: str = "",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lista de organizaciones con paginación y búsqueda."""
    per_page = 10
    skip = (page - 1) * per_page
    
    organizaciones_list = organizaciones.get_organizaciones(db, skip=skip, limit=per_page, search=search if search else None)
    total = organizaciones.count_organizaciones(db, search=search if search else None)
    total_pages = (total + per_page - 1) // per_page
    
    return templates.TemplateResponse("organizaciones/lista.html", {
        "request": request,
        "organizaciones": organizaciones_list,
        "current_page": page,
        "total_pages": total_pages,
        "search": search,
        "total": total,
        "user": current_user
    })


@router.get("/crear", response_class=HTMLResponse)
async def crear_organizacion_form(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Formulario para crear nueva organización."""
    return templates.TemplateResponse("organizaciones/formulario.html", {
        "request": request,
        "user": current_user,
        "action": "crear"
    })


@router.post("/crear")
async def crear_organizacion(
    request: Request,
    org_nombre: str = Form(...),
    org_descripcion: Optional[str] = Form(None),
    org_direccion: Optional[str] = Form(None),
    org_telefono: Optional[str] = Form(None),
    org_email: Optional[str] = Form(None),
    org_tipo: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Crear nueva organización."""
    try:
        organizacion_data = OrganizacionCreate(
            org_nombre=org_nombre,
            org_descripcion=org_descripcion,
            org_direccion=org_direccion,
            org_telefono=org_telefono,
            org_email=org_email,
            org_tipo=org_tipo
        )
        organizaciones.create_organizacion(db, organizacion_data)
        return RedirectResponse(url="/organizaciones/", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        return templates.TemplateResponse("organizaciones/formulario.html", {
            "request": request,
            "user": current_user,
            "action": "crear",
            "error": f"Error al crear organización: {str(e)}"
        })


@router.get("/{organizacion_id}/editar", response_class=HTMLResponse)
async def editar_organizacion_form(
    organizacion_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Formulario para editar organización."""
    organizacion = organizaciones.get_organizacion(db, organizacion_id)
    if not organizacion:
        raise HTTPException(status_code=404, detail="Organización no encontrada")
    
    return templates.TemplateResponse("organizaciones/formulario.html", {
        "request": request,
        "user": current_user,
        "organizacion": organizacion,
        "action": "editar"
    })


@router.post("/{organizacion_id}/editar")
async def editar_organizacion(
    organizacion_id: int,
    request: Request,
    org_nombre: str = Form(...),
    org_descripcion: Optional[str] = Form(None),
    org_direccion: Optional[str] = Form(None),
    org_telefono: Optional[str] = Form(None),
    org_email: Optional[str] = Form(None),
    org_tipo: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Actualizar organización."""
    try:
        organizacion_update = OrganizacionUpdate(
            org_nombre=org_nombre,
            org_descripcion=org_descripcion,
            org_direccion=org_direccion,
            org_telefono=org_telefono,
            org_email=org_email,
            org_tipo=org_tipo
        )
        organizaciones.update_organizacion(db, organizacion_id, organizacion_update)
        return RedirectResponse(url="/organizaciones/", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        organizacion = organizaciones.get_organizacion(db, organizacion_id)
        return templates.TemplateResponse("organizaciones/formulario.html", {
            "request": request,
            "user": current_user,
            "organizacion": organizacion,
            "action": "editar",
            "error": f"Error al actualizar organización: {str(e)}"
        })


@router.post("/{organizacion_id}/eliminar")
async def eliminar_organizacion(
    organizacion_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Eliminar organización."""
    organizaciones.delete_organizacion(db, organizacion_id)
    return RedirectResponse(url="/organizaciones/", status_code=status.HTTP_303_SEE_OTHER)
