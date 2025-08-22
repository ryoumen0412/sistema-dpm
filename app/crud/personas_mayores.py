from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc
from datetime import date, datetime
from typing import List, Optional
from ..models.personas_mayores import (
    PersonaMayor, Macrosector, UnidadVecinal, Genero,
    Nacionalidad, Especialista, Especialidad, Atencion,
    Actividad, Viaje, Talleres)
from ..schemas.personas_mayores import (
    PersonaMayorCreate, PersonaMayorUpdate, EspecialistaCreate,
    EspecialistaUpdate, AtencionCreate, ActividadCreate, ViajeCreate)

# CRUD para Personas Mayores
def get_persona_mayor(db: Session, persona_id: int):
    return db.query(PersonaMayor).options(
        joinedload(PersonaMayor.genero),
        joinedload(PersonaMayor.nacionalidad),
        joinedload(PersonaMayor.macrosector),
        joinedload(PersonaMayor.unidadvecinal)
    ).filter(PersonaMayor.id == persona_id).first()

def get_persona_mayor_by_rut(db: Session, per_rut: str):
    return db.query(PersonaMayor).filter(PersonaMayor.per_rut == per_rut).first()

def get_personas_mayores(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        macrosector_id: Optional[int] = None,
        genero_id: Optional[int] = None
):
    query = db.query(PersonaMayor).options(
        joinedload(PersonaMayor.genero),
        joinedload(PersonaMayor.nacionalidad),
        joinedload(PersonaMayor.macrosector),
        joinedload(PersonaMayor.unidadvecinal)
    )

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (PersonaMayor.per_nombre.ilike(search)) |
            (PersonaMayor.per_apellido.ilike(search)) |
            (PersonaMayor.per_rut.ilike(search))
        )
    if macrosector_id:
        query = query.filter(PersonaMayor.per_macid == macrosector_id)
    if genero_id:
        query = query.filter(PersonaMayor.per_genid == genero_id)

    return query.offset(skip).limit(limit).all()

def create_persona_mayor(db: Session, persona: PersonaMayorCreate):
    db_persona = PersonaMayor(**persona.model_dump())
    db.add(db_persona)
    db.commit()
    db.refresh(db_persona)
    return db_persona

def update_persona_mayor(db: Session, persona_id: int, persona: PersonaMayorUpdate):
    db_persona = get_persona_mayor(db, persona_id)
    if db_persona:
        for field, value in persona.model_dump(exclude_unset=True).items():
            setattr(db_persona, field, value)
        db.commit()
        db.refresh(db_persona)
    return db_persona

def delete_persona_mayor(db: Session, persona_id: int):
    db_persona = get_persona_mayor(db, persona_id)
    if db_persona:
        db.delete(db_persona)
        db.commit()
    return db_persona

