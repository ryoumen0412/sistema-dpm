from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from app.models.personas_mayores import Viaje
from app.schemas.viajes import ViajeCreate, ViajeUpdate


def get_viaje(db: Session, viaje_id: int):
    return db.query(Viaje).filter(Viaje.id == viaje_id).first()


def get_viajes(db: Session, skip: int = 0, limit: int = 100, search: str = None):
    query = db.query(Viaje)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Viaje.via_destino.ilike(search_term),
                Viaje.via_descripcion.ilike(search_term)
            )
        )
    return query.offset(skip).limit(limit).all()


def create_viaje(db: Session, viaje: ViajeCreate):
    db_viaje = Viaje(**viaje.dict())
    db.add(db_viaje)
    db.commit()
    db.refresh(db_viaje)
    return db_viaje


def update_viaje(db: Session, viaje_id: int, viaje_update: ViajeUpdate):
    db_viaje = db.query(Viaje).filter(Viaje.id == viaje_id).first()
    if db_viaje:
        update_data = viaje_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_viaje, field, value)
        db.commit()
        db.refresh(db_viaje)
    return db_viaje


def delete_viaje(db: Session, viaje_id: int):
    db_viaje = db.query(Viaje).filter(Viaje.id == viaje_id).first()
    if db_viaje:
        db.delete(db_viaje)
        db.commit()
    return db_viaje


def count_viajes(db: Session, search: str = None):
    query = db.query(Viaje)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Viaje.via_destino.ilike(search_term),
                Viaje.via_descripcion.ilike(search_term)
            )
        )
    return query.count()
