"""
Base de Conocimiento y Pedagogía Matemática Universitaria Global.
Modelado de las escuelas matemáticas de Harvard, Stanford/MIT, Moscú (MGU), Tsinghua y École Polytechnique.
Incluye soporte para todas las ramas de la ingeniería:
- Inteligencia Artificial y Machine Learning
- Robótica y Control
- Sistemas Operativos y Computación
- Mecánica de Materiales y Dinámica
- Matemáticas y Física Teórica
"""
import os
from typing import List, Dict, Any, Optional
import math

UNIVERSITY_PEDAGOGIES: Dict[str, Dict[str, Any]] = {
    "stanford": {
        "id": "stanford",
        "name": "Stanford & MIT (EE.UU.)",
        "flag": "🇺🇸",
        "tagline": "Intuición Geométrica, Sistemas Dinámicos y Computación",
        "philosophy": (
            "Enfoque inspirado en Gilbert Strang y Stephen Boyd. Prioriza la intuición visual, "
            "la descomposición en subespacios, la optimización convexa y la aplicación directa "
            "en algoritmos de software, robótica moderna y aprendizaje automático (IA)."
        ),
        "tone": "Directo, intuitivo, enfocado en el 'por qué' operacional y la ingeniería aplicada."
    },
    "moscow": {
        "id": "moscow",
        "name": "Universidad Estatal de Moscú - MGU (Rusia)",
        "flag": "🇷🇺",
        "tagline": "Rigor Analítico Extremo y Escuela Teórica de Landau-Lifshitz",
        "philosophy": (
            "Enfoque de la escuela físico-matemática soviética (Landau, Kolmogorov, Arnold). "
            "Exige deducciones analíticas cerradas, invariancia de coordenadas, análisis de condiciones "
            "de contorno y un entendimiento indestructible de los principios de conservación físicos."
        ),
        "tone": "Profundo, analíticamente riguroso, formal y matemáticamente inquebrantable."
    },
    "tsinghua": {
        "id": "tsinghua",
        "name": "Universidad Tsinghua (China)",
        "flag": "🇨🇳",
        "tagline": "Precisión Algebraica Intensiva y Métodos de Ingeniería de Gran Escala",
        "philosophy": (
            "Enfoque de alta intensidad matemática. Se enfoca en transformaciones algebraicas exactas, "
            "identidades profundas, convergencia estricta y escalabilidad en sistemas de IA, "
            "automatización robótica y supercómputo aeroespacial."
        ),
        "tone": "Metódico, quirúrgicamente preciso, exhaustivo en cada manipulación simbólica."
    },
    "harvard": {
        "id": "harvard",
        "name": "Universidad de Harvard (EE.UU.)",
        "flag": "🇺🇸",
        "tagline": "Fundamentos Axiomáticos, Estructuras Abstractas y Teoremas Universales",
        "philosophy": (
            "Enfoque axiomático y conceptual (Spivak, Rudin). Enfatiza la generalización, "
            "la belleza de las estructuras algebraicas, los teoremas de existencia/unicidad "
            "y la conexión entre ramas aparentemente desconectadas de las matemáticas."
        ),
        "tone": "Elegante, axiomático, centrado en teoremas fundamentales y demostraciones claras."
    },
    "polytechnique": {
        "id": "polytechnique",
        "name": "École Polytechnique (Francia)",
        "flag": "🇫🇷",
        "tagline": "Elegancia Estructural Bourbaki y Geometría Diferencial",
        "philosophy": (
            "Heredera de la tradición Bourbaki y Poincaré. Trata las ecuaciones mediante formas "
            "diferenciales, variedades diferenciables y simetrías continuas en física y robótica."
        ),
        "tone": "Geométrico, de alto nivel abstracto y armónico."
    }
}

