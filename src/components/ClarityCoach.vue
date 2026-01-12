<template>
  <div
    class="p-6 max-w-4xl mx-auto clarity-root"
  >
    <!-- Professional Header -->
    <div class="header-section">
      <h1 class="app-title">
        Clarity Coach
      </h1>
      <p class="app-subtitle">
        Professional Mathematics Analysis System
      </p>
    </div>

    <!-- Upload-Komponente -->
    <FileUpload
      @analysis-started="handleAnalysisStarted"
      @analysis-result="handleAnalysisResult"
    />
    
    <!-- DEBUG: Manual Trigger Buttons -->
    <div v-if="response && Array.isArray(response)" style="margin: 1rem 0; padding: 1rem; background: #fef3c7; border: 2px solid #fbbf24; border-radius: 0.5rem;">
      <p style="margin: 0 0 0.5rem 0; font-weight: 600; color: #92400e;">🔧 Debug Controls:</p>
      <div style="display: flex; gap: 0.5rem;">
        <button @click="showSessionForm = true" style="padding: 0.5rem 1rem; background: #3b82f6; color: white; border: none; border-radius: 0.25rem; cursor: pointer; font-weight: 600;">
          📝 Open Session Form
        </button>
        <button @click="showAssessmentModal = true; currentSessionId = 'TEST-001'" style="padding: 0.5rem 1rem; background: #10b981; color: white; border: none; border-radius: 0.25rem; cursor: pointer; font-weight: 600;">
          📊 Open Assessment Modal
        </button>
        <button @click="showSessionForm = false; showAssessmentModal = false" style="padding: 0.5rem 1rem; background: #ef4444; color: white; border: none; border-radius: 0.25rem; cursor: pointer; font-weight: 600;">
          ✕ Close All
        </button>
      </div>
    </div>

    <!-- Hinweisbereich -->
    <div
      v-if="!response && !loading"
      class="upload-hint-container"
    >
      <p class="upload-hint-text">
        Upload an image or PDF containing mathematical problems to begin analysis.
      </p>
    </div>

    <!-- Ladeanzeige -->
    <div v-if="loading" class="mt-6 text-center loading-indicator">
      <div class="loading-spinner"></div>
      <span class="loading-text">Processing analysis...</span>
    </div>

    <!-- Fehleranzeige -->
    <div v-if="response?.error" class="mt-4 error-message">
      <strong>Error:</strong> {{ response.error }}
    </div>

    <!-- Ergebnisse -->
    <div
      v-if="response && Array.isArray(response)"
      class="mt-8 space-y-6"
    >
      <div
        v-for="(task, tIndex) in response"
        :key="tIndex"
        class="bg-white rounded-xl shadow p-4 task-card"
      >
        <!-- Kopfbereich der Aufgabe -->
        <div class="task-header">
          <h2 class="task-title">
            Aufgabe {{ task.number }}:
            <span class="task-topic">{{ task.topic }}</span>
          </h2>
          <span class="task-difficulty">
            Schwierigkeit: {{ task.difficulty }}
          </span>
        </div>

        <!-- Aufgaben-Text (mit Inline-LaTeX) -->
        <p
          class="task-text"
          v-html="renderInline(task.task)"
        ></p>

        <!-- Teilaufgaben + sokratische Fragen -->
        <div v-if="Array.isArray(task.subtasks) && task.subtasks.length">
          <div
            v-for="(sub, sIndex) in task.subtasks"
            :key="sIndex"
            class="subtask-block"
          >
            <h3 class="subtask-title">
              Teilaufgabe {{ sub.label }})
            </h3>

            <!-- Teilaufgaben-Text (mit Inline-LaTeX) -->
            <p
              class="subtask-text"
              v-html="renderInline(sub.task)"
            ></p>

            <!-- Sokratische Frage (einzeln mit Refresh-Button) -->
            <div class="questions-block">
              <div class="question-header-bar">
                <span class="question-label">Sokratische Frage:</span>
                <div class="question-controls">
                  <span class="question-counter">
                    {{ currentQuestionIndex[tIndex]?.[sIndex] + 1 || 1 }} / {{ sub.questions?.length || 0 }}
                  </span>
                  <button
                    v-if="sub.questions && sub.questions.length > 1"
                    class="refresh-question-btn"
                    @click="refreshQuestion(tIndex, sIndex, sub)"
                    title="Show next question"
                  >
                    ↻
                  </button>
                </div>
              </div>
              <div class="current-question-row">
                <span class="question-bullet"></span>
                <span
                  class="question-text"
                  v-html="renderInline(sub.questions?.[currentQuestionIndex[tIndex]?.[sIndex] || 0] || 'Keine Frage verfügbar')"
                ></span>
              </div>
            </div>

            <!-- Action Buttons Row -->
            <div class="action-buttons-row">
              <!-- PHASE 2: Unified Smart Visual Button (when feature flag enabled) -->
              <template v-if="FEATURE_FLAGS.smartVisualHint">
                <button
                  class="action-btn smart-visual-btn"
                  @click="requestSmartVisual(tIndex, sIndex, task, sub)"
                  :disabled="smartVisualLoading[tIndex]?.[sIndex]"
                >
                  <span v-if="smartVisualLoading[tIndex]?.[sIndex]">
                    <span class="loading-dots">Analysiere</span>
                  </span>
                  <span v-else-if="smartVisuals[tIndex]?.[sIndex]">
                    💡 Andere Visualisierung
                  </span>
                  <span v-else>
                    💡 Visuelle Hilfe
                  </span>
                </button>
              </template>
              
              <!-- LEGACY: Separate Visual Buttons (when smartVisualHint disabled) -->
              <template v-else>
                <!-- Visualization Button -->
                <button
                  class="action-btn visualization-btn"
                  @click="toggleVisualization(tIndex, sIndex, task, sub)"
                >
                  <span v-if="visualizations[tIndex]?.[sIndex]">
                    Visualisierung ausblenden
                  </span>
                  <span v-else>
                    Visualisierung anzeigen
                  </span>
                </button>

                <!-- Manim Animation Button -->
                <button
                  class="action-btn animation-btn"
                  @click="toggleAnimation(tIndex, sIndex, task, sub)"
                >
                  <span v-if="animations[tIndex]?.[sIndex]">
                    Animation ausblenden
                  </span>
                  <span v-else>
                    Animation erstellen
                  </span>
                </button>

                <!-- Graph Button -->
                <button
                  class="action-btn graph-btn"
                  @click="toggleGraph(tIndex, sIndex, task, sub)"
                >
                  <span v-if="graphs[tIndex]?.[sIndex]">
                    Grafik ausblenden
                  </span>
                  <span v-else>
                    Grafik erstellen
                  </span>
                </button>
              </template>

              <!-- Hint Button (Progressive Socratic Hints) - Always shown -->
              <button
                class="action-btn hint-btn"
                @click="requestHint(tIndex, sIndex, task, sub)"
              >
                <span v-if="hintLoading[tIndex]?.[sIndex]">
                  Lädt...
                </span>
                <span v-else>
                  🤔 Hilfestellung ({{ hintsUsed[tIndex]?.[sIndex] || 0 }})
                </span>
              </button>
            </div>

            <!-- PHASE 2: Smart Visual Loading & Display -->
            <template v-if="FEATURE_FLAGS.smartVisualHint">
              <!-- Smart Visual Loading -->
              <div
                v-if="smartVisualLoading[tIndex]?.[sIndex]"
                class="smart-visual-loading"
              >
                <div class="loading-spinner"></div>
                <span>KI wählt beste Visualisierung aus...</span>
              </div>

              <!-- Smart Visual Box (Unified Display) -->
              <div
                v-if="smartVisuals[tIndex]?.[sIndex]"
                class="smart-visual-box"
                :class="`visual-type-${smartVisuals[tIndex][sIndex].type}`"
              >
                <div class="smart-visual-header">
                  <h4 class="smart-visual-title">
                    {{ getSmartVisualTitle(smartVisuals[tIndex][sIndex].type) }}
                  </h4>
                  <span class="visual-type-badge">
                    {{ getSmartVisualBadge(smartVisuals[tIndex][sIndex].type) }}
                  </span>
                </div>
                <p class="visual-reason">
                  {{ smartVisuals[tIndex][sIndex].reason }}
                </p>
                
                <!-- Render based on type -->
                <div v-if="smartVisuals[tIndex][sIndex].type === 'graph'" class="smart-visual-content">
                  <div :id="`smart-graph-${tIndex}-${sIndex}`" class="graph-container"></div>
                </div>
                <div v-else-if="smartVisuals[tIndex][sIndex].type === 'animation'" class="smart-visual-content">
                  <div :id="`smart-anim-${tIndex}-${sIndex}`" class="animation-canvas"></div>
                  <button 
                    class="replay-btn"
                    @click="replaySmartAnimation(tIndex, sIndex)"
                    :disabled="smartVisuals[tIndex][sIndex].playing"
                  >
                    {{ smartVisuals[tIndex][sIndex].playing ? '⏳ Läuft...' : '🔄 Wiederholen' }}
                  </button>
                </div>
                <div v-else class="smart-visual-content">
                  <div v-html="formatVisualization(smartVisuals[tIndex][sIndex].data)"></div>
                </div>
              </div>
            </template>

            <!-- LEGACY: Separate Visual Displays (when smartVisualHint disabled) -->
            <template v-else>
              <!-- Ladeanzeige für Visualization -->
              <div
                v-if="visualizationLoading[tIndex]?.[sIndex]"
                class="visualization-loading"
              >
                Visualisierung wird generiert...
              </div>

              <!-- Visualization Box -->
              <div
                v-if="visualizations[tIndex]?.[sIndex]"
                class="visualization-box"
              >
                <h4 class="visualization-title">📊 Schlüsselfakten & Visualisierung</h4>
                <div v-html="formatVisualization(visualizations[tIndex][sIndex])"></div>
              </div>
            </template>

            <!-- LEGACY: Animation & Graph (when smartVisualHint disabled) -->
            <template v-if="!FEATURE_FLAGS.smartVisualHint">
              <!-- Ladeanzeige für Animation -->
              <div
                v-if="animationLoading[tIndex]?.[sIndex]"
                class="animation-loading"
              >
                <div class="loading-spinner"></div>
                <span>Animation wird erstellt... Dies kann bis zu 30 Sekunden dauern.</span>
              </div>

              <!-- Animation Box -->
              <div
                v-if="animations[tIndex]?.[sIndex]"
                class="animation-box"
              >
                <div class="animation-header">
                  <h4 class="animation-title">🎬 Interaktive Animation</h4>
                  <button 
                    class="replay-btn"
                    @click="replayAnimation(tIndex, sIndex)"
                    :disabled="animations[tIndex][sIndex].playing"
                  >
                    {{ animations[tIndex][sIndex].playing ? '⏳ Läuft...' : '🔄 Wiederholen' }}
                  </button>
                </div>
                
                <!-- Animation Container -->
                <div 
                  :id="`anim-${tIndex}-${sIndex}`"
                  class="animation-canvas"
                ></div>
              </div>

              <!-- Ladeanzeige für Graph -->
              <div
                v-if="graphLoading[tIndex]?.[sIndex]"
                class="graph-loading"
              >
                <div class="loading-spinner"></div>
                <span>Grafik wird erstellt...</span>
              </div>

              <!-- Graph Box -->
              <div
                v-if="graphs[tIndex]?.[sIndex]"
                class="graph-box"
              >
                <h4 class="graph-title">📊 Interaktive Grafik</h4>
                <div 
                  :id="`graph-${tIndex}-${sIndex}`"
                  class="graph-container"
                ></div>
              </div>
            </template>

            <!-- Hint Loading -->
            <div
              v-if="hintLoading[tIndex]?.[sIndex]"
              class="hint-loading"
            >
              <div class="loading-spinner"></div>
              <span>Hilfestellung wird generiert...</span>
            </div>

            <!-- Hint Box (Progressive Socratic Hints) -->
            <div
              v-if="hints[tIndex]?.[sIndex]"
              class="hint-box"
            >
              <div class="hint-header">
                <h4 class="hint-title">
                  💡 Hilfestellung (Stufe {{ hints[tIndex][sIndex].level }}/3)
                </h4>
                <span :class="['hint-level-badge', `level-${hints[tIndex][sIndex].level}`]">
                  {{ hints[tIndex][sIndex].level === 1 ? 'Sokratisch' : hints[tIndex][sIndex].level === 2 ? 'Anleitend' : 'Spezifisch' }}
                </span>
              </div>
              <p class="hint-text" v-html="renderInline(hints[tIndex][sIndex].text)"></p>
              <div class="hint-encouragement">
                {{ hints[tIndex][sIndex].encouragement }}
              </div>
              <div v-if="hints[tIndex][sIndex].level < 3" class="hint-more">
                <button 
                  class="more-hint-btn"
                  @click="requestHint(tIndex, sIndex, task, sub)"
                >
                  Weitere Hilfe benötigt?
                </button>
              </div>
            </div>

            <!-- PHASE 3.2: Smart Approach Checker -->
            <template v-if="FEATURE_FLAGS.smartApproachChecker">
              <!-- Toggle Button to Show/Hide Approach Checker Input -->
              <button
                class="action-btn approach-checker-toggle-btn"
                @click="toggleApproachInput(tIndex, sIndex)"
                :disabled="approachCheckLoading[tIndex]?.[sIndex]"
              >
                <span v-if="showApproachInput[tIndex]?.[sIndex]">
                  ✗ Eingabe schließen
                </span>
                <span v-else>
                  ✓ Meinen Ansatz prüfen
                </span>
              </button>

              <!-- Approach Input Area -->
              <div
                v-if="showApproachInput[tIndex]?.[sIndex]"
                class="approach-input-area"
              >
                <label class="approach-input-label">
                  Beschreibe deinen Lösungsansatz oder gib deine bisherige Rechnung ein:
                </label>
                <textarea
                  v-model="studentWork[tIndex][sIndex]"
                  class="approach-textarea"
                  placeholder="z.B.: Ich berechne zuerst die Ableitung f'(x) = 3x² - 6x + 2, dann setze ich sie gleich null..."
                  rows="4"
                ></textarea>
                <div class="approach-input-actions">
                  <button
                    class="check-approach-btn"
                    @click="checkApproach(tIndex, sIndex, task, sub)"
                    :disabled="!studentWork[tIndex]?.[sIndex]?.trim() || approachCheckLoading[tIndex]?.[sIndex]"
                  >
                    <span v-if="approachCheckLoading[tIndex]?.[sIndex]">
                      <span class="loading-dots">Wird geprüft</span>
                    </span>
                    <span v-else>
                      ✓ Ansatz überprüfen
                    </span>
                  </button>
                  <span class="approach-hint-text">
                    Tipp: Je detaillierter deine Beschreibung, desto besser das Feedback!
                  </span>
                </div>
              </div>

              <!-- Approach Check Loading -->
              <div
                v-if="approachCheckLoading[tIndex]?.[sIndex]"
                class="approach-check-loading"
              >
                <div class="loading-spinner"></div>
                <span>Dein Ansatz wird analysiert...</span>
              </div>

              <!-- Approach Check Result -->
              <div
                v-if="approachResults[tIndex]?.[sIndex] && !approachCheckLoading[tIndex]?.[sIndex]"
                class="approach-result-box"
                :class="getApproachResultClass(approachResults[tIndex][sIndex])"
              >
                <div class="approach-result-header">
                  <div class="approach-track-indicator">
                    <span v-if="approachResults[tIndex][sIndex].isOnRightTrack" class="track-icon track-correct">✓</span>
                    <span v-else class="track-icon track-needs-work">○</span>
                    <span class="track-text">
                      {{ approachResults[tIndex][sIndex].isOnRightTrack ? 'Auf dem richtigen Weg!' : 'Noch nicht ganz...' }}
                    </span>
                  </div>
                  <div class="confidence-score">
                    <span class="confidence-label">Bewertung:</span>
                    <div class="confidence-stars">
                      <span 
                        v-for="star in 5" 
                        :key="star" 
                        :class="['star', star <= approachResults[tIndex][sIndex].confidenceScore ? 'filled' : 'empty']"
                      >★</span>
                    </div>
                  </div>
                </div>

                <p class="approach-assessment">
                  {{ approachResults[tIndex][sIndex].overallAssessment }}
                </p>

                <div v-if="approachResults[tIndex][sIndex].strengths?.length" class="approach-strengths">
                  <h5>✓ Was gut war:</h5>
                  <ul>
                    <li v-for="(strength, idx) in approachResults[tIndex][sIndex].strengths" :key="idx">
                      {{ strength }}
                    </li>
                  </ul>
                </div>

                <div v-if="approachResults[tIndex][sIndex].improvements?.length" class="approach-improvements">
                  <h5>→ Verbesserungsvorschläge:</h5>
                  <ul>
                    <li v-for="(improvement, idx) in approachResults[tIndex][sIndex].improvements" :key="idx">
                      {{ improvement }}
                    </li>
                  </ul>
                </div>

                <div v-if="approachResults[tIndex][sIndex].specificIssue" class="approach-specific-issue">
                  <h5>⚠ Spezifisches Problem:</h5>
                  <p>{{ approachResults[tIndex][sIndex].specificIssue }}</p>
                </div>

                <div class="approach-next-step">
                  <h5>📍 Nächster Schritt:</h5>
                  <p>{{ approachResults[tIndex][sIndex].nextStep }}</p>
                </div>

                <div class="approach-encouragement">
                  {{ approachResults[tIndex][sIndex].encouragement }}
                </div>

                <button
                  class="retry-approach-btn"
                  @click="clearApproachResult(tIndex, sIndex)"
                >
                  🔄 Neuen Ansatz eingeben
                </button>
              </div>
            </template>
          </div>
        </div>
        <div
          v-else
          class="no-subtasks"
        >
          Für diese Aufgabe wurden (noch) keine Teilaufgaben erkannt.
        </div>

        <!-- Feedback Buttons (pro Aufgabe) -->
        <div class="feedback-row">
          <button
            @click="giveFeedback(tIndex, 'helpful')"
            :class="[
              'feedback-btn feedback-btn-positive',
              feedback[tIndex] === 'helpful' && 'active'
            ]"
          >
            Helpful
          </button>

          <button
            @click="giveFeedback(tIndex, 'unclear')"
            :class="[
              'feedback-btn feedback-btn-negative',
              feedback[tIndex] === 'unclear' && 'active'
            ]"
          >
            Needs Clarification
          </button>
        </div>
      </div>
    </div>
    
    <!-- Session Logging Form -->
    <SessionForm
      ref="sessionFormRef"
      :isOpen="showSessionForm"
      :fileName="uploadedFileName"
      :fileType="uploadedFileType"
      :taskCount="response?.length || 0"
      :subtaskCount="totalSubtasks"
      @close="showSessionForm = false"
      @submitted="handleSessionSubmitted"
    />
    
    <!-- Post-Session Assessment Modal -->
    <PostSessionAssessment
      :isOpen="showAssessmentModal"
      :sessionId="currentSessionId"
      :questionLoops="totalQuestionLoops"
      :visualHintsUsed="usageStats.smartVisuals || 0"
      :totalHintsUsed="usageStats.hints || 0"
      :approachChecksUsed="usageStats.approachChecks || 0"
      :selfSufficiencyScore="calculatedSelfSufficiencyScore"
      @close="showAssessmentModal = false"
      @submitted="handleAssessmentSubmitted"
    />
  </div>
