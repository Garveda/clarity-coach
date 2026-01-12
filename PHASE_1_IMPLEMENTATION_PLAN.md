# 🚀 Phase 1 Implementation Plan - Assessment Integration

**Date Started:** January 12, 2026  
**Status:** IN PROGRESS  
**Estimated Time:** 6-8 hours  
**Priority:** High

---

## 🎯 Phase 1 Goals

Build the **core assessment infrastructure** that enables:
1. Manual post-session evaluation by tutors
2. Question interaction tracking for effectiveness measurement
3. Separate Assessment Log for research data

---

## 📋 Phase 1 Features (3 Core)

### ✅ Feature 1: Post-Session Assessment Modal

**Purpose:** Capture tutor's evaluation after each session

**Fields to Capture:**
1. **AI Question Quality** (1-5 scale)
2. **Engagement Level** (1-5 scale)
3. **Understanding Progress** (1-5 scale)
4. **Efficiency Score** (1-5 scale)
5. **Learner Type** (Dropdown: Visual, Analytical, Experimental, Mixed)
6. **Question Loops** (Auto-filled from tracking)
7. **Remarks** (Free text - optional)
8. **Further Considerations** (Free text - optional)

**UI Requirements:**
- Modal opens automatically after session ends
- Can be dismissed and reopened
- "Skip for now" option
- "Save and Continue" button
- Validation: Rating scales required
- Professional styling matching current design

**Technical:**
- New component: `src/components/PostSessionAssessment.vue`
- Emits data to parent (ClarityCoach.vue)
- Stores draft in LocalStorage (in case of accidental close)
- Final submit sends to backend

---

### ✅ Feature 2: Question Loop Tracking

**Purpose:** Measure how many times student cycles through questions

**What to Track:**
1. **Total Question Refreshes** per subtask
2. **Question View History** (which questions were shown)
3. **Timestamps** for each refresh
4. **Total Cycles** per session

**Implementation:**
- Extend existing `refreshQuestion()` function in ClarityCoach.vue
- Add new ref: `questionLoopTracking`
- Structure:
  ```javascript
  questionLoopTracking.value = {
    [taskIndex]: {
      [subIndex]: {
        totalRefreshes: 0,
        viewHistory: [
          { questionIndex: 0, timestamp: Date, viewCount: 1 },
          { questionIndex: 1, timestamp: Date, viewCount: 1 }
        ]
      }
    }
  }
  ```
- Auto-calculate total loops for Assessment Modal

**Technical:**
- Modify: `src/components/ClarityCoach.vue` (line ~721)
- Add tracking to `refreshQuestion()` function
- Compute total loops for export

---

### ✅ Feature 3: Assessment Log Excel Export

**Purpose:** Create separate sheet for assessment data

**Excel Structure:**
```
Clarity_Coach_Session_Log.xlsx
├── Technical_Log (existing - 21 columns, auto-populated)
└── Assessment_Log (NEW - 13 columns, manual post-session)
```

**Assessment Log Columns:**
1. Session-ID (link to Technical_Log)
2. Assessment Date
3. Assessment Time
4. Assessor Name (tutor who filled form)
5. AI Question Quality (1-5)
6. Engagement Level (1-5)
7. Understanding Progress (1-5)
8. Efficiency Score (1-5)
9. Learner Type Indicator (text)
10. Question Loops Total (number)
11. Remarks (text)
12. Further Considerations (text)
13. Assessment Completion Status (Complete/Partial/Skipped)

**Technical:**
- New backend endpoint: `/log-assessment`
- Modify: `backend/main.py`
- Use openpyxl to:
  - Check if Assessment_Log sheet exists
  - Create if missing
  - Append assessment data
  - Link via Session-ID

---

## 🛠️ Implementation Steps

### Step 1: Create Post-Session Assessment Component (3 hours)

**Files to Create:**
- `src/components/PostSessionAssessment.vue`

