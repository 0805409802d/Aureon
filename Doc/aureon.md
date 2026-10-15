Este es Aureon, tiene como objetivo ser una IA que me ayude a estudiar de mejor manera con contexto y conocimiento real, funcionando como mi instructor y herramienta de aprendizaje personalizada ("Jarvis" de estudio).

## Stack Tecnológico y Entorno de Ejecución
* **Fase Actual (MVP Local de Estudio Personal):**
  - **Lenguajes:** Python (Backend y Motor Matemático Simbólico), SQL, Flutter (Frontend Multiplataforma / Desktop).
  - **Motor Matemático Didáctico:** SymPy y NumPy (cálculo determinista, exacto y sin alucinaciones).
  - **Backend Local:** FastAPI en Python (comunicación rápida por HTTP / WebSockets).
  - **IA y Tutoría:** Google Cloud Agent Platform / Gemini (para explicaciones teóricas, intuición y pedagogía socrática).
* **Fase Futura (Escalado y Comercial):**
  - Golang (Microservicios de alto rendimiento), Supabase con `pgvector`, MCP (Model Context Protocol), Railway y despliegue en Google Play Console.

---

## Pantallas y Módulos
- **HOME (INDEX):** Punto de partida y resumen general de estudio.
- **ENTORNO DE ESTUDIO (DOBLE CANVAS):** Núcleo didáctico e interactivo de aprendizaje en tiempo real.
- **BIBLIOTECA (LIBRARY):** Aislamiento de conocimiento por materias y temas.
- **BUSQUEDA (SEARCH):** Integración con MCP y fuentes académicas.
- **NOTAS (NOTES):** Registro del progreso, fortalezas, debilidades y repetición espaciada.
- **AJUSTES (SETTINGS):** Configuración visual y parámetros de la IA.
- **SUSCRIPCIONES (SUBSCRIPTIONS) & LOGIN:** (Fase futura comercial).

---

## Entorno de Estudio: Arquitectura del "Doble Canvas"
El entorno de estudio divide la pantalla en dos espacios de trabajo independientes pero perfectamente sincronizados:

### 1. Canvas Numérico / De Trabajo (Lado Ancho - Lado Izquierdo)
* **Enfoque Didáctico y Paramétrico:** Muestra la resolución matemática desglosada paso a paso.
* **Modificación Interactiva de Números:** Si el usuario modifica cualquier variable o número de la ecuación, el sistema **recalcula automáticamente todo el procedimiento matemático en tiempo real**.
* **Ejecución Determinista (Sin IA):** El recálculo y la simplificación de pasos se realiza mediante sistemas existentes de computación algebraica (**Python + SymPy**). Esto garantiza **0% de alucinaciones matemáticas**, precisión absoluta y costo cero de tokens de IA para el cálculo.
* **Extensible por Materia:**
  - *Álgebra y Cálculo:* Expresiones en LaTeX / KaTeX estructurado por bloques interactivos.
  - *Ciencias de la Computación / Software:* Bloques de código y trazas de ejecución.
  - *Robótica y Física:* Gráficos interactivos de funciones, vectores y matrices.

### 2. Canvas de Explicación y Teoría (Lado Delgado - Lado Derecho - Tutor IA)
* Panel interactivo donde vive Aureon como mentor socrático.
* Responde a preguntas específicas del ejercicio activo, tales como:
  - *"¿De dónde sale este número?"*
  - *"¿Qué proceso o propiedad se usa aquí y cómo se llama?"*
  - *"Enséñame paso a paso cómo resolver este tipo de ejercicio."*
  - *"¿En qué situaciones de la vida real o de la ingeniería se utiliza esta fórmula?"*
* **Sincronización Bidireccional:** Al tocar un paso o término en el canvas numérico, el panel de la IA resalta el contexto exacto de dicho término.
* **Voz en Streaming (TTS):** Explicaciones por voz mediante streaming para no generar tiempos de espera.

---

## Las 5 Áreas de Ingeniería Objetivo
El sistema está diseñado para acompañar y formar al usuario a lo largo de toda su formación técnica y superior en 5 disciplinas:
1. **Ingeniería de Software:** Lógica proposicional, aritmética modular, estructuras de datos, optimización y algoritmos.
2. **Ciencias de la Computación:** Matemáticas discretas, teoría de grafos, análisis asintótico (Big-O), probabilidad y autómatas.
3. **Robótica:** Álgebra lineal aplicada (matrices de transformación $SE(3)$, cuaterniones), cinemática directa e inversa, cálculo multivariable y control dinámico (EDOs).
4. **Nanotecnología:** Cálculo multivariable avanzado, ecuaciones diferenciales parciales (EDPs), mecánica cuántica básica (Ecuación de Schrödinger) y física estadística.
5. **Ingeniería Nuclear:** Ecuaciones diferenciales de decaimiento radiactivo, leyes de conservación, ecuación de difusión de neutrones y métodos numéricos de transporte de energía.

---

## Progresión Matemática: Modelo de Arquetipos Paramétricos (Desde Baldor hasta Nivel Avanzado)
En lugar de almacenar miles de ejercicios estáticos de forma manual, el sistema utiliza **Plantillas Paramétricas Generativas**:
* **Total de Arquetipos Maestros:** Aproximadamente **120 a 150 arquetipos de problemas** cubren los fundamentos y las aplicaciones avanzadas de las 5 ingenierías.
* **Progresión por Fases:**
  1. **Nivel 1 (Fundamentos - Baldor):** ~20 arquetipos (Despeje de variables, factorización, productos notables, fracciones algebraicas, ecuaciones lineales, cuadráticas y sistemas $2\times2$).
  2. **Nivel 2 (Cálculo y Álgebra Lineal):** ~45 arquetipos (Límites, derivadas, integrales por sustitución/partes, matrices, determinantes, sistemas de ecuaciones lineales, autovalores y autovectores).
  3. **Nivel 3 (Cálculo Multivariable y Vectorial):** ~25 arquetipos (Gradientes, derivadas parciales, integrales dobles/triples, divergencia y rotacional).
  4. **Nivel 4 (Ecuaciones Diferenciales y Métodos Físicos):** ~35 arquetipos (EDOs de primer y segundo orden, transformadas de Laplace, EDPs de onda/difusión, modelado de reactores y dinámica de robots).
* Cada plantilla programada en SymPy permite generar **infinitas variaciones numéricas** con solo alterar sus coeficientes.

---

## Memoria, Biblioteca y Prevención de Alucinaciones
* **Biblioteca Aislada:** Cada área educativa (ej. `Biblioteca/Robotica/Cinematica_Directa`) mantiene su propio espacio de contexto para evitar que la IA mezcle conceptos de materias incompatibles.
* **RAG y Grounding:** Ingesta de apuntes propios y fuentes oficiales usando `pgvector`/Supabase con temperatura baja (0.1) y preprocesamiento OCR matemático (Mathpix/Visión) para fórmulas complejas.
* **Notas y Repetición Espaciada:** Registro automático de los temas dominados y pendientes por repasar para reforzar la memoria a largo plazo antes de evaluaciones.