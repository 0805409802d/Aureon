// ==============================================================
// AUREON v2.1 CLOUD - CLIENTE DE ESTUDIO INTELIGENTE
// Para: Darlyn David Tenelema Obando
// Instituto Superior Tecnológico Carlos Cisneros - Inteligencia Artificial
// ==============================================================

const API_BASE = window.location.origin.includes('8000') ? '' : 'http://127.0.0.1:8000';

let state = {
  currentView: 'universal', // 'universal' | 'parametric' | 'pomodoro' | 'flashcards' | 'mcp'
  selectedUniversity: 'stanford',
  universities: [],
  archetypes: [],
  activeArchetype: null,
  activeParams: {},
  activeStepNumber: 1,
  currentSolveResult: null,
  speechEnabled: false,
  selectedArea: 'ai',
  lastUniversalResult: null,
  // Estado del Temporizador Pomodoro 10H
  timer: {
    totalSeconds: 50 * 60,
    remainingSeconds: 50 * 60,
    isRunning: false,
    intervalId: null,
    mode: 'ENFOQUE'
  },
  // Estado de Flashcards SM-2
  flashcards: {
    cards: [],
    currentIndex: 0,
    isFlipped: false
  }
};

// ==============================================================
// ELEMENTOS DEL DOM
// ==============================================================
const tabModeUniversal = document.getElementById('tabModeUniversal');
const tabModeParametric = document.getElementById('tabModeParametric');
const tabModePomodoro = document.getElementById('tabModePomodoro');
const tabModeFlashcards = document.getElementById('tabModeFlashcards');
const tabModeMcp = document.getElementById('tabModeMcp');

const universalSolverView = document.getElementById('universalSolverView');
const parametricLabView = document.getElementById('parametricLabView');
const pomodoroLabView = document.getElementById('pomodoroLabView');
const flashcardsLabView = document.getElementById('flashcardsLabView');
const mcpLabView = document.getElementById('mcpLabView');

const universityTabsGroup = document.getElementById('universityTabsGroup');
const pedagogyFlag = document.getElementById('pedagogyFlag');
const pedagogyTagline = document.getElementById('pedagogyTagline');

// Solucionador Universal
const universalEquationInput = document.getElementById('universalEquationInput');
const btnSolveUniversal = document.getElementById('btnSolveUniversal');
const universalInputDisplay = document.getElementById('universalInputDisplay');
const universalSolutionDisplay = document.getElementById('universalSolutionDisplay');
const universalStepsContainer = document.getElementById('universalStepsContainer');
const lessonBodyMarkdown = document.getElementById('lessonBodyMarkdown');
const lessonHeading = document.getElementById('lessonHeading');
const lessonFlag = document.getElementById('lessonFlag');
const btnSpeakLesson = document.getElementById('btnSpeakLesson');
const btnCopyLatex = document.getElementById('btnCopyLatex');
const btnExportUniversalNotes = document.getElementById('btnExportUniversalNotes');
const presetButtons = document.querySelectorAll('.preset-chip');

// Laboratorio Paramétrico
const archetypeSelect = document.getElementById('archetypeSelect');
const paramInputsContainer = document.getElementById('paramInputsContainer');
const btnRecalculate = document.getElementById('btnRecalculate');
const btnRandomize = document.getElementById('btnRandomize');
const originalFormulaDisplay = document.getElementById('originalFormulaDisplay');
const solutionsSummaryBadge = document.getElementById('solutionsSummaryBadge');
const stepsContainer = document.getElementById('stepsContainer');
const realWorldText = document.getElementById('realWorldText');
const currentArchetypeTitle = document.getElementById('currentArchetypeTitle');
const currentArchetypeLevel = document.getElementById('currentArchetypeLevel');
const currentSubjectName = document.getElementById('currentSubjectName');
const areaTabs = document.querySelectorAll('.area-tab-btn');

// Pomodoro y Metas de 10 Horas
const timerTimeDisplay = document.getElementById('timerTimeDisplay');
const timerModeLabel = document.getElementById('timerModeLabel');
const timerProgressCircle = document.getElementById('timerProgressCircle');
const btnTimerStart = document.getElementById('btnTimerStart');
const btnTimerPause = document.getElementById('btnTimerPause');
const btnTimerReset = document.getElementById('btnTimerReset');
const timerChips = document.querySelectorAll('.timer-chip');
const statsHoursNumber = document.getElementById('statsHoursNumber');
const statsTargetNumber = document.getElementById('statsTargetNumber');
const statsSessionsCount = document.getElementById('statsSessionsCount');
const dailyProgressBar = document.getElementById('dailyProgressBar');
const progressPercentText = document.getElementById('progressPercentText');
const remainingMinutesText = document.getElementById('remainingMinutesText');
const hoursBadge = document.getElementById('hoursBadge');
const btnLogSessionManual = document.getElementById('btnLogSessionManual');
const sessionAreaSelect = document.getElementById('sessionAreaSelect');
const sessionMinutesInput = document.getElementById('sessionMinutesInput');
const sessionTopicInput = document.getElementById('sessionTopicInput');

