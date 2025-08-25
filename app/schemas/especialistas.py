from pydantic import BaseModel
from typing import Optional


class EspecialistaBase(BaseModel):
    esp_nombre: str
    esp_apellido: str
    esp_especialidad: str
    esp_telefono: Optional[str] = None
    esp_email: Optional[str] = None
    esp_direccion: Optional[str] = None


class EspecialistaCreate(EspecialistaBase):
    pass


class EspecialistaUpdate(BaseModel):
    esp_nombre: Optional[str] = None
    esp_apellido: Optional[str] = None
    esp_especialidad: Optional[str] = None
    esp_telefono: Optional[str] = None
    esp_email: Optional[str] = None
    esp_direccion: Optional[str] = None


class Especialista(EspecialistaBase):
    esp_id: int

    class Config:
        from_attributes = True
