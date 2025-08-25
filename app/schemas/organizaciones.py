from pydantic import BaseModel
from typing import Optional


class OrganizacionBase(BaseModel):
    org_nombre: str
    org_descripcion: Optional[str] = None
    org_direccion: Optional[str] = None
    org_telefono: Optional[str] = None
    org_email: Optional[str] = None
    org_tipo: Optional[str] = None


class OrganizacionCreate(OrganizacionBase):
    pass


class OrganizacionUpdate(BaseModel):
    org_nombre: Optional[str] = None
    org_descripcion: Optional[str] = None
    org_direccion: Optional[str] = None
    org_telefono: Optional[str] = None
    org_email: Optional[str] = None
    org_tipo: Optional[str] = None


class Organizacion(OrganizacionBase):
    org_id: int

    class Config:
        from_attributes = True
