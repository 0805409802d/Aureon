from typing import Dict, Any
from src.math_engine.base import BaseArchetypeSolver
from src.math_engine.models import SolveResult, MathStep, VisualBlock

class MechanicsStressSolver(BaseArchetypeSolver):
    """
    Arquetipo Didáctico: Esfuerzo Normal, Deformación Unitaria y Ley de Hooke.
    Área: Ingeniería Mecánica y Robótica Estructural
    Fórmulas:
    - Esfuerzo Normal: sigma = F / A
    - Deformación Unitaria: epsilon = delta_L / L0
    - Módulo de Elasticidad (Young): E = sigma / epsilon  => delta_L = (F * L0) / (A * E)
    """

    archetype_id = "mechanics_hooke_stress"
    title = "Esfuerzo, Deformación y Ley de Hooke (Mecánica)"
    default_params = {
        "force_n": 50000.0,       # Fuerza aplicada en Newtons (50 kN)
        "area_mm2": 250.0,        # Área de la sección transversal en mm²
        "initial_len_m": 2.0,     # Longitud inicial L0 en metros
        "young_modulus_gpa": 200.0 # Módulo de Young en GPa (Acero estructural = 200 GPa)
    }

    def solve(self, params: Dict[str, Any]) -> SolveResult:
        F = float(params.get("force_n", 50000.0))
        A_mm2 = float(params.get("area_mm2", 250.0))
        L0 = float(params.get("initial_len_m", 2.0))
        E_gpa = float(params.get("young_modulus_gpa", 200.0))

        # Conversiones al SI
        A_m2 = A_mm2 * 1e-6
        E_pa = E_gpa * 1e9

        # Paso 1: Esfuerzo normal (sigma = F / A)
        sigma_pa = F / A_m2
        sigma_mpa = sigma_pa / 1e6

        # Paso 2: Deformación unitaria (epsilon = sigma / E)
        epsilon = sigma_pa / E_pa

        # Paso 3: Alargamiento total (delta_L = epsilon * L0)
        delta_L_m = epsilon * L0
        delta_L_mm = delta_L_m * 1000.0

        original_latex = r"\sigma = \frac{F}{A}, \quad \epsilon = \frac{\sigma}{E}, \quad \Delta L = \frac{F \cdot L_0}{A \cdot E}"

        step1 = MathStep(
            step_number=1,
            title="Cálculo del Esfuerzo Normal Axial (σ)",
            rule_name="Definición de Tensión Mecánica",
            latex=f"\\sigma = \\frac{{{F}\\text{{ N}}}}{{{A_mm2}\\times 10^{{-6}}\\text{{ m}}^2}} = {sigma_mpa:.2f}\\text{{ MPa}}",
            explanation=f"Se distribuye la carga axial {F} N sobre el área resistente {A_mm2} mm². El esfuerzo resultante es {sigma_mpa:.2f} MPa.",
            source_breakdown=f"Fuerza {F} dividida por sección en m² {A_m2:.6f}.",
            blocks=[
                VisualBlock(block_type="box", content=f"F={F} N"),
                VisualBlock(block_type="operator", content="÷"),
                VisualBlock(block_type="box", content=f"A={A_mm2} mm²"),
                VisualBlock(block_type="result", content=f"σ={sigma_mpa:.2f} MPa", highlight=True)
            ]
        )

        step2 = MathStep(
            step_number=2,
            title="Deformación Elástica Unitaria (ε)",
            rule_name="Ley de Hooke Unidimensional",
            latex=f"\\epsilon = \\frac{{{sigma_mpa:.2f}\\times 10^6\\text{{ Pa}}}}{{{E_gpa}\\times 10^9\\text{{ Pa}}}} = {epsilon:.6f}\\text{{ (adimensional)}}",
            explanation=f"Bajo el régimen elástico lineal, la deformación relativa es directamente proporcional al esfuerzo e inversamente proporcional a la rigidez del material E={E_gpa} GPa.",
            source_breakdown=f"Esfuerzo {sigma_pa:.1f} Pa dividido entre {E_pa:.1e} Pa.",
            blocks=[
                VisualBlock(block_type="box", content=f"σ={sigma_mpa:.2f} MPa"),
                VisualBlock(block_type="operator", content="÷"),
                VisualBlock(block_type="box", content=f"E={E_gpa} GPa"),
                VisualBlock(block_type="result", content=f"ε={epsilon:.6f}", highlight=True)
            ]
        )

        step3 = MathStep(
            step_number=3,
            title="Alargamiento Total de la Barra (ΔL)",
            rule_name="Integración Cinemática Elástica",
            latex=f"\\Delta L = ({epsilon:.6f}) \\times ({L0}\\text{{ m}}) = {delta_L_mm:.3f}\\text{{ mm}}",
            explanation=f"La elongación dimensional neta sufrida por la pieza bajo carga es de {delta_L_mm:.3f} mm sobre una longitud original de {L0} m.",
            source_breakdown=f"Deformación unitaria {epsilon:.6f} multiplicada por longitud {L0} m y convertida a mm.",
            blocks=[
                VisualBlock(block_type="box", content=f"ε={epsilon:.6f}"),
                VisualBlock(block_type="operator", content="×"),
                VisualBlock(block_type="box", content=f"L₀={L0} m"),
                VisualBlock(block_type="result", content=f"ΔL={delta_L_mm:.3f} mm", highlight=True)
            ]
        )

        return SolveResult(
            archetype_id=self.archetype_id,
            title=self.title,
            input_params=params,
            original_latex=original_latex,
            steps=[step1, step2, step3],
            final_solutions=[f"\\sigma = {sigma_mpa:.2f}\\text{{ MPa}}", f"\\Delta L = {delta_L_mm:.3f}\\text{{ mm}}", f"\\epsilon = {epsilon:.6f}"],
            real_world_context=(
                "Indispensable en diseño de eslabones y brazos robóticos, chasis automotrices, "
                "mecanismos aeroespaciales y prevención de falla estructural por fatiga o fluencia."
            )
        )