# Corpus de Conocimiento Curado para Ingesta en Supabase pgvector
UNIVERSITY_KNOWLEDGE_CORPUS: List[Dict[str, Any]] = [
    {
        "university": "Stanford University",
        "country": "USA",
        "discipline": "Inteligencia Artificial & Deep Learning",
        "topic": "Descenso de Gradiente y Retropropagación en Grafos Computacionales",
        "formula_latex": r"\frac{\partial \mathcal{L}}{\partial W^{[l]}} = \frac{1}{m} dZ^{[l]} (A^{[l-1]})^T, \quad W^{[l]} \leftarrow W^{[l]} - \alpha \frac{\partial \mathcal{L}}{\partial W^{[l]}}",
        "pedagogical_style": "Intuición geométrica de optimización convexa y campos vectoriales de gradiente.",
        "content": (
            "En Stanford (Andrew Ng / Stephen Boyd), la retropropagación no es un truco algorítmico, sino la aplicación "
            "directa de la regla de la cadena multivariable sobre tensores en un grafo acíclico dirigido (DAG). "
            "El gradiente ∇L representa el vector normal a las superficies equipotenciales de la pérdida. "
            "Seguir la dirección opuesta al gradiente garantiza el descenso más empinado hacia el mínimo local."
        ),
        "engineering_application": "Entrenamiento de redes neuronales convolucionales, LLMs (Gemini, GPT) y control por aprendizaje reforzado."
    },
    {
        "university": "Stanford University",
        "country": "USA",
        "discipline": "Inteligencia Artificial",
        "topic": "Mecanismo de Auto-Atención Escalada (Transformers)",
        "formula_latex": r"\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{Q K^T}{\sqrt{d_k}}\right) V",
        "pedagogical_style": "Mapeo de similitud proyectiva en espacios euclidianos multidimensionales.",
        "content": (
            "El producto punto entre la matriz de consultas Q y las claves K mide la correlación semántica "
            "entre cada token del texto o dato sensorial. Se divide entre sqrt(d_k) para estabilizar la varianza "
            "a 1 y evitar que el gradiente de softmax se desvanezca en dimensiones altas."
        ),
        "engineering_application": "Arquitecturas de lenguaje natural modernas, visión artificial con ViTs y procesamiento multimodal."
    },
    {
        "university": "Stanford University",
        "country": "USA",
        "discipline": "Robótica y Control",
        "topic": "Matrices de Transformación Homogénea SE(3) y Cinemática Directa",
        "formula_latex": r"T = \begin{bmatrix} R_{3\times 3} & p_{3\times 1} \\ 0_{1\times 3} & 1 \end{bmatrix} \in SE(3)",
        "pedagogical_style": "Visualización de marcos de referencia coordenados móviles ortonormales.",
        "content": (
            "En robótica (John Craig, Stanford), cualquier eslabón de un brazo articulado se describe mediante "
            "una rotación ortogonal R en SO(3) y una traslación p en R^3. La multiplicación encadenada de matrices "
            "T_0^n = T_0^1 T_1^2 ... T_{n-1}^n resuelve la posición del efector final con precisión micrométrica."
        ),
        "engineering_application": "Control de manipuladores industriales (KUKA, ABB), brazos quirúrgicos y robots humanoides."
    },
    {
        "university": "Moscow State University (MGU)",
        "country": "Russia",
        "discipline": "Sistemas Operativos y Cómputo",
        "topic": "Sincronización de Procesos, Exclusión Mutua e Invariantes de Dijkstra",
        "formula_latex": r"P(S): [S > 0 \to S \leftarrow S - 1], \quad V(S): [S \leftarrow S + 1]",
        "pedagogical_style": "Lógica axiomática formal y análisis riguroso de estados concurrentes.",
        "content": (
            "En la escuela de matemáticas y cibernética de MGU, la concurrencia no se prueba empíricamente; "
            "se demuestra formalmente mediante invariantes de estado. Un semáforo garantiza que el número de procesos "
            "en la sección crítica nunca exceda la capacidad disponible, evitando condiciones de carrera y deadlocks."
        ),
        "engineering_application": "Planificadores de núcleos Linux, sistemas de archivos distribuidos y motores de bases de datos ACID."
    },
    {
        "university": "Moscow State University (MGU)",
        "country": "Russia",
        "discipline": "Mecánica del Sólido Continuo",
        "topic": "Tensor de Esfuerzos de Cauchy y Ecuaciones de Equilibrio de Navier",
        "formula_latex": r"\nabla \cdot \boldsymbol{\sigma} + \mathbf{f} = \rho \frac{\partial^2 \mathbf{u}}{\partial t^2}",
        "pedagogical_style": "Deducción invariante basada en balance de momento lineal y principios de conservación.",
        "content": (
            "En la escuela Landau de MGU, el estado tensional de cualquier estructura mecánica se resume en el tensor "
            "simétrico de Cauchy σ_ij. En equilibrio estático, la divergencia de este tensor compensa exactamente "
            "las fuerzas de volumen aplicadas, garantizando estabilidad física indestructible."
        ),
        "engineering_application": "Análisis por elementos finitos (FEA), diseño de chasis aeroespaciales y robótica móvil de alta carga."
    },
    {
        "university": "Tsinghua University",
        "country": "China",
        "discipline": "Álgebra Lineal y Control Moderno",
        "topic": "Valores y Vectores Propios en Sistemas de Espacio de Estados",
        "formula_latex": r"\det(A - \lambda I) = 0, \quad \dot{x}(t) = A x(t) + B u(t)",
        "pedagogical_style": "Descomposición espectral exacta y análisis de polos de estabilidad de Lyapunov.",
        "content": (
            "En Tsinghua, la estabilidad de un sistema dinámico multivariable no es intuitiva, sino un criterio algebraico estricto. "
            "Si las partes reales de todos los valores propios de la matriz de sistema A son estrictamente negativas "
            "(Re(lambda_i) < 0), el sistema regresa asintóticamente a su punto de equilibrio bajo cualquier perturbación."
        ),
        "engineering_application": "Piloto automático de drones, estabilidad de reactores nucleares y control de balance bípedo en robots."
    },
    {
        "university": "Harvard University",
        "country": "USA",
        "discipline": "Cálculo Multivariable",
        "topic": "Teorema Fundamental de Cálculo Vectorial (Stokes y Gauss)",
        "formula_latex": r"\iint_S (\nabla \times \mathbf{F}) \cdot d\mathbf{S} = \oint_{\partial S} \mathbf{F} \cdot d\mathbf{r}",
        "pedagogical_style": "Tratamiento axiomático unificado mediante formas diferenciales dω.",
        "content": (
            "En Harvard, el teorema de Stokes no se memoriza como un caso aislado; se comprende como la ley universal "
            "que conecta la derivada exterior de una forma diferencial en el interior de una variedad con su valor "
            "en la frontera: ∫_M dω = ∫_{∂M} ω. Esto unifica el cálculo elemental, electrodinámica y dinámica de fluidos."
        ),
        "engineering_application": "Electromagnetismo en motores brushless de robótica, simulación hidrodinámica y gráficos por computadora."
    }
]

