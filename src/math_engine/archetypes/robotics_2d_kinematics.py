import math
from typing import Dict, Any
from src.math_engine.base import BaseArchetypeSolver
from src.math_engine.models import SolveResult, MathStep, VisualBlock

class Robotics2dKinematicsSolver(BaseArchetypeSolver):
    archetype_id = "robotics_2d_kinematics"
    title = "Cinemática Directa de Brazo Robótico 2-DOF (Robótica Industrial)"
    default_params = {"L1": 10.0, "L2": 8.0, "theta1_deg": 30.0, "theta2_deg": 45.0}

    def solve(self, params: Dict[str, Any]) -> SolveResult:
        l1 = float(params.get("L1", 10.0))
        l2 = float(params.get("L2", 8.0))
        th1_deg = float(params.get("theta1_deg", 30.0))
        th2_deg = float(params.get("theta2_deg", 45.0))

        if l1 <= 0 or l2 <= 0:
            raise ValueError("Las longitudes de los eslabones L1 y L2 deben ser mayores a cero.")

        th1_rad = math.radians(th1_deg)
        th12_deg = th1_deg + th2_deg
        th12_rad = math.radians(th12_deg)

        original_latex = (
            r"\begin{cases} "
            r"x = L_1 \cos(\theta_1) + L_2 \cos(\theta_1 + \theta_2) \\ "
            r"y = L_1 \sin(\theta_1) + L_2 \sin(\theta_1 + \theta_2) "
            r"\end{cases}"
        )

        steps = []

        # Paso 1: Conversión de ángulos a radianes y ángulo acumulado
        steps.append(MathStep(
            step_number=1,
            title="Conversión angular y cálculo del ángulo acumulado (θ₁ + θ₂)",
            rule_name="Composición angular en cadenas cinemáticas seriales",
            latex=f"\\theta_1 = {th1_deg}^\\circ = {th1_rad:.4f} \\text{{ rad}}, \\quad \\theta_1 + \\theta_2 = {th1_deg}^\\circ + {th2_deg}^\\circ = {th12_deg}^\\circ = {th12_rad:.4f} \\text{{ rad}}",
            explanation=f"En un robot serial, la orientación del segundo eslabón se suma a la del primero: θ₁₂ = {th1_deg}° + {th2_deg}° = {th12_deg}°.",
            source_breakdown=f"Ángulo 1: {th1_deg}°, Ángulo 2: {th2_deg}°, Suma: {th12_deg}°.",
            blocks=[
                VisualBlock(block_type="box", content=f"θ₁ = {th1_deg}°"),
                VisualBlock(block_type="operator", content="+"),
                VisualBlock(block_type="box", content=f"θ₂ = {th2_deg}°"),
                VisualBlock(block_type="operator", content="="),
                VisualBlock(block_type="result", content=f"θ₁₂ = {th12_deg}°", highlight=True)
            ]
        ))

        # Paso 2: Coordenadas de la primera articulación (Codo)
        x1 = l1 * math.cos(th1_rad)
        y1 = l1 * math.sin(th1_rad)
        steps.append(MathStep(
            step_number=2,
            title="Posición del Codo (Articulación 1): (x₁, y₁)",
            rule_name="Proyección trigonométrica del primer eslabón",
            latex=f"x_1 = {l1} \\cdot \\cos({th1_deg}^\\circ) = {x1:.2f}, \\quad y_1 = {l1} \\cdot \\sin({th1_deg}^\\circ) = {y1:.2f}",
            explanation=f"Multiplicamos L₁={l1} por cos({th1_deg}°)={math.cos(th1_rad):.4f} para x₁, y por sin({th1_deg}°)={math.sin(th1_rad):.4f} para y₁.",
            source_breakdown=f"x₁ = {l1} * {math.cos(th1_rad):.4f} = {x1:.2f}; y₁ = {l1} * {math.sin(th1_rad):.4f} = {y1:.2f}.",
            blocks=[
                VisualBlock(block_type="box", content=f"x₁ = {x1:.2f}", label="Codo X"),
                VisualBlock(block_type="box", content=f"y₁ = {y1:.2f}", label="Codo Y")
            ]
        ))

        # Paso 3: Aporte del segundo eslabón
        dx2 = l2 * math.cos(th12_rad)
        dy2 = l2 * math.sin(th12_rad)
        steps.append(MathStep(
            step_number=3,
            title="Aporte del Segundo Eslabón (Δx₂, Δy₂)",
            rule_name="Proyección del eslabón terminal",
            latex=f"\\Delta x_2 = {l2} \\cdot \\cos({th12_deg}^\\circ) = {dx2:.2f}, \\quad \\Delta y_2 = {l2} \\cdot \\sin({th12_deg}^\\circ) = {dy2:.2f}",
            explanation=f"Calculamos la proyección de L₂={l2} respecto al ángulo acumulado {th12_deg}°.",
            source_breakdown=f"Δx₂ = {l2} * cos({th12_deg}°) = {dx2:.2f}; Δy₂ = {l2} * sin({th12_deg}°) = {dy2:.2f}.",
            blocks=[
                VisualBlock(block_type="box", content=f"Δx₂ = {dx2:.2f}"),
                VisualBlock(block_type="box", content=f"Δy₂ = {dy2:.2f}")
            ]
        ))

        # Paso 4: Posición final del Efector (Pinza / Herramienta)
        x_total = x1 + dx2
        y_total = y1 + dy2
        steps.append(MathStep(
            step_number=4,
            title="Coordenadas Totales del Efector Final (x, y)",
            rule_name="Suma Vectorial de Eslabones",
            latex=f"x = {x1:.2f} + ({dx2:.2f}) = {x_total:.2f}, \\quad y = {y1:.2f} + ({dy2:.2f}) = {y_total:.2f}",
            explanation=f"Sumamos las coordenadas del codo con el desplazamiento del segundo eslabón: Efector en ({x_total:.2f}, {y_total:.2f}).",
            source_breakdown=f"x = {x1:.2f} + {dx2:.2f} = {x_total:.2f}; y = {y1:.2f} + {dy2:.2f} = {y_total:.2f}.",
            blocks=[
                VisualBlock(block_type="result", content=f"X = {x_total:.2f}", highlight=True, label="Posición X"),
                VisualBlock(block_type="result", content=f"Y = {y_total:.2f}", highlight=True, label="Posición Y")
            ]
        ))

        return SolveResult(
            archetype_id=self.archetype_id,
            title=self.title,
            input_params=params,
            original_latex=original_latex,
            steps=steps,
            final_solutions=[f"X = {x_total:.2f} cm", f"Y = {y_total:.2f} cm"],
            real_world_context="Robótica: Control de posición y seguimiento de trayectorias en brazos robóticos industriales (SCARA, KUKA, ABB) y pinzas de ensamblaje automatizado."
        )
