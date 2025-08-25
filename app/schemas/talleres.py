from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TallerBase(BaseModel):
    tal_nombre: str
    tal_descripcion: Optional[str] = None
    tal_fecha_inicio: Optional[datetime] = None
    tal_fecha_fin: Optional[datetime] = None
    tal_lugar: Optional[str] = None
    tal_capacidad: Optional[int] = None


class TallerCreate(TallerBase):
    pass


class TallerUpdate(BaseModel):
    tal_nombre: Optional[str] = None
    tal_descripcion: Optional[str] = None
    tal_fecha_inicio: Optional[datetime] = None
    tal_fecha_fin: Optional[datetime] = None
    tal_lugar: Optional[str] = None
    tal_capacidad: Optional[int] = None


class Taller(TallerBase):
    tal_id: int

    class Config:
        from_attributes = True