def get_university_pedagogy(univ_id: str) -> Dict[str, Any]:
    """Obtiene la información pedagógica de una universidad."""
    return UNIVERSITY_PEDAGOGIES.get(univ_id.lower(), UNIVERSITY_PEDAGOGIES["stanford"])

def list_all_pedagogies() -> List[Dict[str, Any]]:
    """Lista todos los enfoques pedagógicos disponibles."""
    return list(UNIVERSITY_PEDAGOGIES.values())

def generate_local_embedding(text: str, dim: int = 768) -> List[float]:
    """
    Genera un vector embedding normalizado de fallback.
    Utiliza proyección armónica determinista de alta fidelidad.
    """
    vec = [0.0] * dim
    for i, char in enumerate(text):
        val = ord(char)
        idx = (i * 37 + val * 17) % dim
        vec[idx] += math.sin(val * (i + 1)) * 1.5 + math.cos(val * 0.3)

    norm = math.sqrt(sum(x * x for x in vec))
    if norm > 0:
        vec = [round(x / norm, 6) for x in vec]
    return vec

def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """Calcula la similitud de coseno entre dos vectores."""
    if len(v1) != len(v2) or not v1:
        return 0.0
    dot = sum(a * b for a, b in zip(v1, v2))
    norm_a = math.sqrt(sum(a * a for a in v1))
    norm_b = math.sqrt(sum(b * b for b in v2))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)

def search_corpus_local(query: str, university: Optional[str] = None, top_k: int = 3) -> List[Dict[str, Any]]:
    """Búsqueda semántica sobre el corpus curricular universitario."""
    query_vec = generate_local_embedding(query.lower())
    results = []

    for doc in UNIVERSITY_KNOWLEDGE_CORPUS:
        if university and university.lower() not in doc["university"].lower():
            continue

        doc_text = f"{doc['topic']} {doc['discipline']} {doc['content']} {doc['formula_latex']}".lower()
        doc_vec = generate_local_embedding(doc_text)
        sim = cosine_similarity(query_vec, doc_vec)

        words = query.lower().split()
        keyword_hits = sum(1 for w in words if len(w) > 3 and w in doc_text)
        score = sim * 0.7 + (keyword_hits * 0.15)

        results.append({
            **doc,
            "similarity": round(float(score), 4)
        })

    results.sort(key=lambda x: x["similarity"], reverse=True)
    return results[:top_k]