// Flashcards SM-2
const activeFlashcard = document.getElementById('activeFlashcard');
const fcSubjectTag = document.getElementById('fcSubjectTag');
const fcQuestionText = document.getElementById('fcQuestionText');
const fcLatexFront = document.getElementById('fcLatexFront');
const fcAnswerText = document.getElementById('fcAnswerText');
const fcLatexBack = document.getElementById('fcLatexBack');
const sm2Buttons = document.querySelectorAll('.sm2-btn');
const savedCardsGrid = document.getElementById('savedCardsGrid');
const cardsCountBadge = document.getElementById('cardsCountBadge');
const btnOpenNewCardModal = document.getElementById('btnOpenNewCardModal');

// Hub MCP
const mcpToolsList = document.getElementById('mcpToolsList');
const mcpToolSelect = document.getElementById('mcpToolSelect');
const mcpToolArgs = document.getElementById('mcpToolArgs');
const btnExecuteMcp = document.getElementById('btnExecuteMcp');
const mcpOutputPre = document.getElementById('mcpOutputPre');

// Tutor Socrático
const activeContextTag = document.getElementById('activeContextTag');
const chatStream = document.getElementById('chatStream');
const chatInput = document.getElementById('chatInput');
const btnSendQuestion = document.getElementById('btnSendQuestion');
const btnToggleSpeech = document.getElementById('btnToggleSpeech');
const supabasePill = document.getElementById('supabasePill');
const supabaseLabel = document.getElementById('supabaseLabel');

// ==============================================================
// SÍNTESIS DE AUDIO (SINTETIZADOR WEB AUDIO PARA CHIMES Y VOZ)
// ==============================================================
function playAudioChime(freq = 587.33, duration = 0.6) {
  try {
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    if (!AudioContext) return;
    const ctx = new AudioContext();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(freq, ctx.currentTime);
    gain.gain.setValueAtTime(0.25, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + duration);
    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.start();
    osc.stop(ctx.currentTime + duration);
  } catch (e) {
    console.warn('Audio chime notice:', e);
  }
}

function speakText(text) {
  if (!('speechSynthesis' in window) || !text) return;
  window.speechSynthesis.cancel();
  const cleanText = text
    .replace(/\$\$(.*?)\$\$/gs, '')
    .replace(/\$(.*?)\$/g, '')
    .replace(/[#*_`]/g, '')
    .substring(0, 350);

  const utterance = new SpeechSynthesisUtterance(cleanText);
  utterance.lang = 'es-ES';
  utterance.rate = 1.05;
  utterance.pitch = 1.0;
  window.speechSynthesis.speak(utterance);
}

// ==============================================================
// RENDERIZADO MATEMÁTICO KaTeX
// ==============================================================
function renderMath(element, latexString, displayMode = false) {
  if (!element || !latexString) return;

  if (window.katex && typeof window.katex.renderToString === 'function') {
    try {
      element.innerHTML = window.katex.renderToString(latexString, {
        displayMode: displayMode,
        throwOnError: false
      });
      return;
    } catch (e) {
      console.warn('KaTeX render error:', e);
    }
  }

  element.innerHTML = formatLatexToHtml(latexString);
}

function formatLatexToHtml(latex) {
  if (!latex) return '';
  let html = latex
    .replace(/\\Delta/g, '&Delta;')
    .replace(/\\sigma/g, '&sigma;')
    .replace(/\\epsilon/g, '&epsilon;')
    .replace(/\\pm/g, '&plusmn;')
    .replace(/\\cdot/g, '&middot;')
    .replace(/\\implies/g, ' &rArr; ')
    .replace(/\\quad/g, ' &nbsp; ')
    .replace(/\\times/g, '&times;')
    .replace(/\\int/g, '&int;')
    .replace(/\\partial/g, '&part;')
    .replace(/\\nabla/g, '&nabla;')
    .replace(/\\text\{(.*?)\}/g, '$1')
    .replace(/\\sqrt\{(.*?)\}/g, '&radic;($1)')
    .replace(/\\frac\{(.*?)\}\{(.*?)\}/g, '<span class="fallback-frac"><span class="top">$1</span><span class="bottom">$2</span></span>')
    .replace(/\^([0-9a-zA-Z]+)/g, '<sup>$1</sup>')
    .replace(/\^{([^}]+)}/g, '<sup>$1</sup>')
    .replace(/_([0-9a-zA-Z]+)/g, '<sub>$1</sub>')
    .replace(/_{([^}]+)}/g, '<sub>$1</sub>');

  return `<span class="fallback-math">${html}</span>`;
}