</template>

<script setup>
import { ref, computed, nextTick } from 'vue'
import FileUpload from './FileUpload.vue'
import SessionForm from './SessionForm.vue'
import PostSessionAssessment from './PostSessionAssessment.vue'
import { toast } from 'vue-sonner'
import katex from 'katex'
import 'katex/dist/katex.min.css'
import gsap from 'gsap'
// Phase 2.2: Replaced Plotly (~2.35MB) with Chart.js (~200KB)
import { Chart, registerables } from 'chart.js'
Chart.register(...registerables)
import { FEATURE_FLAGS } from '../config/featureFlags.js'
import { visualHintService, VISUAL_TYPES } from '../services/visualHintService.js'

const response = ref(null)
const feedback = ref({})
const loading = ref(false)

// Session Form
const showSessionForm = ref(false)
const sessionFormRef = ref(null)
const uploadedFileName = ref('')
const uploadedFileType = ref('')
const usageStats = ref({
  visualizations: 0,
  animations: 0,
  graphs: 0,
  hints: 0,                    // Total hints used
  hintLevels: [],              // Track which levels were used [1,1,2,3,...]
  socraticHintsUsed: 0,        // Level 1 hints count
  directiveHintsUsed: 0,       // Level 2 hints count
  specificHintsUsed: 0,        // Level 3 hints count
  smartVisuals: 0,            // Unified visual count (Phase 2)
  visualTypes: [],             // Track what visual types were used ['graph', 'animation', ...]
  approachChecks: 0,           // Phase 3.3: Track approach check usage
  approachCheckResults: [],    // Track results: [true, false, true, ...]
  tutorInterventions: 0,       // Manual tutor interventions
  studentOverrides: 0          // Student rejected AI suggestions
})

// Progressive Hints System (Replaces Solution)
const hints = ref([])            // [ [{ level, text, encouragement }|null, ...], ... ]
const hintLoading = ref([])      // [ [bool, ...], ... ]
const hintsUsed = ref([])        // [ [number, ...], ... ] - tracks hint count per subtask

// Smart Approach Checker System (Phase 3.2)
const showApproachInput = ref([])     // [ [bool, ...], ... ] - toggle input visibility
const studentWork = ref([])           // [ [string, ...], ... ] - student's work/approach input
const approachCheckLoading = ref([])  // [ [bool, ...], ... ] - loading state
const approachResults = ref([])       // [ [{ isOnRightTrack, overallAssessment, ... }|null, ...], ... ]

// Visualizations & Ladezustand je Teilaufgabe
const visualizations = ref([])        // [ [string|null, ...], ... ]
const visualizationLoading = ref([])  // [ [bool, ...], ... ]

// Animations (Manim) & Ladezustand je Teilaufgabe
const animations = ref([])            // [ [string|null, ...], ... ]
const animationLoading = ref([])      // [ [bool, ...], ... ]

// Graphs (Chart.js - Phase 2.2) & Ladezustand je Teilaufgabe
const graphs = ref([])                // [ [{ data, chartInstance }|null, ...], ... ]
const graphLoading = ref([])          // [ [bool, ...], ... ]
const chartInstances = ref({})        // { 'graph-0-0': Chart instance } - track for cleanup

// Unified Smart Visual System (Phase 2)
const smartVisuals = ref([])          // [ [{ type, data, label }|null, ...], ... ]
const smartVisualLoading = ref([])    // [ [bool, ...], ... ]
const smartVisualTypes = ref([])      // [ [string|null, ...], ... ] - tracks what type was shown
const previousVisuals = ref([])       // [ [string[], ...], ... ] - tracks previous visual types per subtask
const subtaskStartTime = ref([])      // [ [timestamp, ...], ... ] - when subtask was first viewed

// Track current question index for each subtask
const currentQuestionIndex = ref([])  // [ [number, ...], ... ]

// Track question loop interactions for assessment
const questionLoopTracking = ref({})  // { taskIndex: { subIndex: { totalRefreshes, viewHistory } } }

// Assessment Modal
const showAssessmentModal = ref(false)
const currentSessionId = ref('')

// ----------------------
// Computed Properties
// ----------------------
const totalSubtasks = computed(() => {
  if (!response.value || !Array.isArray(response.value)) return 0
  return response.value.reduce((total, task) => {
    return total + (task.subtasks?.length || 0)
  }, 0)
})

