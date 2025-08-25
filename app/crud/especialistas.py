from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from app.models.personas_mayores import Especialista
from app.schemas.especialistas import EspecialistaCreate, EspecialistaUpdate


def get_especialista(db: Session, especialista_id: int):
    return db.query(Especialista).filter(Especialista.esp_id == especialista_id).first()


def get_especialistas(db: Session, skip: int = 0, limit: int = 100, search: str = None):
    query = db.query(Especialista)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Especialista.esp_nombre.ilike(search_term),
                Especialista.esp_apellido.ilike(search_term),
                Especialista.esp_especialidad.ilike(search_term)
            )
        )
    return query.offset(skip).limit(limit).all()


def create_especialista(db: Session, especialista: EspecialistaCreate):
    db_especialista = Especialista(**especialista.dict())
    db.add(db_especialista)
    db.commit()
    db.refresh(db_especialista)
    return db_especialista


def update_especialista(db: Session, especialista_id: int, especialista_update: EspecialistaUpdate):
    db_especialista = db.query(Especialista).filter(Especialista.esp_id == especialista_id).first()
    if db_especialista:
        update_data = especialista_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_especialista, field, value)
        db.commit()
        db.refresh(db_especialista)
    return db_especialista


def delete_especialista(db: Session, especialista_id: int):
    db_especialista = db.query(Especialista).filter(Especialista.esp_id == especialista_id).first()
    if db_especialista:
        db.delete(db_especialista)
        db.commit()
    return db_especialista


def count_especialistas(db: Session, search: str = None):
    query = db.query(Especialista)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Especialista.esp_nombre.ilike(search_term),
                Especialista.esp_apellido.ilike(search_term),
                Especialista.esp_especialidad.ilike(search_term)
            )
        )
    return query.count()