function renderMarkdownWithMath(content) {
  if (!content) return '';

  let html = content
    .replace(/### (.*?)\n/g, '<h3>$1</h3>')
    .replace(/#### (.*?)\n/g, '<h4>$1</h4>')
    .replace(/> (.*?)\n/g, '<blockquote>$1</blockquote>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/^- (.*?)$/gm, '<li>$1</li>')
    .replace(/(<li>.*?<\/li>)/gs, '<ul>$1</ul>')
    .replace(/\n\n/g, '<br><br>');

  html = html.replace(/\$\$(.*?)\$\$/gs, (match, latex) => {
    if (window.katex) {
      try {
        return `<div class="katex-display-block">${window.katex.renderToString(latex.trim(), { displayMode: true, throwOnError: false })}</div>`;
      } catch (e) {}
    }
    return `<div class="katex-display-block">${formatLatexToHtml(latex.trim())}</div>`;
  });

  html = html.replace(/\$([^\$\n]+)\$/g, (match, latex) => {
    if (window.katex) {
      try {
        return window.katex.renderToString(latex.trim(), { displayMode: false, throwOnError: false });
      } catch (e) {}
    }
    return formatLatexToHtml(latex.trim());
  });

  return html;
}

// ==============================================================
// NAVEGACIÓN Y CAMBIO DE VISTAS (5 VISTAS)
// ==============================================================
function switchView(viewName) {
  state.currentView = viewName;

  // Actualizar botones de navegación
  [tabModeUniversal, tabModeParametric, tabModePomodoro, tabModeFlashcards, tabModeMcp].forEach(btn => {
    if (btn) btn.classList.remove('active');
  });

  // Ocultar todos los paneles
  [universalSolverView, parametricLabView, pomodoroLabView, flashcardsLabView, mcpLabView].forEach(panel => {
    if (panel) panel.classList.remove('active');
  });

  if (viewName === 'universal') {
    tabModeUniversal?.classList.add('active');
    universalSolverView?.classList.add('active');
    activeContextTag.textContent = 'Solucionador Universal IA';
  } else if (viewName === 'parametric') {
    tabModeParametric?.classList.add('active');
    parametricLabView?.classList.add('active');
    activeContextTag.textContent = state.activeArchetype?.title || 'Laboratorio de Ingenierías';
  } else if (viewName === 'pomodoro') {
    tabModePomodoro?.classList.add('active');
    pomodoroLabView?.classList.add('active');
    activeContextTag.textContent = 'Estudio Intensivo 10H · Pomodoro';
    fetchDailyStudyStats();
  } else if (viewName === 'flashcards') {
    tabModeFlashcards?.classList.add('active');
    flashcardsLabView?.classList.add('active');
    activeContextTag.textContent = 'Active Recall SM-2';
    loadFlashcardsFromCloud();
  } else if (viewName === 'mcp') {
    tabModeMcp?.classList.add('active');
    mcpLabView?.classList.add('active');
    activeContextTag.textContent = 'Hub MCP · Protocolo JSON-RPC';
    loadMcpTools();
  }
}

// ==============================================================
// SOLUCIONADOR UNIVERSAL IA
// ==============================================================
async function solveUniversalEquation() {
  const equation = universalEquationInput.value.trim();
  if (!equation) return;

  btnSolveUniversal.disabled = true;
  btnSolveUniversal.innerHTML = '<span class="loading-spinner"></span> Resolviendo...';

  try {
    const res = await fetch(`${API_BASE}/api/tutor/solve-custom`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        equation: equation,
        university_lens: state.selectedUniversity
      })
    });

    const data = await res.json();
    state.lastUniversalResult = data;

    // Renderizar Fórmulas Principales
    const symRes = data.symbolic_result || {};
    renderMath(universalInputDisplay, symRes.latex_input || equation, true);
    renderMath(universalSolutionDisplay, symRes.latex_solution || '\\text{Procesado}', true);

    // Renderizar Pasos Analíticos
    universalStepsContainer.innerHTML = '';
    const steps = symRes.steps || [];
    if (steps.length > 0) {
      steps.forEach((st, idx) => {
        const stepEl = document.createElement('div');
        stepEl.className = 'universal-step-item';
        stepEl.innerHTML = `
          <div class="u-step-badge">Paso ${st.step || idx + 1}</div>
          <div class="u-step-content">
            <strong>${st.title || 'Transformación'}</strong>
            <div class="u-step-math" id="uStepMath_${idx}"></div>
          </div>
        `;
        universalStepsContainer.appendChild(stepEl);
        renderMath(document.getElementById(`uStepMath_${idx}`), st.latex || '', true);
      });
    }

    // Renderizar Lección Pedagógica
    const pedagogy = data.university || {};
    lessonFlag.textContent = pedagogy.flag || '🎓';
    lessonHeading.textContent = `Análisis Socrático · ${pedagogy.name || 'Universidad'}`;
    lessonBodyMarkdown.innerHTML = renderMarkdownWithMath(data.explanation || '');

    // Actualizar Contexto Activo del Tutor
    activeContextTag.textContent = `Ecuación: ${equation.substring(0, 30)}`;

    playAudioChime(659.25, 0.5);

    if (state.speechEnabled) {
      speakText(data.explanation);
    }

  } catch (err) {
    console.error('Error al resolver ecuación universal:', err);
    lessonBodyMarkdown.innerHTML = `<div class="error-box">Error al conectar con el servidor: ${err.message}</div>`;
  } finally {
    btnSolveUniversal.disabled = false;
    btnSolveUniversal.innerHTML = '<span class="solve-icon">⚡</span><span>Resolver con IA</span>';
  }
}

