from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from src.database.supabase_client import supabase_manager

router = APIRouter(prefix="/api/library", tags=["Library, Notes & Study Tracker"])

class NoteCreate(BaseModel):
    subject_id: str
    archetype_id: Optional[str] = None
    title: str
    content: str
    mastery_level: int = Field(1, ge=1, le=5)

class NoteReview(BaseModel):
    quality: int = Field(..., ge=0, le=5, description="Calificación SM-2 (0=olvidado, 3=correcto con esfuerzo, 5=perfecto)")

class StudySessionCreate(BaseModel):
    minutes: int = Field(50, ge=1, le=720, description="Minutos de estudio dedicados")
    focus_area: str = Field("ai", description="Área de estudio: ai, robotics, os, mechanics, math")
    topic: Optional[str] = Field(None, description="Tema específico estudiado")
    notes: Optional[str] = Field(None, description="Notas de la sesión")

@router.get("/areas")
def get_areas_with_subjects():
    """Obtiene las áreas de ingeniería y sus materias asociadas desde Supabase Cloud."""
    return supabase_manager.get_areas_with_subjects()

@router.get("/notes")
def get_study_notes(subject_id: Optional[str] = None):
    """Obtiene las notas de estudio y tarjetas de repetición espaciada SM-2."""
    return supabase_manager.get_study_notes(subject_id=subject_id)

@router.post("/notes")
def create_study_note(note: NoteCreate):
    """Guarda una nota de estudio o flashcard en Supabase Cloud."""
    created = supabase_manager.create_study_note(
        subject_id=note.subject_id,
        archetype_id=note.archetype_id,
        title=note.title,
        content=note.content,
        mastery_level=note.mastery_level
    )
    return {"message": "Nota guardada con éxito en Supabase", "note": created}

@router.post("/notes/{note_id}/review")
def review_study_note(note_id: str, review: NoteReview):
    """Actualiza la repetición espaciada SM-2 de una tarjeta según el rendimiento del alumno."""
    res = supabase_manager.update_study_note_review(note_id=note_id, quality=review.quality)
    return {"message": "Repetición espaciada actualizada con algoritmo SM-2", "sm2": res}

@router.post("/sessions")
def log_session(session_data: StudySessionCreate):
    """Registra un bloque de estudio de las 10+ horas diarias de Darlyn."""
    record = supabase_manager.log_study_session(
        minutes=session_data.minutes,
        focus_area=session_data.focus_area,
        topic=session_data.topic,
        notes=session_data.notes
    )
    return {"message": "Sesión de estudio registrada en Supabase Cloud", "session": record}

@router.get("/stats")
def get_study_stats():
    """Obtiene el progreso diario de estudio respecto a la meta de 10 horas."""
    return supabase_manager.get_study_stats_today()
