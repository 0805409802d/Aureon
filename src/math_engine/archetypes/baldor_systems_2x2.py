import sympy as sp
from typing import Dict, Any
from src.math_engine.base import BaseArchetypeSolver
from src.math_engine.models import SolveResult, MathStep, VisualBlock

class BaldorSystems2x2Solver(BaseArchetypeSolver):
    archetype_id = "baldor_system_2x2"
    title = "Sistema de Ecuaciones Lineales 2x2 (Regla de Cramer / Determinantes)"
    default_params = {"a1": 2, "b1": 3, "c1": 13, "a2": 1, "b2": -1, "c2": -1}

    def solve(self, params: Dict[str, Any]) -> SolveResult:
        a1 = sp.Rational(str(params.get("a1", 2)))
        b1 = sp.Rational(str(params.get("b1", 3)))
        c1 = sp.Rational(str(params.get("c1", 13)))
        a2 = sp.Rational(str(params.get("a2", 1)))
        b2 = sp.Rational(str(params.get("b2", -1)))
        c2 = sp.Rational(str(params.get("c2", -1)))

        original_latex = (
            r"\begin{cases} "
            f"{sp.latex(a1)}x + ({sp.latex(b1)})y = {sp.latex(c1)} \\\\ "
            f"{sp.latex(a2)}x + ({sp.latex(b2)})y = {sp.latex(c2)} "
            r"\end{cases}"
        )

        steps = []

        # Paso 1: Matriz y Determinante del Sistema (Δ)
        det_s = a1 * b2 - a2 * b1
        steps.append(MathStep(
            step_number=1,
            title="Calcular el Determinante Principal del Sistema (Δ)",
            rule_name="Determinante de Matriz de Coeficientes 2x2",
            latex=f"\\Delta = \\begin{{vmatrix}} {sp.latex(a1)} & {sp.latex(b1)} \\\\ {sp.latex(a2)} & {sp.latex(b2)} \\end{{vmatrix}} = ({sp.latex(a1)})({sp.latex(b2)}) - ({sp.latex(a2)})({sp.latex(b1)}) = {sp.latex(det_s)}",
            explanation=f"Multiplicamos la diagonal principal ({a1}×{b2}) y restamos la diagonal secundaria ({a2}×{b1}).",
            source_breakdown=f"({a1} * {b2}) - ({a2} * {b1}) = ({a1*b2}) - ({a2*b1}) = {det_s}.",
            blocks=[
                VisualBlock(block_type="box", content=f"a₁·b₂ = {a1*b2}", id="diag_main"),
                VisualBlock(block_type="operator", content="-"),
                VisualBlock(block_type="box", content=f"a₂·b₁ = {a2*b1}", id="diag_sec"),
                VisualBlock(block_type="operator", content="="),
                VisualBlock(block_type="result", content=f"Δ = {det_s}", id="det_s", highlight=True)
            ]
        ))

        if det_s == 0:
            steps.append(MathStep(
                step_number=2,
                title="Sistema sin solución única",
                rule_name="Criterio de Singularidad",
                latex=r"\Delta = 0 \implies \text{El sistema no tiene solución única (rectas paralelas o coincidentes)}",
                explanation="Cuando el determinante es 0, las rectas no se cruzan en un único punto.",
                source_breakdown="Δ = 0",
                blocks=[VisualBlock(block_type="box", content="Sin solución única", highlight=True)]
            ))
            return SolveResult(
                archetype_id=self.archetype_id,
                title=self.title,
                input_params=params,
                original_latex=original_latex,
                steps=steps,
                final_solutions=["Sin solución única (Δ = 0)"],
                real_world_context="Líneas paralelas en navegación de robots móviles o sistemas sin restricción independiente."
            )

        # Paso 2: Determinante de X (Δx)
        det_x = c1 * b2 - c2 * b1
        steps.append(MathStep(
            step_number=2,
            title="Calcular el Determinante respecto a x (Δx)",
            rule_name="Reemplazo de la columna 'x' por los términos independientes",
            latex=f"\\Delta_x = \\begin{{vmatrix}} {sp.latex(c1)} & {sp.latex(b1)} \\\\ {sp.latex(c2)} & {sp.latex(b2)} \\end{{vmatrix}} = ({sp.latex(c1)})({sp.latex(b2)}) - ({sp.latex(c2)})({sp.latex(b1)}) = {sp.latex(det_x)}",
            explanation=f"Cambiamos los coeficientes de 'x' por los términos constantes [{c1}, {c2}] y calculamos el determinante.",
            source_breakdown=f"({c1} * {b2}) - ({c2} * {b1}) = ({c1*b2}) - ({c2*b1}) = {det_x}.",
            blocks=[
                VisualBlock(block_type="box", content=f"c₁·b₂ = {c1*b2}"),
                VisualBlock(block_type="operator", content="-"),
                VisualBlock(block_type="box", content=f"c₂·b₁ = {c2*b1}"),
                VisualBlock(block_type="operator", content="="),
                VisualBlock(block_type="result", content=f"Δx = {det_x}", highlight=True)
            ]
        ))

        # Paso 3: Determinante de Y (Δy)
        det_y = a1 * c2 - a2 * c1
        steps.append(MathStep(
            step_number=3,
            title="Calcular el Determinante respecto a y (Δy)",
            rule_name="Reemplazo de la columna 'y' por los términos independientes",
            latex=f"\\Delta_y = \\begin{{vmatrix}} {sp.latex(a1)} & {sp.latex(c1)} \\\\ {sp.latex(a2)} & {sp.latex(c2)} \\end{{vmatrix}} = ({sp.latex(a1)})({sp.latex(c2)}) - ({sp.latex(a2)})({sp.latex(c1)}) = {sp.latex(det_y)}",
            explanation=f"Cambiamos los coeficientes de 'y' por los términos constantes [{c1}, {c2}] y calculamos el determinante.",
            source_breakdown=f"({a1} * {c2}) - ({a2} * {c1}) = ({a1*c2}) - ({a2*c1}) = {det_y}.",
            blocks=[
                VisualBlock(block_type="box", content=f"a₁·c₂ = {a1*c2}"),
                VisualBlock(block_type="operator", content="-"),
                VisualBlock(block_type="box", content=f"a₂·c₁ = {a2*c1}"),
                VisualBlock(block_type="operator", content="="),
                VisualBlock(block_type="result", content=f"Δy = {det_y}", highlight=True)
            ]
        ))

        # Paso 4: Despeje de incógnitas x = Δx / Δ, y = Δy / Δ
        sol_x = det_x / det_s
        sol_y = det_y / det_s

        steps.append(MathStep(
            step_number=4,
            title="Obtención de la solución (Regla de Cramer: x = Δx/Δ, y = Δy/Δ)",
            rule_name="Cociente de Determinantes",
            latex=f"x = \\frac{{\\Delta_x}}{{\\Delta}} = \\frac{{{sp.latex(det_x)}}}{{{sp.latex(det_s)}}} = {sp.latex(sol_x)}, \\quad y = \\frac{{\\Delta_y}}{{\\Delta}} = \\frac{{{sp.latex(det_y)}}}{{{sp.latex(det_s)}}} = {sp.latex(sol_y)}",
            explanation=f"Dividimos cada determinante secundario entre el determinante principal del sistema.",
            source_breakdown=f"x sale de {det_x}/{det_s} = {sol_x}. y sale de {det_y}/{det_s} = {sol_y}.",
            blocks=[
                VisualBlock(block_type="result", content=f"x = {sol_x}", highlight=True),
                VisualBlock(block_type="result", content=f"y = {sol_y}", highlight=True)
            ]
        ))

        return SolveResult(
            archetype_id=self.archetype_id,
            title=self.title,
            input_params=params,
            original_latex=original_latex,
            steps=steps,
            final_solutions=[f"x = {sp.latex(sol_x)}", f"y = {sp.latex(sol_y)}"],
            real_world_context="Leyes de Kirchhoff en electrónica, cinemática 2D en robótica de planos y asignación óptima de recursos en programación lineal."
        )