const totalQuestionLoops = computed(() => {
  let total = 0
  Object.values(questionLoopTracking.value).forEach(task => {
    Object.values(task).forEach(subtask => {
      total += (subtask.totalRefreshes || 0)
    })
  })
  return total
})

// Calculate self-sufficiency score for assessment modal
const calculatedSelfSufficiencyScore = computed(() => {
  const totalHelp = (usageStats.value.hints || 0) + (usageStats.value.approachChecks || 0)
  if (totalHelp === 0) return 5      // Solved independently
  if (totalHelp <= 2) return 4       // Minimal help
  if (totalHelp <= 5) return 3       // Moderate help
  if (totalHelp <= 8) return 2       // Significant help
  return 1                           // Heavy support needed
})

// ----------------------
// Session Logging Handlers
// ----------------------
function handleSessionSubmitted(result) {
  console.log('Session logged:', result)
  // Update form with current stats
  if (sessionFormRef.value) {
    sessionFormRef.value.updateUsageStats(usageStats.value)
  }
  
  // Capture session ID for later assessment
  if (result && result.session_id) {
    currentSessionId.value = result.session_id
    console.log('[SESSION] Session ID captured:', result.session_id)
    
    // Don't auto-open assessment - let user interact with Clarity Coach first!
    toast.info('Session gespeichert! Nutze jetzt die Clarity Coach Features.', {
      description: 'Assessment kann später über Debug-Button geöffnet werden.'
    })
  }
}

function handleAssessmentSubmitted(result) {
  console.log('Assessment submitted:', result)
  showAssessmentModal.value = false
  toast.success('Thank you for completing the assessment!')
}

// ----------------------
// Hilfsfunktionen LaTeX
// ----------------------
const escapeHtml = (s) =>
  s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;')

/**
 * Inline-LaTeX im Text rendern:
 * erkennt $$...$$, \[...\], \(...\), $...$, und auch rohe LaTeX-Befehle
 * und rendert sie mit KaTeX, der Rest bleibt normaler Text.
 */
function renderInline(text) {
  if (!text) return ''

  // First, handle delimited math
  const delimitedRegex = /(\$\$[^$]+\$\$|\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)|\$[^$]+\$)/g
  
  // Check if text has delimited math
  if (delimitedRegex.test(text)) {
    delimitedRegex.lastIndex = 0 // Reset regex
    let result = ''
    let lastIndex = 0
    let match

    while ((match = delimitedRegex.exec(text)) !== null) {
      const index = match.index
      const raw = match[0]

      if (index > lastIndex) {
        result += escapeHtml(text.slice(lastIndex, index))
      }

      let displayMode = false
      let content = raw

      if (raw.startsWith('$$') && raw.endsWith('$$')) {
        displayMode = true
        content = raw.slice(2, -2)
      } else if (raw.startsWith('\\[') && raw.endsWith('\\]')) {
        displayMode = true
        content = raw.slice(2, -2)
      } else if (raw.startsWith('\\(') && raw.endsWith('\\)')) {
        displayMode = false
        content = raw.slice(2, -2)
      } else if (raw.startsWith('$') && raw.endsWith('$')) {
        displayMode = false
        content = raw.slice(1, -1)
      }

      try {
        const rendered = katex.renderToString(content.trim(), {
          displayMode,
          throwOnError: false
        })
        result += rendered
      } catch (e) {
        result += escapeHtml(raw)
      }

      lastIndex = delimitedRegex.lastIndex
    }

    if (lastIndex < text.length) {
      result += escapeHtml(text.slice(lastIndex))
    }

    return result
  }

  // If no delimited math, look for inline math patterns like f'(x_1) or f''(x_1) = 0
  // Match patterns like: f'(...), f''(...), x_1, x_2, etc.
  const inlineMathRegex = /([a-zA-Z]'*\([^)]+\)|[a-zA-Z]'+'|[a-zA-Z]_\{?\d+\}?|[a-zA-Z]_[a-zA-Z]|\b[a-zA-Z]\s*[=≠≤≥<>]\s*\d+)/g
  
  // Check if text has inline math patterns
  if (inlineMathRegex.test(text)) {
    inlineMathRegex.lastIndex = 0 // Reset regex
    let result = ''
    let lastIndex = 0
    let match
    
    while ((match = inlineMathRegex.exec(text)) !== null) {
      const index = match.index
      const mathPart = match[0]
      
      // Add text before math
      if (index > lastIndex) {
        result += escapeHtml(text.slice(lastIndex, index))
      }
      
      // Try to render the math part
      try {
        const rendered = katex.renderToString(mathPart.trim(), {
          displayMode: false,
          throwOnError: false
        })
        result += rendered
      } catch (e) {
        result += escapeHtml(mathPart)
      }
      
      lastIndex = inlineMathRegex.lastIndex
    }
    
    // Add remaining text
    if (lastIndex < text.length) {
      result += escapeHtml(text.slice(lastIndex))
    }
    
    return result
  }

  return escapeHtml(text)
}

/* Lösungstext (eigene, zeilenweise LaTeX-Logik) */
function formatLatex(text) {
  if (!text) return ''

  const stripDelimiters = (s) => {
    let t = s.trim()
    if (['\\[', '\\]', '\\(', '\\)', '$$', '$'].includes(t)) return ''
    if (t.startsWith('$$') && t.endsWith('$$')) t = t.slice(2, -2).trim()
    if (t.startsWith('\\[') && t.endsWith('\\]')) t = t.slice(2, -2).trim()
    if (t.startsWith('\\(') && t.endsWith('\\)')) t = t.slice(2, -2).trim()
    return t
  }

  const lines = text
    .split('\n')
    .map(l => l.trim())
    .filter(l => l.length > 0)

  // Group consecutive equations together
  const groups = []
  let currentGroup = { type: null, items: [] }
  
  lines.forEach(line => {
    if (line.startsWith('Lösung:') || line.startsWith('Begründung:')) {
      if (currentGroup.items.length > 0) {
        groups.push(currentGroup)
      }
      groups.push({ type: 'header', items: [line] })
      currentGroup = { type: null, items: [] }
      return
    }

    const stripped = stripDelimiters(line)
    if (!stripped) return

    const wordCount = stripped.split(/\s+/).length
    const hasMathSymbols = /[=^\\]/.test(stripped)
    const hasUmlaut = /[äöüÄÖÜß]/.test(stripped)
    const looksLikeEquation = hasMathSymbols && wordCount <= 6 && !hasUmlaut

    if (looksLikeEquation) {
      if (currentGroup.type !== 'equations') {
        if (currentGroup.items.length > 0) {
          groups.push(currentGroup)
        }
        currentGroup = { type: 'equations', items: [] }
      }
      currentGroup.items.push(stripped)
    } else {
      if (currentGroup.items.length > 0) {
        groups.push(currentGroup)
      }
      groups.push({ type: 'text', items: [stripped] })
      currentGroup = { type: null, items: [] }
    }
  })

  if (currentGroup.items.length > 0) {
    groups.push(currentGroup)
  }

  // Render groups
  const htmlParts = groups.map(group => {
    if (group.type === 'header') {
      const line = group.items[0]
      if (line.startsWith('Lösung:')) {
        return `<div class="latex-section-header solution-header">
                  <span class="latex-label">Lösung.</span>
                </div>`
      }
      if (line.startsWith('Begründung:')) {
        return `<div class="latex-section-header proof-header">
                  <span class="latex-label">Begründung.</span>
                </div>`
      }
    }

    if (group.type === 'equations') {
      // Render as aligned equation block
      const equationHtmls = group.items.map(eq => {
        try {
          const rendered = katex.renderToString(eq, {
            displayMode: true,
            throwOnError: false
          })
          return rendered
        } catch (e) {
          return escapeHtml(eq)
        }
      })
      
      return `<div class="latex-aligned-equations">${equationHtmls.join('')}</div>`
    }

    if (group.type === 'text') {
      const line = group.items[0]
      
      // Check if line contains LaTeX commands
      const hasLatexCommands = /\\[a-zA-Z]+|\\{|\\}/.test(line)
      
      if (hasLatexCommands) {
        // Render line with inline LaTeX support
        return `<div class="latex-text-line">${renderInline(line)}</div>`
      }
      
      // Legacy handling for special patterns
      if (line.includes('f(x') && line.includes(' ist ')) {
        const idxIst = line.indexOf(' ist ')
        const mathPart = line.slice(0, idxIst).trim()
        const textPart = line.slice(idxIst).trim()

        let mathHtml = escapeHtml(mathPart)
        try {
          mathHtml = katex.renderToString(mathPart, {
            displayMode: false,
            throwOnError: false
          })
        } catch (e) {}

        return `<div class="latex-text-line">${mathHtml} ${escapeHtml(textPart)}</div>`
      }
      return `<div class="latex-text-line">${escapeHtml(line)}</div>`
    }

    return ''
  })

  return htmlParts.join('')
}

/* ----------------------------------------------------------------------------
 * Analyse beginnt (von FileUpload signalisiert)
 * --------------------------------------------------------------------------*/
function handleAnalysisStarted(fileInfo) {
  loading.value = true
  response.value = null
  hints.value = []
  hintLoading.value = []
  hintsUsed.value = []
  visualizations.value = []
  visualizationLoading.value = []
  animations.value = []
  animationLoading.value = []
  graphs.value = []
  graphLoading.value = []
  // Phase 2: Smart Visual System
  smartVisuals.value = []
  smartVisualLoading.value = []
  smartVisualTypes.value = []
  previousVisuals.value = []
  subtaskStartTime.value = []
  currentQuestionIndex.value = []
  // Phase 3.2: Smart Approach Checker
  showApproachInput.value = []
  studentWork.value = []
  approachCheckLoading.value = []
  approachResults.value = []
  
  // Store file info for session logging
  if (fileInfo) {
    uploadedFileName.value = fileInfo.fileName || ''
    uploadedFileType.value = fileInfo.fileType || ''
  }
  
  // Reset usage stats
  usageStats.value = {
    visualizations: 0,
    animations: 0,
    graphs: 0,
    hints: 0,
    hintLevels: [],
    socraticHintsUsed: 0,
    directiveHintsUsed: 0,
    specificHintsUsed: 0,
    smartVisuals: 0,
    visualTypes: [],
    approachChecks: 0,
    approachCheckResults: [],
    tutorInterventions: 0,
    studentOverrides: 0
  }
  
  // Reset question loop tracking
  questionLoopTracking.value = {}
  
  // Reset assessment modal
  showAssessmentModal.value = false
  currentSessionId.value = ''
}

/* ----------------------------------------------------------------------------
 * Wird ausgelöst, wenn FileUpload.vue die Analyse zurückgibt
 * --------------------------------------------------------------------------*/
function handleAnalysisResult(data) {
  loading.value = false

  if (data.error) {
    response.value = data
    toast.error('Fehler bei der Analyse', {
      description: data.error
    })
    return
  }

  response.value = data

  feedback.value = {}
  response.value.forEach((task, i) => {
    feedback.value[i] = localStorage.getItem(`feedback_task_${i}`) || null
  })

  // Initialize progressive hints (replaces solutions)
  hints.value = response.value.map(task =>
    (task.subtasks || []).map(() => null)
  )
  hintLoading.value = response.value.map(task =>
    (task.subtasks || []).map(() => false)
  )
  hintsUsed.value = response.value.map(task =>
    (task.subtasks || []).map(() => 0)
  )
  visualizations.value = response.value.map(task =>
    (task.subtasks || []).map(() => null)
  )
  visualizationLoading.value = response.value.map(task =>
    (task.subtasks || []).map(() => false)
  )
  animations.value = response.value.map(task =>
    (task.subtasks || []).map(() => null)
  )
  animationLoading.value = response.value.map(task =>
    (task.subtasks || []).map(() => false)
  )
  graphs.value = response.value.map(task =>
    (task.subtasks || []).map(() => null)
  )
  graphLoading.value = response.value.map(task =>
    (task.subtasks || []).map(() => false)
  )
  // Phase 2: Initialize smart visual arrays
  smartVisuals.value = response.value.map(task =>
    (task.subtasks || []).map(() => null)
  )
  smartVisualLoading.value = response.value.map(task =>
    (task.subtasks || []).map(() => false)
  )
  smartVisualTypes.value = response.value.map(task =>
    (task.subtasks || []).map(() => null)
  )
  previousVisuals.value = response.value.map(task =>
    (task.subtasks || []).map(() => [])
  )
  subtaskStartTime.value = response.value.map(task =>
    (task.subtasks || []).map(() => Date.now())
  )
  currentQuestionIndex.value = response.value.map(task =>
    (task.subtasks || []).map(() => 0)  // Start with first question
  )
  // Phase 3.2: Initialize approach checker arrays
  showApproachInput.value = response.value.map(task =>
    (task.subtasks || []).map(() => false)
  )
  studentWork.value = response.value.map(task =>
    (task.subtasks || []).map(() => '')
  )
  approachCheckLoading.value = response.value.map(task =>
    (task.subtasks || []).map(() => false)
  )
  approachResults.value = response.value.map(task =>
    (task.subtasks || []).map(() => null)
  )

  toast.success('Analysis complete', {
    description: 'Socratic questions have been successfully generated.'
  })
  
  // Show session form after analysis
  showSessionForm.value = true
}