**Structure:**
```vue
<template>
  <div class="assessment-overlay" v-if="isOpen">
    <div class="assessment-container">
      <div class="assessment-header">
        <h2>📊 Sitzungsbewertung</h2>
        <p>Bitte bewerten Sie die Clarity Coach Sitzung</p>
      </div>
      
      <form @submit.prevent="submitAssessment">
        <!-- Rating Scales -->
        <div class="assessment-section">
          <h3>Bewertungen (1-5)</h3>
          
          <!-- AI Question Quality -->
          <div class="rating-group">
            <label>KI-Fragenqualität <span class="required">*</span></label>
            <div class="rating-scale">
              <button v-for="n in 5" :key="n" type="button"
                      :class="['rating-btn', { active: ratings.aiQuality === n }]"
                      @click="ratings.aiQuality = n">
                {{ n }}
              </button>
            </div>
            <p class="rating-hint">1 = Verwirrt Schüler | 5 = Optimal sokratisch</p>
          </div>
          
          <!-- Similar for other ratings -->
        </div>
        
        <!-- Learner Type Dropdown -->
        <div class="assessment-section">
          <label>Lerntyp-Indikator</label>
          <select v-model="learnerType">
            <option value="">Bitte wählen</option>
            <option value="visual">Visuell</option>
            <option value="analytical">Analytisch</option>
            <option value="experimental">Experimentell</option>
            <option value="visual-analytical">Visuell-Analytisch</option>
            <option value="visual-experimental">Visuell-Experimentell</option>
            <option value="analytical-experimental">Analytisch-Experimentell</option>
          </select>
        </div>
        
        <!-- Auto-filled metrics -->
        <div class="assessment-section">
          <h3>Automatisch erfasste Metriken</h3>
          <p>Fragenzyklen: <strong>{{ questionLoops }}</strong></p>
        </div>
        
        <!-- Free text -->
        <div class="assessment-section">
          <label>Bemerkungen (optional)</label>
          <textarea v-model="remarks" rows="3"></textarea>
          
          <label>Weitere Überlegungen (optional)</label>
          <textarea v-model="furtherConsiderations" rows="3"></textarea>
        </div>
        
        <!-- Actions -->
        <div class="assessment-actions">
          <button type="button" @click="skipAssessment" class="skip-btn">
            Überspringen
          </button>
          <button type="submit" :disabled="!isValid" class="submit-btn">
            📊 Bewertung speichern
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, defineProps, defineEmits } from 'vue';
import { toast } from 'vue-sonner';

const props = defineProps([
  'isOpen',
  'sessionId',
  'questionLoops'
]);

const emit = defineEmits(['close', 'submitted']);

const ratings = ref({
  aiQuality: null,
  engagement: null,
  understanding: null,
  efficiency: null
});

const learnerType = ref('');
const remarks = ref('');
const furtherConsiderations = ref('');
const assessorName = ref('');

const isValid = computed(() => {
  return ratings.value.aiQuality && 
         ratings.value.engagement && 
         ratings.value.understanding && 
         ratings.value.efficiency;
});

const submitAssessment = async () => {
  if (!isValid.value) {
    toast.error('Bitte füllen Sie alle Pflichtfelder aus');
    return;
  }
  
  const assessmentData = {
    sessionId: props.sessionId,
    assessorName: assessorName.value,
    aiQuestionQuality: ratings.value.aiQuality,
    engagementLevel: ratings.value.engagement,
    understandingProgress: ratings.value.understanding,
    efficiencyScore: ratings.value.efficiency,
    learnerTypeIndicator: learnerType.value || 'Nicht angegeben',
    questionLoops: props.questionLoops,
    remarks: remarks.value,
    furtherConsiderations: furtherConsiderations.value
  };
  
  try {
    const response = await fetch('http://127.0.0.1:8000/log-assessment', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(assessmentData)
    });
    
    if (!response.ok) throw new Error('Fehler beim Speichern');
    
    const result = await response.json();
    toast.success('Bewertung erfolgreich gespeichert!');
    emit('submitted', result);
    emit('close');
  } catch (error) {
    toast.error(`Fehler: ${error.message}`);
  }
};

const skipAssessment = () => {
  if (confirm('Möchten Sie die Bewertung wirklich überspringen?')) {
    emit('close');
  }
};
</script>

<style scoped>
/* Professional styling matching ClarityCoach design */
</style>
```

---

### Step 2: Add Question Loop Tracking (1 hour)

**Files to Modify:**
- `src/components/ClarityCoach.vue`

