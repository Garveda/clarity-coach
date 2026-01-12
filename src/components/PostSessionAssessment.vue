<template>
  <div class="assessment-overlay" v-if="isOpen" @click.self="closeModal">
    <div class="assessment-container">
      <!-- Header -->
      <div class="assessment-header">
        <div class="header-content">
          <h2 class="assessment-title">📊 Sitzungsbewertung</h2>
          <p class="assessment-subtitle">
            Bitte bewerten Sie die Clarity Coach Sitzung
          </p>
          <p class="session-id-display">Session-ID: <strong>{{ sessionId || 'N/A' }}</strong></p>
        </div>
        <button class="close-btn" @click="closeModal" title="Schließen">×</button>
      </div>

      <form @submit.prevent="submitAssessment" class="assessment-form">
        <!-- Assessor Name -->
        <div class="form-section">
          <div class="form-group">
            <label for="assessor">Ihr Name (Tutor/Evaluator)</label>
            <input
              type="text"
              id="assessor"
              v-model="assessorName"
              placeholder="z.B. Prof. Müller"
              class="text-input"
            />
          </div>
        </div>

        <!-- Rating Scales Section -->
        <div class="form-section">
          <h3 class="section-title">⭐ Bewertungen (1-5 Skala)</h3>
          
          <!-- AI Question Quality -->
          <div class="rating-group">
            <label class="rating-label">
              KI-Fragenqualität <span class="required">*</span>
            </label>
            <div class="rating-scale">
              <button
                v-for="n in 5"
                :key="`quality-${n}`"
                type="button"
                :class="['rating-btn', { active: ratings.aiQuality === n }]"
                @click="ratings.aiQuality = n"
                :title="getQualityHint(n)"
              >
                {{ n }}
              </button>
            </div>
            <p class="rating-hint">
              1 = Verwirrt Schüler | 3 = Angemessen | 5 = Optimal sokratisch
            </p>
          </div>

          <!-- Engagement Level -->
          <div class="rating-group">
            <label class="rating-label">
              Engagement-Level <span class="required">*</span>
            </label>
            <div class="rating-scale">
              <button
                v-for="n in 5"
                :key="`engagement-${n}`"
                type="button"
                :class="['rating-btn', { active: ratings.engagement === n }]"
                @click="ratings.engagement = n"
                :title="getEngagementHint(n)"
              >
                {{ n }}
              </button>
            </div>
            <p class="rating-hint">
              1 = Passiv | 3 = Teilnehmend | 5 = Hochengagiert
            </p>
          </div>

          <!-- Understanding Progress -->
          <div class="rating-group">
            <label class="rating-label">
              Verständnisfortschritt <span class="required">*</span>
            </label>
            <div class="rating-scale">
              <button
                v-for="n in 5"
                :key="`understanding-${n}`"
                type="button"
                :class="['rating-btn', { active: ratings.understanding === n }]"
                @click="ratings.understanding = n"
                :title="getUnderstandingHint(n)"
              >
                {{ n }}
              </button>
            </div>
            <p class="rating-hint">
              1 = Kein Fortschritt | 3 = Konzept erfasst | 5 = Transfer möglich
            </p>
          </div>

          <!-- Efficiency Score -->
          <div class="rating-group">
            <label class="rating-label">
              Effizienz-Score <span class="required">*</span>
            </label>
            <div class="rating-scale">
              <button
                v-for="n in 5"
                :key="`efficiency-${n}`"
                type="button"
                :class="['rating-btn', { active: ratings.efficiency === n }]"
                @click="ratings.efficiency = n"
                :title="getEfficiencyHint(n)"
              >
                {{ n }}
              </button>
            </div>
            <p class="rating-hint">
              1 = Ziel nicht erreicht | 3 = Ziel erreicht | 5 = Optimal effizient
            </p>
          </div>
        </div>

        <!-- Learner Type Section -->
        <div class="form-section">
          <h3 class="section-title">🎓 Lerntyp-Indikator</h3>
          <div class="form-group">
            <label for="learner-type">Welcher Lerntyp zeigt sich?</label>
            <select id="learner-type" v-model="learnerType" class="select-input">
              <option value="">Nicht angegeben</option>
              <option value="visual">Visuell (nutzt Grafiken/Animationen)</option>
              <option value="analytical">Analytisch (Schritt-für-Schritt-Logik)</option>
              <option value="experimental">Experimentell (Trial & Error)</option>
              <option value="visual-analytical">Visuell-Analytisch (Kombination)</option>
              <option value="visual-experimental">Visuell-Experimentell (Kombination)</option>
              <option value="analytical-experimental">Analytisch-Experimentell (Kombination)</option>
            </select>
          </div>
        </div>

        <!-- Automatic Metrics Section -->
        <div class="form-section metrics-section">
          <h3 class="section-title">📈 Automatisch erfasste Metriken</h3>
          <div class="metrics-grid">
            <div class="metric-item">
              <span class="metric-label">Fragenzyklen:</span>
              <span class="metric-value">{{ questionLoops || 0 }}</span>
            </div>
            <div class="metric-item">
              <span class="metric-label">Session-ID:</span>
              <span class="metric-value">{{ sessionId || 'N/A' }}</span>
            </div>
          </div>
          <p class="metrics-note">
            Diese Werte wurden automatisch während der Sitzung erfasst.
          </p>
        </div>

        <!-- Free Text Section -->
        <div class="form-section">
          <h3 class="section-title">📝 Zusätzliche Anmerkungen</h3>
          
          <div class="form-group">
            <label for="remarks">Bemerkungen (optional)</label>
            <textarea
              id="remarks"
              v-model="remarks"
              rows="3"
              placeholder="Beobachtungen, Auffälligkeiten, etc."
              class="textarea-input"
            ></textarea>
          </div>

          <div class="form-group">
            <label for="considerations">Weitere Überlegungen (optional)</label>
            <textarea
              id="considerations"
              v-model="furtherConsiderations"
              rows="3"
              placeholder="Empfehlungen, nächste Schritte, etc."
              class="textarea-input"
            ></textarea>
          </div>
        </div>

        <!-- Validation Messages -->
        <div v-if="showValidationError" class="validation-error">
          ⚠️ Bitte füllen Sie alle Pflichtfelder (Bewertungen 1-5) aus.
        </div>

        <!-- Action Buttons -->
        <div class="assessment-actions">
          <button
            type="button"
            @click="skipAssessment"
            class="skip-btn"
          >
            Überspringen
          </button>
          <button
            type="submit"
            :disabled="isSubmitting"
            class="submit-btn"
          >
            <span v-if="!isSubmitting">📊 Bewertung speichern</span>
            <span v-else>Wird gespeichert...</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, defineProps, defineEmits, watch } from 'vue';
