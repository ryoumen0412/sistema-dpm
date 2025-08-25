from pydantic import BaseModel
from typing import Optional
from datetime import date


class ViajeBase(BaseModel):
    via_viaje: str
    via_destino: str
    via_fecha: date


class ViajeCreate(ViajeBase):
    pass


class ViajeUpdate(BaseModel):
    via_viaje: Optional[str] = None
    via_destino: Optional[str] = None
    via_fecha: Optional[date] = None


class Viaje(ViajeBase):
    id: int

    class Config:
        from_attributes = True
