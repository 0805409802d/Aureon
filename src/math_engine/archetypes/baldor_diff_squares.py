import sympy as sp
from typing import Dict, Any
from src.math_engine.base import BaseArchetypeSolver
from src.math_engine.models import SolveResult, MathStep, VisualBlock

class BaldorDiffSquaresSolver(BaseArchetypeSolver):
    archetype_id = "baldor_diff_squares"
    title = "Diferencia de Cuadrados (Baldor)"
    default_params = {"a": 2, "b": 6}

    def solve(self, params: Dict[str, Any]) -> SolveResult:
        a_val = sp.Rational(str(params.get("a", 2)))
        b_val = sp.Rational(str(params.get("b", 6)))

        if a_val == 0 or b_val == 0:
            raise ValueError("Los coeficientes 'a' y 'b' deben ser distintos de cero.")

        x = sp.Symbol('x')
        term1 = (a_val * x)**2
        term2 = b_val**2
        eq_orig = sp.Eq(term1 - term2, 0)
        original_latex = f"({sp.latex(a_val)}x)^2 - ({sp.latex(b_val)})^2 = 0 \\implies {sp.latex(term1)} - {sp.latex(term2)} = 0"

        steps = []

        # Paso 1: Identificación de las bases
        steps.append(MathStep(
            step_number=1,
            title="Identificar las bases cuadráticas A y B",
            rule_name="Reconocimiento del patrón A² - B²",
            latex=f"A = {sp.latex(a_val)}x, \\quad B = {sp.latex(b_val)} \\implies A^2 = {sp.latex(term1)}, \\quad B^2 = {sp.latex(term2)}",
            explanation=f"Extraemos la raíz cuadrada de cada término: √({term1}) = {a_val}x y √({term2}) = {b_val}.",
            source_breakdown=f"Bases extraídas: A = {a_val}x, B = {b_val}.",
            blocks=[
                VisualBlock(block_type="box", content=f"A = {a_val}x", id="base_a", label="Primera Base"),
                VisualBlock(block_type="operator", content="-"),
                VisualBlock(block_type="box", content=f"B = {b_val}", id="base_b", label="Segunda Base")
            ]
        ))

        # Paso 2: Factorización en binomios conjugados (A - B)(A + B) = 0
        factor1 = a_val * x - b_val
        factor2 = a_val * x + b_val
        steps.append(MathStep(
            step_number=2,
            title="Factorización en Producto de Binomios Conjugados",
            rule_name="Regla de Diferencia de Cuadrados: A² - B² = (A - B)(A + B)",
            latex=f"({sp.latex(factor1)})({sp.latex(factor2)}) = 0",
            explanation="La diferencia de dos cuadrados es siempre igual a la suma de las bases multiplicada por su diferencia.",
            source_breakdown=f"({a_val}x - {b_val}) * ({a_val}x + {b_val}) = 0.",
            blocks=[
                VisualBlock(block_type="box", content=f"({a_val}x - {b_val})", highlight=True),
                VisualBlock(block_type="operator", content="×"),
                VisualBlock(block_type="box", content=f"({a_val}x + {b_val})", highlight=True),
                VisualBlock(block_type="operator", content="="),
                VisualBlock(block_type="box", content="0")
            ]
        ))

        # Paso 3: Teorema del Factor Cero
        sol1 = b_val / a_val
        sol2 = -b_val / a_val
        steps.append(MathStep(
            step_number=3,
            title="Aplicar Teorema del Factor Cero para despejar 'x'",
            rule_name="Propiedad del Producto Cero: P · Q = 0 ⟹ P = 0 ó Q = 0",
            latex=f"{sp.latex(a_val)}x - {sp.latex(b_val)} = 0 \\implies x_1 = \\frac{{{sp.latex(b_val)}}}{{{sp.latex(a_val)}}} = {sp.latex(sol1)}, \\quad {sp.latex(a_val)}x + {sp.latex(b_val)} = 0 \\implies x_2 = -\\frac{{{sp.latex(b_val)}}}{{{sp.latex(a_val)}}} = {sp.latex(sol2)}",
            explanation=f"Igualamos cada factor a cero y despejamos: x₁ = {b_val}/{a_val} = {sol1} y x₂ = -{b_val}/{a_val} = {sol2}.",
            source_breakdown=f"x₁ = +({b_val}/{a_val}) = {sol1}; x₂ = -({b_val}/{a_val}) = {sol2}.",
            blocks=[
                VisualBlock(block_type="result", content=f"x₁ = {sol1}", highlight=True),
                VisualBlock(block_type="result", content=f"x₂ = {sol2}", highlight=True)
            ]
        ))

        return SolveResult(
            archetype_id=self.archetype_id,
            title=self.title,
            input_params=params,
            original_latex=original_latex,
            steps=steps,
            final_solutions=[f"x_1 = {sp.latex(sol1)}", f"x_2 = {sp.latex(sol2)}"],
            real_world_context="Cálculo de frecuencias de resonancia simétrica en vigas robóticas, simplificación algebraica en compiladores y cancelación de términos en integrales racionales."
        )
