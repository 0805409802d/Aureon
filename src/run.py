import os
import uvicorn
import sys
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno desde .env si existe
load_dotenv()

# Agregar directorio raíz al PYTHONPATH
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("APP_ENV", "development").lower() == "development"
    
    print(f"[Aureon Core] Servidor escuchando en http://{host}:{port}")
    print(f"[Aureon Core] Documentación Swagger: http://{host}:{port}/docs")
    uvicorn.run("src.api.app:app", host=host, port=port, reload=reload)
