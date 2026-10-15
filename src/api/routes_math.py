from fastapi import APIRouter, HTTPException, Body
from typing import Dict, Any, Optional
from src.math_engine.registry import engine_registry
from src.math_engine.models import SolveResult
from src.database.supabase_client import supabase_manager

router = APIRouter(prefix="/api/math", tags=["Math Engine"])

@router.get("/archetypes")
def list_archetypes(subject_id: Optional[str] = None, area_id: Optional[str] = None):
    """
    Lista todos los arquetipos matemáticos disponibles en Supabase Cloud.
    Filtra por materia o por área de ingeniería (IA, Robótica, SO, Mecánica, Matemáticas).
    """
    return supabase_manager.get_archetypes(subject_id=subject_id, area_id=area_id)

@router.get("/archetypes/{archetype_id}")
def get_archetype(archetype_id: str):
    """Obtiene el detalle de un arquetipo específico con su fórmula y parámetros por defecto."""
    arch = supabase_manager.get_archetype_by_id(archetype_id)
    if not arch:
        raise HTTPException(status_code=404, detail=f"Arquetipo '{archetype_id}' no encontrado.")
    return arch

@router.post("/archetypes/{archetype_id}/solve", response_model=SolveResult)
def solve_archetype(archetype_id: str, params: Optional[Dict[str, Any]] = Body(default=None)):
    """
    Recalcula determinísticamente con SymPy (sin IA) el procedimiento paso a paso.
    Registra el cálculo en el historial de práctica en Supabase Cloud.
    """
    solver = engine_registry.get_solver(archetype_id)
    if not solver:
        raise HTTPException(status_code=404, detail=f"El arquetipo '{archetype_id}' no está registrado en el motor matemático.")

    # Si no se envían parámetros, usar los default del solver
    active_params = params if params is not None and len(params) > 0 else solver.default_params

    try:
        result = solver.solve(active_params)
        
        # Registrar en el historial de práctica en Supabase Cloud
        supabase_manager.log_practice_history(
            archetype_id=archetype_id,
            input_params=active_params,
            solutions=result.final_solutions
        )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al resolver la ecuación con los parámetros dados: {str(e)}")
