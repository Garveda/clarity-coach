# Comprehensive Test Plan: Human-Centered AI Assessment System

**Date:** 2025-01-12  
**Purpose:** Verify all new features work correctly

---

## Pre-Test Checklist

- [ ] Backend server running on `http://127.0.0.1:8000`
- [ ] Frontend server running on `http://localhost:5173`
- [ ] Excel file exists: `Clarity_Coach_Session_Log.xlsx`
- [ ] Browser open to `http://localhost:5173`

---

## Test 1: Existing Features (Regression Test)

### 1.1 File Upload
- [ ] Upload a math task (PDF/image/txt)
- [ ] Verify tasks and subtasks appear
- [ ] Verify Socratic questions display

### 1.2 Progressive Hints
- [ ] Click "🤔 Hilfestellung (0)" on a subtask
- [ ] Verify Level 1 hint appears (Sokratisch badge)
- [ ] Click "Weitere Hilfe benötigt?"
- [ ] Verify Level 2 hint appears (Anleitend badge)
- [ ] Click again for Level 3
- [ ] Verify Level 3 hint (Spezifisch)

### 1.3 Smart Visual Hint
- [ ] Click "💡 Visuelle Hilfe" on a subtask
- [ ] Verify loading message appears
- [ ] Verify graph/animation/key facts display

### 1.4 Approach Checker
- [ ] Click "✓ Meinen Ansatz prüfen"
- [ ] Enter approach text
- [ ] Click "✓ Ansatz überprüfen"
- [ ] Verify feedback appears (no solution revealed)

---

## Test 2: New Assessment Modal Fields

### 2.1 Open Assessment Modal
- [ ] Click "📊 Open Assessment Modal" (debug button)
- [ ] Verify modal opens

### 2.2 Required Fields
- [ ] **Student-ID:** Enter "S001" (required)
- [ ] **AI Question Quality:** Select rating (1-5)
- [ ] **Engagement Level:** Select rating (1-5)
- [ ] **Understanding Progress:** Select rating (1-5)
- [ ] **Efficiency Score:** Select rating (1-5)

### 2.3 New Fields
- [ ] **Grade:** Enter "10a"
- [ ] **Tutor Interventions:** Enter "2"
- [ ] **Student Override:** Check checkbox
- [ ] **Linguistic Neutrality Check:** Check checkbox
- [ ] **Evaluative Language Check:** Check checkbox
- [ ] **Student Feedback Safety:** Select "Yes"
- [ ] **Prompt Strategy:** Enter "Sokratische Fragen verwendet"

### 2.4 Auto-Populated Metrics
- [ ] Verify "Visuelle Hilfen" shows correct count
- [ ] Verify "Hilfestellungen gesamt" shows correct count
- [ ] Verify "Ansatzprüfungen" shows correct count
- [ ] Verify "Selbstständigkeit" shows stars (1-5)

### 2.5 Validation Test
- [ ] Try submitting without Student-ID → Should show error
- [ ] Try submitting without all ratings → Should show error
- [ ] Fill all required fields → Should submit successfully

### 2.6 Submit Assessment
- [ ] Click "📊 Bewertung speichern"
- [ ] Verify success toast appears
- [ ] Verify modal closes

---

## Test 3: Session Logging

### 3.1 Open Session Form
- [ ] Click "📝 Open Session Form" (debug button)
- [ ] Verify form opens

### 3.2 Fill Session Form
- [ ] **Benutzer Name:** "Max Mustermann"
- [ ] **Klasse:** "10a"
- [ ] **Schule:** "Gymnasium Beispiel"
- [ ] **Fach:** "Mathematik"
- [ ] **Thema:** "Quadratische Gleichungen"
- [ ] **Schwierigkeitsgrad:** "Mittel"

