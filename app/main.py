from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .api.routes import auth, personas_mayores, atenciones, reportes, talleres, organizaciones, especialistas, especialidades, actividades, viajes
from .api.routes.auth import get_current_user
from .crud import personas_mayores as crud_pm
from .models.personas_mayores import PersonaMayor, Atencion
from .database import get_db
from sqlalchemy.orm import Session

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema Municipal - Dirección de Personas Mayores",
    version="1.0.0",
    description="Sistema de gestión para la Dirección de Personas Mayores"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Archivos estáticos y templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Agregar filtro personalizado para calcular edad
from datetime import date

def age_filter(birthdate):
    """Calcula la edad basada en la fecha de nacimiento"""
    if not birthdate:
        return 0
    today = date.today()
    return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

templates.env.filters['age'] = age_filter

# Incluir rutas
app.include_router(auth.router, prefix="/auth")
app.include_router(personas_mayores.router)
app.include_router(atenciones.router)
app.include_router(reportes.router)
app.include_router(talleres.router, prefix="/talleres")
app.include_router(organizaciones.router, prefix="/organizaciones")
app.include_router(especialistas.router, prefix="/especialistas")
app.include_router(especialidades.router, prefix="/especialidades")
app.include_router(actividades.router, prefix="/actividades")
app.include_router(viajes.router, prefix="/viajes")

@app.get("/", response_class=HTMLResponse)
def dashboard(
    request: Request,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Estadísticas básicas para el dashboard
    try:
        total_personas = db.query(PersonaMayor).count()
        total_atenciones = db.query(Atencion).count()
        personas_recientes = crud_pm.get_personas_mayores(db, limit=5)
        
        estadisticas = {
            "total_personas": total_personas,
            "total_atenciones": total_atenciones,
            "total_actividades": 0,
            "total_viajes": 0,
            "personas_por_genero": {},
            "personas_por_macrosector": {}
        }
        
        atenciones_recientes = []
        personas_sin_atencion_count = 0
        
    except Exception as e:
        # Si hay error, usar datos básicos
        estadisticas = {
            "total_personas": 0,
            "total_atenciones": 0,
            "total_actividades": 0,
            "total_viajes": 0,
            "personas_por_genero": {},
            "personas_por_macrosector": {}
        }
        personas_recientes = []
        atenciones_recientes = []
        personas_sin_atencion_count = 0
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "current_user": current_user,
        "estadisticas": estadisticas,
        "personas_recientes": personas_recientes,
        "atenciones_recientes": atenciones_recientes,
        "personas_sin_atencion_count": personas_sin_atencion_count
    })

@app.get("/login", response_class=HTMLResponse)
def login_redirect():
    return RedirectResponse(url="/auth/login")

# Middleware para redirigir a login si no está autenticado
@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    # Rutas que no requieren autenticación
    public_paths = ["/auth/login", "/auth/logout", "/static", "/docs", "/openapi.json"]
    
    if any(request.url.path.startswith(path) for path in public_paths):
        response = await call_next(request)
        return response
    
    # Para rutas que requieren autenticación, verificar cookie
    token = request.cookies.get("access_token")
    if not token and request.url.path not in ["/auth/login"]:
        return RedirectResponse(url="/auth/login")
    
    response = await call_next(request)
    return response

# Manejo de errores
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse("errors/404.html", {"request": request}, status_code=404)

@app.exception_handler(500)
async def server_error_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse("errors/500.html", {"request": request}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)