from fastapi import APIRouter, Depends, Request, Form, HTTPException, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import date
from typing import Optional
from ...database import get_db
from ...crud import personas_mayores as crud_pm
from ...schemas.personas_mayores import AtencionCreate
from .auth import get_current_user

router = APIRouter(prefix="/atenciones", tags=["atenciones"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
def listar_atenciones(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, le=100),
    persona_id: Optional[int] = Query(None),
    especialista_id: Optional[int] = Query(None),
    fecha_desde: Optional[date] = Query(None),
    fecha_hasta: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    atenciones = crud_pm.get_atenciones(
        db, skip=skip, limit=limit,
        persona_id=persona_id, especialista_id=especialista_id,
        fecha_desde=fecha_desde, fecha_hasta=fecha_hasta
    )
    
    # Para filtros
    especialistas = crud_pm.get_especialistas(db)
    
    return templates.TemplateResponse("atenciones/lista.html", {
        "request": request,
        "atenciones": atenciones,
        "especialistas": especialistas,
        "persona_id": persona_id,
        "especialista_id": especialista_id,
        "fecha_desde": fecha_desde,
        "fecha_hasta": fecha_hasta
    })

@router.get("/nueva", response_class=HTMLResponse)
def nueva_atencion_form(
    request: Request,
    persona_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    especialistas = crud_pm.get_especialistas(db)
    persona = None
    if persona_id:
        persona = crud_pm.get_persona_mayor(db, persona_id)
    
    return templates.TemplateResponse("atenciones/formulario.html", {
        "request": request,
        "atencion": None,
        "action": "/atenciones/crear",
        "especialistas": especialistas,
        "persona_preseleccionada": persona
    })

@router.post("/crear")
def crear_atencion(
    request: Request,
    at_perid: int = Form(...),
    at_espid: Optional[int] = Form(None),
    at_fecha: date = Form(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        atencion_data = AtencionCreate(
            at_perid=at_perid,
            at_espid=at_espid if at_espid != 0 else None,
            at_fecha=at_fecha
        )
        
        crud_pm.create_atencion(db, atencion_data)
        return RedirectResponse(url="/atenciones/", status_code=303)
        
    except Exception as e:
        especialistas = crud_pm.get_especialistas(db)
        return templates.TemplateResponse("atenciones/formulario.html", {
            "request": request,
            "atencion": None,
            "action": "/atenciones/crear",
            "especialistas": especialistas,
            "error": str(e)
        })
