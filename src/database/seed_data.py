"""
Sembrador de Datos Cloud en Supabase (PostgreSQL + pgvector).
Reemplaza al sembrador local SQLite.
Siembra todas las áreas, materias, arquetipos y conocimiento universitario en Supabase Cloud.
"""
from src.database.supabase_client import supabase_manager

def seed():
    """Siembra las tablas de ingeniería y conocimiento vectorial en Supabase Cloud."""
    print("[Aureon Cloud] Iniciando sincronización con Supabase Cloud...")
    res = supabase_manager.seed_supabase_all()
    if res.get("success"):
        print(f"[OK] Sincronización exitosa con Supabase Cloud: {res.get('message')}")
    else:
        print(f"[Supabase Status] {res.get('message', 'Configura credenciales en .env')}")
    return res

if __name__ == "__main__":
    seed()