/* ----------------------------------------------------------------------------
 * Feedback speichern
 * --------------------------------------------------------------------------*/
function giveFeedback(index, type) {
  feedback.value[index] = type
  localStorage.setItem(`feedback_task_${index}`, type)
  toast.info('Feedback saved successfully.')
}

/* ----------------------------------------------------------------------------
 * Refresh Socratic Question - cycle to next question
 * --------------------------------------------------------------------------*/
function refreshQuestion(taskIndex, subIndex, subtask) {
  if (!subtask.questions || subtask.questions.length === 0) return
  
  // Initialize tracking if needed
  if (!questionLoopTracking.value[taskIndex]) {
    questionLoopTracking.value[taskIndex] = {}
  }
  if (!questionLoopTracking.value[taskIndex][subIndex]) {
    questionLoopTracking.value[taskIndex][subIndex] = {
      totalRefreshes: 0,
      viewHistory: []
    }
  }
  
  const currentIdx = currentQuestionIndex.value[taskIndex][subIndex]
  const nextIdx = (currentIdx + 1) % subtask.questions.length
  
  // Track the refresh
  questionLoopTracking.value[taskIndex][subIndex].totalRefreshes++
  questionLoopTracking.value[taskIndex][subIndex].viewHistory.push({
    questionIndex: nextIdx,
    timestamp: new Date().toISOString(),
    isLoop: nextIdx === 0 && currentIdx !== 0 // Full cycle detected
  })
  
  currentQuestionIndex.value[taskIndex][subIndex] = nextIdx
  
  toast.success('Question updated', {
    description: `Showing question ${nextIdx + 1} of ${subtask.questions.length} (Loops: ${questionLoopTracking.value[taskIndex][subIndex].totalRefreshes})`
  })
}

/* ----------------------------------------------------------------------------
 * Progressive Hint System (Socratic → Directive → Specific)
 * REPLACES the old toggleSolution function
 * --------------------------------------------------------------------------*/
async function requestHint(taskIndex, subIndex, task, subtask) {
  // Initialize arrays if needed
  if (!hints.value[taskIndex]) {
    hints.value[taskIndex] = []
  }
  if (!hintLoading.value[taskIndex]) {
    hintLoading.value[taskIndex] = []
  }
  if (!hintsUsed.value[taskIndex]) {
    hintsUsed.value[taskIndex] = []
  }
  
  // Get current hint level (1, 2, or 3)
  const currentHints = hintsUsed.value[taskIndex][subIndex] || 0
  const nextLevel = Math.min(currentHints + 1, 3)
  
  // If already at level 3, just show encouraging message
  if (currentHints >= 3) {
    toast.info('Maximale Hilfestellung erreicht', {
      description: 'Du hast bereits alle 3 Hilfestellungen erhalten. Versuche jetzt, die Aufgabe zu lösen!'
    })
    return
  }
  
  hintLoading.value[taskIndex][subIndex] = true

  try {
    const res = await fetch(
      'http://127.0.0.1:8000/hint',
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          taskNumber: task.number,
          topic: task.topic,
          taskText: task.task,
          subLabel: subtask.label,
          subtaskText: subtask.task,
          hintLevel: nextLevel,
          previousHints: hints.value[taskIndex][subIndex]?.text || null
        })
      }
    )

    if (!res.ok) {
      throw new Error('Serverfehler beim Laden der Hilfestellung.')
    }

    const data = await res.json()

    if (data.error) {
      throw new Error(data.error)
    }

    // Store the hint
    hints.value[taskIndex][subIndex] = {
      level: nextLevel,
      text: data.hint,
      encouragement: data.encouragement || 'Du schaffst das! 💪'
    }
    
    // Track usage
    hintsUsed.value[taskIndex][subIndex] = nextLevel
    usageStats.value.hints++
    usageStats.value.hintLevels.push(nextLevel)
    
    // Track separate hint level counts
    if (nextLevel === 1) {
      usageStats.value.socraticHintsUsed++
    } else if (nextLevel === 2) {
      usageStats.value.directiveHintsUsed++
    } else if (nextLevel === 3) {
      usageStats.value.specificHintsUsed++
    }
    
    // Show toast based on level
    const levelNames = {
      1: 'Sokratische Frage',
      2: 'Anleitender Hinweis',
      3: 'Spezifische Hilfe'
    }
    toast.success(levelNames[nextLevel], {
      description: `Hilfestellung ${nextLevel}/3`
    })
    
  } catch (err) {
    toast.error('Fehler beim Laden der Hilfestellung', {
      description: err.message
    })
  } finally {
    hintLoading.value[taskIndex][subIndex] = false
  }
}

/* ----------------------------------------------------------------------------
 * PHASE 3.2: Smart Approach Checker Functions
 * --------------------------------------------------------------------------*/

/**
 * Toggle the approach input visibility
 */
function toggleApproachInput(taskIndex, subIndex) {
  // Initialize arrays if needed
  if (!showApproachInput.value[taskIndex]) {
    showApproachInput.value[taskIndex] = []
  }
  if (!studentWork.value[taskIndex]) {
    studentWork.value[taskIndex] = []
  }
  
  // Toggle visibility
  showApproachInput.value[taskIndex][subIndex] = !showApproachInput.value[taskIndex][subIndex]
}

/**
 * Check the student's approach without revealing the solution
 */
async function checkApproach(taskIndex, subIndex, task, subtask) {
  // Initialize arrays if needed
  if (!approachCheckLoading.value[taskIndex]) {
    approachCheckLoading.value[taskIndex] = []
  }
  if (!approachResults.value[taskIndex]) {
    approachResults.value[taskIndex] = []
  }
  
  const work = studentWork.value[taskIndex]?.[subIndex]?.trim()
  
  if (!work) {
    toast.warning('Bitte gib deinen Lösungsansatz ein', {
      description: 'Beschreibe, wie du die Aufgabe lösen würdest.'
    })
    return
  }
  
  approachCheckLoading.value[taskIndex][subIndex] = true
  
  try {
    const res = await fetch('http://127.0.0.1:8000/check-approach', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        taskNumber: task.number,
        topic: task.topic,
        taskText: task.task,
        subLabel: subtask.label,
        subtaskText: subtask.task,
        studentWork: work
      })
    })

    if (!res.ok) {
      throw new Error('Serverfehler beim Prüfen des Ansatzes.')
    }

    const data = await res.json()

    if (data.error) {
      throw new Error(data.error)
    }

    // Store the result
    approachResults.value[taskIndex][subIndex] = {
      isOnRightTrack: data.isOnRightTrack,
      overallAssessment: data.overallAssessment,
      strengths: data.strengths || [],
      improvements: data.improvements || [],
      specificIssue: data.specificIssue,
      nextStep: data.nextStep,
      encouragement: data.encouragement || 'Weiter so!',
      confidenceScore: data.confidenceScore || 3
    }
    
    // Track usage
    usageStats.value.approachChecks = (usageStats.value.approachChecks || 0) + 1
    // Track approach check result (true = on right track, false = needs improvement)
    usageStats.value.approachCheckResults.push(data.isOnRightTrack || false)
    
    // Show toast based on result
    if (data.isOnRightTrack) {
      toast.success('Guter Ansatz!', {
        description: 'Du bist auf dem richtigen Weg.'
      })
    } else {
      toast.info('Feedback erhalten', {
        description: 'Schau dir die Verbesserungsvorschläge an.'
      })
    }
    
    // Hide the input area after checking
    showApproachInput.value[taskIndex][subIndex] = false

  } catch (err) {
    toast.error('Fehler beim Prüfen des Ansatzes', {
      description: err.message
    })
  } finally {
    approachCheckLoading.value[taskIndex][subIndex] = false
  }
}

/**
 * Clear the approach result to enter a new one
 */
function clearApproachResult(taskIndex, subIndex) {
  if (approachResults.value[taskIndex]) {
    approachResults.value[taskIndex][subIndex] = null
  }
  // Clear the student work
  if (studentWork.value[taskIndex]) {
    studentWork.value[taskIndex][subIndex] = ''
  }
  // Show the input area again
  if (showApproachInput.value[taskIndex]) {
    showApproachInput.value[taskIndex][subIndex] = true
  }
}

/**
 * Get the CSS class for approach result based on confidence score
 */
function getApproachResultClass(result) {
  if (!result) return ''
  if (result.isOnRightTrack && result.confidenceScore >= 4) {
    return 'result-excellent'
  } else if (result.isOnRightTrack) {
    return 'result-good'
  } else if (result.confidenceScore >= 2) {
    return 'result-needs-work'
  } else {
    return 'result-off-track'
  }
}

/* ----------------------------------------------------------------------------
 * Visualization laden / ein- und ausblenden
 * --------------------------------------------------------------------------*/
async function toggleVisualization(taskIndex, subIndex, task, subtask) {
  if (visualizations.value[taskIndex]?.[subIndex]) {
    visualizations.value[taskIndex][subIndex] = null
    return
  }

  if (!visualizations.value[taskIndex]) {
    visualizations.value[taskIndex] = []
  }
  if (!visualizationLoading.value[taskIndex]) {
    visualizationLoading.value[taskIndex] = []
  }

  visualizationLoading.value[taskIndex][subIndex] = true

  try {
    const res = await fetch(
      'http://127.0.0.1:8000/visualize',
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          taskNumber: task.number,
          topic: task.topic,
          taskText: task.task,
          subLabel: subtask.label,
          subtaskText: subtask.task
        })
      }
    )

    if (!res.ok) {
      throw new Error('Server error when loading visualization.')
    }

    const data = await res.json()

    if (data.error) {
      throw new Error(data.error)
    }

    visualizations.value[taskIndex][subIndex] =
      data.visualization || 'No visualization was returned.'
      
    // Track usage
    usageStats.value.visualizations++
      
    toast.success('Visualization loaded successfully!')
  } catch (err) {
    toast.error('Error loading visualization', {
      description: err.message
    })
  } finally {
    visualizationLoading.value[taskIndex][subIndex] = false
  }
}

/* ----------------------------------------------------------------------------
 * Animation (Manim) laden / ein- und ausblenden
 * --------------------------------------------------------------------------*/
