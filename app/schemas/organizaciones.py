from pydantic import BaseModel
from typing import Optional


class OrganizacionBase(BaseModel):
    org_comunitaria: str


class OrganizacionCreate(OrganizacionBase):
    pass


class OrganizacionUpdate(BaseModel):
    org_comunitaria: Optional[str] = None


class Organizacion(OrganizacionBase):
    id: int

    class Config:
        from_attributes = True
