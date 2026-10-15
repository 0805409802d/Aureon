import sympy as sp
from typing import Dict, Any
from src.math_engine.base import BaseArchetypeSolver
from src.math_engine.models import SolveResult, MathStep, VisualBlock

class CalculusDerivativeSolver(BaseArchetypeSolver):
    archetype_id = "calculus_derivative_polynomial"
    title = "Derivada de un Polinomio (Cálculo 1 / Optimización)"
    default_params = {"a": 3, "n": 3, "b": 4, "m": 2, "c": -5, "d": 12, "x0": 2}

    def solve(self, params: Dict[str, Any]) -> SolveResult:
        a_val = sp.Rational(str(params.get("a", 3)))
        n_val = int(params.get("n", 3))
        b_val = sp.Rational(str(params.get("b", 4)))
        m_val = int(params.get("m", 2))
        c_val = sp.Rational(str(params.get("c", -5)))
        d_val = sp.Rational(str(params.get("d", 12)))
        x0_val = sp.Rational(str(params.get("x0", 2)))

        x = sp.Symbol('x')
        f_expr = a_val * x**n_val + b_val * x**m_val + c_val * x + d_val
        original_latex = f"f(x) = {sp.latex(f_expr)}"

        steps = []

        # Paso 1: Enunciado de la regla de la potencia término a término
        steps.append(MathStep(
            step_number=1,
            title="Aplicar la Regla de la Potencia: d/dx [k · xᵖ] = k · p · xᵖ⁻¹",
            rule_name="Regla de la Potencia y Linealidad de la Derivada",
            latex=r"\frac{d}{dx}[f(x)] = \frac{d}{dx}[a x^n] + \frac{d}{dx}[b x^m] + \frac{d}{dx}[c x] + \frac{d}{dx}[d]",
            explanation="La derivada de una suma es la suma de las derivadas. Para cada término multiplicamos el exponente por el coeficiente y restamos 1 al exponente.",
            source_breakdown=f"Términos a derivar: {a_val}x^{n_val}, {b_val}x^{m_val}, {c_val}x, y constante {d_val}.",
            blocks=[
                VisualBlock(block_type="box", content=f"{a_val}x^{n_val}", label="Término 1"),
                VisualBlock(block_type="operator", content="+"),
                VisualBlock(block_type="box", content=f"{b_val}x^{m_val}", label="Término 2"),
                VisualBlock(block_type="operator", content="+"),
                VisualBlock(block_type="box", content=f"{c_val}x", label="Término 3"),
                VisualBlock(block_type="operator", content="+"),
                VisualBlock(block_type="box", content=f"{d_val}", label="Constante")
            ]
        ))

        # Paso 2: Derivación término por término
        term1_coef = a_val * n_val
        term1_exp = n_val - 1
        term2_coef = b_val * m_val
        term2_exp = m_val - 1
        term3_coef = c_val

        f_prime = sp.diff(f_expr, x)

        steps.append(MathStep(
            step_number=2,
            title="Cálculo algebraico de cada coeficiente derivado",
            rule_name="Multiplicación coeficiente × exponente",
            latex=f"f'(x) = ({n_val} \\cdot {sp.latex(a_val)})x^{{{term1_exp}}} + ({m_val} \\cdot {sp.latex(b_val)})x^{{{term2_exp}}} + ({sp.latex(c_val)}) + 0 = {sp.latex(f_prime)}",
            explanation=f"Primer término: {n_val}×{a_val} = {term1_coef} con x^{term1_exp}. Segundo término: {m_val}×{b_val} = {term2_coef} con x^{term2_exp}. Tercer término: {c_val}. La constante {d_val} se deriva a 0.",
            source_breakdown=f"({a_val}*{n_val})={term1_coef}, ({b_val}*{m_val})={term2_coef}, d/dx({c_val}x)={c_val}, d/dx({d_val})=0.",
            blocks=[
                VisualBlock(block_type="box", content=f"{term1_coef}x^{term1_exp}", highlight=True),
                VisualBlock(block_type="operator", content="+"),
                VisualBlock(block_type="box", content=f"{term2_coef}x^{term2_exp}", highlight=True),
                VisualBlock(block_type="operator", content="+"),
                VisualBlock(block_type="box", content=f"{term3_coef}", highlight=True)
            ]
        ))

        # Paso 3: Evaluación en el punto x0
        slope = f_prime.subs(x, x0_val)
        steps.append(MathStep(
            step_number=3,
            title=f"Evaluación en x = {x0_val} (Pendiente de la recta tangente / Velocidad)",
            rule_name="Tasa de Cambio Instantánea",
            latex=f"f'({x0_val}) = {term1_coef}({x0_val})^{{{term1_exp}}} + {term2_coef}({x0_val})^{{{term2_exp}}} + ({term3_coef}) = {sp.latex(slope)}",
            explanation=f"Sustituyendo x={x0_val} obtenemos la pendiente m = {slope}. En física representa la velocidad instantánea; en IA representa la dirección del gradiente.",
            source_breakdown=f"f'({x0_val}) evaluado da exactamente {slope}.",
            blocks=[
                VisualBlock(block_type="result", content=f"f'({x0_val}) = {slope}", id="eval_slope", highlight=True, label="Tasa de Cambio")
            ]
        ))

        return SolveResult(
            archetype_id=self.archetype_id,
            title=self.title,
            input_params=params,
            original_latex=original_latex,
            steps=steps,
            final_solutions=[f"f'(x) = {sp.latex(f_prime)}", f"f'({x0_val}) = {sp.latex(slope)}"],
            real_world_context="Inteligencia Artificial: Algoritmo de Descenso de Gradiente (actualización de pesos W = W - η * dL/dW). Robótica: Cálculo de velocidad y aceleración instantánea de motores."
        )
