import sympy as sp
from typing import Dict, Any
from src.math_engine.base import BaseArchetypeSolver
from src.math_engine.models import SolveResult, MathStep, VisualBlock

class NuclearDecaySolver(BaseArchetypeSolver):
    archetype_id = "physics_nuclear_decay"
    title = "Ley de Decaimiento Radiactivo (Ingeniería Nuclear / Nanotecnología)"
    default_params = {"N0": 1000, "half_life": 5.0, "t": 10.0}

    def solve(self, params: Dict[str, Any]) -> SolveResult:
        n0 = float(params.get("N0", 1000))
        t_half = float(params.get("half_life", 5.0))
        t = float(params.get("t", 10.0))

        if t_half <= 0:
            raise ValueError("La vida media (T_1/2) debe ser mayor a 0.")
        if t < 0:
            raise ValueError("El tiempo transcurrido (t) no puede ser negativo.")

        original_latex = r"N(t) = N_0 \cdot e^{-\lambda t} \quad \text{donde} \quad \lambda = \frac{\ln(2)}{T_{1/2}}"

        steps = []

        # Paso 1: Constante de desintegración lambda
        ln2 = 0.693147
        decay_const = ln2 / t_half
        steps.append(MathStep(
            step_number=1,
            title="Cálculo de la constante de decaimiento (λ)",
            rule_name="Cinética de decaimiento exponencial de primer orden",
            latex=f"\\lambda = \\frac{{\\ln(2)}}{{T_{{1/2}}}} = \\frac{{0.693147}}{{{t_half}}} = {decay_const:.6f} \\text{{ año}}^{{-1}}",
            explanation=f"La constante λ indica la probabilidad de desintegración por unidad de tiempo. Dividimos ln(2) ≈ 0.693147 entre la vida media T_1/2 = {t_half}.",
            source_breakdown=f"ln(2)/{t_half} = {decay_const:.6f}.",
            blocks=[
                VisualBlock(block_type="box", content="ln(2) ≈ 0.693147"),
                VisualBlock(block_type="operator", content="÷"),
                VisualBlock(block_type="box", content=f"T_1/2 = {t_half}"),
                VisualBlock(block_type="operator", content="="),
                VisualBlock(block_type="result", content=f"λ = {decay_const:.6f}", highlight=True)
            ]
        ))

        # Paso 2: Exponente -λ * t
        exponent = -decay_const * t
        steps.append(MathStep(
            step_number=2,
            title="Cálculo del factor de atenuación exponencial (-λ · t)",
            rule_name="Producto de la tasa de decaimiento y el tiempo",
            latex=f"-\\lambda \\cdot t = -({decay_const:.6f}) \\cdot ({t}) = {exponent:.4f}",
            explanation=f"Multiplicamos la constante λ por el tiempo transcurrido t = {t} años con signo negativo.",
            source_breakdown=f"-({decay_const:.6f}) * {t} = {exponent:.4f}.",
            blocks=[
                VisualBlock(block_type="box", content=f"-λ = -{decay_const:.6f}"),
                VisualBlock(block_type="operator", content="×"),
                VisualBlock(block_type="box", content=f"t = {t}"),
                VisualBlock(block_type="operator", content="="),
                VisualBlock(block_type="box", content=f"Exponente = {exponent:.4f}")
            ]
        ))

        # Paso 3: Factor e^(-λ*t) y núcleos restantes N(t)
        import math
        exp_factor = math.exp(exponent)
        n_remaining = n0 * exp_factor
        n_decayed = n0 - n_remaining

        steps.append(MathStep(
            step_number=3,
            title="Sustitución en la fórmula general N(t) = N₀ · e^(-λt)",
            rule_name="Evaluación exponencial",
            latex=f"N({t}) = {n0} \\cdot e^{{{exponent:.4f}}} = {n0} \\cdot {exp_factor:.6f} = {n_remaining:.2f} \\text{{ núcleos}}",
            explanation=f"El factor e^({exponent:.4f}) es {exp_factor:.4f}. Multiplicándolo por los {n0} núcleos iniciales, quedan {n_remaining:.2f} núcleos activos.",
            source_breakdown=f"{n0} * {exp_factor:.6f} = {n_remaining:.2f}.",
            blocks=[
                VisualBlock(block_type="box", content=f"N₀ = {n0}"),
                VisualBlock(block_type="operator", content="×"),
                VisualBlock(block_type="box", content=f"e^({exponent:.4f}) = {exp_factor:.4f}"),
                VisualBlock(block_type="operator", content="="),
                VisualBlock(block_type="result", content=f"N(t) = {n_remaining:.2f}", highlight=True)
            ]
        ))

        # Paso 4: Núcleos transformados o desintegrados
        steps.append(MathStep(
            step_number=4,
            title="Cálculo de núcleos desintegrados (ΔN)",
            rule_name="Conservación del número bariónico / masa",
            latex=f"\\Delta N = N_0 - N(t) = {n0} - {n_remaining:.2f} = {n_decayed:.2f} \\text{{ núcleos desintegrados}}",
            explanation=f"Se han transmutado o emitido partículas correspondientes a {n_decayed:.2f} núcleos ({ (n_decayed/n0)*100:.1f}% de la muestra).",
            source_breakdown=f"{n0} - {n_remaining:.2f} = {n_decayed:.2f}.",
            blocks=[
                VisualBlock(block_type="result", content=f"Desintegrados: {n_decayed:.2f} ({(n_decayed/n0)*100:.1f}%)", highlight=True)
            ]
        ))

        return SolveResult(
            archetype_id=self.archetype_id,
            title=self.title,
            input_params=params,
            original_latex=original_latex,
            steps=steps,
            final_solutions=[f"N({t}) = {n_remaining:.2f} núcleos", f"ΔN = {n_decayed:.2f} desintegrados"],
            real_world_context="Ingeniería Nuclear: Estimación de radiactividad en barras de combustible agotado y blindaje. Nanotecnología: Vida útil de trazadores radiactivos y nanosensores médicos."
        )
