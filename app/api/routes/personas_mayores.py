from fastapi import APIRouter, Depends, Request, Form, HTTPException, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import date, datetime
from typing import Optional
from ...database import get_db
from ...crud import personas_mayores as crud_pm
from ...schemas.personas_mayores import PersonaMayorCreate, PersonaMayorUpdate
from .auth import get_current_user

router = APIRouter(prefix="/personas", tags=["personas_mayores"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
def listar_personas(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, le=100),
    search: Optional[str] = Query(None),
    macrosector_id: Optional[int] = Query(None),
    genero_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    personas = crud_pm.get_personas_mayores(
        db, skip=skip, limit=limit, 
        search=search, macrosector_id=macrosector_id, genero_id=genero_id
    )
    
    # Para filtros
    generos = crud_pm.get_generos(db)
    macrosectores = crud_pm.get_macrosectores(db)
    
    return templates.TemplateResponse("personas/lista.html", {
        "request": request,
        "personas": personas,
        "generos": generos,
        "macrosectores": macrosectores,
        "search": search,
        "macrosector_id": macrosector_id,
        "genero_id": genero_id,
        "skip": skip,
        "limit": limit
    })

@router.get("/nueva", response_class=HTMLResponse)
def nueva_persona_form(
    request: Request,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    generos = crud_pm.get_generos(db)
    nacionalidades = crud_pm.get_nacionalidades(db)
    macrosectores = crud_pm.get_macrosectores(db)
    unidades_vecinales = crud_pm.get_unidades_vecinales(db)
    
    return templates.TemplateResponse("personas/formulario.html", {
        "request": request,
        "persona": None,
        "action": "/personas/crear",
        "generos": generos,
        "nacionalidades": nacionalidades,
        "macrosectores": macrosectores,
        "unidades_vecinales": unidades_vecinales
    })

@router.post("/crear")
def crear_persona(
    request: Request,
    per_rut: str = Form(...),
    per_nombre: str = Form(...),
    per_apellido: str = Form(...),
    per_birthdate: date = Form(...),
    per_direccion: Optional[str] = Form(None),
    per_genid: Optional[int] = Form(None),
    per_nacid: Optional[int] = Form(None),
    per_macid: Optional[int] = Form(None),
    per_uniid: Optional[int] = Form(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        # Verificar si el RUT ya existe
        persona_existente = crud_pm.get_persona_mayor_by_rut(db, per_rut)
        if persona_existente:
            raise ValueError("Ya existe una persona con este RUT")
        
        persona_data = PersonaMayorCreate(
            per_rut=per_rut,
            per_nombre=per_nombre,
            per_apellido=per_apellido,
            per_birthdate=per_birthdate,
            per_direccion=per_direccion,
            per_genid=per_genid if per_genid != 0 else None,
            per_nacid=per_nacid if per_nacid != 0 else None,
            per_macid=per_macid if per_macid != 0 else None,
            per_uniid=per_uniid if per_uniid != 0 else None
        )
        
        crud_pm.create_persona_mayor(db, persona_data)
        return RedirectResponse(url="/personas/", status_code=303)
        
    except Exception as e:
        generos = crud_pm.get_generos(db)
        nacionalidades = crud_pm.get_nacionalidades(db)
        macrosectores = crud_pm.get_macrosectores(db)
        unidades_vecinales = crud_pm.get_unidades_vecinales(db)
        
        return templates.TemplateResponse("personas/formulario.html", {
            "request": request,
            "persona": None,
            "action": "/personas/crear",
            "generos": generos,
            "nacionalidades": nacionalidades,
            "macrosectores": macrosectores,
            "unidades_vecinales": unidades_vecinales,
            "error": str(e)
        })

@router.get("/{persona_id}", response_class=HTMLResponse)
def detalle_persona(
    persona_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    persona = crud_pm.get_persona_mayor(db, persona_id)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    
    # Obtener últimas atenciones
    atenciones = crud_pm.get_atenciones_persona(db, persona_id, limit=5)
    
    # Calcular edad
    edad = crud_pm.calcular_edad(persona.per_birthdate)
    
    return templates.TemplateResponse("personas/detalle.html", {
        "request": request,
        "persona": persona,
        "atenciones": atenciones,
        "edad": edad
    })

@router.get("/{persona_id}/editar", response_class=HTMLResponse)
def editar_persona_form(
    persona_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    persona = crud_pm.get_persona_mayor(db, persona_id)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    
    generos = crud_pm.get_generos(db)
    nacionalidades = crud_pm.get_nacionalidades(db)
    macrosectores = crud_pm.get_macrosectores(db)
    unidades_vecinales = crud_pm.get_unidades_vecinales(db)
    
    return templates.TemplateResponse("personas/formulario.html", {
        "request": request,
        "persona": persona,
        "action": f"/personas/{persona_id}/actualizar",
        "generos": generos,
        "nacionalidades": nacionalidades,
        "macrosectores": macrosectores,
        "unidades_vecinales": unidades_vecinales
    })

@router.post("/{persona_id}/actualizar")
def actualizar_persona(
    persona_id: int,
    request: Request,
    per_rut: str = Form(...),
    per_nombre: str = Form(...),
    per_apellido: str = Form(...),
    per_birthdate: date = Form(...),
    per_direccion: Optional[str] = Form(None),
    per_genid: Optional[int] = Form(None),
    per_nacid: Optional[int] = Form(None),
    per_macid: Optional[int] = Form(None),
    per_uniid: Optional[int] = Form(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        persona_data = PersonaMayorUpdate(
            per_rut=per_rut,
            per_nombre=per_nombre,
            per_apellido=per_apellido,
            per_birthdate=per_birthdate,
            per_direccion=per_direccion,
            per_genid=per_genid if per_genid != 0 else None,
            per_nacid=per_nacid if per_nacid != 0 else None,
            per_macid=per_macid if per_macid != 0 else None,
            per_uniid=per_uniid if per_uniid != 0 else None
        )
        
        crud_pm.update_persona_mayor(db, persona_id, persona_data)
        return RedirectResponse(url=f"/personas/{persona_id}", status_code=303)
        
    except Exception as e:
        persona = crud_pm.get_persona_mayor(db, persona_id)
        generos = crud_pm.get_generos(db)
        nacionalidades = crud_pm.get_nacionalidades(db)
        macrosectores = crud_pm.get_macrosectores(db)
        unidades_vecinales = crud_pm.get_unidades_vecinales(db)
        
        return templates.TemplateResponse("personas/formulario.html", {
            "request": request,
            "persona": persona,
            "action": f"/personas/{persona_id}/actualizar",
            "generos": generos,
            "nacionalidades": nacionalidades,
            "macrosectores": macrosectores,
            "unidades_vecinales": unidades_vecinales,
            "error": str(e)
        })