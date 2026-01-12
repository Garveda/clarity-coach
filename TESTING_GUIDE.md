# Clarity Coach - Testing Guide

**Version:** 2.0  
**Date:** 2026-01-12

---

## Quick Start Testing

### Prerequisites

1. Backend running: `http://127.0.0.1:8000`
2. Frontend running: `http://localhost:5173`
3. OpenAI API key configured in `.env`
4. Excel file exists: `Clarity_Coach_Session_Log.xlsx`

---

## Test Checklist

### 1. File Upload System

- [ ] **PDF Upload**
  - Upload a math PDF file
  - Verify loading indicator appears
  - Confirm tasks are parsed correctly
  - Check subtasks are extracted

- [ ] **Image Upload (PNG/JPG)**
  - Upload a math image
  - Verify OCR extracts text
  - Confirm analysis completes

- [ ] **Text File Upload**
  - Upload a .txt file with math problems
  - Verify parsing works

- [ ] **Error Handling**
  - Try uploading an unsupported file type
  - Verify error message appears

### 2. Socratic Questions

- [ ] **Question Display**
  - Each subtask shows a socratic question
  - Questions are in German
  - LaTeX renders correctly

- [ ] **Question Refresh**
  - Click refresh button on a question
  - Verify new question appears
  - Check question counter increments

### 3. Progressive Hints (Phase 3.1)

- [ ] **Level 1 - Socratic**
  - Click "🤔 Hilfestellung" first time
  - Verify hint is a guiding question
  - Badge shows "Sokratisch"

- [ ] **Level 2 - Directive**
  - Click "Weitere Hilfe benötigt?"
  - Verify hint is more specific
  - Badge shows "Anleitend"

- [ ] **Level 3 - Specific**
  - Request third hint
  - Verify hint is very specific
  - "Weitere Hilfe" button hidden

- [ ] **Maximum Reached**
  - Try requesting 4th hint
  - Verify toast message: "Maximale Hilfestellung erreicht"

### 4. Smart Visual Hint (Phase 2)

- [ ] **Button Visibility**
  - Verify "💡 Visuelle Hilfe" button appears
  - Legacy buttons (Visualization, Animation, Graph) hidden

- [ ] **Visual Selection**
  - Click visual hint button
  - Loading indicator appears
  - Appropriate visual type is selected

- [ ] **Graph Display**
  - For function tasks, verify graph renders
  - Chart is interactive (zoom, hover)
  - Axis labels are correct

- [ ] **Animation Display**
  - Verify animation plays
  - Steps appear sequentially
  - LaTeX in animation renders

- [ ] **Key Facts Display**
  - Verify key facts list appears
  - LaTeX formulas render correctly

### 5. Smart Approach Checker (Phase 3.2)

- [ ] **Input Toggle**
  - Click "✓ Meinen Ansatz prüfen"
  - Input area appears
  - Placeholder text visible

- [ ] **Empty Input Validation**
  - Click check without input
  - Warning toast appears

- [ ] **Correct Approach**
  - Enter a correct approach
  - Submit and verify:
    - "Auf dem richtigen Weg!" message
    - High confidence stars (4-5)
    - Strengths listed

- [ ] **Incorrect Approach**
  - Enter an incorrect approach
  - Submit and verify:
    - "Noch nicht ganz..." message
    - Lower confidence stars (1-3)
    - Improvements listed
    - Specific issue shown (if any)

- [ ] **No Solution Revealed**
  - Verify feedback never reveals actual solution
  - Only hints and guidance provided

- [ ] **Retry Function**
  - Click "🔄 Neuen Ansatz eingeben"
  - Input area reappears
  - Previous result cleared

### 6. Session Form

- [ ] **Form Opens**
  - Session form appears after file upload
  - File info auto-populated

- [ ] **Required Fields**
  - Try submitting with empty required fields
  - Validation prevents submission

- [ ] **Usage Statistics Display**
  - Stats section shows correct counts
  - Self-sufficiency stars display

- [ ] **Self-Sufficiency Calculation**
  - Use 0 hints → Score 5
  - Use 1-2 hints → Score 4
  - Use 3-5 hints → Score 3
  - Use 6-8 hints → Score 2
  - Use 9+ hints → Score 1

- [ ] **Form Submission**
  - Fill all required fields
  - Click "Sitzung protokollieren"
  - Success toast appears
  - Form closes

### 7. Excel Export

- [ ] **Session Log**
  - Open `Clarity_Coach_Session_Log.xlsx`
  - New row added with correct data
  - All 23 columns populated:
    - Session_ID, Datum, Uhrzeit
    - User info (Name, Klasse, Schule)
    - Task info (Fach, Thema, etc.)
    - Usage stats (Vis, Anim, Grafiken, Hints)
    - **Ansatzpruefungen_Genutzt** [NEW]
    - **Selbststaendigkeits_Score** [NEW]
    - Feedback, Duration, Notes

### 8. Feature Flags

- [ ] **Legacy Mode Test**
  - Set `legacyVisualButtons: true` in featureFlags.js
  - Restart frontend
  - Verify 3 separate buttons appear

- [ ] **Approach Checker Toggle**
  - Set `smartApproachChecker: false`
  - Restart frontend
  - Verify approach checker hidden

### 9. Error Handling

- [ ] **API Timeout**
  - Simulate slow connection
  - Verify timeout handling

- [ ] **Network Error**
  - Stop backend
  - Try action, verify error message

- [ ] **Invalid Response**
  - Backend returns error
  - Error toast displayed

### 10. Performance

- [ ] **Large File Upload**
  - Upload multi-page PDF
  - Verify all pages processed
  - No browser freeze

- [ ] **Multiple Actions**
  - Click multiple buttons rapidly
  - No duplicate requests
  - Loading states correct

---

## Test Scenarios

### Scenario A: Independent Student

1. Upload a task
2. Read socratic questions
3. Solve without hints
4. Check approach (should pass)
5. Log session
6. **Expected:** Self-sufficiency score 5

### Scenario B: Guided Student

1. Upload a task
2. Request Level 1 hint
3. Request Level 2 hint
4. Use visual help
5. Check approach
6. Log session
7. **Expected:** Self-sufficiency score 3-4

### Scenario C: Struggling Student

1. Upload a task
2. Request all 3 hint levels
3. Check approach multiple times
4. Use visual help
5. Log session
6. **Expected:** Self-sufficiency score 1-2

---

## Regression Tests

### After Code Changes

1. [ ] All hint levels still work
2. [ ] Visual selection logic correct
3. [ ] Approach checker returns proper feedback
4. [ ] Excel export includes all columns
5. [ ] Self-sufficiency calculation accurate

---

## Browser Compatibility

Test in:
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Edge (latest)
- [ ] Safari (if available)

---

## Sign-Off

| Tester | Date | Version | Status |
|--------|------|---------|--------|
| | | 2.0 | |

---

**Notes:**
- Document any bugs found
- Note any UI/UX improvements needed
- Record performance issues