### 3.3 Verify Usage Statistics
- [ ] Verify "Visualisierungen" count matches
- [ ] Verify "Animationen" count matches
- [ ] Verify "Grafiken" count matches
- [ ] Verify "Hilfestellungen" count matches
- [ ] Verify "Ansatzprüfungen" count matches
- [ ] Verify "Selbstständigkeit" shows stars

### 3.4 Submit Session
- [ ] Click "📊 Sitzung protokollieren"
- [ ] Verify success toast with Session-ID
- [ ] Note the Session-ID (e.g., "20250112-001")

---

## Test 4: Excel Export Verification

### 4.1 Open Excel File
- [ ] Open `Clarity_Coach_Session_Log.xlsx`
- [ ] Check `Session_Log` sheet

### 4.2 Verify Session_Log
- [ ] Verify date format is `DD.MM.YYYY` (e.g., "12.01.2025")
- [ ] Verify all session data present
- [ ] Note Session-ID

### 4.3 Check Assessment_Log Sheet
- [ ] Switch to `Assessment_Log` sheet
- [ ] Verify **21 columns** present:
  1. Session-ID ✅
  2. Date (DD.MM.YYYY) ✅
  3. Student-ID ✅
  4. Grade ✅
  5. Topic Area ✅
  6. Topic Detail ✅
  7. Topic Complexity (1-5) ✅
  8. AI Question Quality (1-5) ✅
  9. Prompt Strategy ✅
  10. Tutor Interventions ✅
  11. Student Override (Yes/No) ✅
  12. Learner Type Indicator ✅
  13. Understanding Progress (1-5) ✅
  14. Linguistic Neutrality Check (Yes/No) ✅
  15. Engagement Level (1-5) ✅
  16. Evaluative Language Check (Yes/No) ✅
  17. Student Feedback Safety (Yes/No/Unclear) ✅
  18. Question Loops ✅
  19. Efficiency Score (1-5) ✅
  20. Remarks ✅
  21. Further Considerations ✅

### 4.4 Verify Data Integrity
- [ ] Verify Session-ID matches between Session_Log and Assessment_Log
- [ ] Verify Topic Area/Detail/Complexity joined from Session_Log
- [ ] Verify date format is DD.MM.YYYY
- [ ] Verify boolean values are "Yes"/"No"
- [ ] Verify all entered data is present

---

## Test 5: Data Validation

### 5.1 Duplicate Prevention
- [ ] Try submitting assessment for same Session-ID again
- [ ] Should show error: "Assessment for session X already exists"

### 5.2 Scale Validation
- [ ] Try submitting with rating > 5 (if possible)
- [ ] Should show validation error

### 5.3 Required Fields
- [ ] Try submitting without Student-ID
- [ ] Should show validation error

---

## Test 6: Session Tracking Enhancement

### 6.1 Verify Hint Level Tracking
- [ ] Use Level 1 hint → Check `socraticHintsUsed` increments
- [ ] Use Level 2 hint → Check `directiveHintsUsed` increments
- [ ] Use Level 3 hint → Check `specificHintsUsed` increments

### 6.2 Verify Approach Check Results
- [ ] Use approach checker multiple times
- [ ] Verify `approachCheckResults` array tracks results

---

## Test 7: Dashboard (Optional - Component Created)

### 7.1 Dashboard Component
- [ ] Component exists: `AssessmentDashboard.vue`
- [ ] Can be imported (if route added)

---

## Expected Results

### ✅ All Tests Should Pass:
1. Existing features work (no regression)
2. All 21 assessment fields present
3. Auto-populated metrics display correctly
4. Excel export has 21 columns
5. Date format is DD.MM.YYYY
6. Data validation works
7. Duplicate prevention works
8. Session tracking enhanced

---

## Issues Found

Document any issues here:
- [ ] Issue 1: ...
- [ ] Issue 2: ...

---

## Test Completion

- [ ] All tests completed
- [ ] All issues documented
- [ ] Excel file verified
- [ ] Ready for production

---

**Test Date:** _______________  
**Tester:** _______________  
**Status:** ⏳ In Progress / ✅ Complete
