"""
Router API para el Tutor Aureon Inteligente (Canvas de Explicación y Pedagogía).
Conexión con Gemini 3.1, SymPy, Supabase pgvector y pedagogías de Harvard, Stanford, MGU, Tsinghua y Polytechnique.
100% Persistencia en la Nube con Supabase Cloud.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

from src.math_engine.registry import engine_registry
from src.database.supabase_client import supabase_manager
from src.knowledge.universities import list_all_pedagogies, get_university_pedagogy
from src.ai.gemini_tutor import gemini_tutor

router = APIRouter(prefix="/api/tutor", tags=["Aureon Tutor Inteligente"])

class TutorQuery(BaseModel):
    archetype_id: str
    step_number: Optional[int] = Field(None, description="Número del paso seleccionado en el canvas numérico")
    question_type: str = Field(..., description="Opciones: 'source_of_number', 'process_name', 'step_by_step', 'real_world_use', 'custom'")
    user_question: Optional[str] = Field(None, description="Pregunta específica o personalizada del usuario")
    params: Optional[Dict[str, Any]] = Field(default=None, description="Parámetros numéricos activos del ejercicio")
    university_lens: Optional[str] = Field("stanford", description="Lente pedagógico: stanford, moscow, tsinghua, harvard, polytechnique")

class CustomEquationQuery(BaseModel):
    equation: str = Field(..., description="Cualquier ecuación, EDO, integral o problema matemático")
    university_lens: Optional[str] = Field("stanford", description="Universidad a emular: stanford, moscow, tsinghua, harvard, polytechnique")
    user_notes: Optional[str] = Field(None, description="Notas o dudas específicas del alumno")

class RagSearchQuery(BaseModel):
    query: str
    university: Optional[str] = None
    discipline: Optional[str] = None
    top_k: Optional[int] = 3

@router.get("/universities")
def get_universities():
    """Retorna las pedagogías universitarias internacionales soportadas por Aureon."""
    return list_all_pedagogies()

@router.post("/explain")
def explain_step(query: TutorQuery):
    """
    Endpoint del Tutor Aureon (Canvas Delgado).
    Responde con IA Gemini 3.1 y lente pedagógico universitario seleccionado.
    Persiste la interacción en Supabase Cloud.
    """
    solver = engine_registry.get_solver(query.archetype_id)
    if not solver:
        raise HTTPException(status_code=404, detail=f"Arquetipo '{query.archetype_id}' no encontrado.")

    active_params = query.params if query.params else solver.default_params
    result = solver.solve(active_params)

    # Buscar el paso relevante
    selected_step_data = None
    if query.step_number is not None:
        for s in result.steps:
            if s.step_number == query.step_number:
                selected_step_data = s.model_dump()
                break

    # Consultar al motor de IA con el lente universitario
    explanation = gemini_tutor.answer_interactive_query(
        archetype_title=result.title,
        step_number=query.step_number,
        question_type=query.question_type,
        user_question=query.user_question,
        active_params=active_params,
        step_data=selected_step_data,
        university_lens=query.university_lens or "stanford"
    )

    # Registrar la interacción en Supabase Cloud
    supabase_manager.log_tutor_interaction(
        archetype_id=query.archetype_id,
        step_number=query.step_number,
        question_type=query.question_type,
        user_question=query.user_question or query.question_type,
        tutor_explanation=explanation
    )

    return {
        "archetype_id": query.archetype_id,
        "step_number": query.step_number,
        "question_type": query.question_type,
        "university_lens": query.university_lens,
        "explanation": explanation
    }

@router.post("/solve-custom")
def solve_custom_equation(query: CustomEquationQuery):
    """
    Solucionador Universal IA para CUALQUIER ecuación matemática o problema de ingeniería.
    Combina cálculo determinista SymPy + IA Gemini 3.1 + RAG Universitario + Supabase Cloud.
    """
    if not query.equation or not query.equation.strip():
        raise HTTPException(status_code=400, detail="Debes proporcionar una ecuación o expresión matemática.")

    result = gemini_tutor.explain_custom_equation(
        equation_input=query.equation.strip(),
        university_lens=query.university_lens or "stanford",
        user_notes=query.user_notes
    )
    return result

@router.post("/rag-search")
def search_rag(query: RagSearchQuery):
    """Búsqueda semántica en la base de datos vectorial de conocimientos universitarios (pgvector)."""
    results = supabase_manager.query_knowledge(
        query=query.query,
        university=query.university,
        discipline=query.discipline,
        top_k=query.top_k or 3
    )
    return {
        "query": query.query,
        "source": "supabase_pgvector" if supabase_manager.is_connected() else "high_precision_vector_engine",
        "results": results
    }

@router.post("/sync-supabase")
def sync_supabase():
    """Siembra y sincroniza todas las áreas, materias y conocimientos en Supabase Cloud."""
    res = supabase_manager.seed_supabase_all()
    return res

@router.get("/status")
def tutor_status():
    """Retorna el estado de conexión de los subsistemas de IA y Base de Datos."""
    return {
        "gemini_model": gemini_tutor.model_name,
        "gemini_active": bool(gemini_tutor._call_gemini("Ping", "Responde Pong") is not None),
        "supabase_connected": supabase_manager.is_connected(),
        "supabase_vector_enabled": supabase_manager.enabled,
        "available_universities": [p["name"] for p in list_all_pedagogies()]
    }
