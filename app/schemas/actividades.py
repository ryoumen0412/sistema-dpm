from pydantic import BaseModel
from typing import Optional
from datetime import date


class ActividadBase(BaseModel):
    act_actividad: str
    act_fecha: date


class ActividadCreate(ActividadBase):
    pass


class ActividadUpdate(BaseModel):
    act_actividad: Optional[str] = None
    act_fecha: Optional[date] = None


class Actividad(ActividadBase):
    id: int

    class Config:
        from_attributes = True
