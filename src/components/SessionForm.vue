<template>
  <div class="session-form-modal" v-if="isOpen" @click.self="closeForm">
    <div class="session-form-container">
      <div class="form-header">
        <h2>📝 Sitzungsinformationen</h2>
        <p class="form-subtitle">Bitte fülle das Formular aus, um die Sitzung zu protokollieren</p>
        <button class="close-btn" @click="closeForm" title="Schließen">×</button>
      </div>

      <form @submit.prevent="submitForm" class="session-form">
        <!-- Personal Information Section -->
        <div class="form-section">
          <h3>👤 Persönliche Informationen</h3>
          <div class="form-row">
            <div class="form-group">
              <label for="benutzer_name">Name des Benutzers <span class="required">*</span></label>
              <input 
                type="text" 
                id="benutzer_name" 
                v-model="formData.benutzer_name" 
                required
                placeholder="z.B. Max Mustermann"
              />
            </div>
            <div class="form-group">
              <label for="klasse">Klasse <span class="required">*</span></label>
              <input 
                type="text" 
                id="klasse" 
                v-model="formData.klasse" 
                required
                placeholder="z.B. 10a"
              />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="schule">Schule <span class="required">*</span></label>
              <input 
                type="text" 
                id="schule" 
                v-model="formData.schule" 
                required
                placeholder="z.B. Gymnasium Beispiel"
              />
            </div>
            <div class="form-group">
              <label for="fach">Fach <span class="required">*</span></label>
              <select id="fach" v-model="formData.fach" required>
                <option value="">-- Wählen --</option>
                <option value="Mathematik">Mathematik</option>
                <option value="Physik">Physik</option>
                <option value="Chemie">Chemie</option>
                <option value="Biologie">Biologie</option>
                <option value="Informatik">Informatik</option>
                <option value="Sonstiges">Sonstiges</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Task Information Section -->
        <div class="form-section">
          <h3>📚 Aufgabeninformationen</h3>
          <div class="form-row">
            <div class="form-group">
              <label for="thema">Thema <span class="required">*</span></label>
              <input 
                type="text" 
                id="thema" 
                v-model="formData.thema" 
                required
                placeholder="z.B. Quadratische Gleichungen"
              />
            </div>
            <div class="form-group">
              <label for="aufgabentyp">Aufgabentyp</label>
              <input 
                type="text" 
                id="aufgabentyp" 
                v-model="formData.aufgabentyp"
                placeholder="z.B. Gleichungen lösen"
              />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="schwierigkeitsgrad">Schwierigkeitsgrad <span class="required">*</span></label>
              <select id="schwierigkeitsgrad" v-model="formData.schwierigkeitsgrad" required>
                <option value="">-- Wählen --</option>
                <option value="Leicht">Leicht</option>
                <option value="Mittel">Mittel</option>
                <option value="Anspruchsvoll">Anspruchsvoll</option>
              </select>
            </div>
            <div class="form-group">
              <label for="feedback">Feedback</label>
              <select id="feedback" v-model="formData.feedback">
                <option value="">-- Wählen --</option>
                <option value="Helpful">Helpful</option>
                <option value="Needs Clarification">Needs Clarification</option>
                <option value="Keine Angabe">Keine Angabe</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Notes Section -->
        <div class="form-section">
          <h3>📝 Zusätzliche Informationen</h3>
          <div class="form-group full-width">
            <label for="notizen">Notizen</label>
            <textarea 
              id="notizen" 
              v-model="formData.notizen" 
              rows="3"
              placeholder="Optionale Notizen zur Sitzung..."
            ></textarea>
          </div>
        </div>

        <!-- Hidden fields (auto-filled) -->
        <input type="hidden" v-model="formData.datei_name" />
        <input type="hidden" v-model="formData.datei_typ" />
        <input type="hidden" v-model="formData.anzahl_aufgaben" />
        <input type="hidden" v-model="formData.anzahl_teilaufgaben" />
        <input type="hidden" v-model="formData.visualisierungen_genutzt" />
        <input type="hidden" v-model="formData.animationen_genutzt" />
        <input type="hidden" v-model="formData.grafiken_genutzt" />
        <input type="hidden" v-model="formData.loesungen_angezeigt" />
        <input type="hidden" v-model="formData.sitzungsdauer_minuten" />

        <!-- Form Actions -->
        <div class="form-actions">
          <button type="button" class="btn-cancel" @click="closeForm">
            Abbrechen
          </button>
          <button type="submit" class="btn-submit" :disabled="isSubmitting">
            <span v-if="!isSubmitting">📊 Sitzung protokollieren</span>
            <span v-else>Wird gespeichert...</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { toast } from 'vue-sonner';

const props = defineProps({
  isOpen: Boolean,
  fileName: String,
  fileType: String,
  taskCount: Number,
  subtaskCount: Number
});

const emit = defineEmits(['close', 'submitted']);

const isSubmitting = ref(false);
const formData = ref({
  benutzer_name: '',
  klasse: '',
  schule: '',
  fach: '',
  thema: '',
  aufgabentyp: '',
  schwierigkeitsgrad: '',
  datei_name: '',
  datei_typ: '',
  anzahl_aufgaben: 0,
  anzahl_teilaufgaben: 0,
  visualisierungen_genutzt: 0,
  animationen_genutzt: 0,
  grafiken_genutzt: 0,
  loesungen_angezeigt: 0,
  feedback: '',
  sitzungsdauer_minuten: 0,
  notizen: ''
});