**Changes:**

1. Add new ref for tracking:
```javascript
const questionLoopTracking = ref({})
```

2. Modify `refreshQuestion()` function:
```javascript
function refreshQuestion(taskIndex, subIndex, subtask) {
  if (!subtask.questions || subtask.questions.length <= 1) return

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

  // Get current and next index
  const currentIdx = currentQuestionIndex.value[taskIndex]?.[subIndex] || 0
  const nextIdx = (currentIdx + 1) % subtask.questions.length

  // Update tracking
  questionLoopTracking.value[taskIndex][subIndex].totalRefreshes++
  questionLoopTracking.value[taskIndex][subIndex].viewHistory.push({
    questionIndex: nextIdx,
    timestamp: new Date(),
    isLoop: nextIdx === 0 && currentIdx !== 0 // Detected full cycle
  })

  // Update current question index
  if (!currentQuestionIndex.value[taskIndex]) {
    currentQuestionIndex.value[taskIndex] = []
  }
  currentQuestionIndex.value[taskIndex][subIndex] = nextIdx

  toast.success('Question updated', {
    description: `Showing question ${nextIdx + 1} of ${subtask.questions.length}`
  })
}
```

3. Add computed property for total loops:
```javascript
const totalQuestionLoops = computed(() => {
  let total = 0
  Object.values(questionLoopTracking.value).forEach(task => {
    Object.values(task).forEach(subtask => {
      total += subtask.totalRefreshes
    })
  })
  return total
})
```

---

### Step 3: Create Assessment Log Backend (1.5 hours)

**Files to Modify:**
- `backend/main.py`

**New Endpoint:**

```python
@app.post("/log-assessment")
async def log_assessment(assessment_data: dict = Body(...)):
    """
    Log post-session assessment to separate Excel sheet
    """
    excel_file_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 
        "Clarity_Coach_Session_Log.xlsx"
    )
    
    try:
        print("[ASSESSMENT] Starting assessment log...")
        
        # Load workbook
        if not os.path.exists(excel_file_path):
            raise HTTPException(
                status_code=404, 
                detail="Session log file not found. Create a session first."
            )
        
        workbook = openpyxl.load_workbook(excel_file_path)
        
        # Create Assessment_Log sheet if it doesn't exist
        if "Assessment_Log" not in workbook.sheetnames:
            sheet = workbook.create_sheet("Assessment_Log")
            
            # Add headers
            headers = [
                "Session-ID", "Assessment Date", "Assessment Time", 
                "Assessor Name", "AI Question Quality", "Engagement Level",
                "Understanding Progress", "Efficiency Score", 
                "Learner Type Indicator", "Question Loops Total",
                "Remarks", "Further Considerations", "Completion Status"
            ]
            sheet.append(headers)
            
            # Apply header styling
            header_font = Font(bold=True, color="FFFFFF")
            header_fill = PatternFill(
                start_color="2C5F8D", 
                end_color="2C5F8D", 
                fill_type="solid"
            )
            header_alignment = Alignment(horizontal="center", vertical="center")
            
            for col_num, header in enumerate(headers, 1):
                col_letter = get_column_letter(col_num)
                sheet[f"{col_letter}1"].font = header_font
                sheet[f"{col_letter}1"].fill = header_fill
                sheet[f"{col_letter}1"].alignment = header_alignment
                sheet.column_dimensions[col_letter].width = 18
        else:
            sheet = workbook["Assessment_Log"]
        
        # Prepare assessment row
        now = datetime.now()
        row_data = [
            assessment_data.get("sessionId", ""),
            now.strftime("%Y-%m-%d"),
            now.strftime("%H:%M:%S"),
            assessment_data.get("assessorName", ""),
            assessment_data.get("aiQuestionQuality", 0),
            assessment_data.get("engagementLevel", 0),
            assessment_data.get("understandingProgress", 0),
            assessment_data.get("efficiencyScore", 0),
            assessment_data.get("learnerTypeIndicator", ""),
            assessment_data.get("questionLoops", 0),
            assessment_data.get("remarks", ""),
            assessment_data.get("furtherConsiderations", ""),
            "Complete"
        ]
        
        sheet.append(row_data)
        workbook.save(excel_file_path)
        
        print(f"[ASSESSMENT] Assessment logged for session: {assessment_data.get('sessionId')}")
        return {
            "message": "Assessment logged successfully",
            "sessionId": assessment_data.get("sessionId")
        }
        
    except Exception as e:
        print(f"[ERROR] Failed to log assessment: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to log assessment: {str(e)}"
        )
```