async function toggleAnimation(taskIndex, subIndex, task, subtask) {
  if (animations.value[taskIndex]?.[subIndex]) {
    animations.value[taskIndex][subIndex] = null
    return
  }

  if (!animations.value[taskIndex]) {
    animations.value[taskIndex] = []
  }
  if (!animationLoading.value[taskIndex]) {
    animationLoading.value[taskIndex] = []
  }

  animationLoading.value[taskIndex][subIndex] = true

  try {
    const res = await fetch(
      'http://127.0.0.1:8000/animate',
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          taskNumber: task.number,
          topic: task.topic,
          taskText: task.task,
          subLabel: subtask.label,
          subtaskText: subtask.task
        })
      }
    )

    if (!res.ok) {
      throw new Error('Serverfehler beim Erstellen der Animation.')
    }

    const data = await res.json()

    if (data.error) {
      toast.error('Fehler beim Erstellen der Animation', {
        description: data.error
      })
    } else if (data.animationData) {
      // Success - store animation data
      animations.value[taskIndex][subIndex] = {
        data: data.animationData,
        playing: false
      }
      
      // Track usage
      usageStats.value.animations++
      
      toast.success('Animation erstellt!')
      
      // Auto-play after a short delay
      await nextTick()
      setTimeout(() => {
        playAnimation(taskIndex, subIndex)
      }, 300)
    }
  } catch (err) {
    toast.error('Fehler beim Erstellen der Animation', {
      description: err.message
    })
  } finally {
    animationLoading.value[taskIndex][subIndex] = false
  }
}

/* ----------------------------------------------------------------------------
 * Play Animation - Render steps with GSAP + KaTeX
 * --------------------------------------------------------------------------*/
async function playAnimation(taskIndex, subIndex) {
  const anim = animations.value[taskIndex]?.[subIndex]
  if (!anim || !anim.data) return
  
  const animId = `anim-${taskIndex}-${subIndex}`
  
  await nextTick()
  
  const container = document.getElementById(animId)
  if (!container) return
  
  // Mark as playing
  animations.value[taskIndex][subIndex].playing = true
  
  // Clear container
  container.innerHTML = ''
  
  const { title, steps } = anim.data
  
  // Create title
  const titleEl = document.createElement('div')
  titleEl.className = 'anim-title'
  titleEl.textContent = title
  container.appendChild(titleEl)
  
  gsap.from(titleEl, { opacity: 0, y: -20, duration: 0.8 })
  
  // Create step container
  const stepsContainer = document.createElement('div')
  stepsContainer.className = 'anim-steps-container'
  container.appendChild(stepsContainer)
  
  // Animate each step
  for (let i = 0; i < steps.length; i++) {
    const step = steps[i]
    
    await new Promise(resolve => setTimeout(resolve, i === 0 ? 1000 : 500))
    
    // Create step element
    const stepEl = document.createElement('div')
    stepEl.className = 'anim-step'
    stepEl.id = `${animId}-step-${step.id}`
    
    // Add description
    const descEl = document.createElement('div')
    descEl.className = 'anim-description'
    descEl.textContent = step.description
    stepEl.appendChild(descEl)
    
    // Add LaTeX equation
    if (step.latex) {
      const latexEl = document.createElement('div')
      latexEl.className = 'anim-latex'
      
      try {
        const rendered = katex.renderToString(step.latex, {
          displayMode: true,
          throwOnError: false
        })
        latexEl.innerHTML = rendered
      } catch (e) {
        latexEl.textContent = step.latex
      }
      
      stepEl.appendChild(latexEl)
    }
    
    stepsContainer.appendChild(stepEl)
    
    // Apply animation based on type
    const duration = step.duration || 1.0
    
    switch (step.animation) {
      case 'fadeIn':
        gsap.from(stepEl, { opacity: 0, duration })
        break
      case 'fadeOut':
        gsap.to(stepEl, { opacity: 0, duration })
        break
      case 'scale':
        gsap.from(stepEl, { scale: 0, duration, ease: 'back.out(1.7)' })
        break
      case 'bounce':
        gsap.from(stepEl, { y: -50, duration, ease: 'bounce.out' })
        break
      case 'highlight':
        gsap.from(stepEl, { 
          backgroundColor: '#fef08a', 
          duration, 
          repeat: 1, 
          yoyo: true 
        })
        break
      case 'transform':
        gsap.from(stepEl, { 
          opacity: 0, 
          scale: 0.8, 
          rotation: 5, 
          duration, 
          ease: 'power2.out' 
        })
        break
      default:
        gsap.from(stepEl, { opacity: 0, y: 20, duration })
    }
  }
  
  // Mark as done
  setTimeout(() => {
    if (animations.value[taskIndex]?.[subIndex]) {
      animations.value[taskIndex][subIndex].playing = false
    }
  }, steps.length * 1000 + 2000)
}

/* ----------------------------------------------------------------------------
 * Replay Animation
 * --------------------------------------------------------------------------*/
function replayAnimation(taskIndex, subIndex) {
  playAnimation(taskIndex, subIndex)
  toast.info('Animation wird wiederholt')
}

/* ----------------------------------------------------------------------------
 * Graph (Plotly) laden / ein- und ausblenden
 * --------------------------------------------------------------------------*/
async function toggleGraph(taskIndex, subIndex, task, subtask) {
  if (graphs.value[taskIndex]?.[subIndex]) {
    graphs.value[taskIndex][subIndex] = null
    return
  }

  if (!graphs.value[taskIndex]) {
    graphs.value[taskIndex] = []
  }
  if (!graphLoading.value[taskIndex]) {
    graphLoading.value[taskIndex] = []
  }

  graphLoading.value[taskIndex][subIndex] = true

  try {
    const res = await fetch(
      'http://127.0.0.1:8000/plot',
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          taskNumber: task.number,
          topic: task.topic,
          taskText: task.task,
          subLabel: subtask.label,
          subtaskText: subtask.task
        })
      }
    )

    if (!res.ok) {
      throw new Error('Serverfehler beim Erstellen der Grafik.')
    }

    const data = await res.json()

    if (data.error) {
      toast.error('Fehler beim Erstellen der Grafik', {
        description: data.error
      })
    } else if (data.plotData) {
      // Success - store plot data and render
      graphs.value[taskIndex][subIndex] = {
        data: data.plotData,
        rendered: false
      }
      
      // Track usage
      usageStats.value.graphs++
      
      toast.success('Grafik erstellt!')
      
      // Render the plot after a short delay
      await nextTick()
      setTimeout(() => {
        renderPlot(taskIndex, subIndex)
      }, 100)
    } else if (data.message) {
      // Not applicable for this task
      toast.info('Keine Grafik verfügbar', {
        description: data.message
      })
    }
  } catch (err) {
    toast.error('Fehler beim Erstellen der Grafik', {
      description: err.message
    })
  } finally {
    graphLoading.value[taskIndex][subIndex] = false
  }
}

/* ============================================================================
 * PHASE 2: Smart Visual System
 * Uses AI to intelligently select the best visual aid for each task
 * ============================================================================*/

/**
 * Request a smart visual hint - AI selects the best visualization type
 */