// Session start time
const sessionStartTime = ref(Date.now());

// Watch for prop changes and update form data
watch(() => props.fileName, (newVal) => {
  if (newVal) formData.value.datei_name = newVal;
});

watch(() => props.fileType, (newVal) => {
  if (newVal) formData.value.datei_typ = newVal;
});

watch(() => props.taskCount, (newVal) => {
  if (newVal) formData.value.anzahl_aufgaben = newVal;
});

watch(() => props.subtaskCount, (newVal) => {
  if (newVal) formData.value.anzahl_teilaufgaben = newVal;
});

// Update usage stats from parent
const updateUsageStats = (stats) => {
  formData.value.visualisierungen_genutzt = stats.visualizations || 0;
  formData.value.animationen_genutzt = stats.animations || 0;
  formData.value.grafiken_genutzt = stats.graphs || 0;
  formData.value.loesungen_angezeigt = stats.solutions || 0;
};

// Calculate session duration
const calculateDuration = () => {
  const duration = (Date.now() - sessionStartTime.value) / 1000 / 60; // minutes
  formData.value.sitzungsdauer_minuten = Math.round(duration * 10) / 10; // Round to 1 decimal
};

const closeForm = () => {
  emit('close');
};

const submitForm = async () => {
  isSubmitting.value = true;
  
  try {
    // Calculate session duration
    calculateDuration();
    
    // Send to backend
    const response = await fetch('http://127.0.0.1:8000/log-session', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData.value),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || 'Fehler beim Speichern');
    }

    const result = await response.json();
    
    console.log('Session logged successfully:', result);
    
    toast.success(`Sitzung erfolgreich protokolliert! (ID: ${result.session_id})`);
    
    // Reset form
    resetForm();
    
    emit('submitted', result);
    
    // Small delay to ensure toast is shown
    setTimeout(() => {
      emit('close');
    }, 500);
    
  } catch (error) {
    console.error('Error logging session:', error);
    toast.error(`Fehler beim Protokollieren: ${error.message}`);
  } finally {
    isSubmitting.value = false;
  }
};

const resetForm = () => {
  formData.value = {
    benutzer_name: '',
    klasse: '',
    schule: '',
    fach: '',
    thema: '',
    aufgabentyp: '',
    schwierigkeitsgrad: '',
    datei_name: props.fileName || '',
    datei_typ: props.fileType || '',
    anzahl_aufgaben: props.taskCount || 0,
    anzahl_teilaufgaben: props.subtaskCount || 0,
    visualisierungen_genutzt: 0,
    animationen_genutzt: 0,
    grafiken_genutzt: 0,
    loesungen_angezeigt: 0,
    feedback: '',
    sitzungsdauer_minuten: 0,
    notizen: ''
  };
  sessionStartTime.value = Date.now();
};

// Expose method to update stats
defineExpose({
  updateUsageStats
});
</script>

<style scoped>
.session-form-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 10000;
  padding: 20px;
  overflow-y: auto;
}

.session-form-container {
  background: white;
  border-radius: 16px;
  max-width: 800px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.form-header {
  background: linear-gradient(135deg, #1e3a5f 0%, #2c5f8d 100%);
  color: white;
  padding: 30px;
  border-radius: 16px 16px 0 0;
  position: relative;
}

.form-header h2 {
  margin: 0 0 10px 0;
  font-size: 28px;
  font-weight: 700;
}

.form-subtitle {
  margin: 0;
  opacity: 0.9;
  font-size: 14px;
}

.close-btn {
  position: absolute;
  top: 20px;
  right: 20px;
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  font-size: 32px;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
  transition: all 0.2s;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: rotate(90deg);
}

.session-form {
  padding: 30px;
}

.form-section {
  margin-bottom: 30px;
  padding-bottom: 30px;
  border-bottom: 2px solid #f0f0f0;
}

.form-section:last-of-type {
  border-bottom: none;
}

.form-section h3 {
  color: #1e3a5f;
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 20px 0;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.form-row:last-child {
  margin-bottom: 0;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-group label {
  color: #333;
  font-weight: 600;
  margin-bottom: 8px;
  font-size: 14px;
}

.required {
  color: #ef4444;
}

.form-group input,
.form-group select,
.form-group textarea {
  padding: 12px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  font-family: inherit;
  transition: all 0.2s;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-group textarea {
  resize: vertical;
  min-height: 80px;
}

.form-actions {
  display: flex;
  gap: 15px;
  justify-content: flex-end;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 2px solid #f0f0f0;
}

.btn-cancel,
.btn-submit {
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.btn-cancel {
  background: #f3f4f6;
  color: #6b7280;
}

.btn-cancel:hover {
  background: #e5e7eb;
}

.btn-submit {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
}

.btn-submit:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(59, 130, 246, 0.3);
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Responsive */
@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .session-form-container {
    max-height: 95vh;
  }
  
  .form-header {
    padding: 20px;
  }
  
  .form-header h2 {
    font-size: 22px;
  }
  
  .session-form {
    padding: 20px;
  }
}
</style>