---

### Step 4: Integration (1 hour)

**Files to Modify:**
- `src/components/ClarityCoach.vue`

**Changes:**

1. Import new component:
```javascript
import PostSessionAssessment from './PostSessionAssessment.vue'
```

2. Add state for assessment modal:
```javascript
const showAssessmentModal = ref(false)
const currentSessionId = ref('')
```

3. Modify `handleAnalysisResult()` to trigger assessment:
```javascript
function handleAnalysisResult(data) {
  loading.value = false
  
  if (data.error) {
    toast.error('Analysis failed', { description: data.error })
    return
  }
  
  response.value = data
  // ... existing code ...
  
  toast.success('Analysis complete', {
    description: 'Socratic questions have been successfully generated.'
  })
  
  // Trigger assessment modal after short delay
  setTimeout(() => {
    showAssessmentModal.value = true
  }, 2000) // 2 seconds after results appear
}
```

4. Handle assessment submission:
```javascript
function handleAssessmentSubmitted(result) {
  console.log('Assessment submitted:', result)
  showAssessmentModal.value = false
  toast.success('Thank you for completing the assessment!')
}
```

5. Add component to template:
```vue
<!-- Post-Session Assessment Modal -->
<PostSessionAssessment
  :isOpen="showAssessmentModal"
  :sessionId="currentSessionId"
  :questionLoops="totalQuestionLoops"
  @close="showAssessmentModal = false"
  @submitted="handleAssessmentSubmitted"
/>
```

---

## 🧪 Testing Plan

### Test Case 1: Complete Flow
1. Upload a file
2. Wait for analysis
3. Interact with questions (click refresh 5+ times)
4. Assessment modal should appear
5. Fill out all required fields
6. Submit assessment
7. Check Excel file:
   - Technical_Log sheet has session entry
   - Assessment_Log sheet has assessment entry
   - Session-IDs match

### Test Case 2: Question Loop Tracking
1. Upload file
2. Click refresh button multiple times on different subtasks
3. Verify `totalQuestionLoops` increases
4. Check that tracking data is passed to assessment modal

### Test Case 3: Skip Assessment
1. Complete session
2. Click "Skip" in assessment modal
3. Verify modal closes
4. Check that no assessment entry is created

### Test Case 4: Validation
1. Try to submit assessment with missing required fields
2. Verify error toast appears
3. Fill all fields and submit
4. Verify success

---

## 📊 Success Criteria

Phase 1 is complete when:
- ✅ Post-Session Assessment Modal appears after every session
- ✅ All 8 assessment fields can be filled and submitted
- ✅ Question loop tracking accurately counts refreshes
- ✅ Assessment data is saved to separate Excel sheet
- ✅ Session-IDs correctly link Technical_Log and Assessment_Log
- ✅ Professional styling matches existing design
- ✅ Error handling works (missing files, validation, etc.)
- ✅ User can skip assessment if needed

---

## 🎯 Next Steps After Phase 1

Once Phase 1 is tested and working:

**Evaluate:**
- Is the assessment modal useful?
- Is tracking data accurate?
- Does Excel export work smoothly?
- Any UI improvements needed?

**Then Decide:**
- Proceed to Phase 2 (Bias Detection + Tutor Interventions)?
- Or Phase 3 (Dashboard)?
- Or refine Phase 1 based on feedback?

---

## 📝 Implementation Notes

**Estimated Timeline:**
- Component creation: 3 hours
- Tracking implementation: 1 hour
- Backend endpoint: 1.5 hours
- Integration: 1 hour
- Testing: 1.5 hours
- Documentation: 1 hour
**Total: 8 hours**

**Dependencies:**
- ✅ No new npm packages needed
- ✅ openpyxl already installed
- ✅ All styling uses existing CSS patterns

---

**Status:** Ready to implement  
**Next Action:** Create PostSessionAssessment.vue component
