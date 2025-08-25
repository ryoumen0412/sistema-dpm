from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TallerAsistenciaBase(BaseModel):
    per_id: int
    tal_id: int
    fecha_inscripcion: Optional[datetime] = None
    asistio: Optional[bool] = None


class TallerAsistenciaCreate(TallerAsistenciaBase):
    pass


class TallerAsistenciaUpdate(BaseModel):
    fecha_inscripcion: Optional[datetime] = None
    asistio: Optional[bool] = None


class TallerAsistencia(TallerAsistenciaBase):
    id: int

    class Config:
        from_attributes = True


class ViajeAsistenciaBase(BaseModel):
    per_id: int
    via_id: int
    fecha_inscripcion: Optional[datetime] = None
    asistio: Optional[bool] = None


class ViajeAsistenciaCreate(ViajeAsistenciaBase):
    pass


class ViajeAsistenciaUpdate(BaseModel):
    fecha_inscripcion: Optional[datetime] = None
    asistio: Optional[bool] = None


class ViajeAsistencia(ViajeAsistenciaBase):
    id: int

    class Config:
        from_attributes = True


class MembresiaOrgBase(BaseModel):
    per_id: int
    org_id: int
    fecha_ingreso: Optional[datetime] = None
    cargo: Optional[str] = None
    activo: Optional[bool] = True


class MembresiaOrgCreate(MembresiaOrgBase):
    pass


class MembresiaOrgUpdate(BaseModel):
    fecha_ingreso: Optional[datetime] = None
    cargo: Optional[str] = None
    activo: Optional[bool] = None


class MembresiaOrg(MembresiaOrgBase):
    id: int

    class Config:
        from_attributes = True