// Guardar solución como Flashcard SM-2 en Supabase
async function saveUniversalAsFlashcard() {
  if (!state.lastUniversalResult) {
    alert("Primero resuelve una ecuación para guardarla como flashcard.");
    return;
  }
  const data = state.lastUniversalResult;
  const eq = data.equation_input || "Ecuación";
  const sol = data.symbolic_result?.latex_solution || "Solución analítica";

  try {
    const res = await fetch(`${API_BASE}/api/library/notes`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        subject_id: "ai_foundations",
        title: `Resolver: ${eq}`,
        content: `Solución: $$${sol}$$\n\n${(data.explanation || '').substring(0, 300)}...`,
        mastery_level: 1
      })
    });
    const result = await res.json();
    alert("✓ Guardado con éxito en Supabase Cloud con algoritmo de repetición espaciada SM-2.");
    playAudioChime(880, 0.4);
  } catch (err) {
    alert("Error al guardar en Supabase: " + err.message);
  }
}

// ==============================================================
// LABORATORIO PARAMÉTRICO DE INGENIERÍAS
// ==============================================================
async function loadArchetypes(areaId = null) {
  try {
    const url = areaId ? `${API_BASE}/api/math/archetypes?area_id=${areaId}` : `${API_BASE}/api/math/archetypes`;
    const res = await fetch(url);
    const list = await res.json();
    state.archetypes = list;

    archetypeSelect.innerHTML = '';
    list.forEach(arch => {
      const opt = document.createElement('option');
      opt.value = arch.id;
      opt.textContent = `[${arch.subject_name || 'Ingeniería'}] ${arch.title}`;
      archetypeSelect.appendChild(opt);
    });

    if (list.length > 0) {
      selectArchetype(list[0].id);
    }
  } catch (err) {
    console.error('Error cargando arquetipos:', err);
  }
}

function selectArchetype(archetypeId) {
  const arch = state.archetypes.find(a => a.id === archetypeId);
  if (!arch) return;

  state.activeArchetype = arch;
  state.activeParams = { ...arch.default_params };

  currentArchetypeTitle.textContent = arch.title;
  currentArchetypeLevel.textContent = `Nivel ${arch.difficulty || 1}`;
  currentSubjectName.textContent = `Materia: ${arch.subject_name || 'Ingeniería'}`;
  activeContextTag.textContent = arch.title;

  buildParamInputs(arch.param_schema, state.activeParams);
  recalculateArchetype();
}

function buildParamInputs(schema, activeParams) {
  paramInputsContainer.innerHTML = '';
  if (!schema) return;

  Object.keys(schema).forEach(key => {
    const field = schema[key];
    const wrapper = document.createElement('div');
    wrapper.className = 'param-input-item';

    const label = document.createElement('label');
    label.textContent = `${field.label || key}:`;

    const input = document.createElement('input');
    input.type = 'number';
    input.step = 'any';
    input.className = 'param-field';
    input.value = activeParams[key] !== undefined ? activeParams[key] : (field.default || 0);

    input.addEventListener('input', (e) => {
      state.activeParams[key] = parseFloat(e.target.value) || 0;
    });

    wrapper.appendChild(label);
    wrapper.appendChild(input);
    paramInputsContainer.appendChild(wrapper);
  });
}

async function recalculateArchetype() {
  if (!state.activeArchetype) return;

  try {
    const res = await fetch(`${API_BASE}/api/math/archetypes/${state.activeArchetype.id}/solve`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(state.activeParams)
    });

    const data = await res.json();
    state.currentSolveResult = data;

    renderMath(originalFormulaDisplay, data.original_latex, true);
    solutionsSummaryBadge.innerHTML = (data.final_solutions || []).map(sol => 
      `<div class="sol-badge">${formatLatexToHtml(sol)}</div>`
    ).join('');

    renderSteps(data.steps || []);
    realWorldText.textContent = data.real_world_context || '';

  } catch (err) {
    console.error('Error al resolver arquetipo:', err);
  }
}