import { toast } from 'vue-sonner';

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  sessionId: {
    type: String,
    default: ''
  },
  questionLoops: {
    type: Number,
    default: 0
  }
});

const emit = defineEmits(['close', 'submitted']);

// Form data
const assessorName = ref('');
const ratings = ref({
  aiQuality: null,
  engagement: null,
  understanding: null,
  efficiency: null
});
const learnerType = ref('');
const remarks = ref('');
const furtherConsiderations = ref('');

// UI state
const isSubmitting = ref(false);
const showValidationError = ref(false);

// Validation
const isValid = computed(() => {
  return ratings.value.aiQuality !== null &&
         ratings.value.engagement !== null &&
         ratings.value.understanding !== null &&
         ratings.value.efficiency !== null;
});

// Tooltips
const getQualityHint = (n) => {
  const hints = {
    1: 'Nicht zielführend, verwirrt Schüler',
    2: 'Zu abstrakt oder unklar',
    3: 'Angemessen, aber verbesserungsfähig',
    4: 'Gut geführt, zielgerichtet',
    5: 'Optimal sokratisch, fördert tiefes Verständnis'
  };
  return hints[n];
};

const getEngagementHint = (n) => {
  const hints = {
    1: 'Passiv, wenig Beteiligung',
    2: 'Reagierend, antwortet nur auf Fragen',
    3: 'Teilnehmend, folgt aktiv',
    4: 'Aktiv fragend, eigene Gedanken einbringend',
    5: 'Hochengagiert, exploriert selbstständig'
  };
  return hints[n];
};

