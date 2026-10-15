import sympy as sp
from typing import Dict, Any
from src.math_engine.base import BaseArchetypeSolver
from src.math_engine.models import SolveResult, MathStep, VisualBlock

class BaldorFactoringSolver(BaseArchetypeSolver):
    archetype_id = "baldor_factoring_trinomial"
    title = "Factorización de Trinomio de la forma x² + bx + c"
    default_params = {"b": 7, "c": 10}

    def solve(self, params: Dict[str, Any]) -> SolveResult:
        b_val = sp.Rational(str(params.get("b", 7)))
        c_val = sp.Rational(str(params.get("c", 10)))

        x = sp.Symbol('x')
        poly = x**2 + b_val * x + c_val
        original_latex = f"x^2 + ({sp.latex(b_val)})x + ({sp.latex(c_val)})"

        steps = []

        # Paso 1: Enunciado de la regla de los dos números
        steps.append(MathStep(
            step_number=1,
            title="Búsqueda de los dos números (p y q)",
            rule_name="Regla de Factorización de Trinomio Cuadrático",
            latex=r"x^2 + bx + c = (x + p)(x + q) \quad \text{donde} \quad p + q = b, \quad p \cdot q = c",
            explanation=f"Necesitamos hallar dos números p y q tales que sumados den b={b_val} y multiplicados den c={c_val}.",
            source_breakdown=f"Buscamos: p + q = {b_val} y p * q = {c_val}.",
            blocks=[
                VisualBlock(block_type="box", content=f"p + q = {b_val}", label="Suma requerida"),
                VisualBlock(block_type="box", content=f"p · q = {c_val}", label="Producto requerido")
            ]
        ))

        # Paso 2: Cálculo simbólico de p y q usando las raíces
        # x^2 + bx + c = 0 -> raíces r1, r2 -> factores (x - r1)(x - r2) = (x + p)(x + q) -> p = -r1, q = -r2
        roots = sp.solve(poly, x)
        
        if len(roots) == 2:
            p = -roots[0]
            q = -roots[1]
        elif len(roots) == 1:
            p = -roots[0]
            q = -roots[0]
        else:
            p = None
            q = None

        if p is not None and q is not None:
            factored_expr = (x + p) * (x + q)
            factored_latex = f"(x + {sp.latex(p)})(x + {sp.latex(q)})" if p >= 0 and q >= 0 else f"(x - {sp.latex(abs(p))})(x - {sp.latex(abs(q))})"

            steps.append(MathStep(
                step_number=2,
                title=f"Encontrar los números: p = {p} y q = {q}",
                rule_name="Verificación de pares de factores",
                latex=f"p = {sp.latex(p)}, \\quad q = {sp.latex(q)} \\implies ({sp.latex(p)}) + ({sp.latex(q)}) = {sp.latex(b_val)}, \\quad ({sp.latex(p)})({sp.latex(q)}) = {sp.latex(c_val)}",
                explanation=f"Comprobamos: {p} + {q} = {p+q} (coincide con b) y {p} × {q} = {p*q} (coincide con c).",
                source_breakdown=f"{p} y {q} cumplen simultáneamente ambas condiciones.",
                blocks=[
                    VisualBlock(block_type="box", content=f"p = {p}", highlight=True),
                    VisualBlock(block_type="box", content=f"q = {q}", highlight=True)
                ]
            ))

            steps.append(MathStep(
                step_number=3,
                title="Construcción de los binomios factores",
                rule_name="Expresión factorizada",
                latex=f"x^2 + {sp.latex(b_val)}x + {sp.latex(c_val)} = (x + ({sp.latex(p)}))(x + ({sp.latex(q)}))",
                explanation=f"Reemplazamos p y q en la estructura (x + p)(x + q).",
                source_breakdown="Sustitución directa de los valores calculados.",
                blocks=[
                    VisualBlock(block_type="result", content=f"(x + {p})(x + {q})", highlight=True)
                ]
            ))
            final_sol = [f"(x + {sp.latex(p)})(x + {sp.latex(q)})"]
        else:
            steps.append(MathStep(
                step_number=2,
                title="Trinomio no factorizable en racionales",
                rule_name="Polinomio irreducible sobre Q",
                latex=r"\text{No existen enteros ni racionales p, q que cumplan la condición.}",
                explanation="El trinomio requiere números irracionales o complejos.",
                source_breakdown="Sin solución racional simple.",
                blocks=[VisualBlock(block_type="box", content="Irreducible sobre Q", highlight=True)]
            ))
            final_sol = ["No factorizable en números racionales simples"]

        return SolveResult(
            archetype_id=self.archetype_id,
            title=self.title,
            input_params=params,
            original_latex=original_latex,
            steps=steps,
            final_solutions=final_sol,
            real_world_context="Descomposición de funciones de transferencia en polos para evaluar la estabilidad de un brazo robótico o filtro de audio digital."
        )
