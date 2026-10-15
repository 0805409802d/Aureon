from pathlib import Path
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env antes de inicializar componentes
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src.database.supabase_client import supabase_manager
from src.api.routes_math import router as math_router
from src.api.routes_library import router as library_router
from src.api.routes_tutor import router as tutor_router
from src.api.routes_mcp import router as mcp_router

WEB_DIR = Path(__file__).resolve().parent.parent / "web"

def create_app() -> FastAPI:
    app = FastAPI(
        title="Aureon AI Cloud API",
        description=(
            "Sistema tutor inteligente, motor matemático paramétrico y servidor MCP "
            "para ingeniería (IA, Robótica, SO, Mecánica, Matemáticas) "
            "con Google Gemini 3.1 y persistencia 100% en la nube con Supabase pgvector."
        ),
        version="2.1.0"
    )

    # Permitir peticiones cross-origin
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Registrar routers API
    app.include_router(math_router)
    app.include_router(library_router)
    app.include_router(tutor_router)
    app.include_router(mcp_router)

    @app.on_event("startup")
    def on_startup():
        print("[Aureon Cloud] Iniciando servidor en Railway...")
        print(f"[Supabase Cloud] Conectado: {supabase_manager.is_connected()}")
        print(f"[MCP Protocol] Servidor MCP activo en /api/mcp")

    @app.get("/api/health")
    def health():
        return {
            "name": "Aureon AI Cloud System",
            "status": "online",
            "version": "2.1.0",
            "environment": os.getenv("APP_ENV", "production"),
            "persistence": "supabase_cloud_postgresql_pgvector",
            "supabase_cloud": {
                "connected": supabase_manager.is_connected(),
                "vector_enabled": supabase_manager.enabled
            },
            "mcp_protocol": {
                "enabled": True,
                "endpoint": "/api/mcp",
                "tools_count": 5
            },
            "gemini_model": os.getenv("GEMINI_MODEL", "gemini-2.5-pro"),
            "student_profile": {
                "name": "Darlyn David Tenelema Obando",
                "institution": "Instituto Superior Tecnológico Carlos Cisneros",
                "career": "Inteligencia Artificial"
            },
            "docs": "/docs"
        }

    # Servir la interfaz web en la raíz
    if WEB_DIR.exists():
        app.mount("/", StaticFiles(directory=str(WEB_DIR), html=True), name="web")

    return app

app = create_app()
