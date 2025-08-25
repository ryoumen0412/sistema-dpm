from pydantic import BaseModel
from typing import Optional


class TallerBase(BaseModel):
    tal_taller: str


class TallerCreate(TallerBase):
    pass


class TallerUpdate(BaseModel):
    tal_taller: Optional[str] = None


class Taller(TallerBase):
    id: int

    class Config:
        from_attributes = True