function renderSteps(steps) {
  stepsContainer.innerHTML = '';
  steps.forEach((step, idx) => {
    const stepCard = document.createElement('div');
    stepCard.className = `step-card ${step.step_number === state.activeStepNumber ? 'focused-step' : ''}`;
    stepCard.dataset.step = step.step_number;

    stepCard.innerHTML = `
      <div class="step-card-header">
        <span class="step-number-pill">Paso ${step.step_number}</span>
        <strong>${step.title}</strong>
        <span class="step-rule-tag">${step.rule_name}</span>
      </div>
      <div class="step-latex" id="stepLatex_${idx}"></div>
      <div class="step-explanation">${step.explanation}</div>
      <div class="visual-blocks-strip" id="blocksStrip_${idx}"></div>
    `;

    stepCard.addEventListener('click', () => {
      document.querySelectorAll('.step-card').forEach(c => c.classList.remove('focused-step'));
      stepCard.classList.add('focused-step');
      state.activeStepNumber = step.step_number;
      activeContextTag.textContent = `Paso ${step.step_number}: ${step.title}`;
    });

    stepsContainer.appendChild(stepCard);
    renderMath(document.getElementById(`stepLatex_${idx}`), step.latex, true);

    const blocksStrip = document.getElementById(`blocksStrip_${idx}`);
    (step.blocks || []).forEach(b => {
      const bEl = document.createElement('span');
      bEl.className = `v-block v-${b.block_type} ${b.highlight ? 'v-highlight' : ''}`;
      bEl.textContent = b.content;
      bEl.title = "Haz clic para consultar con el tutor socrático";
      bEl.addEventListener('click', (e) => {
        e.stopPropagation();
        askTutorAboutStep(step.step_number, 'source_of_number', `¿De dónde sale el término ${b.content}?`);
      });
      blocksStrip.appendChild(bEl);
    });
  });
}

// ==============================================================
// VISTA 3: TEMPORIZADOR POMODORO & SEGUIMIENTO DE 10 HORAS
// ==============================================================
function updateTimerDisplay() {
  const mins = Math.floor(state.timer.remainingSeconds / 60);
  const secs = state.timer.remainingSeconds % 60;
  timerTimeDisplay.textContent = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;

  // Actualizar círculo SVG
  const circleCircumference = 553; // 2 * PI * 88
  const progressRatio = (state.timer.totalSeconds - state.timer.remainingSeconds) / state.timer.totalSeconds;
  const offset = circleCircumference * (1 - progressRatio);
  timerProgressCircle.style.strokeDashoffset = offset;
}

function startPomodoro() {
  if (state.timer.isRunning) return;
  state.timer.isRunning = true;
  playAudioChime(523.25, 0.4);

  state.timer.intervalId = setInterval(() => {
    if (state.timer.remainingSeconds > 0) {
      state.timer.remainingSeconds--;
      updateTimerDisplay();
    } else {
      // Bloque completado
      pausePomodoro();
      playAudioChime(783.99, 1.2);
      alert("¡Excelente trabajo, Darlyn! Bloque completado.");
      autoLogCompletedPomodoro();
    }
  }, 1000);
}

function pausePomodoro() {
  state.timer.isRunning = false;
  if (state.timer.intervalId) {
    clearInterval(state.timer.intervalId);
    state.timer.intervalId = null;
  }
}

function resetPomodoro() {
  pausePomodoro();
  state.timer.remainingSeconds = state.timer.totalSeconds;
  updateTimerDisplay();
}

async function autoLogCompletedPomodoro() {
  const completedMins = Math.round(state.timer.totalSeconds / 60);
  try {
    await fetch(`${API_BASE}/api/library/sessions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        minutes: completedMins,
        focus_area: state.selectedArea || 'ai',
        topic: state.activeArchetype?.title || 'Estudio Continuo',
        notes: 'Bloque Pomodoro completado con éxito'
      })
    });
    fetchDailyStudyStats();
  } catch (e) {
    console.error('Error logging pomodoro:', e);
  }
}

async function fetchDailyStudyStats() {
  try {
    const res = await fetch(`${API_BASE}/api/library/stats`);
    const data = await res.json();

    statsHoursNumber.textContent = data.hours_today.toFixed(1);
    statsTargetNumber.textContent = data.target_hours.toFixed(1);
    statsSessionsCount.textContent = data.sessions_count;

    dailyProgressBar.style.width = `${data.progress_percent}%`;
    progressPercentText.textContent = `${data.progress_percent}% de la meta`;
    remainingMinutesText.textContent = `${data.remaining_minutes} min restantes`;
    hoursBadge.textContent = `${data.hours_today.toFixed(1)} / 10h`;

  } catch (e) {
    console.warn('Error fetching stats:', e);
  }
}

async function logSessionManual() {
  const area = sessionAreaSelect.value;
  const mins = parseInt(sessionMinutesInput.value, 10) || 50;
  const topic = sessionTopicInput.value.trim() || 'Estudio intensivo';

  try {
    await fetch(`${API_BASE}/api/library/sessions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        minutes: mins,
        focus_area: area,
        topic: topic,
        notes: 'Sesión registrada manualmente'
      })
    });
    alert(`✓ Sesión de ${mins} minutos registrada en Supabase Cloud.`);
    sessionTopicInput.value = '';
    fetchDailyStudyStats();
    playAudioChime(659.25, 0.4);
  } catch (e) {
    alert('Error al registrar sesión: ' + e.message);
  }
}

