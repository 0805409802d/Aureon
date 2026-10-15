-- ====================================================================
-- AUREON CLOUD - ESQUEMA INTEGRAL SUPABASE (POSTGRESQL + PGVECTOR)
-- ====================================================================
-- 100% Cloud Persistence en Supabase (Sin bases de datos locales)
-- Para: Darlyn David Tenelema Obando
-- Instituto Superior Tecnológico Carlos Cisneros - Inteligencia Artificial
-- ====================================================================

-- 1. Extensiones Necesarias
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 2. Áreas de Ingeniería Transversales
CREATE TABLE IF NOT EXISTS areas (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    icon TEXT,
    sort_order INT DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())
);

-- 3. Materias del Plan de Estudios
CREATE TABLE IF NOT EXISTS subjects (
    id TEXT PRIMARY KEY,
    area_id TEXT NOT NULL REFERENCES areas(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    level INT NOT NULL DEFAULT 1,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())
);

-- 4. Arquetipos Matemáticos y Fórmulas Paramétricas
CREATE TABLE IF NOT EXISTS archetypes (
    id TEXT PRIMARY KEY,
    subject_id TEXT NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    formula_latex TEXT NOT NULL,
    default_params JSONB NOT NULL DEFAULT '{}'::jsonb,
    param_schema JSONB NOT NULL DEFAULT '{}'::jsonb,
    difficulty INT DEFAULT 1,
    real_world_context TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())
);

-- 5. Historial de Práctica y Cálculos Resueltos
CREATE TABLE IF NOT EXISTS practice_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    archetype_id TEXT NOT NULL,
    input_params JSONB NOT NULL,
    solutions JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())
);

-- 6. Notas de Estudio y Repetición Espaciada (Algoritmo SM-2 Flashcards)
CREATE TABLE IF NOT EXISTS study_notes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    subject_id TEXT NOT NULL,
    archetype_id TEXT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    mastery_level INT DEFAULT 1,        -- 1 a 5
    interval_days INT DEFAULT 1,        -- Días para la próxima revisión
    ease_factor FLOAT DEFAULT 2.5,      -- Multiplicador SM-2 (2.5 estándar)
    repetitions INT DEFAULT 0,          -- Repeticiones exitosas consecutivas
    next_review_date TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())
);

-- 7. Registro de Sesiones de Estudio Intensivo (10+ Horas Diarias)
CREATE TABLE IF NOT EXISTS study_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id TEXT DEFAULT 'darlyn_david',
    minutes_studied INT NOT NULL DEFAULT 50, -- Bloque Pomodoro o tiempo continuo
    focus_area TEXT NOT NULL,                -- 'ai', 'robotics', 'os', 'mechanics', 'math'
    topic TEXT,
    notes TEXT,
    completed_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())
);

-- 8. Interacciones con el Tutor Socrático
CREATE TABLE IF NOT EXISTS tutor_interactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    archetype_id TEXT NOT NULL,
    step_number INT,
    question_type TEXT NOT NULL,
    user_question TEXT NOT NULL,
    tutor_explanation TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())
);

-- 9. Base de Datos Vectorial de Conocimiento Universitario (RAG con pgvector)
CREATE TABLE IF NOT EXISTS university_knowledge (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    university VARCHAR(100) NOT NULL,
    country VARCHAR(50) NOT NULL,
    discipline VARCHAR(100) NOT NULL,
    topic VARCHAR(150) NOT NULL,
    formula_latex TEXT,
    pedagogical_style TEXT NOT NULL,
    content TEXT NOT NULL,
    engineering_application TEXT,
    embedding VECTOR(768),              -- Vector embedding de 768 dimensiones
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())
);

-- 10. Sesiones Completas del Solucionador Universal IA
CREATE TABLE IF NOT EXISTS student_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id TEXT DEFAULT 'darlyn_david',
    equation_input TEXT NOT NULL,
    discipline TEXT,
    university_lens TEXT,
    solution_latex TEXT,
    pedagogical_breakdown JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())
);