const getUnderstandingHint = (n) => {
  const hints = {
    1: 'Kein Fortschritt erkennbar',
    2: 'Teilweise verstanden, große Lücken',
    3: 'Konzept im Kern erfasst',
    4: 'Kann Konzept anwenden',
    5: 'Transfer auf neue Problemstellungen möglich'
  };
  return hints[n];
};

const getEfficiencyHint = (n) => {
  const hints = {
    1: 'Ziel nicht erreicht',
    2: 'Ziel teilweise erreicht, ineffizient',
    3: 'Ziel erreicht, durchschnittliche Effizienz',
    4: 'Ziel gut erreicht, effizient',
    5: 'Ziel optimal erreicht, sehr effizient'
  };
  return hints[n];
};

// Methods
const closeModal = () => {
  if (confirm('Möchten Sie die Bewertung wirklich schließen? Ungespeicherte Daten gehen verloren.')) {
    emit('close');
  }
};

const skipAssessment = () => {
  if (confirm('Möchten Sie die Bewertung wirklich überspringen?')) {
    emit('close');
    toast.info('Bewertung übersprungen');
  }
};

const submitAssessment = async () => {
  showValidationError.value = false;
  
  if (!isValid.value) {
    showValidationError.value = true;
    toast.error('Bitte füllen Sie alle Pflichtfelder aus');
    return;
  }
  
  isSubmitting.value = true;
  
  const assessmentData = {
    sessionId: props.sessionId,
    assessorName: assessorName.value || 'Nicht angegeben',
    aiQuestionQuality: ratings.value.aiQuality,
    engagementLevel: ratings.value.engagement,
    understandingProgress: ratings.value.understanding,
    efficiencyScore: ratings.value.efficiency,
    learnerTypeIndicator: learnerType.value || 'Nicht angegeben',
    questionLoops: props.questionLoops || 0,
    remarks: remarks.value || '',
    furtherConsiderations: furtherConsiderations.value || ''
  };
  
  try {
    const response = await fetch('http://127.0.0.1:8000/log-assessment', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(assessmentData)
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Fehler beim Speichern');
    }
    
    const result = await response.json();
    
    console.log('[ASSESSMENT] Success response:', result);
    
    // Reset submitting state immediately
    isSubmitting.value = false;
    
    toast.success('Bewertung erfolgreich gespeichert!', {
      description: `Session-ID: ${props.sessionId}`
    });
    
    resetForm();
    
    console.log('[ASSESSMENT] Emitting submitted event');
    emit('submitted', result);
    
    // Close immediately instead of waiting
    console.log('[ASSESSMENT] Closing modal now');
    emit('close');
    
  } catch (error) {
    console.error('Error submitting assessment:', error);
    toast.error(`Fehler beim Speichern: ${error.message}`);
    isSubmitting.value = false;
  }
};

const resetForm = () => {
  assessorName.value = '';
  ratings.value = {
    aiQuality: null,
    engagement: null,
    understanding: null,
    efficiency: null
  };
  learnerType.value = '';
  remarks.value = '';
  furtherConsiderations.value = '';
  showValidationError.value = false;
};

// Watch for modal opening
watch(() => props.isOpen, (newVal) => {
  if (newVal) {
    // Reset validation error when modal opens
    showValidationError.value = false;
  }
});
</script>

<style scoped>
/* Overlay */
.assessment-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
  padding: 1rem;
  overflow-y: auto;
}

