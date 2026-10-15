import sympy as sp
from typing import Dict, Any
from src.math_engine.base import BaseArchetypeSolver
from src.math_engine.models import SolveResult, MathStep, VisualBlock

class BaldorQuadraticSolver(BaseArchetypeSolver):
    archetype_id = "baldor_quadratic_eq"
    title = "Ecuación Cuadrática Completa (Fórmula General)"
    default_params = {"a": 1, "b": -5, "c": 6}

    def solve(self, params: Dict[str, Any]) -> SolveResult:
        a_val = sp.Rational(str(params.get("a", 1)))
        b_val = sp.Rational(str(params.get("b", -5)))
        c_val = sp.Rational(str(params.get("c", 6)))

        if a_val == 0:
            raise ValueError("El coeficiente 'a' no puede ser 0 en una ecuación cuadrática (sería lineal).")

        x = sp.Symbol('x')
        eq_orig = sp.Eq(a_val * x**2 + b_val * x + c_val, 0)
        original_latex = sp.latex(eq_orig)

        steps = []

        # Paso 1: Coeficientes
        steps.append(MathStep(
            step_number=1,
            title="Identificación de Coeficientes de la forma canónica ax² + bx + c = 0",
            rule_name="Forma Canónica Cuadrática",
            latex=f"a = {sp.latex(a_val)}, \\quad b = {sp.latex(b_val)}, \\quad c = {sp.latex(c_val)}",
            explanation=f"Identificamos el término cuadrático a={a_val}, el término lineal b={b_val} y el término independiente c={c_val}.",
            source_breakdown="Son los coeficientes asignados directamente en la ecuación cuadrática.",
            blocks=[
                VisualBlock(block_type="box", content=f"a = {a_val}", id="coef_a", label="Cuadrático"),
                VisualBlock(block_type="box", content=f"b = {b_val}", id="coef_b", label="Lineal"),
                VisualBlock(block_type="box", content=f"c = {c_val}", id="coef_c", label="Independiente")
            ]
        ))

        # Paso 2: Discriminante Δ = b² - 4ac
        b_sq = b_val**2
        four_ac = 4 * a_val * c_val
        discriminant = b_sq - four_ac

        steps.append(MathStep(
            step_number=2,
            title="Cálculo del Discriminante (Δ = b² - 4ac)",
            rule_name="Discriminante Polinomial",
            latex=f"\\Delta = ({sp.latex(b_val)})^2 - 4({sp.latex(a_val)})({sp.latex(c_val)}) = {sp.latex(b_sq)} - ({sp.latex(four_ac)}) = {sp.latex(discriminant)}",
            explanation=f"Calculamos b² = ({b_val})² = {b_sq} y le restamos 4ac = 4({a_val})({c_val}) = {four_ac}. El resultado es {discriminant}.",
            source_breakdown=f"El {b_sq} sale de ({b_val})², el {four_ac} sale de multiplicar 4×({a_val})×({c_val}), y la resta {b_sq} - {four_ac} resulta en {discriminant}.",
            blocks=[
                VisualBlock(block_type="box", content=f"b² = {b_sq}", id="term_b2"),
                VisualBlock(block_type="operator", content="-"),
                VisualBlock(block_type="box", content=f"4ac = {four_ac}", id="term_4ac"),
                VisualBlock(block_type="operator", content="="),
                VisualBlock(block_type="result", content=f"Δ = {discriminant}", id="discriminant_val", highlight=True)
            ]
        ))

        # Paso 3: Análisis del tipo de soluciones
        if discriminant > 0:
            nature = "El discriminante es mayor a cero (Δ > 0): existen dos raíces reales y distintas."
        elif discriminant == 0:
            nature = "El discriminante es igual a cero (Δ = 0): existe una única raíz real repetida (raíz doble)."
        else:
            nature = "El discriminante es negativo (Δ < 0): existen dos raíces complejas conjugadas (involucran la unidad imaginaria i)."

        steps.append(MathStep(
            step_number=3,
            title="Análisis de la naturaleza de las raíces",
            rule_name="Criterio del Discriminante",
            latex=f"\\Delta = {sp.latex(discriminant)} \\implies {sp.latex(sp.Symbol('Soluciones:'))} \\text{{ {nature} }}",
            explanation=nature,
            source_breakdown=f"Depende exclusivamente del signo de Δ={discriminant}.",
            blocks=[
                VisualBlock(block_type="box", content=nature, id="root_nature", highlight=True)
            ]
        ))

        # Paso 4: Sustitución en la Fórmula General
        # x = (-b ± sqrt(Δ)) / (2a)
        neg_b = -b_val
        two_a = 2 * a_val
        sqrt_disc = sp.sqrt(discriminant)

        explanation_step4 = (
            f"Aplicamos la Fórmula Resolvente General: x = (-b ± √(Δ)) / (2a).\n\n"
            f"• ¿De dónde sale esta fórmula?: Proviene de completar el trinomio cuadrado perfecto en ax² + bx + c = 0.\n"
            f"• ¿Por qué hay una raíz cuadrada?: Para despejar una incógnita que está elevada al cuadrado (x + b/2a)², se debe aplicar la operación inversa a ambos miembros, que es la raíz cuadrada (±√).\n"
            f"• ¿Por qué parece que no se usa el término c={c_val}?: ¡El número {c_val} SÍ se utilizó! Se calculó en el Paso 2 dentro del discriminante: Δ = ({b_val})² - 4({a_val})({c_val}) = {b_sq} - {four_ac} = {discriminant}. Por eso aquí ya solo colocamos √({discriminant}) directamente en lugar de repetir la cuenta.\n"
            f"• Denominador: 2a = 2({a_val}) = {two_a}."
        )

        steps.append(MathStep(
            step_number=4,
            title="Sustitución en la Fórmula Resolvente General: x = (-b ± √Δ) / 2a",
            rule_name="Fórmula de Bhaskara / Deducción por Completación de Cuadrados",
            latex=f"x = \\frac{{-({sp.latex(b_val)}) \\pm \\sqrt{{{sp.latex(discriminant)}}}}}{{2({sp.latex(a_val)})}} = \\frac{{{sp.latex(neg_b)} \\pm \\sqrt{{{sp.latex(discriminant)}}}}}{{{sp.latex(two_a)}}}",
            explanation=explanation_step4,
            source_breakdown=(
                f"El término -b es el opuesto de ({b_val}) = {neg_b}. "
                f"Dentro de la raíz se coloca el discriminante Δ = {discriminant} (el cual absorbió a c={c_val} en el Paso 2). "
                f"El denominador es 2·a = 2({a_val}) = {two_a}."
            ),
            blocks=[
                VisualBlock(block_type="box", content=f"-b = {neg_b}", id="neg_b"),
                VisualBlock(block_type="operator", content="±"),
                VisualBlock(block_type="box", content=f"√({discriminant})", id="sqrt_term", label=f"Contiene a c={c_val}"),
                VisualBlock(block_type="operator", content="÷", label="División por denominador"),
                VisualBlock(block_type="box", content=f"2a = {two_a}", id="two_a", label="Denominador")
            ]
        ))


        # Paso 5: Cálculo individual de x1 y x2
        x1 = (neg_b + sqrt_disc) / two_a
        x2 = (neg_b - sqrt_disc) / two_a

        steps.append(MathStep(
            step_number=5,
            title="Cálculo de las dos raíces (x₁ y x₂)",
            rule_name="Bifurcación por signo (±)",
            latex=f"x_1 = \\frac{{{sp.latex(neg_b)} + {sp.latex(sqrt_disc)}}}{{{sp.latex(two_a)}}} = {sp.latex(x1)}, \\quad x_2 = \\frac{{{sp.latex(neg_b)} - {sp.latex(sqrt_disc)}}}{{{sp.latex(two_a)}}} = {sp.latex(x2)}",
            explanation=f"Para x₁ tomamos el signo positivo (+), dando {x1}. Para x₂ tomamos el signo negativo (-), dando {x2}.",
            source_breakdown=f"x₁ = ({neg_b} + {sqrt_disc}) / {two_a} = {x1}; x₂ = ({neg_b} - {sqrt_disc}) / {two_a} = {x2}.",
            blocks=[
                VisualBlock(block_type="result", content=f"x₁ = {x1}", id="root_x1", highlight=True),
                VisualBlock(block_type="result", content=f"x₂ = {x2}", id="root_x2", highlight=True)
            ]
        ))

        return SolveResult(
            archetype_id=self.archetype_id,
            title=self.title,
            input_params=params,
            original_latex=original_latex,
            steps=steps,
            final_solutions=[f"x_1 = {sp.latex(x1)}", f"x_2 = {sp.latex(x2)}"],
            real_world_context="Robótica: Trayectoria balística y curvas de frenado. Computación: Algoritmos O(n²) y árboles balanceados. Nuclear: Balance de reactividad cuadrática."
        )
