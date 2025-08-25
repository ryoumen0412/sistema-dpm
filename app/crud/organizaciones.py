from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from app.models.personas_mayores import OrganizacionComunitaria
from app.schemas.organizaciones import OrganizacionCreate, OrganizacionUpdate


def get_organizacion(db: Session, organizacion_id: int):
    return db.query(OrganizacionComunitaria).filter(OrganizacionComunitaria.org_id == organizacion_id).first()


def get_organizaciones(db: Session, skip: int = 0, limit: int = 100, search: str = None):
    query = db.query(OrganizacionComunitaria)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                OrganizacionComunitaria.org_nombre.ilike(search_term),
                OrganizacionComunitaria.org_descripcion.ilike(search_term)
            )
        )
    return query.offset(skip).limit(limit).all()


def create_organizacion(db: Session, organizacion: OrganizacionCreate):
    db_organizacion = OrganizacionComunitaria(**organizacion.dict())
    db.add(db_organizacion)
    db.commit()
    db.refresh(db_organizacion)
    return db_organizacion


def update_organizacion(db: Session, organizacion_id: int, organizacion_update: OrganizacionUpdate):
    db_organizacion = db.query(OrganizacionComunitaria).filter(OrganizacionComunitaria.org_id == organizacion_id).first()
    if db_organizacion:
        update_data = organizacion_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_organizacion, field, value)
        db.commit()
        db.refresh(db_organizacion)
    return db_organizacion


def delete_organizacion(db: Session, organizacion_id: int):
    db_organizacion = db.query(OrganizacionComunitaria).filter(OrganizacionComunitaria.org_id == organizacion_id).first()
    if db_organizacion:
        db.delete(db_organizacion)
        db.commit()
    return db_organizacion


def count_organizaciones(db: Session, search: str = None):
    query = db.query(OrganizacionComunitaria)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                OrganizacionComunitaria.org_nombre.ilike(search_term),
                OrganizacionComunitaria.org_descripcion.ilike(search_term)
            )
        )
    return query.count()
