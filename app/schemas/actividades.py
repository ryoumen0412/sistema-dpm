from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ActividadBase(BaseModel):
    act_nombre: str
    act_descripcion: Optional[str] = None
    act_fecha: Optional[datetime] = None
    act_lugar: Optional[str] = None
    act_tipo: Optional[str] = None


class ActividadCreate(ActividadBase):
    pass


class ActividadUpdate(BaseModel):
    act_nombre: Optional[str] = None
    act_descripcion: Optional[str] = None
    act_fecha: Optional[datetime] = None
    act_lugar: Optional[str] = None
    act_tipo: Optional[str] = None


class Actividad(ActividadBase):
    act_id: int

    class Config:
        from_attributes = True
