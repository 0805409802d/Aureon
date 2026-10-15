"""
Módulo de Conexión de Base de Datos - Aureon Cloud.
Base de datos local SQLite eliminada.
Toda la persistencia se realiza 100% en la nube a través de Supabase Cloud y pgvector.
"""
from src.database.supabase_client import supabase_manager

def init_db():
    """Notifica la inicialización del sistema en la nube con Supabase."""
    print("[Aureon Cloud] Persistencia local SQLite eliminada. Sistema conectado a Supabase Cloud + pgvector.")
    return True

if __name__ == "__main__":
    init_db()