// ==============================================================
// VISTA 4: ACTIVE RECALL & FLASHCARDS SM-2
// ==============================================================
async function loadFlashcardsFromCloud() {
  try {
    const res = await fetch(`${API_BASE}/api/library/notes`);
    const cards = await res.json();
    state.flashcards.cards = cards;
    cardsCountBadge.textContent = cards.length;

    renderFlashcardDeck();
    renderSavedCardsList(cards);
  } catch (e) {
    console.error('Error cargando flashcards:', e);
  }
}

function renderFlashcardDeck() {
  const cards = state.flashcards.cards;
  if (!cards || cards.length === 0) {
    fcQuestionText.textContent = "No hay flashcards registradas aún.";
    fcAnswerText.textContent = "Crea una nueva tarjeta o guarda una solución del Solucionador Universal con 1 clic.";
    fcLatexFront.innerHTML = '';
    fcLatexBack.innerHTML = '';
    return;
  }

  const idx = state.flashcards.currentIndex % cards.length;
  const c = cards[idx];

  fcSubjectTag.textContent = c.subject_id || 'Ingeniería';
  fcQuestionText.textContent = c.title;
  fcAnswerText.innerHTML = renderMarkdownWithMath(c.content);
  activeFlashcard.classList.remove('flipped');
  state.flashcards.isFlipped = false;
}

function flipFlashcard() {
  state.flashcards.isFlipped = !state.flashcards.isFlipped;
  activeFlashcard.classList.toggle('flipped', state.flashcards.isFlipped);
  playAudioChime(440, 0.15);
}

async function rateFlashcardSM2(quality) {
  const cards = state.flashcards.cards;
  if (!cards || cards.length === 0) return;

  const current = cards[state.flashcards.currentIndex % cards.length];
  const cardId = current.id || current.title;

  try {
    await fetch(`${API_BASE}/api/library/notes/${cardId}/review`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ quality: parseInt(quality, 10) })
    });

    playAudioChime(quality >= 4 ? 880 : 440, 0.3);

    // Pasar a la siguiente tarjeta
    state.flashcards.currentIndex++;
    renderFlashcardDeck();

  } catch (e) {
    console.error('Error calificado SM-2:', e);
  }
}

function renderSavedCardsList(cards) {
  savedCardsGrid.innerHTML = '';
  cards.forEach((c, i) => {
    const item = document.createElement('div');
    item.className = 'mini-card-item';
    item.innerHTML = `
      <div class="mini-card-title">${c.title}</div>
      <div class="mini-card-meta">Dominio: ${c.mastery_level || 1}/5 · Reps: ${c.repetitions || 0}</div>
    `;
    item.addEventListener('click', () => {
      state.flashcards.currentIndex = i;
      renderFlashcardDeck();
    });
    savedCardsGrid.appendChild(item);
  });
}

function openNewCardPrompt() {
  const title = prompt("Pregunta o Teorema de la Flashcard:");
  if (!title) return;
  const content = prompt("Respuesta o demostración detallada:");
  if (!content) return;

  fetch(`${API_BASE}/api/library/notes`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      subject_id: state.selectedArea || "ai_foundations",
      title: title,
      content: content,
      mastery_level: 1
    })
  }).then(() => {
    alert("✓ Flashcard creada en Supabase Cloud.");
    loadFlashcardsFromCloud();
  });
}

// ==============================================================
// VISTA 5: HUB MCP & EJECUTOR JSON-RPC
// ==============================================================
async function loadMcpTools() {
  try {
    const res = await fetch(`${API_BASE}/api/mcp/tools`);
    const data = await res.json();
    const tools = data.tools || [];

    mcpToolsList.innerHTML = '';
    tools.forEach(t => {
      const card = document.createElement('div');
      card.className = 'mcp-tool-badge';
      card.innerHTML = `
        <div class="mcp-tool-name">λ ${t.name}</div>
        <div class="mcp-tool-desc">${t.description}</div>
      `;
      mcpToolsList.appendChild(card);
    });
  } catch (e) {
    console.error('Error cargando herramientas MCP:', e);
  }
}

