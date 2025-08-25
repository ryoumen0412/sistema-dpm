from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from typing import List, Optional
from app.models.personas_mayores import Especialista, Especialidad
from app.schemas.especialistas import EspecialistaCreate, EspecialistaUpdate


def get_especialista(db: Session, especialista_id: int):
    return db.query(Especialista).options(joinedload(Especialista.especialidad)).filter(Especialista.id == especialista_id).first()


def get_especialistas(db: Session, skip: int = 0, limit: int = 100, search: str = None):
    query = db.query(Especialista).options(joinedload(Especialista.especialidad))
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Especialista.esp_nombre.ilike(search_term),
                Especialista.esp_apellido.ilike(search_term),
                Especialista.esp_rut.ilike(search_term)
            )
        )
    return query.offset(skip).limit(limit).all()


def count_especialistas(db: Session, search: str = None):
    query = db.query(Especialista)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Especialista.esp_nombre.ilike(search_term),
                Especialista.esp_apellido.ilike(search_term),
                Especialista.esp_rut.ilike(search_term)
            )
        )


    return query.count()


def create_especialista(db: Session, especialista: EspecialistaCreate):
    db_especialista = Especialista(**especialista.dict())
    db.add(db_especialista)
    db.commit()
    db.refresh(db_especialista)
    return db_especialista


def update_especialista(db: Session, especialista_id: int, especialista_update: EspecialistaUpdate):
    db_especialista = db.query(Especialista).filter(Especialista.id == especialista_id).first()
    if db_especialista:
        for key, value in especialista_update.dict(exclude_unset=True).items():
            setattr(db_especialista, key, value)
        db.commit()
        db.refresh(db_especialista)
    return db_especialista


def delete_especialista(db: Session, especialista_id: int):
    db_especialista = db.query(Especialista).filter(Especialista.id == especialista_id).first()
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
