from typing import Dict, Any
from src.math_engine.base import BaseArchetypeSolver
from src.math_engine.models import SolveResult, MathStep, VisualBlock

class NanoSchrodingerSolver(BaseArchetypeSolver):
    archetype_id = "nano_schrodinger_infinite_well"
    title = "Pozo de Potencial Cuántico 1D (Nanotecnología / Puntos Cuánticos)"
    default_params = {"n": 1, "L_nm": 1.0, "mass_ratio": 1.0}

    def solve(self, params: Dict[str, Any]) -> SolveResult:
        n = int(params.get("n", 1))
        l_nm = float(params.get("L_nm", 1.0))
        mass_ratio = float(params.get("mass_ratio", 1.0))

        if n <= 0:
            raise ValueError("El número cuántico 'n' debe ser un entero positivo (1, 2, 3, ...).")
        if l_nm <= 0:
            raise ValueError("El ancho del pozo 'L_nm' debe ser mayor a cero.")
        if mass_ratio <= 0:
            raise ValueError("La masa relativa 'mass_ratio' debe ser mayor a cero.")

        # Constantes fundamentales
        h = 6.62607015e-34    # J*s
        m_e = 9.1093837e-31   # kg
        m = mass_ratio * m_e
        l_meters = l_nm * 1e-9 # nm a metros
        ev_joule = 1.602176634e-19

        original_latex = r"E_n = \frac{n^2 h^2}{8 m L^2} \quad (\text{Niveles de Energía Cuantizados})"

        steps = []

        # Paso 1: Conversión de escala nanométrica al Sistema Internacional
        steps.append(MathStep(
            step_number=1,
            title=f"Conversión de dimensiones a escala nanométrica (L = {l_nm} nm)",
            rule_name="Condición de frontera cuántica: ψ(0) = ψ(L) = 0",
            latex=f"L = {l_nm} \\text{{ nm}} = {l_meters:.2e} \\text{{ m}}, \\quad m = ({mass_ratio}) \\cdot m_e = {m:.3e} \\text{{ kg}}",
            explanation=f"A escala nano ({l_nm} nm), los electrones están confinados espacialmente y sus niveles de energía dejan de ser continuos y se cuantizan.",
            source_breakdown=f"L = {l_nm} * 10^-9 m, masa m = {mass_ratio} * 9.11e-31 kg.",
            blocks=[
                VisualBlock(block_type="box", content=f"L = {l_nm} nm", label="Ancho del Pozo"),
                VisualBlock(block_type="box", content=f"n = {n}", label="Nivel Cuántico"),
                VisualBlock(block_type="box", content=f"m = {mass_ratio} m_e", label="Masa efectiva")
            ]
        ))

        # Paso 2: Cálculo del denominador 8 * m * L²
        l_sq = l_meters**2
        denom = 8 * m * l_sq
        steps.append(MathStep(
            step_number=2,
            title="Cálculo del factor de confinamiento espacial (8 · m · L²)",
            rule_name="Término geométrico de confinamiento cuántico",
            latex=f"8 m L^2 = 8 \\cdot ({m:.2e}) \\cdot ({l_meters:.2e})^2 = {denom:.3e} \\text{{ J}} \\cdot \\text{{s}}^2",
            explanation="A menor tamaño de la nanopartícula (menor L), el denominador se vuelve mucho más pequeño y la energía del electrón se dispara.",
            source_breakdown=f"8 * {m:.2e} * ({l_meters:.2e})^2 = {denom:.3e}.",
            blocks=[
                VisualBlock(block_type="box", content=f"L² = {l_sq:.2e} m²"),
                VisualBlock(block_type="operator", content="×"),
                VisualBlock(block_type="box", content=f"8m = {8*m:.2e} kg"),
                VisualBlock(block_type="operator", content="="),
                VisualBlock(block_type="result", content=f"{denom:.2e}", highlight=True)
            ]
        ))

        # Paso 3: Cálculo de la energía en Julios y conversión a Electronvoltios (eV)
        h_sq = h**2
        n_sq = n**2
        e_joules = (n_sq * h_sq) / denom
        e_ev = e_joules / ev_joule

        steps.append(MathStep(
            step_number=3,
            title=f"Energía del nivel cuántico n = {n} (En Electronvoltios)",
            rule_name="Energía de Confinamiento Cuántico de Schrödinger",
            latex=f"E_{{{n}}} = \\frac{{({n})^2 \\cdot (6.626 \\times 10^{{-34}})^2}}{{{denom:.2e}}} = {e_joules:.3e} \\text{{ J}} = {e_ev:.3f} \\text{{ eV}}",
            explanation=f"Para n={n}, el electrón posee una energía discreta de {e_ev:.3f} eV. El electrón no puede existir con energías intermedias.",
            source_breakdown=f"E = ({n}^2 * h^2) / (8*m*L^2) = {e_joules:.2e} J / 1.6e-19 = {e_ev:.3f} eV.",
            blocks=[
                VisualBlock(block_type="box", content=f"n² = {n_sq}"),
                VisualBlock(block_type="operator", content="×"),
                VisualBlock(block_type="box", content="h² ≈ 4.39×10⁻⁶⁷"),
                VisualBlock(block_type="operator", content="÷"),
                VisualBlock(block_type="box", content=f"8mL² = {denom:.2e}"),
                VisualBlock(block_type="operator", content="="),
                VisualBlock(block_type="result", content=f"E_{n} = {e_ev:.3f} eV", highlight=True)
            ]
        ))

        # Paso 4: Brecha de energía y fotón emitido (transición n -> n-1)
        if n > 1:
            e_lower_ev = (1**2 * h_sq / denom) / ev_joule
            delta_e = e_ev - e_lower_ev
            lambda_nm = (1239.84 / delta_e) if delta_e > 0 else 0
            steps.append(MathStep(
                step_number=4,
                title=f"Emisión de Fotón por Salto Cuántico (n={n} → n=1)",
                rule_name="Ley de Planck-Einstein: ΔE = h · c / λ",
                latex=f"\\Delta E = E_{{{n}}} - E_1 = {e_ev:.3f} - {e_lower_ev:.3f} = {delta_e:.3f} \\text{{ eV}} \\implies \\lambda = \\frac{{1240}}{{\\Delta E}} = {lambda_nm:.1f} \\text{{ nm}}",
                explanation=f"Al decaer al nivel fundamental, la nanopartícula emite un fotón de {lambda_nm:.1f} nm de longitud de onda (Luz coloreada en Quantum Dots).",
                source_breakdown=f"ΔE = {delta_e:.3f} eV, λ = 1240 / {delta_e:.3f} = {lambda_nm:.1f} nm.",
                blocks=[
                    VisualBlock(block_type="result", content=f"ΔE = {delta_e:.3f} eV", highlight=True),
                    VisualBlock(block_type="result", content=f"Longitud de onda λ = {lambda_nm:.1f} nm", highlight=True)
                ]
            ))
            final_solutions = [f"E_{n} = {e_ev:.3f} eV", f"ΔE (salto a n=1) = {delta_e:.3f} eV ({lambda_nm:.1f} nm)"]
        else:
            steps.append(MathStep(
                step_number=4,
                title="Estado Fundamental (Ground State n = 1)",
                rule_name="Principio de Incertidumbre de Heisenberg: E_zero > 0",
                latex=r"E_{\text{zero-point}} = E_1 > 0 \implies \text{El electrón nunca puede estar completamente en reposo dentro del nanoporo}",
                explanation="Incluso a cero absoluto (0 Kelvin), el electrón retiene esta energía de punto cero debido al confinamiento cuántico.",
                source_breakdown="Consecuencia directa del confinamiento espacial cuántico.",
                blocks=[VisualBlock(block_type="result", content=f"Energía de Punto Cero = {e_ev:.3f} eV", highlight=True)]
            ))
            final_solutions = [f"E_1 = {e_ev:.3f} eV (Estado Fundamental)"]

        return SolveResult(
            archetype_id=self.archetype_id,
            title=self.title,
            input_params=params,
            original_latex=original_latex,
            steps=steps,
            final_solutions=final_solutions,
            real_world_context="Nanotecnología: Puntos Cuánticos (QLEDs para pantallas de televisión y microscopía fluorescente), transistores de nanoalambres y celdas solares nanoestructuradas."
        )
