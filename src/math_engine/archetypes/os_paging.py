from typing import Dict, Any
from src.math_engine.base import BaseArchetypeSolver
from src.math_engine.models import SolveResult, MathStep, VisualBlock

class OsPagingSolver(BaseArchetypeSolver):
    """
    Arquetipo Didáctico: Paginación de Memoria Virtual y Traducción de Direcciones.
    Área: Sistemas Operativos
    Fórmulas:
    - Número de Página = Virtual_Address // Page_Size
    - Offset = Virtual_Address % Page_Size
    - Physical_Address = (Frame_Number * Page_Size) + Offset
    """

    archetype_id = "os_paging_translation"
    title = "Paginación y Memoria Virtual (Sistemas Operativos)"
    default_params = {
        "virtual_address": 10500, # Dirección virtual en bytes
        "page_size": 4096,        # Tamaño de página (4KB estándar)
        "frame_number": 7         # Marco físico asignado en la tabla de páginas
    }

    def solve(self, params: Dict[str, Any]) -> SolveResult:
        va = int(params.get("virtual_address", 10500))
        page_size = int(params.get("page_size", 4096))
        frame_num = int(params.get("frame_number", 7))

        # Paso 1: Número de página (VPN)
        vpn = va // page_size

        # Paso 2: Offset (Desplazamiento)
        offset = va % page_size

        # Paso 3: Dirección Física (PA)
        pa = (frame_num * page_size) + offset

        original_latex = r"VA = (p \times S) + d \implies PA = (f \times S) + d"

        step1 = MathStep(
            step_number=1,
            title="Extracción del Número de Página Virtual (VPN)",
            rule_name="División Entera por Tamaño de Página",
            latex=f"p = \\lfloor \\frac{{{va}}}{{{page_size}}} \\rfloor = {vpn}",
            explanation=f"La MMU (Memory Management Unit) divide la dirección virtual {va} entre el tamaño de página {page_size} bytes (4KB) para indexar la Page Table.",
            source_breakdown=f"{va} dividido entre {page_size} da cociente entero {vpn}.",
            blocks=[
                VisualBlock(block_type="box", content=f"VA={va}"),
                VisualBlock(block_type="operator", content="÷"),
                VisualBlock(block_type="box", content=f"PageSize={page_size}"),
                VisualBlock(block_type="result", content=f"Página p={vpn}", highlight=True)
            ]
        )

        step2 = MathStep(
            step_number=2,
            title="Cálculo del Desplazamiento (Offset d)",
            rule_name="Operación Módulo Residual",
            latex=f"d = {va} \\pmod{{{page_size}}} = {offset}",
            explanation=f"El offset dentro de la página permanece invariante tanto en la memoria virtual como en la memoria RAM física.",
            source_breakdown=f"Residuo de {va} % {page_size} = {offset} bytes.",
            blocks=[
                VisualBlock(block_type="box", content=f"VA={va}"),
                VisualBlock(block_type="operator", content="mod"),
                VisualBlock(block_type="box", content=f"{page_size}"),
                VisualBlock(block_type="result", content=f"Offset d={offset}", highlight=True)
            ]
        )

        step3 = MathStep(
            step_number=3,
            title="Traducción a Dirección Física en Memoria RAM (Physical Address)",
            rule_name="Mapeo de Marco (Frame) y Adición de Offset",
            latex=f"PA = ({frame_num} \\times {page_size}) + {offset} = {frame_num * page_size} + {offset} = {pa}",
            explanation=f"La tabla de páginas mapeó la página {vpn} al frame físico {frame_num}. Multiplicando por {page_size} y sumando el offset {offset}, el bus de datos accede a la celda física {pa}.",
            source_breakdown=f"Base física ({frame_num} * {page_size}) = {frame_num * page_size}, sumando {offset} da {pa}.",
            blocks=[
                VisualBlock(block_type="box", content=f"Marco f={frame_num}"),
                VisualBlock(block_type="operator", content="×"),
                VisualBlock(block_type="box", content=f"S={page_size}"),
                VisualBlock(block_type="operator", content="+"),
                VisualBlock(block_type="box", content=f"d={offset}"),
                VisualBlock(block_type="result", content=f"PA={pa}", highlight=True)
            ]
        )

        return SolveResult(
            archetype_id=self.archetype_id,
            title=self.title,
            input_params=params,
            original_latex=original_latex,
            steps=[step1, step2, step3],
            final_solutions=[f"PA = {pa}", f"p = {vpn}", f"d = {offset}"],
            real_world_context=(
                "Núcleo de los sistemas operativos modernos (Linux, Windows, macOS, Android). "
                "Permite el aislamiento seguro de procesos, memoria virtual protegida, swap y TLB."
            )
        )
