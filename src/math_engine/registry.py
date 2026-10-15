from typing import Dict, Optional, List
from src.math_engine.base import BaseArchetypeSolver
from src.math_engine.models import SolveResult
from src.math_engine.archetypes.baldor_linear import BaldorLinearSolver
from src.math_engine.archetypes.baldor_quadratic import BaldorQuadraticSolver
from src.math_engine.archetypes.baldor_systems_2x2 import BaldorSystems2x2Solver
from src.math_engine.archetypes.baldor_factoring import BaldorFactoringSolver
from src.math_engine.archetypes.baldor_diff_squares import BaldorDiffSquaresSolver
from src.math_engine.archetypes.calculus_derivative import CalculusDerivativeSolver
from src.math_engine.archetypes.linear_algebra_matrix_mult import MatrixMult2x2Solver
from src.math_engine.archetypes.cs_modulo_euclid import CsModuloEuclidSolver
from src.math_engine.archetypes.robotics_2d_kinematics import Robotics2dKinematicsSolver
from src.math_engine.archetypes.nano_schrodinger import NanoSchrodingerSolver
from src.math_engine.archetypes.physics_nuclear_decay import NuclearDecaySolver
from src.math_engine.archetypes.ai_backprop import AiBackpropSolver
from src.math_engine.archetypes.os_paging import OsPagingSolver
from src.math_engine.archetypes.mechanics_stress import MechanicsStressSolver

class MathEngineRegistry:
    """Registro central de solucionadores de arquetipos matemáticos e ingeniería."""

    def __init__(self):
        self._solvers: Dict[str, BaseArchetypeSolver] = {}
        self._register_defaults()

    def register(self, solver: BaseArchetypeSolver):
        self._solvers[solver.archetype_id] = solver

    def _register_defaults(self):
        # Fundamentos y Baldor
        self.register(BaldorLinearSolver())
        self.register(BaldorQuadraticSolver())
        self.register(BaldorSystems2x2Solver())
        self.register(BaldorFactoringSolver())
        self.register(BaldorDiffSquaresSolver())
        # Cálculo y Álgebra Lineal
        self.register(CalculusDerivativeSolver())
        self.register(MatrixMult2x2Solver())
        self.register(CsModuloEuclidSolver())
        # Ingenierías Específicas
        self.register(AiBackpropSolver())
        self.register(Robotics2dKinematicsSolver())
        self.register(OsPagingSolver())
        self.register(MechanicsStressSolver())
        self.register(NanoSchrodingerSolver())
        self.register(NuclearDecaySolver())

    def get_solver(self, archetype_id: str) -> Optional[BaseArchetypeSolver]:
        return self._solvers.get(archetype_id)

    def list_archetypes(self) -> List[str]:
        return list(self._solvers.keys())

    def solve(self, archetype_id: str, params: dict) -> SolveResult:
        solver = self.get_solver(archetype_id)
        if not solver:
            raise KeyError(f"El arquetipo matemático '{archetype_id}' no está registrado en el motor.")
        return solver.solve(params)

# Instancia singleton del registro
engine_registry = MathEngineRegistry()
