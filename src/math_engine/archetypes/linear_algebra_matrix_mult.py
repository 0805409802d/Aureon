import sympy as sp
from typing import Dict, Any
from src.math_engine.base import BaseArchetypeSolver
from src.math_engine.models import SolveResult, MathStep, VisualBlock

class MatrixMult2x2Solver(BaseArchetypeSolver):
    archetype_id = "linear_algebra_matrix_mult_2x2"
    title = "Transformación Lineal: Multiplicación Matriz-Vector 2x2"
    default_params = {"a": 0, "b": -1, "c": 1, "d": 0, "x": 3, "y": 4}

    def solve(self, params: Dict[str, Any]) -> SolveResult:
        a = sp.Rational(str(params.get("a", 0)))
        b = sp.Rational(str(params.get("b", -1)))
        c = sp.Rational(str(params.get("c", 1)))
        d = sp.Rational(str(params.get("d", 0)))
        x_val = sp.Rational(str(params.get("x", 3)))
        y_val = sp.Rational(str(params.get("y", 4)))

        M = sp.Matrix([[a, b], [c, d]])
        v = sp.Matrix([x_val, y_val])
        res_vector = M * v

        original_latex = (
            r"\begin{pmatrix} "
            f"{sp.latex(a)} & {sp.latex(b)} \\\\ "
            f"{sp.latex(c)} & {sp.latex(d)} "
            r"\end{pmatrix} "
            r"\begin{pmatrix} "
            f"{sp.latex(x_val)} \\\\ {sp.latex(y_val)} "
            r"\end{pmatrix}"
        )

        steps = []

        # Paso 1: Planteamiento de filas y columnas
        steps.append(MathStep(
            step_number=1,
            title="Estructura de la Transformación: Producto Fila por Columna",
            rule_name="Definición de Producto Matriz-Vector",
            latex=r"M \cdot v = \begin{pmatrix} \text{Fila}_1 \cdot v \\ \text{Fila}_2 \cdot v \end{pmatrix} = \begin{pmatrix} a \cdot x + b \cdot y \\ c \cdot x + d \cdot y \end{pmatrix}",
            explanation="Cada componente del vector resultante es el producto escalar entre una fila de la matriz y el vector de entrada.",
            source_breakdown=f"Fila 1: [{a}, {b}] · [{x_val}, {y_val}]. Fila 2: [{c}, {d}] · [{x_val}, {y_val}].",
            blocks=[
                VisualBlock(block_type="box", content=f"[{a}, {b}]", label="Fila 1"),
                VisualBlock(block_type="operator", content="·"),
                VisualBlock(block_type="box", content=f"[{x_val}, {y_val}]ᵀ", label="Vector v")
            ]
        ))

        # Paso 2: Cálculo de la Primera Componente (x')
        term_ax = a * x_val
        term_by = b * y_val
        x_prime = term_ax + term_by

        steps.append(MathStep(
            step_number=2,
            title="Cálculo de la primera componente x' = a·x + b·y",
            rule_name="Producto Escalar Fila 1",
            latex=f"x' = ({sp.latex(a)})({sp.latex(x_val)}) + ({sp.latex(b)})({sp.latex(y_val)}) = {sp.latex(term_ax)} + ({sp.latex(term_by)}) = {sp.latex(x_prime)}",
            explanation=f"Multiplicamos {a}×{x_val} = {term_ax} y sumamos {b}×{y_val} = {term_by}. La nueva coordenada x' es {x_prime}.",
            source_breakdown=f"({a} * {x_val}) + ({b} * {y_val}) = {term_ax} + {term_by} = {x_prime}.",
            blocks=[
                VisualBlock(block_type="box", content=f"{a}×{x_val} = {term_ax}"),
                VisualBlock(block_type="operator", content="+"),
                VisualBlock(block_type="box", content=f"{b}×{y_val} = {term_by}"),
                VisualBlock(block_type="operator", content="="),
                VisualBlock(block_type="result", content=f"x' = {x_prime}", highlight=True)
            ]
        ))

        # Paso 3: Cálculo de la Segunda Componente (y')
        term_cx = c * x_val
        term_dy = d * y_val
        y_prime = term_cx + term_dy

        steps.append(MathStep(
            step_number=3,
            title="Cálculo de la segunda componente y' = c·x + d·y",
            rule_name="Producto Escalar Fila 2",
            latex=f"y' = ({sp.latex(c)})({sp.latex(x_val)}) + ({sp.latex(d)})({sp.latex(y_val)}) = {sp.latex(term_cx)} + ({sp.latex(term_dy)}) = {sp.latex(y_prime)}",
            explanation=f"Multiplicamos {c}×{x_val} = {term_cx} y sumamos {d}×{y_val} = {term_dy}. La nueva coordenada y' es {y_prime}.",
            source_breakdown=f"({c} * {x_val}) + ({d} * {y_val}) = {term_cx} + {term_dy} = {y_prime}.",
            blocks=[
                VisualBlock(block_type="box", content=f"{c}×{x_val} = {term_cx}"),
                VisualBlock(block_type="operator", content="+"),
                VisualBlock(block_type="box", content=f"{d}×{y_val} = {term_dy}"),
                VisualBlock(block_type="operator", content="="),
                VisualBlock(block_type="result", content=f"y' = {y_prime}", highlight=True)
            ]
        ))

        # Paso 4: Vector Transformado Final
        steps.append(MathStep(
            step_number=4,
            title="Vector Transformado Resultante",
            rule_name="Vector Transformado en R²",
            latex=f"v' = \\begin{{pmatrix}} {sp.latex(x_prime)} \\\\ {sp.latex(y_prime)} \\end{{pmatrix}}",
            explanation=f"El vector [{x_val}, {y_val}]ᵀ se ha transformado en [{x_prime}, {y_prime}]ᵀ bajo la matriz M.",
            source_breakdown="Vector columna final ensamblado.",
            blocks=[
                VisualBlock(block_type="result", content=f"[{x_prime}, {y_prime}]ᵀ", highlight=True, label="Vector v'")
            ]
        ))

        return SolveResult(
            archetype_id=self.archetype_id,
            title=self.title,
            input_params=params,
            original_latex=original_latex,
            steps=steps,
            final_solutions=[f"x' = {sp.latex(x_prime)}", f"y' = {sp.latex(y_prime)}"],
            real_world_context="Robótica: Rotación y traslación de marcos de referencia (Frames). Ciencias de la Computación: Transformaciones de vértices en motores 3D (OpenGL, Vulkan) y capas lineales en redes neuronales (y = Wx + b)."
        )
