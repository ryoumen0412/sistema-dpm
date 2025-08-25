from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from app.models.personas_mayores import Especialidad
from app.schemas.especialidades import EspecialidadCreate, EspecialidadUpdate


def get_especialidad(db: Session, especialidad_id: int):
    return db.query(Especialidad).filter(Especialidad.id == especialidad_id).first()


def get_especialidades(db: Session, skip: int = 0, limit: int = 100, search: str = None):
    query = db.query(Especialidad)
    if search:
        search_term = f"%{search}%"
        query = query.filter(Especialidad.espe_especialidad.ilike(search_term))
    return query.offset(skip).limit(limit).all()


def count_especialidades(db: Session, search: str = None):
    query = db.query(Especialidad)
    if search:
        search_term = f"%{search}%"
        query = query.filter(Especialidad.espe_especialidad.ilike(search_term))
    return query.count()


def create_especialidad(db: Session, especialidad: EspecialidadCreate):
    db_especialidad = Especialidad(**especialidad.dict())
    db.add(db_especialidad)
    db.commit()
    db.refresh(db_especialidad)
    return db_especialidad


def update_especialidad(db: Session, especialidad_id: int, especialidad_update: EspecialidadUpdate):
    db_especialidad = db.query(Especialidad).filter(Especialidad.id == especialidad_id).first()
    if db_especialidad:
        for key, value in especialidad_update.dict(exclude_unset=True).items():
            setattr(db_especialidad, key, value)
        db.commit()
        db.refresh(db_especialidad)
    return db_especialidad


def delete_especialidad(db: Session, especialidad_id: int):
    db_especialidad = db.query(Especialidad).filter(Especialidad.id == especialidad_id).first()
    if db_especialidad:
        db.delete(db_especialidad)
        db.commit()
    return db_especialidad
