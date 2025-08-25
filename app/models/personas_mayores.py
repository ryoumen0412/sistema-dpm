from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table
from sqlalchemy.orm import relationship
from ..database import Base

class PersonaMayor(Base):
    __tablename__ = "per_mayores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    per_rut = Column(String(255), unique=True, nullable=False)
    per_nombre = Column(String(255), nullable=False)
    per_apellido = Column(String(255), nullable=False)
    per_birthdate = Column(Date, nullable=False)
    per_genid = Column(Integer, ForeignKey("gen_genero.id", ondelete="SET NULL"))
    per_nacid = Column(Integer, ForeignKey("nac_nacionalidad.id", ondelete="SET NULL"))
    per_direccion = Column(String(255))
    per_macid = Column(Integer, ForeignKey("mac_macrosector.id", ondelete="SET NULL"))
    per_uniid = Column(Integer, ForeignKey("uni_unidadvecinal.id", ondelete="SET NULL"))
    per_benefvinculos = Column(Integer, ForeignKey("vin_vinculos.id", ondelete="SET NULL"))
    per_beneflimpieza = Column(Integer, ForeignKey("lim_limpiezacalef.id", ondelete="SET NULL"))
    per_benefprogcuidadores = Column(Integer, ForeignKey("pro_progcuidadores.id", ondelete="SET NULL"))

    # Relationships
    genero = relationship("Genero", back_populates="personas")
    nacionalidad = relationship("Nacionalidad", back_populates="personas")
    macrosector = relationship("Macrosector", back_populates="personas")
    unidad_vecinal = relationship("UnidadVecinal", back_populates="personas")
    beneficio_vinculos = relationship("Vinculo", back_populates="personas")
    beneficio_limpieza = relationship("LimpiezaCalefaccion", back_populates="personas")
    beneficio_prog_cuidadores = relationship("ProgramaCuidadores", back_populates="personas")

    # Many-to-many relationships
    atenciones = relationship("Atencion", back_populates="personas")
    actividades = relationship("Actividad", secondary="actividades_asist", back_populates="personas")
    talleres = relationship("Talleres", secondary="talleres_asist", back_populates="personas")
    viajes = relationship("Viaje", secondary="viajes_asist", back_populates="personas")
    organizaciones = relationship("OrganizacionComunitaria", secondary="membresias_org", back_populates="personas")

class Macrosector(Base):
    __tablename__ = "mac_macrosector"

    id = Column(Integer, primary_key=True, autoincrement=True)
    macrosector = Column(String(255), nullable=False)

    personas = relationship("PersonaMayor", back_populates="macrosector")
    centros_comunitarios = relationship("CentroComunitario", back_populates="macrosector")

class UnidadVecinal(Base):
    __tablename__ = "uni_unidadvecinal"

    id = Column(Integer, primary_key=True, autoincrement=True)
    unidadvecinal = Column(String(255), nullable=False)

    personas = relationship("PersonaMayor", back_populates="unidad_vecinal")
    centros_comunitarios = relationship("CentroComunitario", back_populates="unidad_vecinal")

class Genero(Base):
    __tablename__ = "gen_genero"

    id = Column(Integer, primary_key=True, autoincrement=True)
    genero = Column(String(255), nullable=False)

    personas = relationship("PersonaMayor", back_populates="genero")

class Nacionalidad(Base):
    __tablename__ = "nac_nacionalidad"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nacionalidad = Column(String(255), nullable=False)

    personas = relationship("PersonaMayor", back_populates="nacionalidad")

class Talleres(Base):
    __tablename__ = "tal_talleres"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tal_taller = Column(String(255), nullable=False)

    personas = relationship("PersonaMayor", secondary="talleres_asist", back_populates="talleres")

class CentroComunitario(Base):
    __tablename__ = "cent_com"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cent_centcom = Column(String(255))
    cent_direccion = Column(String(255))
    cent_macid = Column(Integer, ForeignKey("mac_macrosector.id", ondelete="SET NULL"))
    cent_uniid = Column(Integer, ForeignKey("uni_unidadvecinal.id", ondelete="SET NULL"))

    macrosector = relationship("Macrosector", back_populates="centros_comunitarios")
    unidad_vecinal = relationship("UnidadVecinal", back_populates="centros_comunitarios")