async function executeMcpTool() {
  const toolName = mcpToolSelect.value;
  let args = {};
  try {
    args = JSON.parse(mcpToolArgs.value);
  } catch (e) {
    alert("Argumentos inválidos. Deben ser un JSON válido.");
    return;
  }

  btnExecuteMcp.disabled = true;
  mcpOutputPre.textContent = "Ejecutando herramienta MCP en el servidor...";

  try {
    const res = await fetch(`${API_BASE}/api/mcp/tools/call`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: toolName, arguments: args })
    });
    const result = await res.json();
    mcpOutputPre.textContent = JSON.stringify(result, null, 2);
    playAudioChime(784, 0.4);
  } catch (err) {
    mcpOutputPre.textContent = "Error: " + err.message;
  } finally {
    btnExecuteMcp.disabled = false;
  }
}

// ==============================================================
// TUTOR SOCRÁTICO (SIDEBAR DERECHO)
// ==============================================================
async function askTutorAboutStep(stepNumber, questionType, customText = null) {
  if (!state.activeArchetype && state.currentView === 'parametric') return;

  const archId = state.activeArchetype ? state.activeArchetype.id : 'baldor_quadratic_eq';

  // Inyectar burbuja de usuario
  addChatMessage(customText || getQuestionPromptLabel(questionType), 'user');
  const tutorBubble = addChatMessage('<span class="loading-dots">Razonando socráticamente con Gemini 3.1...</span>', 'tutor');

  try {
    const res = await fetch(`${API_BASE}/api/tutor/explain`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        archetype_id: archId,
        step_number: stepNumber,
        question_type: questionType,
        user_question: customText,
        params: state.activeParams,
        university_lens: state.selectedUniversity
      })
    });

    const data = await res.json();
    tutorBubble.innerHTML = renderMarkdownWithMath(data.explanation || 'Sin respuesta.');

    if (state.speechEnabled) {
      speakText(data.explanation);
    }

  } catch (e) {
    tutorBubble.innerHTML = `Error al consultar con el tutor: ${e.message}`;
  }
}

function getQuestionPromptLabel(type) {
  const map = {
    'source_of_number': 'Explícame de dónde sale este número',
    'process_name': '¿Qué proceso se usa aquí y cómo se llama?',
    'step_by_step': 'Enséñame paso a paso cómo resolver este ejercicio',
    'real_world_use': '¿En qué situaciones voy a usarlos en ingeniería?',
    'feynman': 'Modo Feynman: Pruébame a mí con una pregunta de examen'
  };
  return map[type] || 'Pregunta del alumno';
}

function addChatMessage(content, sender = 'tutor') {
  const bubble = document.createElement('div');
  bubble.className = `chat-bubble ${sender}`;
  bubble.innerHTML = content;
  chatStream.appendChild(bubble);
  chatStream.scrollTop = chatStream.scrollHeight;
  return bubble;
}

