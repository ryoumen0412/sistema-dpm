from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from app.models.personas_mayores import Actividad
from app.schemas.actividades import ActividadCreate, ActividadUpdate


def get_actividad(db: Session, actividad_id: int):
    return db.query(Actividad).filter(Actividad.id == actividad_id).first()


def get_actividades(db: Session, skip: int = 0, limit: int = 100, search: str = None):
    query = db.query(Actividad)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            Actividad.act_actividad.ilike(search_term)
        )
    return query.offset(skip).limit(limit).all()


def create_actividad(db: Session, actividad: ActividadCreate):
    db_actividad = Actividad(**actividad.dict())
    db.add(db_actividad)
    db.commit()
    db.refresh(db_actividad)
    return db_actividad


def update_actividad(db: Session, actividad_id: int, actividad_update: ActividadUpdate):
    db_actividad = db.query(Actividad).filter(Actividad.id == actividad_id).first()
    if db_actividad:
        update_data = actividad_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_actividad, field, value)
        db.commit()
        db.refresh(db_actividad)
    return db_actividad


def delete_actividad(db: Session, actividad_id: int):
    db_actividad = db.query(Actividad).filter(Actividad.id == actividad_id).first()
    if db_actividad:
        db.delete(db_actividad)
        db.commit()
    return db_actividad


def count_actividades(db: Session, search: str = None):
    query = db.query(Actividad)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            Actividad.act_actividad.ilike(search_term)
        )
    return query.count()