class OrganizacionComunitaria(Base):
    __tablename__ = "org_com"

    id = Column(Integer, primary_key=True, autoincrement=True)
    org_comunitaria = Column(String(255))

    personas = relationship("PersonaMayor", secondary="membresias_org", back_populates="organizaciones")

class Especialista(Base):
    __tablename__ = "esp_especialistas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    esp_rut = Column(String(255), unique=True, nullable=False)
    esp_nombre = Column(String(255), nullable=False)
    esp_apellido = Column(String(255), nullable=False)
    esp_espeid = Column(Integer, ForeignKey("espe_especialidades.id", ondelete="SET NULL"))

    atenciones = relationship("Atencion", back_populates="especialista")
    especialidad = relationship("Especialidad", back_populates="especialistas")

class Especialidad(Base):
    __tablename__ = "espe_especialidades"

    id = Column(Integer, primary_key=True, autoincrement=True)
    espe_especialidad = Column(String(255), nullable=False)

    especialistas = relationship("Especialista", back_populates="especialidad")

class Atencion(Base):
    __tablename__ = "at_atenciones"

    id = Column(Integer, primary_key=True, autoincrement=True)
    at_perid = Column(Integer, ForeignKey("per_mayores.id", ondelete="CASCADE"))
    at_espid = Column(Integer, ForeignKey("esp_especialistas.id", ondelete="SET NULL"))
    at_fecha = Column(Date, nullable=False)

    personas = relationship("PersonaMayor", back_populates="atenciones")
    especialista = relationship("Especialista", back_populates="atenciones")

class Actividad(Base):
    __tablename__ = "act_actividades"

    id = Column(Integer, primary_key=True, autoincrement=True)
    act_actividad = Column(String(255), nullable=False)
    act_fecha = Column(Date, nullable=False)

    personas = relationship("PersonaMayor", secondary="actividades_asist", back_populates="actividades")

class Vinculo(Base):
    __tablename__ = "vin_vinculos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    vin_vinculo = Column(String(2))

    personas = relationship("PersonaMayor", back_populates="beneficio_vinculos")

class ProgramaCuidadores(Base):
    __tablename__ = "pro_progcuidadores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pro_procui = Column(String(2))

    personas = relationship("PersonaMayor", back_populates="beneficio_prog_cuidadores")

class LimpiezaCalefaccion(Base):
    __tablename__ = "lim_limpiezacalef"

    id = Column(Integer, primary_key=True, autoincrement=True)
    lim_limpieza = Column(String(2))

    personas = relationship("PersonaMayor", back_populates="beneficio_limpieza")

class Viaje(Base):
    __tablename__ = "via_viajes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    via_viaje = Column(String(255), nullable=False)
    via_destino = Column(String(255), nullable=False)
    via_fecha = Column(Date, nullable=False)

    personas = relationship("PersonaMayor", secondary="viajes_asist", back_populates="viajes")

# Many-to-many association tables
class ActividadAsistencia(Base):
    __tablename__ = "actividades_asist"
    
    actasist_perid = Column(Integer, ForeignKey("per_mayores.id", ondelete="CASCADE"), primary_key=True)
    actasist_actid = Column(Integer, ForeignKey("act_actividades.id", ondelete="CASCADE"), primary_key=True)

class TallerAsistencia(Base):
    __tablename__ = "talleres_asist"
    
    talasist_perid = Column(Integer, ForeignKey("per_mayores.id", ondelete="CASCADE"), primary_key=True)
    talasist_talid = Column(Integer, ForeignKey("tal_talleres.id", ondelete="CASCADE"), primary_key=True)

class ViajeAsistencia(Base):
    __tablename__ = "viajes_asist"
    
    viaasist_perid = Column(Integer, ForeignKey("per_mayores.id", ondelete="CASCADE"), primary_key=True)
    viaasist_viaid = Column(Integer, ForeignKey("via_viajes.id", ondelete="CASCADE"), primary_key=True)

class MembresiaOrganizacion(Base):
    __tablename__ = "membresias_org"
    
    memorg_perid = Column(Integer, ForeignKey("per_mayores.id", ondelete="CASCADE"), primary_key=True)
    memorg_orgid = Column(Integer, ForeignKey("org_com.id", ondelete="CASCADE"), primary_key=True)