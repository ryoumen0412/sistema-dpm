from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .api.routes import auth, personas_mayores, atenciones, reportes
from .api.routes.auth import get_current_user
from .crud import personas_mayores as crud_pm
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

# Incluir rutas
app.include_router(auth.router, prefix="/auth")
app.include_router(personas_mayores.router)
app.include_router(atenciones.router)
app.include_router(reportes.router)

@app.get("/", response_class=HTMLResponse)
def dashboard(
    request: Request,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Estadísticas para el dashboard
    estadisticas = crud_pm.get_estadisticas_generales(db)
    personas_recientes = crud_pm.get_personas_mayores(db, limit=5)
    atenciones_recientes = crud_pm.get_atenciones(db, limit=5)
    personas_sin_atencion = crud_pm.get_personas_sin_atencion_reciente(db, dias=30)
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "current_user": current_user,
        "estadisticas": estadisticas,
        "personas_recientes": personas_recientes,
        "atenciones_recientes": atenciones_recientes,
        "personas_sin_atencion_count": len(personas_sin_atencion)
    })

@app.get("/login", response_class=HTMLResponse)
def login_redirect():
    return RedirectResponse(url="/auth/login")

# Middleware para redirigir a login si no está autenticado
@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    # Rutas que no requieren autenticación
    public_paths = ["/auth/login", "/static", "/docs", "/openapi.json"]
    
    if any(request.url.path.startswith(path) for path in public_paths):
        response = await call_next(request)
        return response
    
    # Verificar cookie de autenticación
    token = request.cookies.get("access_token")
    if not token and request.url.path != "/auth/login":
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