from pydantic import BaseModel
from typing import Optional


class EspecialistaBase(BaseModel):
    esp_rut: str
    esp_nombre: str
    esp_apellido: str
    esp_espeid: Optional[int] = None


class EspecialistaCreate(EspecialistaBase):
    pass


class EspecialistaUpdate(BaseModel):
    esp_rut: Optional[str] = None
    esp_nombre: Optional[str] = None
    esp_apellido: Optional[str] = None
    esp_espeid: Optional[int] = None


class Especialista(EspecialistaBase):
    id: int
    especialidad: Optional[dict] = None

    class Config:
        from_attributes = True


class EspecialidadBase(BaseModel):
    espe_especialidad: str


class EspecialidadCreate(EspecialidadBase):
    pass


class Especialidad(EspecialidadBase):
    id: int

    class Config:
        from_attributes = True