# Función para calcular edad
def calcular_edad(fecha_nacimiento: date) -> int:
    today = date.today()
    edad = today.year - fecha_nacimiento.year - ((today.month, today.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    return edad

# CRUD para entidades de referencia
def get_generos(db: Session):
    return db.query(Genero).all()

def get_nacionalidades(db: Session):
    return db.query(Nacionalidad).all()

def get_macrosectores(db: Session):
    return db.query(Macrosector).all()

def get_unidades_vecinales(db: Session):
    return db.query(UnidadVecinal).all()

# CRUD para Especialistas
def get_especialista(db: Session, especialista_id: int):
    return db.query(Especialista).options(
        joinedload(Especialista.especialidad)
    ).filter(Especialista.id == especialista_id).first()

def get_especialistas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Especialista).options(
        joinedload(Especialista.especialidad)
    ).offset(skip).limit(limit).all()

def create_especialista(db: Session, especialista: EspecialistaCreate):
    db_especialista = Especialista(**especialista.model_dump())
    db.add(db_especialista)
    db.commit()
    db.refresh(db_especialista)
    return db_especialista

def get_especialidades(db: Session):
    return db.query(Especialidad).all()

# CRUD para Atenciones
def get_atencion(db: Session, atencion_id: int):
    return db.query(Atencion).options(
        joinedload(Atencion.persona),
        joinedload(Atencion.especialista)
    ).filter(Atencion.id == atencion_id).first()

def get_atenciones(db: Session, skip: int = 0, limit: int = 100, persona_id: Optional[int] = None, especialista_id: Optional[int] = None, fecha_desde: Optional[date] = None, fecha_hasta: Optional[date] =None):

    query = db.query(Atencion).options(joinedload(Atencion.persona), joinedload(Atencion.especialista))
    if persona_id:
        query = query.filter(Atencion.at_perid == persona_id)

    if especialista_id:
        query = query.filter(Atencion.at_espid == especialista_id)

    if fecha_desde:
        query = query.filter(Atencion.at_fecha >= fecha_desde)

    if fecha_hasta:
        query = query.filter(Atencion.at_fecha <= fecha_hasta)
    
    return query.order_by(desc(Atencion.at_fecha)).offset(skip).limit(limit).all()

def create_atencion(db: Session, atencion: AtencionCreate):
    db_atencion = Atencion(**atencion.model_dump())
    db.add(db_atencion)
    db.commit()
    db.refresh(db_atencion)
    return db_atencion

def get_atenciones_persona(db: Session, persona_id: int, limit: int = 100):
    return db.query(Atencion).filter(Atencion.at_perid == persona_id).order_by(desc(Atencion.at_fecha)).limit(limit).all()

# CRUD para Actividades

def get_actividades(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Actividad).order_by(desc(Actividad.act_fecha)).offset(skip).limit(limit).all()

def create_actividad(db: Session, actividad: ActividadCreate):
    db_actividad = Actividad(**actividad.model_dump())
    db.add(db_actividad)
    db.commit()
    db.refresh(db_actividad)
    return db_actividad

def get_talleres(db: Session):
    return db.query(Talleres).all()

# CRUD para Viajes
def get_viajes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Viaje).order_by(desc(Viaje.via_fecha)).offset(skip).limit(limit).all()

def create_viaje(db: Session, viaje: ViajeCreate):
    db_viaje = Viaje(**viaje.model_dump())
    db.add(db_viaje)
    db.commit()
    db.refresh(db_viaje)
    return db_viaje

# Funciones de Estadísticas y Reportes
def get_estadistics_generales(db: Session):
    total_personas = db.query(func.count(PersonaMayor).count())
    total_atenciones = db.query(Atencion).count()
    total_actividades = db.query(Actividad).count()
    total_viajes = db.query(Viaje).count()

    # Personas por género
    personas_por_genero = db.query(
        Genero.genero,
        func.count(PersonaMayor.id).label('count')).outerjoin(PersonaMayor).group_by(Genero.genero).all()
    
    # Personas por macrosector
    personas_por_macrosector = db.query(
        Macrosector.macrosector,
        func.count(PersonaMayor.id).label('count')).outerjoin(PersonaMayor).group_by(Macrosector.macrosector).all()
    
    return {
        "total_personas": total_personas,
        "total_atenciones": total_atenciones,
        "total_actividades": total_actividades,
        "total_viajes": total_viajes,
        "personas_por_genero": {item[0]: item[1] for item in personas_por_genero},
        "personas_por_macrosector": {item[0]: item[1] for item in personas_por_macrosector}
    }

def get_personas_con_resumen(db: Session, skip: int = 0, limit: int = 100):
    '''Obtiene personas con resumen de sus atenciones.'''
    query = db.query(
        PersonaMayor.id,
        PersonaMayor.per_nombre,
        PersonaMayor.per_apellido,
        PersonaMayor.per_rut,
        PersonaMayor.per_birthdate,
        Genero.genero,
        Macrosector.macrosector,
        func.count(Atencion.id).label('total_atenciones'),
        func.max(Atencion.at_fecha).label('ultima_atencion')
    ).outerjoin(Genero).outerjoin(Macrosector).outerjoin(Atencion).group_by(
        PersonaMayor.id,
        PersonaMayor.per_nombre,
        PersonaMayor.per_apellido,
        PersonaMayor.per_rut,
        PersonaMayor.per_birthdate,
        Genero.genero,
        Macrosector.macrosector
    ).offset(skip).limit(limit).all()

    resultado = []
    for item in query:
        edad = calcular_edad(item.per_birthdate)
        resultado.append({
            'id': item.id,
            'nombre_completo': f"{item.per_nombre} {item.per_apellido}",
            'rut': item.per_rut,
            'edad': edad,
            'genero': item.genero,
            'macrosector': item.macrosector,
            'total_atenciones': item.total_atenciones or 0,
            'ultima_atencion': item.ultima_atencion
        })
    
    return resultado