/* Container */
.assessment-container {
  background: #ffffff;
  border-radius: 1rem;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  width: 100%;
  max-width: 700px;
  max-height: 90vh;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

/* Header */
.assessment-header {
  background: linear-gradient(to right, #1e3a5f, #2c5f8d);
  color: white;
  padding: 1.5rem 2rem;
  border-top-left-radius: 1rem;
  border-top-right-radius: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.header-content {
  flex: 1;
}

.assessment-title {
  margin: 0 0 0.5rem 0;
  font-size: 1.5rem;
  font-weight: 700;
}

.assessment-subtitle {
  margin: 0 0 0.75rem 0;
  font-size: 0.95rem;
  opacity: 0.95;
}

.session-id-display {
  margin: 0;
  font-size: 0.85rem;
  opacity: 0.9;
  font-family: 'Courier New', monospace;
}

.close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 2rem;
  cursor: pointer;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  transition: background-color 0.2s ease;
  line-height: 1;
}

.close-btn:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

/* Form */
.assessment-form {
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.form-section {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.section-title {
  margin: 0 0 0.75rem 0;
  font-size: 1.15rem;
  font-weight: 600;
  color: #1e3a5f;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* Form Groups */
.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 600;
  color: #2d3748;
  font-size: 0.95rem;
}

.text-input,
.select-input,
.textarea-input {
  padding: 0.75rem;
  border: 1px solid #cbd5e1;
  border-radius: 0.5rem;
  font-size: 0.95rem;
  color: #2d3748;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.text-input:focus,
.select-input:focus,
.textarea-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.textarea-input {
  resize: vertical;
  font-family: inherit;
}

/* Rating Groups */
.rating-group {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 0.5rem;
}

.rating-label {
  font-weight: 600;
  color: #1e3a5f;
  font-size: 0.95rem;
}

.required {
  color: #e53e3e;
  margin-left: 0.25rem;
}

.rating-scale {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
}

.rating-btn {
  width: 3.5rem;
  height: 3.5rem;
  border: 2px solid #cbd5e1;
  background: white;
  border-radius: 0.5rem;
  font-size: 1.25rem;
  font-weight: 600;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s ease;
}

.rating-btn:hover {
  border-color: #2c5f8d;
  background: #f1f5f9;
  transform: translateY(-2px);
}

.rating-btn.active {
  border-color: #2c5f8d;
  background: linear-gradient(to right, #1e3a5f, #2c5f8d);
  color: white;
  transform: scale(1.1);
}

.rating-hint {
  margin: 0;
  font-size: 0.85rem;
  color: #64748b;
  text-align: center;
  font-style: italic;
}

/* Metrics Section */
.metrics-section {
  background: #eff6ff;
  padding: 1.5rem;
  border-radius: 0.5rem;
  border: 1px solid #bfdbfe;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 0.75rem;
}

.metric-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background: white;
  border-radius: 0.375rem;
  border: 1px solid #dbeafe;
}

.metric-label {
  font-weight: 500;
  color: #475569;
  font-size: 0.9rem;
}

.metric-value {
  font-weight: 700;
  color: #1e3a5f;
  font-size: 1rem;
  font-family: 'Courier New', monospace;
}

.metrics-note {
  margin: 0;
  font-size: 0.85rem;
  color: #64748b;
  font-style: italic;
}

/* Validation Error */
.validation-error {
  padding: 1rem;
  background: #fee2e2;
  border: 1px solid #fca5a5;
  border-radius: 0.5rem;
  color: #991b1b;
  font-weight: 500;
  text-align: center;
}

/* Action Buttons */
.assessment-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
}

.skip-btn,
.submit-btn {
  padding: 0.875rem 1.75rem;
  border-radius: 0.5rem;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.skip-btn {
  background: #e2e8f0;
  color: #475569;
  border: 1px solid #cbd5e1;
}

.skip-btn:hover {
  background: #cbd5e1;
  color: #334155;
}

.submit-btn {
  background: linear-gradient(to right, #1e3a5f, #2c5f8d);
  color: white;
  border: 1px solid #1e3a5f;
}

.submit-btn:hover:not(:disabled) {
  background: linear-gradient(to right, #2c5f8d, #3b82f6);
  box-shadow: 0 4px 12px rgba(44, 95, 141, 0.4);
  transform: translateY(-2px);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Responsive */
@media (max-width: 768px) {
  .assessment-container {
    max-width: 100%;
    border-radius: 0;
    max-height: 100vh;
  }

  .assessment-header {
    border-radius: 0;
  }

  .rating-scale {
    flex-wrap: wrap;
  }

  .rating-btn {
    width: 3rem;
    height: 3rem;
    font-size: 1.1rem;
  }

  .assessment-actions {
    flex-direction: column-reverse;
  }

  .skip-btn,
  .submit-btn {
    width: 100%;
  }
}
</style>
