import sympy as sp
from typing import Dict, Any
from src.math_engine.base import BaseArchetypeSolver
from src.math_engine.models import SolveResult, MathStep, VisualBlock

class BaldorLinearSolver(BaseArchetypeSolver):
    archetype_id = "baldor_linear_eq"
    title = "Ecuación Lineal de Primer Grado (Baldor)"
    default_params = {"a": 3, "b": 5, "c": 20}

    def solve(self, params: Dict[str, Any]) -> SolveResult:
        # Convertir a tipos numéricos de SymPy
        a_val = sp.Rational(str(params.get("a", 3)))
        b_val = sp.Rational(str(params.get("b", 5)))
        c_val = sp.Rational(str(params.get("c", 20)))

        if a_val == 0:
            raise ValueError("El coeficiente 'a' no puede ser 0 en una ecuación de primer grado.")

        x = sp.Symbol('x')
        eq_orig = sp.Eq(a_val * x + b_val, c_val)
        original_latex = sp.latex(eq_orig)

        steps = []

        # Paso 1: Planteamiento
        steps.append(MathStep(
            step_number=1,
            title="Identificar la forma general",
            rule_name="Ecuación lineal canónica",
            latex=f"{sp.latex(a_val * x + b_val)} = {sp.latex(c_val)}",
            explanation=f"Tenemos la variable 'x' multiplicada por el coeficiente {a_val}, sumada con el término constante {b_val}, igualada a {c_val}.",
            source_breakdown=f"Los términos provienen directamente de los valores iniciales: a={a_val}, b={b_val}, c={c_val}.",
            blocks=[
                VisualBlock(block_type="box", content=f"{a_val}x", id="term_var", label="Término con variable"),
                VisualBlock(block_type="operator", content="+" if b_val >= 0 else "-", id="op_add"),
                VisualBlock(block_type="box", content=f"{abs(b_val)}", id="term_const", label="Constante"),
                VisualBlock(block_type="operator", content="=", id="op_eq"),
                VisualBlock(block_type="box", content=f"{c_val}", id="term_target", label="Resultado"),
            ]
        ))

        # Paso 2: Aislar el término con la incógnita (transposición de términos)
        diff = c_val - b_val
        sign_word = "restamos" if b_val > 0 else "sumamos"
        steps.append(MathStep(
            step_number=2,
            title=f"Transponer término constante: {sign_word} {abs(b_val)} a ambos lados",
            rule_name="Propiedad uniforme de la adición/sustracción",
            latex=f"{sp.latex(a_val * x)} = {sp.latex(c_val)} - ({sp.latex(b_val)}) \\implies {sp.latex(a_val * x)} = {sp.latex(diff)}",
            explanation=f"Para dejar solo el término con 'x' a la izquierda, aplicamos la operación inversa de {b_val} a ambos miembros de la ecuación.",
            source_breakdown=f"El número {diff} sale de la operación ({c_val}) - ({b_val}) = {diff}.",
            blocks=[
                VisualBlock(block_type="box", content=f"{a_val}x", id="term_var_isolated"),
                VisualBlock(block_type="operator", content="="),
                VisualBlock(block_type="box", content=f"{diff}", id="term_diff", label=f"({c_val} - {b_val})", highlight=True)
            ]
        ))

        # Paso 3: Despejar la incógnita dividiendo entre 'a'
        sol = diff / a_val
        steps.append(MathStep(
            step_number=3,
            title=f"Dividir ambos lados entre el coeficiente {a_val}",
            rule_name="Propiedad uniforme de la división",
            latex=f"x = \\frac{{{sp.latex(diff)}}}{{{sp.latex(a_val)}}}",
            explanation=f"Como {a_val} está multiplicando a 'x', dividimos ambos lados entre {a_val} para obtener el valor unitario de 'x'.",
            source_breakdown=f"El numerador {diff} es el resultado del paso anterior y el denominador {a_val} es el coeficiente original de x.",
            blocks=[
                VisualBlock(block_type="box", content="x", id="var_final"),
                VisualBlock(block_type="operator", content="="),
                VisualBlock(block_type="box", content=f"{diff}", id="numerator", label="Numerador"),
                VisualBlock(block_type="operator", content="÷", id="op_div"),
                VisualBlock(block_type="box", content=f"{a_val}", id="denominator", label="Denominador")
            ]
        ))

        # Paso 4: Reducción y solución final
        steps.append(MathStep(
            step_number=4,
            title="Simplificación de la fracción",
            rule_name="Simplificación algebraica de racionales",
            latex=f"x = {sp.latex(sol)}",
            explanation=f"Reduciendo a su mínima expresión obtenemos el valor exacto de x = {sol}.",
            source_breakdown=f"{sol} es la fracción simplificada de {diff}/{a_val}.",
            blocks=[
                VisualBlock(block_type="result", content=f"x = {sol}", id="final_result", highlight=True, label="Solución Exacta")
            ]
        ))

        return SolveResult(
            archetype_id=self.archetype_id,
            title=self.title,
            input_params=params,
            original_latex=original_latex,
            steps=steps,
            final_solutions=[f"x = {sp.latex(sol)}"],
            real_world_context="Calibración de sensores robóticos: Offset = V_out - V_ref. En software: cálculo de complejidad lineal O(n) y balances de carga."
        )
