import sympy as sp
from typing import Dict, Any
from src.math_engine.base import BaseArchetypeSolver
from src.math_engine.models import SolveResult, MathStep, VisualBlock

class CsModuloEuclidSolver(BaseArchetypeSolver):
    archetype_id = "cs_modulo_euclid"
    title = "Algoritmo de Euclides y Aritmética Modular (CS / Criptografía)"
    default_params = {"a": 252, "b": 105}

    def solve(self, params: Dict[str, Any]) -> SolveResult:
        a_orig = int(params.get("a", 252))
        b_orig = int(params.get("b", 105))

        if a_orig <= 0 or b_orig <= 0:
            raise ValueError("Ambos números deben ser enteros positivos mayores a cero.")

        # Ordenar a >= b
        a = max(a_orig, b_orig)
        b = min(a_orig, b_orig)

        original_latex = f"\\gcd({a}, {b}) \\quad \\text{{y}} \\quad {a} \\pmod{{{b}}}"

        steps = []
        step_num = 1
        curr_a = a
        curr_b = b

        while curr_b != 0:
            q = curr_a // curr_b
            r = curr_a % curr_b

            steps.append(MathStep(
                step_number=step_num,
                title=f"División Euclidiana: {curr_a} entre {curr_b}",
                rule_name="Teorema de la División: a = b · q + r (0 ≤ r < b)",
                latex=f"{curr_a} = ({curr_b}) \\cdot ({q}) + {r} \\implies {curr_a} \\equiv {r} \\pmod{{{curr_b}}}",
                explanation=f"Dividimos {curr_a} entre {curr_b}: cociente q = {q} y residuo r = {r}.",
                source_breakdown=f"Cociente q={q} (cuántas veces cabe {curr_b} en {curr_a}), Residuo r={r} ({curr_a} - {curr_b}*{q}).",
                blocks=[
                    VisualBlock(block_type="box", content=f"a = {curr_a}", label="Dividendo"),
                    VisualBlock(block_type="operator", content="="),
                    VisualBlock(block_type="box", content=f"b = {curr_b}", label="Divisor"),
                    VisualBlock(block_type="operator", content="×"),
                    VisualBlock(block_type="box", content=f"q = {q}", label="Cociente"),
                    VisualBlock(block_type="operator", content="+"),
                    VisualBlock(block_type="result", content=f"r = {r}", highlight=True, label="Residuo")
                ]
            ))

            if r == 0:
                gcd_val = curr_b
                break

            curr_a = curr_b
            curr_b = r
            step_num += 1

        # Paso final de conclusión
        steps.append(MathStep(
            step_number=step_num + 1,
            title=f"Identificación del Máximo Común Divisor: MCD = {gcd_val}",
            rule_name="Criterio de Terminación de Euclides",
            latex=f"\\gcd({a_orig}, {b_orig}) = {gcd_val}",
            explanation=f"Como el último residuo no nulo fue {gcd_val}, ese es el Máximo Común Divisor entre {a_orig} y {b_orig}.",
            source_breakdown="El MCD es el último divisor que produjo residuo cero.",
            blocks=[
                VisualBlock(block_type="result", content=f"MCD = {gcd_val}", highlight=True, label="Resultado Final")
            ]
        ))

        return SolveResult(
            archetype_id=self.archetype_id,
            title=self.title,
            input_params=params,
            original_latex=original_latex,
            steps=steps,
            final_solutions=[f"MCD({a_orig}, {b_orig}) = {gcd_val}", f"{a_orig} mod {b_orig} = {a_orig % b_orig}"],
            real_world_context="Criptografía RSA: Generación de llaves públicas y privadas (cálculo del inverso multiplicativo con Euclides extendido). Ciencias de la Computación: Tablas Hash y generadores de números pseudoaleatorios congruenciales."
        )