// ==============================================================
// INICIALIZACIÓN DE EVENTOS Y ARRANQUE
// ==============================================================
document.addEventListener('DOMContentLoaded', async () => {
  // 1. Selector de Vistas
  tabModeUniversal?.addEventListener('click', () => switchView('universal'));
  tabModeParametric?.addEventListener('click', () => switchView('parametric'));
  tabModePomodoro?.addEventListener('click', () => switchView('pomodoro'));
  tabModeFlashcards?.addEventListener('click', () => switchView('flashcards'));
  tabModeMcp?.addEventListener('click', () => switchView('mcp'));

  // 2. Lentes Universitarios
  document.querySelectorAll('.univ-tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.univ-tab-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      state.selectedUniversity = btn.dataset.univ;
      const flags = { stanford: '🇺🇸', moscow: '🇷🇺', tsinghua: '🇨🇳', harvard: '🇺🇸', polytechnique: '🇫🇷' };
      const titles = {
        stanford: 'Stanford & MIT · Intuición de Sistemas Dinámicos y Computación',
        moscow: 'Universidad Estatal de Moscú · Rigor Analítico Escuela Landau',
        tsinghua: 'Universidad Tsinghua · Precisión Algebraica Intensiva',
        harvard: 'Harvard · Fundamentos Axiomáticos y Estructuras',
        polytechnique: 'École Polytechnique · Geometría y Formas Diferenciales'
      };
      pedagogyFlag.textContent = flags[state.selectedUniversity] || '🎓';
      pedagogyTagline.textContent = titles[state.selectedUniversity] || '';
      playAudioChime(523, 0.2);
    });
  });

  // 3. Solucionador Universal
  btnSolveUniversal?.addEventListener('click', solveUniversalEquation);
  universalEquationInput?.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') solveUniversalEquation();
  });
  presetButtons.forEach(b => {
    b.addEventListener('click', () => {
      universalEquationInput.value = b.dataset.eq;
      solveUniversalEquation();
    });
  });
  btnCopyLatex?.addEventListener('click', () => {
    const sol = state.lastUniversalResult?.symbolic_result?.latex_solution;
    if (sol) {
      navigator.clipboard.writeText(sol);
      alert("✓ Fórmula LaTeX copiada al portapapeles.");
    }
  });
  btnExportUniversalNotes?.addEventListener('click', saveUniversalAsFlashcard);
  btnSpeakLesson?.addEventListener('click', () => {
    const text = state.lastUniversalResult?.explanation;
    if (text) speakText(text);
  });

  // 4. Laboratorio Paramétrico
  archetypeSelect?.addEventListener('change', (e) => selectArchetype(e.target.value));
  btnRecalculate?.addEventListener('click', recalculateArchetype);
  btnRandomize?.addEventListener('click', () => {
    if (!state.activeArchetype) return;
    Object.keys(state.activeParams).forEach(k => {
      const cur = state.activeParams[k];
      state.activeParams[k] = Math.round(cur * (0.8 + Math.random() * 0.4) * 10) / 10;
    });
    buildParamInputs(state.activeArchetype.param_schema, state.activeParams);
    recalculateArchetype();
  });

  areaTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      areaTabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      state.selectedArea = tab.dataset.area;
      loadArchetypes(state.selectedArea);
    });
  });

  // 5. Pomodoro
  btnTimerStart?.addEventListener('click', startPomodoro);
  btnTimerPause?.addEventListener('click', pausePomodoro);
  btnTimerReset?.addEventListener('click', resetPomodoro);
  timerChips.forEach(chip => {
    chip.addEventListener('click', () => {
      timerChips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      const mins = parseInt(chip.dataset.mins, 10);
      pausePomodoro();
      state.timer.totalSeconds = mins * 60;
      state.timer.remainingSeconds = mins * 60;
      timerModeLabel.textContent = mins === 10 ? 'MODO DESCANSO' : 'MODO ENFOQUE';
      updateTimerDisplay();
    });
  });
  btnLogSessionManual?.addEventListener('click', logSessionManual);

  // 6. Flashcards
  activeFlashcard?.addEventListener('click', flipFlashcard);
  sm2Buttons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      rateFlashcardSM2(btn.dataset.quality);
    });
  });
  btnOpenNewCardModal?.addEventListener('click', openNewCardPrompt);

  // 7. MCP Hub
  btnExecuteMcp?.addEventListener('click', executeMcpTool);
  mcpToolSelect?.addEventListener('change', (e) => {
    const map = {
      'solve_equation_symbolic': '{"equation": "diff(y(x), x, 2) + 4*y(x) = sin(x)", "university_lens": "stanford"}',
      'query_engineering_knowledge': '{"query": "retropropagacion gradiente redes neuronales", "top_k": 3}',
      'log_study_session_pomodoro': '{"minutes": 50, "focus_area": "ai", "topic": "Backpropagation", "notes": "Bloque de estudio"}',
      'create_study_flashcard': '{"subject_id": "ai_foundations", "title": "Loss MSE", "content": "Error cuadrático medio"}',
      'solve_parametric_archetype': '{"archetype_id": "ai_backprop_grad", "params": {"x": 2.0, "w": 0.5, "b": 0.1, "y_true": 1.0, "lr": 0.1}}'
    };
    mcpToolArgs.value = map[e.target.value] || '{}';
  });

  // 8. Botones del Boceto Didáctico (Canvas Lateral)
  document.querySelectorAll('.sketch-prompt-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const type = btn.dataset.type;
      if (type === 'feynman') {
        askTutorAboutStep(state.activeStepNumber, 'custom', "Pon a prueba mis conocimientos: hazme una pregunta conceptual profunda sobre este paso para evaluar si realmente lo domino.");
      } else {
        askTutorAboutStep(state.activeStepNumber, type);
      }
    });
  });

  // 9. Input del Chat Lateral
  btnSendQuestion?.addEventListener('click', () => {
    const q = chatInput.value.trim();
    if (!q) return;
    askTutorAboutStep(state.activeStepNumber, 'custom', q);
    chatInput.value = '';
  });
  chatInput?.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      const q = chatInput.value.trim();
      if (!q) return;
      askTutorAboutStep(state.activeStepNumber, 'custom', q);
      chatInput.value = '';
    }
  });

  // 10. Toggle de Voz
  btnToggleSpeech?.addEventListener('click', () => {
    state.speechEnabled = !state.speechEnabled;
    btnToggleSpeech.style.opacity = state.speechEnabled ? '1' : '0.5';
    btnToggleSpeech.style.color = state.speechEnabled ? '#06b6d4' : '';
    if (state.speechEnabled) {
      speakText("Voz activada. El tutor leerá las explicaciones.");
    } else {
      window.speechSynthesis?.cancel();
    }
  });

  // Arranque Inicial
  updateTimerDisplay();
  await loadArchetypes('ai');
  fetchDailyStudyStats();
});
