from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class VisualBlock(BaseModel):
    """Representa una caja o bloque visual en el Canvas Numérico (como en el boceto)."""
    block_type: str = Field(..., description="Tipo de bloque: 'box', 'operator', 'fraction', 'result'")
    content: str = Field(..., description="Texto o valor visible en la caja (ej: '3x', '+', '5', '÷')")
    id: Optional[str] = Field(None, description="Identificador único para interactividad con la IA")
    highlight: bool = Field(False, description="Si debe iluminarse en pantalla")
    label: Optional[str] = Field(None, description="Etiqueta explicativa superior o inferior")

class MathStep(BaseModel):
    """Representa un paso completo del procedimiento didáctico."""
    step_number: int
    title: str
    rule_name: str
    latex: str
    explanation: str
    source_breakdown: Optional[str] = Field(None, description="Explica de dónde salieron los números en este paso")
    blocks: List[VisualBlock] = Field(default_factory=list)

class SolveResult(BaseModel):
    """Resultado estructurado de resolver un arquetipo matemático paramétrico."""
    archetype_id: str
    title: str
    input_params: Dict[str, Any]
    original_latex: str
    steps: List[MathStep]
    final_solutions: List[str]
    real_world_context: str
