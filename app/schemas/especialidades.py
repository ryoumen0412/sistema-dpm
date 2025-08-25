from pydantic import BaseModel
from typing import Optional

class EspecialidadBase(BaseModel):
    espe_especialidad: str

class EspecialidadCreate(EspecialidadBase):
    pass

class EspecialidadUpdate(EspecialidadBase):
    pass

class Especialidad(EspecialidadBase):
    id: int

    class Config:
        from_attributes = True
