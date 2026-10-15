from abc import ABC, abstractmethod
from typing import Dict, Any
from src.math_engine.models import SolveResult

class BaseArchetypeSolver(ABC):
    """Clase base abstracta para todos los solucionadores de arquetipos matemáticos."""
    
    archetype_id: str
    title: str
    default_params: Dict[str, Any]

    @abstractmethod
    def solve(self, params: Dict[str, Any]) -> SolveResult:
        """Calcula el paso a paso didáctico usando SymPy y devuelve SolveResult."""
        pass
