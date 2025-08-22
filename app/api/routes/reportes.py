from fastapi import APIRouter, Depends, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import date
from typing import Optional
from ...database import get_db
from ...crud import personas_mayores as crud_pm
from .auth import get_current_user

router = APIRouter(prefix="/reportes", tags=["reportes"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
def menu_reportes(
    request: Request,
    current_user = Depends(get_current_user)
):
    return templates.TemplateResponse("reportes/menu.html", {
        "request": request
    })

@router.get("/estadisticas", response_class=HTMLResponse)
def estadisticas_generales(
    request: Request,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    estadisticas = crud_pm.get_estadisticas_generales(db)
    personas_resumen = crud_pm.get_personas_con_resumen(db, limit=10)
    
    return templates.TemplateResponse("reportes/estadisticas.html", {
        "request": request,
        "estadisticas": estadisticas,
        "personas_resumen": personas_resumen
    })

@router.get("/personas-sin-atencion", response_class=HTMLResponse)
def personas_sin_atencion_reciente(
    request: Request,
    dias: int = Query(90, ge=1, le=365),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    personas = crud_pm.get_personas_sin_atencion_reciente(db, dias)
    
    return templates.TemplateResponse("reportes/personas_sin_atencion.html", {
        "request": request,
        "personas": personas,
        "dias": dias
    })

@router.get("/busqueda-avanzada", response_class=HTMLResponse)
def busqueda_avanzada(
    request: Request,
    nombre: Optional[str] = Query(None),
    apellido: Optional[str] = Query(None),
    rut: Optional[str] = Query(None),
    edad_min: Optional[int] = Query(None),
    edad_max: Optional[int] = Query(None),
    macrosector_id: Optional[int] = Query(None),
    genero_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    personas = []
    generos = crud_pm.get_generos(db)
    macrosectores = crud_pm.get_macrosectores(db)
    
    # Solo buscar si hay al menos un filtro
    if any([nombre, apellido, rut, edad_min, edad_max, macrosector_id, genero_id]):
        personas = crud_pm.buscar_personas_avanzado(
            db, nombre=nombre, apellido=apellido, rut=rut,
            edad_min=edad_min, edad_max=edad_max,
            macrosector_id=macrosector_id, genero_id=genero_id
        )
    
    return templates.TemplateResponse("reportes/busqueda_avanzada.html", {
        "request": request,
        "personas": personas,
        "generos": generos,
        "macrosectores": macrosectores,
        "filtros": {
            "nombre": nombre,
            "apellido": apellido,
            "rut": rut,
            "edad_min": edad_min,
            "edad_max": edad_max,
            "macrosector_id": macrosector_id,
            "genero_id": genero_id
        }
    })