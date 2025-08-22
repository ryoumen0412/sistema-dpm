from pydantic import BaseModel, field_validator
from datetime import date
from typing import Optional, List

#Schemas para entidades de referencia

class GeneroBase(BaseModel):
    genero: str

class GeneroCreate(GeneroBase):
    pass

class Genero(GeneroBase):
    id: int

    class Config:
        from_attributes = True

class NacionalidadBase(BaseModel):
    nacionalidad: str

class NacionalidadCreate(NacionalidadBase):
    pass

class Nacionalidad(NacionalidadBase):
    id: int

    class Config:
        from_attributes = True

class MacrosectorBase(BaseModel):
    macrosector: str

class MacrosectorCreate(MacrosectorBase):
    pass

class Macrosector(MacrosectorBase):
    id: int

    class Config:
        from_attributes = True

class UnidadVecinalBase(BaseModel):
    unidadvecinal: str

class UnidadVecinalCreate(UnidadVecinalBase):
    pass

class UnidadVecinal(UnidadVecinalBase):
    id: int

    class Config:
        from_attributes = True

#Schemas para personas mayores

class PersonaMayorBase(BaseModel):
    per_rut: str
    per_nombre: str
    per_apellido: str
    per_birthdate: date
    per_direccion: Optional[str] = None
    per_genid: Optional[int] = None
    per_nacid: Optional[int] = None
    per_macid: Optional[int] = None
    per_uniid: Optional[int] = None
    per_benefvinculos: Optional[int] = None
    per_beneflimpieza: Optional[int] = None
    per_benefprogcuidadores: Optional[int] = None

    @field_validator('per_rut')
    def validar_rut(cls, v):
        if not v or len(v) < 7:
            raise ValueError('RUT debe tener al menos 7 carateres')
        return v.upper()
    
    @field_validator('per_birthdate')
    def validar_fecha_nacimiento(cls, v):
        if v > date.today():
            raise ValueError('Fecha de nacimiento no puede ser futura')
        
        edad = (date.today() - v).days // 365
        if edad < 60:
            raise ValueError('La persona debe ser mayor de 60 años')
        return v
    
class PersonaMayorCreate(PersonaMayorBase):
    pass

class PersonaMayorUpdate(BaseModel):
    per_rut: Optional[str] = None
    per_nombre: Optional[str] = None
    per_apellido: Optional[str] = None
    per_birthdate: Optional[date] = None
    per_direccion: Optional[str] = None
    per_genid: Optional[int] = None
    per_nacid: Optional[int] = None
    per_macid: Optional[int] = None
    per_uniid: Optional[int] = None
    per_benefvinculos: Optional[int] = None
    per_beneflimpieza: Optional[int] = None
    per_benefprogcuidadores: Optional[int] = None

class PersonaMayor(PersonaMayorBase):
    id: int

    class Config:
        from_attributes = True

class PersonaMayorDetallada(PersonaMayor):
    genero: Optional[Genero] = None
    nacionalidad: Optional[Nacionalidad] = None
    macrosector: Optional[Macrosector] = None
    unidadvecinal: Optional[UnidadVecinal] = None

    class Config:
        from_attributes = True

# Schemas para Especialistas
class EspecialidadBase(BaseModel):
    espe_especialidad: str

class EspecialidadCreate(EspecialidadBase):
    pass

class Especialidad(EspecialidadBase):
    id: int

    class Config:
        from_attributes = True

class EspecialistaBase(BaseModel):
    esp_rut: str
    esp_nombre: str
    esp_apellido: str
    esp_direccion: Optional[str] = None

class EspecialistaCreate(EspecialistaBase):
    pass

class EspecialistaUpdate(BaseModel):
    esp_rut: Optional[str] = None
    esp_nombre: Optional[str] = None
    esp_apellido: Optional[str] = None
    esp_direccion: Optional[str] = None

class Especialista(EspecialistaBase):
    id: int
    especialidad: Optional[Especialidad] = None

    class Config:
        from_attributes = True

#Schemas para Atenciones
class AtencionBase(BaseModel):
    at_perid: int
    at_espid: Optional[int] = None
    at_fecha: date

class AtencionCreate(AtencionBase):
    pass

class AtencionUpdate(BaseModel):
    at_perid: Optional[int] = None
    at_espid: Optional[int] = None
    at_fecha: Optional[date] = None

class Atencion(AtencionBase):
    id: int
    especialista: Optional[Especialista] = None

    class Config:
        from_attributes = True

# Schemas para Actividades
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


# Schemas para Talleres
class TallerBase(BaseModel):
    tal_taller: str

class TallerCreate(TallerBase):
    pass

class Taller(TallerBase):
    id: int

    class Config:
        from_attributes = True

# Schemas para Viajes
class ViajeBase(BaseModel):
    via_viaje: Optional[str] = None
    via_fecha: Optional[date] = None
    via_destino: Optional[str] = None

class ViajeCreate(ViajeBase):
    pass

class ViajeUpdate(ViajeBase):
    via_viaje: Optional[str] = None
    via_fecha: Optional[date] = None
    via_destino: Optional[str] = None

class Viaje(ViajeBase):
    id: int

    class Config:
        from_attributes = True

# Schema para reportes y consultas complejas
class ResumenPersona(BaseModel):
    id: int
    nombre_completo: str
    rut: str
    edad: int
    genero: Optional[str] = None
    macrosector: Optional[str] = None
    total_atenciones: int
    ultima_atencion: Optional[date] = None

class EstadisticasGenerales(BaseModel):
    total_personas: int
    total_atenciones: int
    total_actividades: int
    total_viajes: int
    personas_por_genero: dict
    personas_por_macrosector: dict

