#!/usr/bin/env python3
"""
Script to insert example data into the sistema-dpm database
"""

import sys
import os
sys.path.append(os.getcwd())

from datetime import datetime, date
from app.database import SessionLocal
from app.models.personas_mayores import (
    Talleres, OrganizacionComunitaria, Especialista, 
    Actividad, Viaje, PersonaMayor
)

def insert_sample_data():
    db = SessionLocal()
    
    try:
        print("🌱 Insertando datos de ejemplo...")
        
        # 1. TALLERES
        print("\n📚 Insertando talleres...")
        talleres_data = [
            {"tal_taller": "Taller de Memoria y Estimulación Cognitiva"},
            {"tal_taller": "Taller de Manualidades y Artesanía"},
            {"tal_taller": "Taller de Cocina Saludable"},
            {"tal_taller": "Taller de Yoga y Relajación"},
            {"tal_taller": "Taller de Alfabetización Digital"},
            {"tal_taller": "Taller de Jardinería Urbana"},
            {"tal_taller": "Taller de Pintura y Dibujo"},
        ]
        
        for taller_data in talleres_data:
            taller = Talleres(**taller_data)
            db.add(taller)
        
        # 2. ORGANIZACIONES COMUNITARIAS
        print("🏢 Insertando organizaciones comunitarias...")
        organizaciones_data = [
            {"org_comunitaria": "Junta de Vecinos Villa Esperanza"},
            {"org_comunitaria": "Club de Adulto Mayor Los Aromos"},
            {"org_comunitaria": "Centro Comunitario San José"},
            {"org_comunitaria": "Cooperativa de Servicios Amanecer"},
            {"org_comunitaria": "Fundación Manos Amigas"},
            {"org_comunitaria": "Agrupación Tercera Edad Activa"},
            {"org_comunitaria": "Centro de Día Los Cerezos"},
        ]
        
        for org_data in organizaciones_data:
            org = OrganizacionComunitaria(**org_data)
            db.add(org)
        
        # 3. ESPECIALISTAS - Primero necesitamos crear especialidades
        print("🩺 Insertando especialidades...")
        from app.models.personas_mayores import Especialidad
        
        especialidades_data = [
            {"espe_especialidad": "Medicina General"},
            {"espe_especialidad": "Geriatría"},
            {"espe_especialidad": "Kinesiología"},
            {"espe_especialidad": "Psicología Clínica"},
            {"espe_especialidad": "Enfermería Geriátrica"},
            {"espe_especialidad": "Nutrición y Dietética"},
            {"espe_especialidad": "Terapia Ocupacional"},
        ]
        
        for esp_data in especialidades_data:
            especialidad = Especialidad(**esp_data)
            db.add(especialidad)
        
        db.flush()  # Para obtener los IDs
        
        print("👨‍⚕️ Insertando especialistas...")
        especialistas_data = [
            {"esp_rut": "12345678-9", "esp_nombre": "Carlos", "esp_apellido": "Rodríguez", "esp_espeid": 1},
            {"esp_rut": "23456789-0", "esp_nombre": "María", "esp_apellido": "González", "esp_espeid": 2},
            {"esp_rut": "34567890-1", "esp_nombre": "Pedro", "esp_apellido": "Martínez", "esp_espeid": 3},
            {"esp_rut": "45678901-2", "esp_nombre": "Ana", "esp_apellido": "López", "esp_espeid": 4},
            {"esp_rut": "56789012-3", "esp_nombre": "Isabel", "esp_apellido": "Silva", "esp_espeid": 5},
            {"esp_rut": "67890123-4", "esp_nombre": "José", "esp_apellido": "Fernández", "esp_espeid": 6},
            {"esp_rut": "78901234-5", "esp_nombre": "Carmen", "esp_apellido": "Vega", "esp_espeid": 7},
        ]
        
        for esp_data in especialistas_data:
            esp = Especialista(**esp_data)
            db.add(esp)
        
        # 4. ACTIVIDADES
        print("🎭 Insertando actividades...")
        actividades_data = [
            {"act_actividad": "Bingo de la Tercera Edad", "act_fecha": date(2025, 9, 15)},
            {"act_actividad": "Caminata Grupal por el Parque", "act_fecha": date(2025, 9, 8)},
            {"act_actividad": "Festival de Cueca Adulto Mayor", "act_fecha": date(2025, 9, 18)},
            {"act_actividad": "Charla sobre Alimentación Saludable", "act_fecha": date(2025, 9, 12)},
            {"act_actividad": "Encuentro Social de Primavera", "act_fecha": date(2025, 9, 21)},
            {"act_actividad": "Misa y Desayuno Comunitario", "act_fecha": date(2025, 9, 10)},
            {"act_actividad": "Torneo de Dominó", "act_fecha": date(2025, 9, 25)},
            {"act_actividad": "Tarde de Karaoke", "act_fecha": date(2025, 10, 5)},
        ]
        
        for act_data in actividades_data:
            act = Actividad(**act_data)
            db.add(act)
        
        # 5. VIAJES
        print("🚌 Insertando viajes...")
        viajes_data = [
            {"via_viaje": "Paseo Termal", "via_destino": "Termas de Chillán", "via_fecha": date(2025, 10, 15)},
            {"via_viaje": "Tour Histórico", "via_destino": "Valparaíso", "via_fecha": date(2025, 11, 5)},
            {"via_viaje": "Día de Playa", "via_destino": "Viña del Mar", "via_fecha": date(2025, 10, 28)},
            {"via_viaje": "Día de Campo", "via_destino": "Cajón del Maipo", "via_fecha": date(2025, 11, 12)},
            {"via_viaje": "Visita Cultural", "via_destino": "Rancagua", "via_fecha": date(2025, 11, 20)},
            {"via_viaje": "Ruta Neruda", "via_destino": "Isla Negra", "via_fecha": date(2025, 12, 3)},
            {"via_viaje": "Paseo Cordillerano", "via_destino": "Farellones", "via_fecha": date(2025, 12, 10)},
        ]
        
        for viaje_data in viajes_data:
            viaje = Viaje(**viaje_data)
            db.add(viaje)
        
        # Commit all changes
        db.commit()
        
        # Verificar que se insertaron los datos
        talleres_count = db.query(Talleres).count()
        org_count = db.query(OrganizacionComunitaria).count()
        esp_count = db.query(Especialista).count()
        act_count = db.query(Actividad).count()
        viajes_count = db.query(Viaje).count()
        especialidades_count = db.query(Especialidad).count()
        personas_count = db.query(PersonaMayor).count()
        
        print(f"\n✅ Datos insertados exitosamente:")
        print(f"   📚 Talleres: {talleres_count}")
        print(f"   🏢 Organizaciones: {org_count}")
        print(f"   🩺 Especialidades: {especialidades_count}")
        print(f"   👨‍⚕️ Especialistas: {esp_count}")
        print(f"   🎭 Actividades: {act_count}")
        print(f"   🚌 Viajes: {viajes_count}")
        print(f"   👥 Personas Mayores: {personas_count}")
        
        print(f"\n🎉 ¡Base de datos poblada con éxito!")
        print(f"Ahora puedes navegar por las siguientes secciones:")
        print(f"   • http://localhost:8000/talleres/")
        print(f"   • http://localhost:8000/organizaciones/")
        print(f"   • http://localhost:8000/especialistas/")
        print(f"   • http://localhost:8000/actividades/")
        print(f"   • http://localhost:8000/viajes/")
        
    except Exception as e:
        print(f"❌ Error insertando datos: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    insert_sample_data()