-- ====================================================================
-- ÍNDICES DE ALTO RENDIMIENTO
-- ====================================================================
CREATE INDEX IF NOT EXISTS idx_subjects_area ON subjects(area_id);
CREATE INDEX IF NOT EXISTS idx_archetypes_subject ON archetypes(subject_id);
CREATE INDEX IF NOT EXISTS idx_notes_subject ON study_notes(subject_id);
CREATE INDEX IF NOT EXISTS idx_notes_review ON study_notes(next_review_date);
CREATE INDEX IF NOT EXISTS idx_sessions_user ON study_sessions(user_id, completed_at);
CREATE INDEX IF NOT EXISTS idx_knowledge_univ ON university_knowledge(university);
CREATE INDEX IF NOT EXISTS idx_knowledge_disc ON university_knowledge(discipline);

-- Índice HNSW para Búsqueda Vectorial Coseno Ultrarrápida
CREATE INDEX IF NOT EXISTS idx_university_knowledge_embedding 
ON university_knowledge 
USING hnsw (embedding vector_cosine_ops);

-- ====================================================================
-- FUNCIÓN RPC: BÚSQUEDA VECTORIAL SEMÁNTICA (RAG)
-- ====================================================================
CREATE OR REPLACE FUNCTION match_university_knowledge (
    query_embedding VECTOR(768),
    match_threshold FLOAT DEFAULT 0.35,
    match_count INT DEFAULT 4,
    filter_university TEXT DEFAULT NULL,
    filter_discipline TEXT DEFAULT NULL
)
RETURNS TABLE (
    id UUID,
    university VARCHAR(100),
    country VARCHAR(50),
    discipline VARCHAR(100),
    topic VARCHAR(150),
    formula_latex TEXT,
    pedagogical_style TEXT,
    content TEXT,
    engineering_application TEXT,
    similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        uk.id,
        uk.university,
        uk.country,
        uk.discipline,
        uk.topic,
        uk.formula_latex,
        uk.pedagogical_style,
        uk.content,
        uk.engineering_application,
        1 - (uk.embedding <=> query_embedding) AS similarity
    FROM university_knowledge uk
    WHERE 
        (filter_university IS NULL OR uk.university ILIKE '%' || filter_university || '%')
        AND (filter_discipline IS NULL OR uk.discipline ILIKE '%' || filter_discipline || '%')
        AND (1 - (uk.embedding <=> query_embedding)) > match_threshold
    ORDER BY uk.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

-- ====================================================================
-- POLÍTICAS DE ACCESO (ROW LEVEL SECURITY)
-- ====================================================================
ALTER TABLE areas ENABLE ROW LEVEL SECURITY;
ALTER TABLE subjects ENABLE ROW LEVEL SECURITY;
ALTER TABLE archetypes ENABLE ROW LEVEL SECURITY;
ALTER TABLE practice_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE study_notes ENABLE ROW LEVEL SECURITY;
ALTER TABLE study_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE tutor_interactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE university_knowledge ENABLE ROW LEVEL SECURITY;
ALTER TABLE student_sessions ENABLE ROW LEVEL SECURITY;

-- Permitir acceso completo con anon key a la API de Aureon
CREATE POLICY "Permitir acceso publico a areas" ON areas FOR ALL USING (true);
CREATE POLICY "Permitir acceso publico a subjects" ON subjects FOR ALL USING (true);
CREATE POLICY "Permitir acceso publico a archetypes" ON archetypes FOR ALL USING (true);
CREATE POLICY "Permitir acceso publico a practice_history" ON practice_history FOR ALL USING (true);
CREATE POLICY "Permitir acceso publico a study_notes" ON study_notes FOR ALL USING (true);
CREATE POLICY "Permitir acceso publico a study_sessions" ON study_sessions FOR ALL USING (true);
CREATE POLICY "Permitir acceso publico a tutor_interactions" ON tutor_interactions FOR ALL USING (true);
CREATE POLICY "Permitir acceso publico a university_knowledge" ON university_knowledge FOR ALL USING (true);
CREATE POLICY "Permitir acceso publico a student_sessions" ON student_sessions FOR ALL USING (true);
