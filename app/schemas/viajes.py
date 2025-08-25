from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ViajeBase(BaseModel):
    via_destino: str
    via_fecha_salida: Optional[datetime] = None
    via_fecha_regreso: Optional[datetime] = None
    via_descripcion: Optional[str] = None
    via_costo: Optional[float] = None
    via_capacidad: Optional[int] = None


class ViajeCreate(ViajeBase):
    pass


class ViajeUpdate(BaseModel):
    via_destino: Optional[str] = None
    via_fecha_salida: Optional[datetime] = None
    via_fecha_regreso: Optional[datetime] = None
    via_descripcion: Optional[str] = None
    via_costo: Optional[float] = None
    via_capacidad: Optional[int] = None


class Viaje(ViajeBase):
    via_id: int

    class Config:
        from_attributes = True
