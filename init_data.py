#!/usr/bin/env python3
"""
Script to initialize the database with sample data
"""
import sys
sys.path.append('.')

from app.database import SessionLocal, engine
from app.models.personas_mayores import *
from app.models.user import User
from passlib.context import CryptContext
from datetime import date

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def init_reference_data(db):
    """Initialize reference tables with basic data"""
    
    # Géneros
    generos = [
        Genero(genero="Masculino"),
        Genero(genero="Femenino"),
        Genero(genero="Otro")
    ]
    
    # Nacionalidades
    nacionalidades = [
        Nacionalidad(nacionalidad="Chilena"),
        Nacionalidad(nacionalidad="Peruana"),
        Nacionalidad(nacionalidad="Boliviana"),
        Nacionalidad(nacionalidad="Argentina"),
        Nacionalidad(nacionalidad="Otro")
    ]
    
    # Macrosectores
    macrosectores = [
        Macrosector(macrosector="Norte"),
        Macrosector(macrosector="Sur"),
        Macrosector(macrosector="Centro"),
        Macrosector(macrosector="Oriente"),
        Macrosector(macrosector="Poniente")
    ]
    
    # Unidades vecinales
    unidades_vecinales = [
        UnidadVecinal(unidadvecinal="UV-01 Centro"),
        UnidadVecinal(unidadvecinal="UV-02 Las Flores"),
        UnidadVecinal(unidadvecinal="UV-03 Villa España"),
        UnidadVecinal(unidadvecinal="UV-04 El Bosque"),
        UnidadVecinal(unidadvecinal="UV-05 San Pedro")
    ]
    
    # Especialidades
    especialidades = [
        Especialidad(espe_especialidad="Medicina General"),
        Especialidad(espe_especialidad="Kinesiología"),
        Especialidad(espe_especialidad="Trabajo Social"),
        Especialidad(espe_especialidad="Psicología"),
        Especialidad(espe_especialidad="Enfermería")
    ]
    
    # Vínculos
    vinculos = [
        Vinculo(vin_vinculo="SI"),
        Vinculo(vin_vinculo="NO")
    ]
    
    # Programa Cuidadores
    prog_cuidadores = [
        ProgramaCuidadores(pro_procui="SI"),
        ProgramaCuidadores(pro_procui="NO")
    ]
    
    # Limpieza y Calefacción
    limpieza_calef = [
        LimpiezaCalefaccion(lim_limpieza="SI"),
        LimpiezaCalefaccion(lim_limpieza="NO")
    ]
    
    # Talleres
    talleres = [
        Talleres(tal_taller="Yoga para Adultos Mayores"),
        Talleres(tal_taller="Manualidades"),
        Talleres(tal_taller="Computación Básica"),
        Talleres(tal_taller="Baile Entretenido"),
        Talleres(tal_taller="Cocina Saludable")
    ]
    
    # Add all reference data
    for item_list in [generos, nacionalidades, macrosectores, unidades_vecinales, 
                      especialidades, vinculos, prog_cuidadores, limpieza_calef, talleres]:
        for item in item_list:
            db.add(item)
    
    db.commit()
    print("✓ Reference data initialized")

def create_admin_user(db):
    """Create an admin user"""
    admin_user = User(
        usr="admin",
        psswrd=pwd_context.hash("admin123")
    )
    db.add(admin_user)
    db.commit()
    print("✓ Admin user created (username: admin, password: admin123)")

def create_sample_data(db):
    """Create some sample personas mayores"""
    
    sample_personas = [
        PersonaMayor(
            per_rut="12345678-9",
            per_nombre="María",
            per_apellido="González",
            per_birthdate=date(1955, 3, 15),
            per_direccion="Av. Principal 123",
            per_genid=2,  # Femenino
            per_nacid=1,  # Chilena
            per_macid=1,  # Norte
            per_uniid=1,  # UV-01 Centro
            per_benefvinculos=1,  # SI
            per_beneflimpieza=1,  # SI
            per_benefprogcuidadores=2  # NO
        ),
        PersonaMayor(
            per_rut="98765432-1",
            per_nombre="Carlos",
            per_apellido="Rodríguez",
            per_birthdate=date(1960, 8, 22),
            per_direccion="Calle Los Robles 456",
            per_genid=1,  # Masculino
            per_nacid=1,  # Chilena
            per_macid=2,  # Sur
            per_uniid=2,  # UV-02 Las Flores
            per_benefvinculos=2,  # NO
            per_beneflimpieza=1,  # SI
            per_benefprogcuidadores=1  # SI
        ),
        PersonaMayor(
            per_rut="11223344-5",
            per_nombre="Ana",
            per_apellido="Morales",
            per_birthdate=date(1952, 12, 5),
            per_direccion="Pasaje Las Violetas 789",
            per_genid=2,  # Femenino
            per_nacid=1,  # Chilena
            per_macid=3,  # Centro
            per_uniid=3,  # UV-03 Villa España
            per_benefvinculos=1,  # SI
            per_beneflimpieza=2,  # NO
            per_benefprogcuidadores=1  # SI
        )
    ]
    
    # Add sample personas
    for persona in sample_personas:
        db.add(persona)
    
    db.commit()
    print("✓ Sample personas mayores created")

def main():
    """Initialize the database with sample data"""
    db = SessionLocal()
    
    try:
        print("🔄 Initializing database with sample data...")
        
        # Check if data already exists
        if db.query(User).count() > 0:
            print("⚠️  Database already has data. Skipping initialization.")
            return
        
        init_reference_data(db)
        create_admin_user(db)
        create_sample_data(db)
        
        print("✅ Database initialization completed successfully!")
        print("\n🔑 You can now log in with:")
        print("   Username: admin")
        print("   Password: admin123")
        print("\n🌐 Access the application at: http://localhost:8000")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