def buscar_personas_avanzado(
    db: Session,
    nombre: Optional[str] = None,
    apellido: Optional[str] = None,
    rut: Optional[str] = None,
    edad_min: Optional[int] = None,
    edad_max: Optional[int] = None,
    macrosector_id: Optional[int] = None,
    genero_id: Optional[int] = None,
    con_atenciones: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100
):
    """Búsqueda avanzada de personas mayores"""
    query = db.query(PersonaMayor).options(
        joinedload(PersonaMayor.genero),
        joinedload(PersonaMayor.macrosector)
    )
    
    if nombre:
        query = query.filter(PersonaMayor.per_nombre.ilike(f"%{nombre}%"))
    
    if apellido:
        query = query.filter(PersonaMayor.per_apellido.ilike(f"%{apellido}%"))
        
    if rut:
        query = query.filter(PersonaMayor.per_rut.ilike(f"%{rut}%"))
        
    if macrosector_id:
        query = query.filter(PersonaMayor.per_macid == macrosector_id)
        
    if genero_id:
        query = query.filter(PersonaMayor.per_genid == genero_id)
    
    # Filtro por edad (requiere cálculo en Python para ser más preciso)
    personas = query.offset(skip).limit(limit).all()
    
    if edad_min is not None or edad_max is not None or con_atenciones is not None:
        resultado = []
        for persona in personas:
            edad = calcular_edad(persona.per_birthdate)
            
            # Filtro por edad
            if edad_min is not None and edad < edad_min:
                continue
            if edad_max is not None and edad > edad_max:
                continue
                
            # Filtro por atenciones
            if con_atenciones is not None:
                tiene_atenciones = db.query(Atencion).filter(Atencion.at_perid == persona.id).first() is not None
                if con_atenciones and not tiene_atenciones:
                    continue
                if not con_atenciones and tiene_atenciones:
                    continue
            
            resultado.append(persona)
        
        return resultado
    
    return personas

def get_reporte_atenciones_mensual(db: Session, año: int, mes: int):
    """Reporte de atenciones por mes"""
    from datetime import date
    fecha_inicio = date(año, mes, 1)
    if mes == 12:
        fecha_fin = date(año + 1, 1, 1)
    else:
        fecha_fin = date(año, mes + 1, 1)
    
    atenciones = db.query(Atencion).options(
        joinedload(Atencion.persona),
        joinedload(Atencion.especialista)
    ).filter(
        Atencion.at_fecha >= fecha_inicio,
        Atencion.at_fecha < fecha_fin
    ).order_by(Atencion.at_fecha).all()
    
    return atenciones

def get_personas_sin_atencion_reciente(db: Session, dias: int = 90):
    """Obtiene personas que no han tenido atención en X días"""
    from datetime import date, timedelta
    fecha_limite = date.today() - timedelta(days=dias)
    
    # Subquery para obtener la última atención de cada persona
    subquery = db.query(
        Atencion.at_perid,
        func.max(Atencion.at_fecha).label('ultima_atencion')
    ).group_by(Atencion.at_perid).subquery()
    
    # Personas con última atención anterior a fecha_limite o sin atenciones
    personas = db.query(PersonaMayor).options(
        joinedload(PersonaMayor.genero),
        joinedload(PersonaMayor.macrosector)
    ).outerjoin(
        subquery, PersonaMayor.id == subquery.c.at_perid
    ).filter(
        (subquery.c.ultima_atencion < fecha_limite) | 
        (subquery.c.ultima_atencion == None)
    ).all()
    
    return personas