async function requestSmartVisual(taskIndex, subIndex, task, subtask) {
  // Initialize arrays if needed
  if (!smartVisuals.value[taskIndex]) smartVisuals.value[taskIndex] = []
  if (!smartVisualLoading.value[taskIndex]) smartVisualLoading.value[taskIndex] = []
  if (!previousVisuals.value[taskIndex]) previousVisuals.value[taskIndex] = []
  if (!subtaskStartTime.value[taskIndex]) subtaskStartTime.value[taskIndex] = []
  
  // If visual already shown, request a different type
  if (smartVisuals.value[taskIndex][subIndex]) {
    const currentType = smartVisuals.value[taskIndex][subIndex].type
    if (!previousVisuals.value[taskIndex][subIndex]) {
      previousVisuals.value[taskIndex][subIndex] = []
    }
    previousVisuals.value[taskIndex][subIndex].push(currentType)
  }
  
  smartVisualLoading.value[taskIndex][subIndex] = true
  
  try {
    // Calculate student progress
    const startTime = subtaskStartTime.value[taskIndex]?.[subIndex] || Date.now()
    const timeSpent = Math.floor((Date.now() - startTime) / 1000) // seconds
    
    const studentProgress = {
      timeSpent,
      hintsUsed: hintsUsed.value[taskIndex]?.[subIndex] || 0,
      questionsViewed: questionLoopTracking.value[taskIndex]?.[subIndex]?.totalRefreshes || 0
    }
    
    // Use the smart visual service to select best type
    const context = {
      taskText: task.task,
      subtaskText: subtask.task,
      topic: task.topic,
      learnerType: 'visual', // Could be from user profile in future
      studentProgress,
      previousVisuals: previousVisuals.value[taskIndex]?.[subIndex] || []
    }
    
    const selection = visualHintService.selectBestVisual(context)
    
    console.log('[SMART VISUAL] Selected:', selection.type, '-', selection.reason)
    
    // Fetch the appropriate visual from backend
    const endpoint = selection.endpoint
    
    const res = await fetch(
      `http://127.0.0.1:8000${endpoint}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          taskNumber: task.number,
          topic: task.topic,
          taskText: task.task,
          subLabel: subtask.label,
          subtaskText: subtask.task
        })
      }
    )
    
    if (!res.ok) {
      throw new Error('Serverfehler beim Laden der Visualisierung.')
    }
    
    const data = await res.json()
    
    if (data.error) {
      throw new Error(data.error)
    }
    
    // Process response based on type
    let visualData = null
    let playing = false
    
    if (selection.type === VISUAL_TYPES.GRAPH) {
      if (data.plottable === false) {
        // Fall back to key facts if graph not possible
        selection.type = VISUAL_TYPES.KEY_FACTS
        selection.reason = data.message || 'Grafik nicht verfügbar - Schlüsselfakten anzeigen'
        
        // Fetch key facts instead
        const keyFactsRes = await fetch(
          'http://127.0.0.1:8000/visualize',
          {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              taskNumber: task.number,
              topic: task.topic,
              taskText: task.task,
              subLabel: subtask.label,
              subtaskText: subtask.task
            })
          }
        )
        const keyFactsData = await keyFactsRes.json()
        visualData = keyFactsData.visualization || 'Keine Visualisierung verfügbar.'
      } else {
        visualData = data.plotData
      }
    } else if (selection.type === VISUAL_TYPES.ANIMATION) {
      visualData = data.animationData
      playing = false
    } else {
      // Key facts / visualization
      visualData = data.visualization || 'Keine Visualisierung verfügbar.'
    }
    
    // Store the result
    smartVisuals.value[taskIndex][subIndex] = {
      type: selection.type,
      data: visualData,
      reason: selection.reason,
      playing
    }
    
    // Track usage
    usageStats.value.smartVisuals++
    usageStats.value.visualTypes.push(selection.type)
    
    toast.success(visualHintService.getVisualLabel(selection.type), {
      description: selection.reason
    })
    
    // Render the visual after DOM update
    await nextTick()
    
    if (selection.type === VISUAL_TYPES.GRAPH && visualData) {
      setTimeout(() => renderSmartGraph(taskIndex, subIndex), 100)
    } else if (selection.type === VISUAL_TYPES.ANIMATION && visualData) {
      setTimeout(() => playSmartAnimation(taskIndex, subIndex), 300)
    }
    
  } catch (err) {
    console.error('[SMART VISUAL] Error:', err)
    toast.error('Fehler beim Laden der Visualisierung', {
      description: err.message
    })
  } finally {
    smartVisualLoading.value[taskIndex][subIndex] = false
  }
}

/**
 * Get title for smart visual type
 */
function getSmartVisualTitle(type) {
  const titles = {
    [VISUAL_TYPES.GRAPH]: '📊 Interaktive Grafik',
    [VISUAL_TYPES.ANIMATION]: '🎬 Schrittweise Animation',
    [VISUAL_TYPES.KEY_FACTS]: '💡 Schlüsselfakten',
    [VISUAL_TYPES.FORMULA]: '📐 Formelübersicht',
    [VISUAL_TYPES.DIAGRAM]: '📝 Konzeptdiagramm'
  }
  return titles[type] || '💡 Visuelle Hilfe'
}

/**
 * Get badge text for smart visual type
 */
function getSmartVisualBadge(type) {
  const badges = {
    [VISUAL_TYPES.GRAPH]: 'Interaktiv',
    [VISUAL_TYPES.ANIMATION]: 'Animiert',
    [VISUAL_TYPES.KEY_FACTS]: 'Fakten',
    [VISUAL_TYPES.FORMULA]: 'Formeln',
    [VISUAL_TYPES.DIAGRAM]: 'Diagramm'
  }
  return badges[type] || 'Visuell'
}

/**
 * Render a smart graph using Chart.js (Phase 2.2 - Replaced Plotly)
 */
function renderSmartGraph(taskIndex, subIndex) {
  const smartVisual = smartVisuals.value[taskIndex]?.[subIndex]
  if (!smartVisual || smartVisual.type !== VISUAL_TYPES.GRAPH || !smartVisual.data) return
  
  const plotId = `smart-graph-${taskIndex}-${subIndex}`
  const container = document.getElementById(plotId)
  
  if (!container) {
    console.error(`Smart graph container not found: ${plotId}`)
    return
  }
  
  try {
    // Destroy existing chart if any
    const existingKey = `smart-${taskIndex}-${subIndex}`
    if (chartInstances.value[existingKey]) {
      chartInstances.value[existingKey].destroy()
      delete chartInstances.value[existingKey]
    }
    
    // Clear container and create canvas
    container.innerHTML = ''
    const canvas = document.createElement('canvas')
    canvas.id = `smart-chart-${taskIndex}-${subIndex}`
    canvas.style.width = '100%'
    canvas.style.height = '400px'
    container.appendChild(canvas)
    
    // Parse the Chart.js config from backend
    const chartConfig = JSON.parse(smartVisual.data)
    
    // Create the chart
    const ctx = canvas.getContext('2d')
    const chartInstance = new Chart(ctx, {
      type: chartConfig.type || 'scatter',
      data: chartConfig.data,
      options: chartConfig.options
    })
    
    // Store instance for cleanup
    chartInstances.value[existingKey] = chartInstance
    
    console.log('[CHART.JS] Smart graph rendered successfully')
  } catch (e) {
    console.error('Error rendering smart graph:', e)
    toast.error('Fehler beim Rendern der Grafik')
  }
}

/**
 * Play a smart animation using GSAP + KaTeX
 */
async function playSmartAnimation(taskIndex, subIndex) {
  const smartVisual = smartVisuals.value[taskIndex]?.[subIndex]
  if (!smartVisual || smartVisual.type !== VISUAL_TYPES.ANIMATION || !smartVisual.data) return
  
  const animId = `smart-anim-${taskIndex}-${subIndex}`
  
  await nextTick()
  
  const container = document.getElementById(animId)
  if (!container) return
  
  // Mark as playing
  smartVisuals.value[taskIndex][subIndex].playing = true
  
  // Clear container
  container.innerHTML = ''
  
  const { title, steps } = smartVisual.data
  
  // Create title
  const titleEl = document.createElement('div')
  titleEl.className = 'anim-title'
  titleEl.textContent = title
  container.appendChild(titleEl)
  
  gsap.from(titleEl, { opacity: 0, y: -20, duration: 0.8 })
  
  // Create step container
  const stepsContainer = document.createElement('div')
  stepsContainer.className = 'anim-steps-container'
  container.appendChild(stepsContainer)
  
  // Animate each step
  for (let i = 0; i < steps.length; i++) {
    const step = steps[i]
    
    await new Promise(resolve => setTimeout(resolve, i === 0 ? 1000 : 500))
    
    // Create step element
    const stepEl = document.createElement('div')
    stepEl.className = 'anim-step'
    stepEl.id = `${animId}-step-${step.id}`
    
    // Add description
    const descEl = document.createElement('div')
    descEl.className = 'anim-description'
    descEl.textContent = step.description
    stepEl.appendChild(descEl)
    
    // Add LaTeX equation
    if (step.latex) {
      const latexEl = document.createElement('div')
      latexEl.className = 'anim-latex'
      
      try {
        const rendered = katex.renderToString(step.latex, {
          displayMode: true,
          throwOnError: false
        })
        latexEl.innerHTML = rendered
      } catch (e) {
        latexEl.textContent = step.latex
      }
      
      stepEl.appendChild(latexEl)
    }
    
    stepsContainer.appendChild(stepEl)
    
    // Apply animation based on type
    const duration = step.duration || 1.0
    
    switch (step.animation) {
      case 'fadeIn':
        gsap.from(stepEl, { opacity: 0, duration })
        break
      case 'fadeOut':
        gsap.to(stepEl, { opacity: 0, duration })
        break
      case 'scale':
        gsap.from(stepEl, { scale: 0, duration, ease: 'back.out(1.7)' })
        break
      case 'bounce':
        gsap.from(stepEl, { y: -50, duration, ease: 'bounce.out' })
        break
      case 'highlight':
        gsap.from(stepEl, { 
          backgroundColor: '#fef08a', 
          duration, 
          repeat: 1, 
          yoyo: true 
        })
        break
      case 'transform':
        gsap.from(stepEl, { 
          opacity: 0, 
          scale: 0.8, 
          rotation: 5, 
          duration, 
          ease: 'power2.out' 
        })
        break
      default:
        gsap.from(stepEl, { opacity: 0, y: 20, duration })
    }
  }
  
  // Mark as done
  setTimeout(() => {
    if (smartVisuals.value[taskIndex]?.[subIndex]) {
      smartVisuals.value[taskIndex][subIndex].playing = false
    }
  }, steps.length * 1000 + 2000)
}

/**
 * Replay a smart animation
 */
function replaySmartAnimation(taskIndex, subIndex) {
  playSmartAnimation(taskIndex, subIndex)
  toast.info('Animation wird wiederholt')
}

/* ----------------------------------------------------------------------------
 * Render Plot with Chart.js (Phase 2.2 - Replaced Plotly)
 * --------------------------------------------------------------------------*/
function renderPlot(taskIndex, subIndex) {
  const graph = graphs.value[taskIndex]?.[subIndex]
  if (!graph || !graph.data || graph.rendered) return
  
  const plotId = `graph-${taskIndex}-${subIndex}`
  const container = document.getElementById(plotId)
  
  if (!container) {
    console.error(`Plot container not found: ${plotId}`)
    return
  }
  
  try {
    // Destroy existing chart if any
    const existingKey = `${taskIndex}-${subIndex}`
    if (chartInstances.value[existingKey]) {
      chartInstances.value[existingKey].destroy()
      delete chartInstances.value[existingKey]
    }
    
    // Clear container and create canvas
    container.innerHTML = ''
    const canvas = document.createElement('canvas')
    canvas.id = `chart-${taskIndex}-${subIndex}`
    canvas.style.width = '100%'
    canvas.style.height = '400px'
    container.appendChild(canvas)
    
    // Parse the Chart.js config from backend
    const chartConfig = JSON.parse(graph.data)
    
    // Create the chart
    const ctx = canvas.getContext('2d')
    const chartInstance = new Chart(ctx, {
      type: chartConfig.type || 'scatter',
      data: chartConfig.data,
      options: chartConfig.options
    })
    
    // Store instance for cleanup
    chartInstances.value[existingKey] = chartInstance
    
    // Mark as rendered
    graphs.value[taskIndex][subIndex].rendered = true
    
    console.log('[CHART.JS] Graph rendered successfully')
  } catch (e) {
    console.error('Error rendering Chart.js plot:', e)
    toast.error('Fehler beim Rendern der Grafik')
  }
}

/* ----------------------------------------------------------------------------
 * Copy to Clipboard
 * --------------------------------------------------------------------------*/
function copyToClipboard(text) {
  navigator.clipboard.writeText(text).then(() => {
    toast.success('Code in Zwischenablage kopiert!')
  }).catch(err => {
    toast.error('Fehler beim Kopieren', {
      description: err.message
    })
  })
}

/* ----------------------------------------------------------------------------
 * Format Visualization - Structure key facts visually
 * --------------------------------------------------------------------------*/
function formatVisualization(text) {
  if (!text) return ''

  // First, replace \[ and \] with $$ for proper KaTeX rendering
  text = text.replace(/\\\[/g, '$$').replace(/\\\]/g, '$$')
  
  // Split by newlines and structure the content
  const lines = text.split('\n').filter(line => line.trim())
  
  let html = '<div class="visualization-content">'
  
  lines.forEach(line => {
    const trimmedLine = line.trim()
    
    // Check for different types of content
    if (trimmedLine.startsWith('**') && trimmedLine.endsWith('**')) {
      // Bold headers
      const headerText = trimmedLine.slice(2, -2)
      html += `<div class="viz-header">${escapeHtml(headerText)}</div>`
    } else if (trimmedLine.startsWith('- ') || trimmedLine.startsWith('• ')) {
      // Bullet points
      const bulletText = trimmedLine.slice(2)
      html += `<div class="viz-bullet">
                <span class="viz-bullet-dot"></span>
                <span class="viz-bullet-text">${renderInline(bulletText)}</span>
              </div>`
    } else if (trimmedLine.match(/^\d+\./)) {
      // Numbered items
      html += `<div class="viz-numbered">${renderInline(trimmedLine)}</div>`
    } else if (trimmedLine.includes(':')) {
      // Key-value pairs
      const [key, ...valueParts] = trimmedLine.split(':')
      const value = valueParts.join(':')
      html += `<div class="viz-keyvalue">
                <span class="viz-key">${escapeHtml(key)}:</span>
                <span class="viz-value">${renderInline(value)}</span>
              </div>`
    } else {
      // Regular text
      html += `<div class="viz-text">${renderInline(trimmedLine)}</div>`
    }
  })
  
  html += '</div>'
  return html
}
</script>

<style>
body {
  font-family: 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
  background: linear-gradient(135deg, #f5f7fa 0%, #e8edf2 100%);
  margin: 0;
  padding: 0;
  min-height: 100vh;
}

.clarity-root {
  position: relative;
  padding: 2rem 1.5rem;
}

/* Professional color scheme */
:root {
  --primary-color: #1e3a5f;
  --secondary-color: #2c5f8d;
  --accent-color: #3b82f6;
  --success-color: #10b981;
  --error-color: #ef4444;
  --bg-light: #ffffff;
  --bg-soft: #f8fafc;
  --text-primary: #1e293b;
  --text-secondary: #64748b;
  --border-color: #e2e8f0;
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

/* Professional Header */
.header-section {
  text-align: center;
  margin-bottom: 3rem;
  padding-bottom: 2rem;
  border-bottom: 2px solid var(--border-color);
}

.app-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--primary-color);
  margin: 0 0 0.5rem 0;
  letter-spacing: -0.02em;
}

.app-subtitle {
  font-size: 1rem;
  color: var(--text-secondary);
  font-weight: 500;
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

/* Loading Indicator */
.upload-hint-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 40vh;
  padding: 2rem;
  text-align: center;
}

.upload-hint-text {
  color: #64748b;
  font-size: 1.1rem;
  margin: 0;
  max-width: 600px;
}

.loading-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 2rem;
}

.loading-spinner {
  width: 24px;
  height: 24px;
  border: 3px solid var(--border-color);
  border-top-color: var(--accent-color);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-text {
  color: var(--text-secondary);
  font-weight: 500;
}

/* Error Message */
.error-message {
  background-color: #fef2f2;
  border: 1px solid #fecaca;
  border-left: 4px solid var(--error-color);
  color: #991b1b;
  padding: 1rem 1.5rem;
  border-radius: 0.375rem;
  text-align: center;
}

/* Task Cards */
.task-card {
  text-align: left;
  background: var(--bg-light);
  border: 1px solid var(--border-color);
  border-top: 3px solid var(--secondary-color);
  box-shadow: var(--shadow-md);
  transition: box-shadow 0.2s ease;
}

.task-card:hover {
  box-shadow: var(--shadow-lg);
}

/* Task Header */
.task-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid var(--border-color);
}

.task-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--primary-color);
  margin: 0;
}

.task-topic {
  font-weight: 500;
  color: var(--secondary-color);
}

.task-difficulty {
  font-size: 0.75rem;
  padding: 0.375rem 0.75rem;
  border-radius: 0.25rem;
  background-color: var(--bg-soft);
  color: var(--text-secondary);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border: 1px solid var(--border-color);
}

/* Task and Subtask Text */
.task-text,
.subtask-text {
  margin: 0 0 1rem 0;
  color: var(--text-primary);
  white-space: pre-line;
  line-height: 1.7;
  font-size: 0.95rem;
}

/* Subtask Section */
.subtask-block {
  border-top: 2px solid var(--border-color);
  padding-top: 1.25rem;
  margin-top: 1.25rem;
  background: var(--bg-soft);
  padding: 1.25rem;
  border-radius: 0.375rem;
  border-left: 3px solid var(--accent-color);
}

.subtask-title {
  font-weight: 700;
  color: var(--primary-color);
  margin: 0 0 0.75rem 0;
  font-size: 1.05rem;
}

/* Questions Block - Professional Design */
.questions-block {
  margin-top: 1.25rem;
  padding: 1.25rem;
  background: var(--bg-light);
  border-radius: 0.375rem;
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow-sm);
}

.question-header-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid var(--border-color);
}

.question-label {
  font-weight: 700;
  font-size: 0.75rem;
  color: var(--secondary-color);
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.question-controls {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.question-counter {
  font-size: 0.75rem;
  color: var(--text-secondary);
  font-weight: 600;
  padding: 0.375rem 0.75rem;
  background: var(--bg-soft);
  border-radius: 0.25rem;
  border: 1px solid var(--border-color);
}

.refresh-question-btn {
  background: var(--bg-light);
  border: 1px solid var(--accent-color);
  color: var(--accent-color);
  border-radius: 0.25rem;
  padding: 0.375rem 0.75rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 36px;
}

.refresh-question-btn:hover {
  background: var(--accent-color);
  color: var(--bg-light);
  transform: scale(1.05);
  box-shadow: var(--shadow-md);
}

.refresh-question-btn:active {
  transform: scale(0.98);
}

.current-question-row {
  display: flex;
  align-items: flex-start;
  padding: 1rem;
  background: var(--bg-soft);
  border-radius: 0.25rem;
  border-left: 3px solid var(--accent-color);
}

.question-bullet {
  margin-top: 0.4rem;
  margin-right: 0.75rem;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: var(--accent-color);
  flex-shrink: 0;
}

.question-text {
  color: var(--text-primary);
  line-height: 1.7;
  font-size: 0.95rem;
  flex: 1;
  font-weight: 500;
}

/* Action Buttons Row */
.action-buttons-row {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.action-btn {
  flex: 1;
  font-size: 0.875rem;
  color: var(--bg-light);
  padding: 0.625rem 1.5rem;
  cursor: pointer;
  border-radius: 0.25rem;
  font-weight: 600;
  transition: all 0.2s ease;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border: none;
}

.visualization-btn {
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  box-shadow: 0 2px 4px rgba(99, 102, 241, 0.3);
}

.visualization-btn:hover {
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
  box-shadow: var(--shadow-md);
  transform: translateY(-1px);
}

.animation-btn {
  background: linear-gradient(135deg, #ec4899 0%, #f43f5e 100%);
  box-shadow: 0 2px 4px rgba(236, 72, 153, 0.3);
}

.animation-btn:hover {
  background: linear-gradient(135deg, #db2777 0%, #e11d48 100%);
  box-shadow: var(--shadow-md);
  transform: translateY(-1px);
}

.graph-btn {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  box-shadow: 0 2px 4px rgba(16, 185, 129, 0.3);
}

.graph-btn:hover {
  background: linear-gradient(135deg, #059669 0%, #047857 100%);
  box-shadow: var(--shadow-md);
  transform: translateY(-1px);
}

.hint-btn {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  box-shadow: 0 2px 4px rgba(245, 158, 11, 0.3);
}

.hint-btn:hover {
  background: linear-gradient(135deg, #d97706 0%, #b45309 100%);
  box-shadow: var(--shadow-md);
  transform: translateY(-1px);
}

/* Phase 2: Smart Visual Button */
.smart-visual-btn {
  background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%);
  box-shadow: 0 2px 4px rgba(139, 92, 246, 0.3);
  flex: 2; /* Make it slightly larger to indicate primary action */
}

.smart-visual-btn:hover {
  background: linear-gradient(135deg, #7c3aed 0%, #4f46e5 100%);
  box-shadow: var(--shadow-md);
  transform: translateY(-1px);
}

.smart-visual-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.loading-dots {
  display: inline-block;
}

.loading-dots::after {
  content: '';
  animation: dots 1.5s steps(4, end) infinite;
}

@keyframes dots {
  0%, 20% { content: ''; }
  40% { content: '.'; }
  60% { content: '..'; }
  80%, 100% { content: '...'; }
}

.action-btn:active {
  transform: scale(0.98);
}

.visualization-loading,
.hint-loading {
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin-top: 0.75rem;
  font-style: italic;
  padding: 0.5rem;
  background: var(--bg-soft);
  border-radius: 0.25rem;
  text-align: center;
}

.hint-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  border: 2px solid #f59e0b;
}

/* Phase 2: Smart Visual Loading & Box */
.smart-visual-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin-top: 0.75rem;
  padding: 1rem;
  background: linear-gradient(135deg, #ede9fe 0%, #ddd6fe 100%);
  border: 2px solid #a78bfa;
  border-radius: 0.5rem;
  font-weight: 500;
  color: #5b21b6;
}

.smart-visual-box {
  margin-top: 1.25rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, #faf5ff 0%, #f3e8ff 100%);
  border: 2px solid #c4b5fd;
  border-left: 5px solid #8b5cf6;
  border-radius: 0.5rem;
  box-shadow: var(--shadow-md);
  position: relative;
}

.smart-visual-box::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(to right, #8b5cf6 0%, transparent 50%);
}

/* Type-specific styling */
.smart-visual-box.visual-type-graph {
  border-left-color: #10b981;
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
  border-color: #86efac;
}

.smart-visual-box.visual-type-animation {
  border-left-color: #ec4899;
  background: linear-gradient(135deg, #fdf2f8 0%, #fce7f3 100%);
  border-color: #fbcfe8;
}

.smart-visual-box.visual-type-key_facts {
  border-left-color: #6366f1;
  background: linear-gradient(135deg, #eef2ff 0%, #e0e7ff 100%);
  border-color: #c7d2fe;
}

.smart-visual-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid rgba(139, 92, 246, 0.3);
}

.smart-visual-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #5b21b6;
  margin: 0;
}

.visual-type-badge {
  font-size: 0.75rem;
  padding: 0.375rem 0.75rem;
  border-radius: 9999px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%);
  color: white;
}

.visual-type-graph .visual-type-badge {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.visual-type-animation .visual-type-badge {
  background: linear-gradient(135deg, #ec4899 0%, #f43f5e 100%);
}

.visual-type-key_facts .visual-type-badge {
  background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
}

.visual-reason {
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin: 0 0 1rem 0;
  padding: 0.5rem 0.75rem;
  background: rgba(255, 255, 255, 0.7);
  border-radius: 0.25rem;
  font-style: italic;
  border-left: 3px solid rgba(139, 92, 246, 0.5);
}

.smart-visual-content {
  margin-top: 1rem;
}

.smart-visual-content .graph-container,
.smart-visual-content .animation-canvas {
  background: white;
  border-radius: 0.5rem;
  padding: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.smart-visual-content .replay-btn {
  margin-top: 1rem;
}

.animation-loading,
.graph-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin-top: 0.75rem;
  padding: 1rem;
  background: linear-gradient(135deg, #fce7f3 0%, #fef2f2 100%);
  border: 2px solid #fbcfe8;
  border-radius: 0.5rem;
  font-weight: 500;
}

.graph-loading {
  background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
  border: 2px solid #6ee7b7;
}

/* Visualization Box */
.visualization-box {
  margin-top: 1.25rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, #f0f4ff 0%, #e8eeff 100%);
  border: 2px solid #c7d2fe;
  border-left: 5px solid #6366f1;
  border-radius: 0.5rem;
  box-shadow: var(--shadow-md);
  position: relative;
}

.visualization-box::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(to right, #6366f1 0%, transparent 50%);
}

.visualization-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #4338ca;
  margin: 0 0 1rem 0;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #c7d2fe;
}

.visualization-content {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.viz-header {
  font-size: 1.05rem;
  font-weight: 700;
  color: #4338ca;
  margin-top: 1rem;
  margin-bottom: 0.5rem;
}

.viz-header:first-child {
  margin-top: 0;
}

.viz-bullet {
  display: flex;
  align-items: flex-start;
  padding: 0.5rem 0.75rem;
  background: rgba(255, 255, 255, 0.7);
  border-radius: 0.375rem;
  transition: all 0.2s ease;
}

.viz-bullet:hover {
  background: rgba(255, 255, 255, 0.95);
  transform: translateX(4px);
}

.viz-bullet-dot {
  width: 8px;
  height: 8px;
  background: #6366f1;
  border-radius: 50%;
  margin-top: 0.5rem;
  margin-right: 0.75rem;
  flex-shrink: 0;
}

.viz-bullet-text {
  flex: 1;
  color: var(--text-primary);
  line-height: 1.6;
}

.viz-numbered {
  padding: 0.5rem 0.75rem;
  background: rgba(255, 255, 255, 0.7);
  border-radius: 0.375rem;
  color: var(--text-primary);
  line-height: 1.6;
  border-left: 3px solid #818cf8;
}

.viz-keyvalue {
  display: flex;
  align-items: baseline;
  padding: 0.5rem 0.75rem;
  background: rgba(255, 255, 255, 0.7);
  border-radius: 0.375rem;
  gap: 0.5rem;
}

.viz-key {
  font-weight: 700;
  color: #4338ca;
  flex-shrink: 0;
}

.viz-value {
  color: var(--text-primary);
  line-height: 1.6;
}

.viz-text {
  padding: 0.5rem 0.75rem;
  color: var(--text-primary);
  line-height: 1.6;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 0.375rem;
}

/* Animation Box (Manim) */
.animation-box {
  margin-top: 1.25rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, #fef2f2 0%, #fff1f2 100%);
  border: 2px solid #fecaca;
  border-left: 5px solid #ec4899;
  border-radius: 0.5rem;
  box-shadow: var(--shadow-md);
  position: relative;
}

.animation-box::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(to right, #ec4899 0%, transparent 50%);
}

.animation-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #be185d;
  margin: 0 0 1rem 0;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #fecaca;
}

/* Animation Header */
.animation-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.replay-btn {
  background: linear-gradient(135deg, #ec4899 0%, #f43f5e 100%);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  text-transform: none;
  letter-spacing: normal;
}

.replay-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #db2777 0%, #e11d48 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(236, 72, 153, 0.3);
}

.replay-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Animation Canvas Container */
.animation-canvas {
  min-height: 300px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(252, 231, 243, 0.3) 100%);
  border-radius: 0.5rem;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  border: 2px solid rgba(236, 72, 153, 0.2);
}

/* Animation Elements */
.anim-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #be185d;
  text-align: center;
  margin-bottom: 1rem;
}

.anim-steps-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.anim-step {
  background: white;
  border-radius: 0.5rem;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border-left: 4px solid #ec4899;
  transition: all 0.3s ease;
}

.anim-step:hover {
  box-shadow: 0 4px 12px rgba(236, 72, 153, 0.2);
  transform: translateX(4px);
}

.anim-description {
  font-size: 1rem;
  color: var(--text-primary);
  font-weight: 600;
  margin-bottom: 1rem;
  line-height: 1.6;
}

.anim-latex {
  background: linear-gradient(135deg, #fef3f9 0%, #fff 100%);
  padding: 1.5rem;
  border-radius: 0.375rem;
  border: 1px solid rgba(236, 72, 153, 0.2);
  text-align: center;
}

.anim-latex .katex-display {
  margin: 0;
  font-size: 1.3em;
}

.anim-latex .katex {
  color: var(--text-primary);
}

/* Graph Box (Plotly) */
.graph-box {
  margin-top: 1.25rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
  border: 2px solid #86efac;
  border-left: 5px solid #10b981;
  border-radius: 0.5rem;
  box-shadow: var(--shadow-md);
  position: relative;
}

.graph-box::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(to right, #10b981 0%, transparent 50%);
}

.graph-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #065f46;
  margin: 0 0 1rem 0;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #86efac;
}

.graph-container {
  background: white;
  border-radius: 0.5rem;
  padding: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  min-height: 400px;
}

/* Make plotly responsive */
.graph-container :deep(.plotly) {
  width: 100% !important;
  height: 100% !important;
}

.graph-container :deep(.js-plotly-plot) {
  width: 100% !important;
}

/* Progressive Hint Box (Replaces Solution Box) */
.hint-box {
  margin-top: 1.25rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
  border: 2px solid #fbbf24;
  border-left: 5px solid #f59e0b;
  border-radius: 0.5rem;
  box-shadow: var(--shadow-md);
  position: relative;
}

.hint-box::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(to right, #f59e0b 0%, transparent 50%);
}

.hint-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #fde68a;
}

.hint-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #92400e;
  margin: 0;
}

.hint-level-badge {
  font-size: 0.75rem;
  padding: 0.375rem 0.75rem;
  border-radius: 9999px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.hint-level-badge.level-1 {
  background: #dbeafe;
  color: #1e40af;
}

.hint-level-badge.level-2 {
  background: #fef3c7;
  color: #92400e;
}

.hint-level-badge.level-3 {
  background: #fee2e2;
  color: #991b1b;
}

.hint-text {
  font-size: 1rem;
  color: var(--text-primary);
  line-height: 1.8;
  margin: 0 0 1rem 0;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 0.375rem;
  border-left: 3px solid #f59e0b;
}

.hint-encouragement {
  font-size: 0.95rem;
  color: #059669;
  font-weight: 600;
  padding: 0.75rem 1rem;
  background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
  border-radius: 0.375rem;
  text-align: center;
  margin-top: 1rem;
}

.hint-more {
  margin-top: 1rem;
  text-align: center;
}

.more-hint-btn {
  background: transparent;
  border: 2px dashed #f59e0b;
  color: #92400e;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.more-hint-btn:hover {
  background: #fef3c7;
  border-style: solid;
}

/* ============================================================
   PHASE 3.2: Smart Approach Checker Styles
   Date: 2026-01-12
   Purpose: Validate student's work without revealing solution
   ============================================================ */

/* Approach Checker Toggle Button */
.approach-checker-toggle-btn {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
  margin-top: 0.75rem;
  width: 100%;
  box-shadow: 0 2px 4px rgba(139, 92, 246, 0.3);
}

.approach-checker-toggle-btn:hover {
  background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%);
  box-shadow: var(--shadow-md);
  transform: translateY(-1px);
}

/* Approach Input Area */
.approach-input-area {
  margin-top: 1rem;
  padding: 1.25rem;
  background: linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%);
  border: 2px solid #c4b5fd;
  border-radius: 0.5rem;
  animation: slideDown 0.3s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.approach-input-label {
  display: block;
  font-weight: 600;
  color: #5b21b6;
  margin-bottom: 0.75rem;
  font-size: 0.875rem;
}

.approach-textarea {
  width: 100%;
  min-height: 100px;
  padding: 0.875rem;
  border: 2px solid #c4b5fd;
  border-radius: 0.375rem;
  font-family: inherit;
  font-size: 0.9375rem;
  line-height: 1.6;
  resize: vertical;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
  background: white;
}

.approach-textarea:focus {
  outline: none;
  border-color: #8b5cf6;
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.15);
}

.approach-textarea::placeholder {
  color: #a78bfa;
  font-style: italic;
}

.approach-input-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-top: 1rem;
}

.check-approach-btn {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 0.375rem;
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(139, 92, 246, 0.3);
  white-space: nowrap;
}

.check-approach-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

.check-approach-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.approach-hint-text {
  font-size: 0.8125rem;
  color: #7c3aed;
  font-style: italic;
}

/* Approach Check Loading */
.approach-check-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  font-size: 0.875rem;
  color: #6d28d9;
  margin-top: 1rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%);
  border: 2px solid #c4b5fd;
  border-radius: 0.5rem;
  font-weight: 500;
}

/* Approach Result Box */
.approach-result-box {
  margin-top: 1.25rem;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: var(--shadow-md);
  position: relative;
  border-left: 5px solid;
  animation: fadeIn 0.3s ease-out;
}

.approach-result-box.result-excellent {
  background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
  border-color: #10b981;
}

.approach-result-box.result-good {
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
  border-color: #22c55e;
}

.approach-result-box.result-needs-work {
  background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
  border-color: #f59e0b;
}

.approach-result-box.result-off-track {
  background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
  border-color: #ef4444;
}

.approach-result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid rgba(0, 0, 0, 0.1);
}

.approach-track-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.track-icon {
  font-size: 1.5rem;
  font-weight: 700;
}

.track-icon.track-correct {
  color: #10b981;
}

.track-icon.track-needs-work {
  color: #f59e0b;
}

.track-text {
  font-weight: 700;
  font-size: 1rem;
}

.confidence-score {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.confidence-label {
  font-size: 0.75rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.confidence-stars {
  display: flex;
  gap: 2px;
}

.star {
  font-size: 1.125rem;
}

.star.filled {
  color: #f59e0b;
}

.star.empty {
  color: #d1d5db;
}

.approach-assessment {
  font-size: 1rem;
  line-height: 1.6;
  margin-bottom: 1rem;
  font-weight: 500;
  color: var(--text-primary);
}

.approach-strengths,
.approach-improvements,
.approach-specific-issue,
.approach-next-step {
  margin-bottom: 1rem;
  padding: 0.75rem 1rem;
  background: rgba(255, 255, 255, 0.7);
  border-radius: 0.375rem;
}

.approach-strengths h5,
.approach-improvements h5,
.approach-specific-issue h5,
.approach-next-step h5 {
  margin: 0 0 0.5rem 0;
  font-size: 0.875rem;
  font-weight: 700;
}

.approach-strengths { background: rgba(16, 185, 129, 0.1); }
.approach-strengths h5 { color: #065f46; }

.approach-improvements { background: rgba(245, 158, 11, 0.1); }
.approach-improvements h5 { color: #92400e; }

.approach-specific-issue { background: rgba(239, 68, 68, 0.1); }
.approach-specific-issue h5 { color: #991b1b; }

.approach-next-step { background: rgba(59, 130, 246, 0.1); }
.approach-next-step h5 { color: #1e40af; }

.approach-strengths ul,
.approach-improvements ul {
  margin: 0;
  padding-left: 1.25rem;
}

.approach-strengths li,
.approach-improvements li {
  margin-bottom: 0.25rem;
  font-size: 0.875rem;
  line-height: 1.5;
}

.approach-specific-issue p,
.approach-next-step p {
  margin: 0;
  font-size: 0.875rem;
  line-height: 1.5;
}

.approach-encouragement {
  color: #059669;
  font-weight: 600;
  padding: 0.75rem 1rem;
  background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
  border-radius: 0.375rem;
  text-align: center;
  margin-top: 1rem;
  font-size: 0.9375rem;
}

.retry-approach-btn {
  display: block;
  width: 100%;
  margin-top: 1rem;
  background: transparent;
  border: 2px dashed #8b5cf6;
  color: #6d28d9;
  padding: 0.625rem 1rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.retry-approach-btn:hover {
  background: #f5f3ff;
  border-style: solid;
}

/* ============================================================
   REMOVED: Solution Box - Violates Socratic Method
   Date: 2026-01-12
   Reason: Showing full solutions directly contradicts the 
   Socratic questioning philosophy of Clarity Coach.
   
   REPLACED BY: Progressive Hint System (.hint-box)
   See Phase 1 of UI/UX Optimization
   ============================================================ */

/* Professional Section Headers */
.latex-section-header {
  margin: 1.5rem 0 1rem 0;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid var(--border-color);
  position: relative;
}

/* Legacy hint header - kept for hint formatting */
.latex-section-header.hint-header {
  margin-top: 0 !important;
  border-bottom: 2px solid #f59e0b;
}

.latex-section-header.proof-header {
  border-bottom: 2px solid var(--text-secondary);
}

.latex-label {
  font-family: 'Georgia', 'Cambria', serif;
  font-weight: 700;
  font-size: 1.125rem;
  font-style: normal;
  color: var(--primary-color);
  letter-spacing: 0.01em;
}

.hint-header .latex-label {
  color: #92400e;
}

.proof-header .latex-label::after {
  content: '';
  margin-left: 0.5rem;
}

/* Professional Aligned Equations Block */
.latex-aligned-equations {
  margin: 1.5rem 0;
  padding: 1.5rem 2rem;
  background: var(--bg-soft);
  border: 1px solid var(--border-color);
  border-left: 4px solid var(--secondary-color);
  border-radius: 0.375rem;
  position: relative;
  box-shadow: var(--shadow-sm);
}

.latex-aligned-equations::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(to right, var(--secondary-color) 0%, transparent 50%);
}

/* Individual Equations */
.latex-aligned-equations .katex-display {
  margin: 1rem 0 !important;
  padding: 0.75rem 1.25rem;
  background: var(--bg-light);
  border-radius: 0.25rem;
  border: 1px solid var(--border-color);
  transition: all 0.2s ease;
  position: relative;
}

.latex-aligned-equations .katex-display:first-child {
  margin-top: 0 !important;
}

.latex-aligned-equations .katex-display:last-child {
  margin-bottom: 0 !important;
}

.latex-aligned-equations .katex-display:hover {
  background: var(--bg-light);
  border-color: var(--accent-color);
  box-shadow: var(--shadow-sm);
}

.latex-aligned-equations .katex {
  font-size: 1.15em;
  color: var(--text-primary);
}

/* Text Lines with Math Content */
.latex-text-line {
  margin: 1rem 0;
  padding: 0.75rem 1.25rem;
  color: var(--text-primary);
  line-height: 1.8;
  font-size: 1rem;
  background: var(--bg-soft);
  border-radius: 0.25rem;
  border-left: 3px solid var(--border-color);
  transition: all 0.2s ease;
}

.latex-text-line:hover {
  background: var(--bg-light);
  border-left-color: var(--accent-color);
}

/* Inline math within text */
.latex-text-line .katex {
  font-size: 1.05em;
  color: var(--text-primary);
  margin: 0 0.2em;
}

/* Proper spacing between elements */
.latex-text-line + .latex-aligned-equations {
  margin-top: 1.5rem;
}

.latex-aligned-equations + .latex-text-line {
  margin-top: 1.5rem;
}

/* Smooth fade-in animation for hint box */
.hint-box > * {
  animation: fadeIn 0.25s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-3px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Professional Feedback Buttons */
.feedback-row {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border-color);
}

.feedback-btn {
  flex: 1;
  padding: 0.75rem 1.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border-radius: 0.25rem;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid var(--border-color);
  background: var(--bg-light);
  color: var(--text-secondary);
}

.feedback-btn-positive:hover {
  border-color: var(--success-color);
  color: var(--success-color);
}

.feedback-btn-positive.active {
  background: var(--success-color);
  border-color: var(--success-color);
  color: var(--bg-light);
  box-shadow: var(--shadow-md);
}

.feedback-btn-negative:hover {
  border-color: var(--error-color);
  color: var(--error-color);
}

.feedback-btn-negative.active {
  background: var(--error-color);
  border-color: var(--error-color);
  color: var(--bg-light);
  box-shadow: var(--shadow-md);
}

.feedback-btn:active {
  transform: scale(0.98);
}

button {
  transition: all 0.2s ease;
}

/* No Subtasks Message */
.no-subtasks {
  font-size: 0.875rem;
  color: var(--text-secondary);
  font-style: italic;
  margin-top: 1rem;
  padding: 1rem;
  background: var(--bg-soft);
  border-radius: 0.25rem;
  text-align: center;
}
</style>
