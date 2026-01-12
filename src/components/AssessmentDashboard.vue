<template>
  <div class="dashboard-container">
    <div class="dashboard-header">
      <h1 class="dashboard-title">📊 Assessment Dashboard</h1>
      <p class="dashboard-subtitle">Human-Centered AI Assessment Analytics</p>
    </div>

    <!-- Filters -->
    <div class="filters-section">
      <h3>Filter</h3>
      <div class="filters-grid">
        <div class="filter-group">
          <label>Student-ID</label>
          <input v-model="filters.studentId" type="text" placeholder="z.B. S001" />
        </div>
        <div class="filter-group">
          <label>Von Datum</label>
          <input v-model="filters.dateFrom" type="date" />
        </div>
        <div class="filter-group">
          <label>Bis Datum</label>
          <input v-model="filters.dateTo" type="date" />
        </div>
        <div class="filter-group">
          <label>Themenbereich</label>
          <select v-model="filters.topicArea">
            <option value="">Alle</option>
            <option value="Mathematik">Mathematik</option>
            <option value="Physik">Physik</option>
            <option value="Chemie">Chemie</option>
          </select>
        </div>
        <div class="filter-group">
          <label>Klasse</label>
          <input v-model="filters.grade" type="text" placeholder="z.B. 10a" />
        </div>
        <div class="filter-actions">
          <button @click="applyFilters" class="btn-primary">Filter anwenden</button>
          <button @click="resetFilters" class="btn-secondary">Zurücksetzen</button>
        </div>
      </div>
    </div>

    <!-- Basic Stats -->
    <div class="stats-section">
      <h2>Grundstatistiken</h2>
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-label">Gesamt Sitzungen</div>
          <div class="stat-value">{{ totalSessions }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Durchschnittliche KI-Fragenqualität</div>
          <div class="stat-value">{{ avgAIQuality.toFixed(2) }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Durchschnittliches Engagement</div>
          <div class="stat-value">{{ avgEngagement.toFixed(2) }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Durchschnittlicher Verständnisfortschritt</div>
          <div class="stat-value">{{ avgUnderstanding.toFixed(2) }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Durchschnittliche Effizienz</div>
          <div class="stat-value">{{ avgEfficiency.toFixed(2) }}</div>
        </div>
      </div>
    </div>

    <!-- Dimension Breakdown -->
    <div class="dimensions-section">
      <h2>Dimensionen-Analyse</h2>
      <div class="dimensions-grid">
        <!-- Dimension 1: Transparency -->
        <div class="dimension-card">
          <h3>🔍 Transparenz</h3>
          <div class="dimension-metric">
            <span class="metric-label">Durchschnittliche KI-Fragenqualität:</span>
            <span class="metric-value">{{ avgAIQuality.toFixed(2) }}/5</span>
          </div>
          <div class="dimension-chart">
            <canvas :id="'chart-transparency'"></canvas>
          </div>
        </div>

        <!-- Dimension 2: Controllability -->
        <div class="dimension-card">
          <h3>🎛️ Kontrollierbarkeit</h3>
          <div class="dimension-metric">
            <span class="metric-label">Interventionsrate:</span>
            <span class="metric-value">{{ interventionRate.toFixed(1) }}%</span>
          </div>
          <div class="dimension-metric">
            <span class="metric-label">Schüler-Überschreibungen:</span>
            <span class="metric-value">{{ studentOverrideRate.toFixed(1) }}%</span>
          </div>
        </div>

        <!-- Dimension 3: Fairness -->
        <div class="dimension-card">
          <h3>⚖️ Fairness</h3>
          <div class="dimension-metric">
            <span class="metric-label">Durchschnittlicher Verständnisfortschritt:</span>
            <span class="metric-value">{{ avgUnderstanding.toFixed(2) }}/5</span>
          </div>
          <div class="dimension-chart">
            <canvas :id="'chart-fairness'"></canvas>
          </div>
        </div>

        <!-- Dimension 4: Psychological Safety -->
        <div class="dimension-card">
          <h3>🛡️ Psychologische Sicherheit</h3>
          <div class="dimension-metric">
            <span class="metric-label">Durchschnittliches Engagement:</span>
            <span class="metric-value">{{ avgEngagement.toFixed(2) }}/5</span>
          </div>
          <div class="dimension-metric">
            <span class="metric-label">Feedback-Sicherheit (Ja):</span>
            <span class="metric-value">{{ feedbackSafetyRate.toFixed(1) }}%</span>
          </div>
        </div>

        <!-- Dimension 5: Effectiveness -->
        <div class="dimension-card">
          <h3>✅ Effektivität</h3>
          <div class="dimension-metric">
            <span class="metric-label">Durchschnittliche Effizienz:</span>
            <span class="metric-value">{{ avgEfficiency.toFixed(2) }}/5</span>
          </div>
          <div class="dimension-metric">
            <span class="metric-label">Durchschnittliche Fragezyklen:</span>
            <span class="metric-value">{{ avgQuestionLoops.toFixed(1) }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Trend Chart -->
    <div class="trend-section">
      <h2>Trend über Zeit</h2>
      <div class="trend-chart">
        <canvas id="chart-trend"></canvas>
      </div>
    </div>

    <!-- Export -->
    <div class="export-section">
      <button @click="exportToCSV" class="btn-primary">📥 Als CSV exportieren</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { Chart, registerables } from 'chart.js'
Chart.register(...registerables)

const filters = ref({
  studentId: '',
  dateFrom: '',
  dateTo: '',
  topicArea: '',
  grade: ''
})

const assessments = ref([])
const filteredAssessments = ref([])

// Computed stats
const totalSessions = computed(() => filteredAssessments.value.length)

const avgAIQuality = computed(() => {
  if (filteredAssessments.value.length === 0) return 0
  const sum = filteredAssessments.value.reduce((acc, a) => acc + (a.aiQuestionQuality || 0), 0)
  return sum / filteredAssessments.value.length
})

const avgEngagement = computed(() => {
  if (filteredAssessments.value.length === 0) return 0
  const sum = filteredAssessments.value.reduce((acc, a) => acc + (a.engagementLevel || 0), 0)
  return sum / filteredAssessments.value.length
})

const avgUnderstanding = computed(() => {
  if (filteredAssessments.value.length === 0) return 0
  const sum = filteredAssessments.value.reduce((acc, a) => acc + (a.understandingProgress || 0), 0)
  return sum / filteredAssessments.value.length
})

const avgEfficiency = computed(() => {
  if (filteredAssessments.value.length === 0) return 0
  const sum = filteredAssessments.value.reduce((acc, a) => acc + (a.efficiencyScore || 0), 0)
  return sum / filteredAssessments.value.length
})

const interventionRate = computed(() => {
  if (filteredAssessments.value.length === 0) return 0
  const withInterventions = filteredAssessments.value.filter(a => (a.tutorInterventions || 0) > 0).length
  return (withInterventions / filteredAssessments.value.length) * 100
})

const studentOverrideRate = computed(() => {
  if (filteredAssessments.value.length === 0) return 0
  const withOverrides = filteredAssessments.value.filter(a => a.studentOverride === 'Yes' || a.studentOverride === true).length
  return (withOverrides / filteredAssessments.value.length) * 100
})

const feedbackSafetyRate = computed(() => {
  if (filteredAssessments.value.length === 0) return 0
  const safe = filteredAssessments.value.filter(a => a.studentFeedbackSafety === 'Yes' || a.studentFeedbackSafety === 'yes').length
  return (safe / filteredAssessments.value.length) * 100
})

const avgQuestionLoops = computed(() => {
  if (filteredAssessments.value.length === 0) return 0
  const sum = filteredAssessments.value.reduce((acc, a) => acc + (a.questionLoops || 0), 0)
  return sum / filteredAssessments.value.length
})

// Load assessments from backend
async function loadAssessments() {
  try {
    // In a real implementation, this would fetch from backend API
    // For now, we'll use a placeholder
    console.log('[DASHBOARD] Loading assessments...')
    // TODO: Implement API endpoint to fetch assessment data
    filteredAssessments.value = []
  } catch (error) {
    console.error('[DASHBOARD] Error loading assessments:', error)
  }
}

function applyFilters() {
  // Filter logic would go here
  loadAssessments()
}

function resetFilters() {
  filters.value = {
    studentId: '',
    dateFrom: '',
    dateTo: '',
    topicArea: '',
    grade: ''
  }
  loadAssessments()
}

function exportToCSV() {
  // CSV export logic
  console.log('[DASHBOARD] Exporting to CSV...')
}

onMounted(() => {
  loadAssessments()
})
</script>

<style scoped>
.dashboard-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

.dashboard-header {
  margin-bottom: 2rem;
}

.dashboard-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1e3a5f;
  margin: 0 0 0.5rem 0;
}

.dashboard-subtitle {
  color: #64748b;
  margin: 0;
}

.filters-section {
  background: #f8fafc;
  padding: 1.5rem;
  border-radius: 0.5rem;
  margin-bottom: 2rem;
}

.filters-section h3 {
  margin: 0 0 1rem 0;
  color: #1e3a5f;
}

.filters-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  align-items: end;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-group label {
  font-weight: 600;
  color: #2d3748;
  font-size: 0.9rem;
}

.filter-group input,
.filter-group select {
  padding: 0.5rem;
  border: 1px solid #cbd5e1;
  border-radius: 0.25rem;
  font-size: 0.9rem;
}

.filter-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-primary,
.btn-secondary {
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  font-weight: 600;
  cursor: pointer;
  border: none;
}

.btn-primary {
  background: #2c5f8d;
  color: white;
}

.btn-secondary {
  background: #e2e8f0;
  color: #475569;
}

.stats-section,
.dimensions-section,
.trend-section {
  margin-bottom: 2rem;
}

.stats-section h2,
.dimensions-section h2,
.trend-section h2 {
  color: #1e3a5f;
  margin-bottom: 1rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.stat-label {
  font-size: 0.9rem;
  color: #64748b;
  margin-bottom: 0.5rem;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: #1e3a5f;
}

.dimensions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.dimension-card {
  background: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.dimension-card h3 {
  color: #1e3a5f;
  margin: 0 0 1rem 0;
}

.dimension-metric {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
  border-bottom: 1px solid #e2e8f0;
}

.metric-label {
  color: #64748b;
  font-size: 0.9rem;
}

.metric-value {
  font-weight: 600;
  color: #1e3a5f;
}

.dimension-chart {
  margin-top: 1rem;
  height: 200px;
}

.trend-chart {
  background: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  height: 400px;
}

.export-section {
  text-align: center;
  padding: 2rem 0;
}
</style>
