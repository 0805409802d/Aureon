import sympy as sp
from typing import Dict, Any
from src.math_engine.base import BaseArchetypeSolver
from src.math_engine.models import SolveResult, MathStep, VisualBlock

class AiBackpropSolver(BaseArchetypeSolver):
    """
    Arquetipo Didáctico: Retropropagación y Gradiente Descendente en Redes Neuronales.
    Área: Inteligencia Artificial
    Cálculo de la derivada de la función de coste con respecto al peso: dL/dw = (y_pred - y_true) * x
    """

    archetype_id = "ai_backprop_grad"
    title = "Retropropagación y Gradiente Descendente (IA)"
    default_params = {
        "x": 2.0,      # Entrada de la neurona
        "w": 0.5,      # Peso inicial
        "b": 0.1,      # Sesgo (bias)
        "y_true": 1.0, # Etiqueta real deseada
        "lr": 0.1      # Tasa de aprendizaje (learning rate eta)
    }

    def solve(self, params: Dict[str, Any]) -> SolveResult:
        x_val = float(params.get("x", 2.0))
        w_val = float(params.get("w", 0.5))
        b_val = float(params.get("b", 0.1))
        y_true = float(params.get("y_true", 1.0))
        lr = float(params.get("lr", 0.1))

        # Paso 1: Forward Pass (Pre-activación z = w*x + b)
        z = w_val * x_val + b_val
        y_pred = z # Neurona lineal para análisis limpio
        loss = 0.5 * (y_pred - y_true) ** 2

        # Paso 2: Derivada de la pérdida respecto a z: dL/dz = (y_pred - y_true)
        dL_dz = y_pred - y_true

        # Paso 3: Derivada de z respecto al peso w: dz/dw = x
        dz_dw = x_val

        # Paso 4: Regla de la Cadena: dL/dw = dL/dz * dz/dw
        grad_w = dL_dz * dz_dw

        # Paso 5: Actualización del peso por Descenso de Gradiente: w_new = w - lr * grad_w
        w_new = w_val - lr * grad_w

        original_latex = r"L = \frac{1}{2}(\hat{y} - y)^2, \quad \hat{y} = w \cdot x + b, \quad w \leftarrow w - \eta \frac{\partial L}{\partial w}"

        step1 = MathStep(
            step_number=1,
            title="Propagación Hacia Adelante (Forward Pass)",
            rule_name="Combinación Lineal y Salida",
            latex=f"\\hat{{y}} = ({w_val} \\times {x_val}) + {b_val} = {z:.4f}",
            explanation=f"Se calcula la activación de la neurona. Con entrada x={x_val}, peso w={w_val} y sesgo b={b_val}, la predicción es y_pred = {y_pred:.4f}.",
            source_breakdown=f"Multiplicación de peso w={w_val} por entrada x={x_val} sumando sesgo b={b_val}.",
            blocks=[
                VisualBlock(block_type="box", content=f"w={w_val}"),
                VisualBlock(block_type="operator", content="×"),
                VisualBlock(block_type="box", content=f"x={x_val}"),
                VisualBlock(block_type="operator", content="+"),
                VisualBlock(block_type="box", content=f"b={b_val}"),
                VisualBlock(block_type="result", content=f"ŷ={y_pred:.4f}", highlight=True)
            ]
        )

        step2 = MathStep(
            step_number=2,
            title="Cálculo del Error Cuadrático Medio (Loss)",
            rule_name="Función de Coste MSE",
            latex=f"L = \\frac{{1}}{{2}}({y_pred:.4f} - {y_true})^2 = {loss:.6f}",
            explanation=f"La función de pérdida cuantifica la discrepancia entre la predicción y el valor real objetivo ({y_true}).",
            source_breakdown=f"La diferencia de error es ({y_pred:.4f} - {y_true}) = {dL_dz:.4f}. Elevada al cuadrado y dividida entre 2 da {loss:.6f}.",
            blocks=[
                VisualBlock(block_type="box", content=f"ŷ - y = {dL_dz:.4f}"),
                VisualBlock(block_type="operator", content="→"),
                VisualBlock(block_type="result", content=f"L = {loss:.6f}", highlight=True)
            ]
        )

        step3 = MathStep(
            step_number=3,
            title="Regla de la Cadena y Gradiente del Peso",
            rule_name="Retropropagación (Backpropagation)",
            latex=f"\\frac{{\\partial L}}{{\\partial w}} = \\frac{{\\partial L}}{{\\partial \\hat{{y}}}} \\cdot \\frac{{\\partial \\hat{{y}}}}{{\\partial w}} = ({dL_dz:.4f}) \\times ({x_val}) = {grad_w:.4f}",
            explanation=f"Por la regla de la cadena de cálculo multivariable, el gradiente indica la dirección y pendiente en la que varía la pérdida con respecto al peso.",
            source_breakdown=f"Multiplicación del error residual {dL_dz:.4f} por la entrada {x_val}.",
            blocks=[
                VisualBlock(block_type="box", content=f"dL/dŷ={dL_dz:.4f}"),
                VisualBlock(block_type="operator", content="×"),
                VisualBlock(block_type="box", content=f"dŷ/dw={x_val}"),
                VisualBlock(block_type="result", content=f"∇w = {grad_w:.4f}", highlight=True)
            ]
        )

        step4 = MathStep(
            step_number=4,
            title="Actualización del Peso por Descenso de Gradiente (SGD)",
            rule_name="Regla de Aprendizaje",
            latex=f"w_{{nuevo}} = {w_val} - ({lr} \\times {grad_w:.4f}) = {w_new:.4f}",
            explanation=f"El peso se desplaza en el sentido contrario al gradiente con tasa de aprendizaje η={lr}. El nuevo peso ajustado es {w_new:.4f}.",
            source_breakdown=f"Resta del paso de gradiente: {w_val} - {lr * grad_w:.4f} = {w_new:.4f}.",
            blocks=[
                VisualBlock(block_type="box", content=f"w={w_val}"),
                VisualBlock(block_type="operator", content="-"),
                VisualBlock(block_type="box", content=f"η·∇w={lr * grad_w:.4f}"),
                VisualBlock(block_type="result", content=f"w_nuevo={w_new:.4f}", highlight=True)
            ]
        )

        return SolveResult(
            archetype_id=self.archetype_id,
            title=self.title,
            input_params=params,
            original_latex=original_latex,
            steps=[step1, step2, step3, step4],
            final_solutions=[f"w_{{nuevo}} = {w_new:.4f}", f"L = {loss:.6f}", f"\\nabla_w = {grad_w:.4f}"],
            real_world_context=(
                "Base matemática de todo el Deep Learning moderno: ChatGPT, Gemini, visión por computadora "
                "y robótica autónoma. La retropropagación ajusta billones de parámetros mediante cálculo diferencial."
            )
        )
