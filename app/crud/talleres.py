from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from app.models.personas_mayores import Talleres
from app.schemas.talleres import TallerCreate, TallerUpdate


def get_taller(db: Session, taller_id: int):
    return db.query(Talleres).filter(Talleres.tal_id == taller_id).first()


def get_talleres(db: Session, skip: int = 0, limit: int = 100, search: str = None):
    query = db.query(Talleres)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Talleres.tal_nombre.ilike(search_term),
                Talleres.tal_descripcion.ilike(search_term)
            )
        )
    return query.offset(skip).limit(limit).all()


def create_taller(db: Session, taller: TallerCreate):
    db_taller = Talleres(**taller.dict())
    db.add(db_taller)
    db.commit()
    db.refresh(db_taller)
    return db_taller


def update_taller(db: Session, taller_id: int, taller_update: TallerUpdate):
    db_taller = db.query(Talleres).filter(Talleres.tal_id == taller_id).first()
    if db_taller:
        update_data = taller_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_taller, field, value)
        db.commit()
        db.refresh(db_taller)
    return db_taller


def delete_taller(db: Session, taller_id: int):
    db_taller = db.query(Talleres).filter(Talleres.tal_id == taller_id).first()
    if db_taller:
        db.delete(db_taller)
        db.commit()
    return db_taller


def count_talleres(db: Session, search: str = None):
    query = db.query(Talleres)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Talleres.tal_nombre.ilike(search_term),
                Talleres.tal_descripcion.ilike(search_term)
            )
        )
    return query.count()
