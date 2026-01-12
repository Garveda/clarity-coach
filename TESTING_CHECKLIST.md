# 🧪 Phase 1 Testing Checklist

**Date:** January 12, 2026  
**Servers Running:** ✅ Both active  
**Tester:** Attila  

---

## ✅ Pre-Test Setup

- [x] Backend running on http://127.0.0.1:8000
- [x] Frontend running on http://localhost:5173/
- [ ] Excel file backed up (recommended)
- [ ] Browser: Chrome/Edge (recommended)
- [ ] Test file ready (math problem PDF/image)

---

## 🧪 Test 1: Complete Happy Path (Core Flow)

**Goal:** Test entire assessment flow from upload to Excel export

### Steps:

**1.1 Open Application**
- [ ] Go to http://localhost:5173/
- [ ] Page loads without errors
- [ ] "Clarity Coach" header visible
- [ ] Upload area visible

**1.2 Upload File**
- [ ] Click upload area or drag file
- [ ] Select test file (PDF or image with math problem)
- [ ] "Processing analysis..." appears
- [ ] Wait for analysis (30-60 seconds)

**Expected:** No errors in browser console (F12)

---

**1.3 Interact with Questions** ⭐ **NEW FEATURE**
- [ ] Results appear with tasks and subtasks
- [ ] Socratic questions visible
- [ ] Click "↻" refresh button on **first subtask** → **5 times**
- [ ] Toast shows "Loops: 5" in description
- [ ] Click "↻" refresh button on **second subtask** → **3 times**
- [ ] Toast shows "Loops: 3" in description
- [ ] Use at least one visualization (purple button)
- [ ] Use at least one solution (blue button)

**Expected Total Loops:** 8 (5 + 3)

**Check Console:** Any errors? (F12 → Console tab)

---

**1.4 Session Form Appears**
- [ ] Session Form modal opens automatically
- [ ] Fill out:
  - **Benutzer Name:** "Test Student"
  - **Klasse:** "10a"
  - **Schule:** "Test Gymnasium"
  - **Fach:** "Mathematik"
  - **Thema:** "Kubische Gleichungen"
  - **Aufgabentyp:** "Gleichung lösen"
  - **Schwierigkeitsgrad:** "Mittel"
  - **Feedback:** "Good test session"
- [ ] Click "📊 Sitzung protokollieren"
- [ ] Success toast appears
- [ ] Form closes

**Expected:** Session-ID generated (e.g., "20260112-001")

---

**1.5 Assessment Modal Appears** ⭐ **NEW FEATURE**
- [ ] **Wait 2 seconds after Session Form closes**
- [ ] Assessment Modal opens automatically! 🎉
- [ ] Modal title: "📊 Sitzungsbewertung"
- [ ] Session-ID displayed at top
- [ ] **Automatic Metrics Section shows:**
  - Fragenzyklen: **8** (should match our clicks!)
  - Session-ID: (e.g., "20260112-001")

**If modal doesn't appear:**
- Check browser console for errors
- Check backend terminal for errors

---

**1.6 Fill Out Assessment** ⭐ **NEW FEATURE**
- [ ] **Ihr Name:** "Prof. Test"
- [ ] **KI-Fragenqualität:** Click **4**
- [ ] **Engagement-Level:** Click **3**
- [ ] **Verständnisfortschritt:** Click **4**
- [ ] **Effizienz-Score:** Click **3**
- [ ] **Lerntyp:** Select "Visuell"
- [ ] **Bemerkungen:** "Excellent interaction, student was engaged"
- [ ] **Weitere Überlegungen:** "Recommend more visual tasks"

**Test Validation:**
- [ ] Try clicking "Bewertung speichern" without ratings
- [ ] Red error should appear: "Bitte füllen Sie alle Pflichtfelder aus"
- [ ] Now fill all ratings (as above)
- [ ] Click "📊 Bewertung speichern"

**Expected:**
- [ ] Success toast: "Bewertung erfolgreich gespeichert!"
- [ ] Modal closes after ~0.5 seconds
- [ ] No errors in console

---

**1.7 Verify Excel Export** ⭐ **CRITICAL CHECK**
- [ ] Open `Clarity_Coach_Session_Log.xlsx`
- [ ] **Check Sheet Tabs at Bottom:**
  - [ ] "Session_Log" sheet exists (old)
  - [ ] "Assessment_Log" sheet exists ⭐ **NEW!**

**1.8 Check Session_Log Sheet (Technical Data)**
- [ ] Switch to "Session_Log" sheet
- [ ] Find your session (should be last row)
- [ ] Verify data:
  - Session-ID: (e.g., "20260112-001")
  - Date: Today's date
  - Benutzer Name: "Test Student"
  - Klasse: "10a"
  - Thema: "Kubische Gleichungen"
  - Visualisierungen genutzt: ≥1
  - Lösungen angezeigt: ≥1
  - Session Dauer: >0 seconds
  - Feedback: "Good test session"

**1.9 Check Assessment_Log Sheet** ⭐ **NEW FEATURE**
- [ ] Switch to "Assessment_Log" sheet
- [ ] **Check Header Row:**
  - Blue background
  - White text
  - Columns: Session-ID, Assessment Date, Assessment Time, Assessor Name, AI Question Quality, Engagement Level, Understanding Progress, Efficiency Score, Learner Type Indicator, Question Loops Total, Remarks, Further Considerations, Completion Status

- [ ] **Check Your Assessment (Last Row):**
  - Session-ID: **Matches Session_Log** ✅ (e.g., "20260112-001")
  - Assessment Date: Today
  - Assessment Time: Recent time
  - Assessor Name: "Prof. Test"
  - AI Question Quality: 4
  - Engagement Level: 3
  - Understanding Progress: 4
  - Efficiency Score: 3
  - Learner Type Indicator: "Visuell"
  - Question Loops Total: **8** ✅
  - Remarks: "Excellent interaction..."
  - Further Considerations: "Recommend more..."
  - Completion Status: "Complete"

**✅ CRITICAL:** Session-ID in Assessment_Log **MUST MATCH** Session-ID in Session_Log!

---

### ✅ Test 1 Results:

- [ ] **Pass** - All steps worked perfectly
- [ ] **Partial Pass** - Minor issues (note below)
- [ ] **Fail** - Major issues (describe below)

**Notes/Issues:**
```
(Write any issues, bugs, or observations here)




```

---

## 🧪 Test 2: Question Loop Accuracy

**Goal:** Verify question loop counting is accurate

### Steps:

**2.1 Fresh Session**
- [ ] Refresh browser (Ctrl+F5)
- [ ] Upload new file
- [ ] Wait for analysis

**2.2 Controlled Clicking**
- [ ] On **Subtask 1:** Click "↻" exactly **7 times**
- [ ] Count manually: 1, 2, 3, 4, 5, 6, 7
- [ ] Check toast: "Loops: 7"
- [ ] On **Subtask 2:** Click "↻" exactly **3 times**
- [ ] Check toast: "Loops: 3"

**2.3 Submit**
- [ ] Fill Session Form → Submit
- [ ] Wait for Assessment Modal
- [ ] **Check "Fragenzyklen":** Should show **10** (7+3)

**2.4 Verify Excel**
- [ ] Submit assessment
- [ ] Check Assessment_Log
- [ ] Question Loops Total: **10** ✅

### ✅ Test 2 Results:

- [ ] **Pass** - Count is accurate
- [ ] **Fail** - Count is wrong (expected:__ actual:__)

**Notes:**
```




```

---

## 🧪 Test 3: Skip Assessment

**Goal:** Test skip functionality

### Steps:

**3.1 Start Session**
- [ ] Upload file
- [ ] Wait for analysis
- [ ] Fill Session Form → Submit

**3.2 Skip Assessment**
- [ ] Assessment Modal opens
- [ ] Click "Überspringen" button
- [ ] Confirmation dialog appears: "Möchten Sie die Bewertung wirklich überspringen?"
- [ ] Click "OK" to confirm
- [ ] Toast: "Bewertung übersprungen"
- [ ] Modal closes

**3.3 Verify Excel**
- [ ] Open Excel file
- [ ] Check Session_Log: Entry exists ✅
- [ ] Check Assessment_Log: **NO new entry** ✅

### ✅ Test 3 Results:

- [ ] **Pass** - Skip worked, no assessment entry
- [ ] **Fail** - Assessment was saved despite skip

**Notes:**
```




```

---

## 🧪 Test 4: Validation

**Goal:** Test form validation

### Steps:

**4.1 Empty Submission**
- [ ] Assessment Modal opens
- [ ] Leave ALL ratings empty
- [ ] Click "Bewertung speichern"
- [ ] **Expected:**
  - Red error box appears
  - Toast error: "Bitte füllen Sie alle Pflichtfelder aus"
  - Modal stays open
  - No data saved

**4.2 Partial Fill**
- [ ] Fill only 2 ratings (e.g., quality=4, engagement=3)
- [ ] Leave understanding and efficiency empty
- [ ] Try to submit
- [ ] **Expected:** Same validation error

**4.3 Complete Fill**
- [ ] Fill all 4 ratings
- [ ] Leave optional fields empty (assessor, learner type, remarks)
- [ ] Submit
- [ ] **Expected:** Success! (Optional fields are truly optional)

### ✅ Test 4 Results:

- [ ] **Pass** - Validation works correctly
- [ ] **Fail** - Validation doesn't work

**Notes:**
```




```

---

## 🧪 Test 5: UI/UX Experience

**Goal:** Evaluate user experience

### Questions:

**Timing:**
- [ ] Is the 2-second delay before Assessment Modal good?
- [ ] Too fast? Too slow? Just right?

**Assessment Modal:**
- [ ] Is the modal easy to read and understand?
- [ ] Are the rating scales intuitive (1-5)?
- [ ] Are the tooltips helpful?
- [ ] Is the "Fragenzyklen" auto-fill clear?

**Question Loop Tracking:**
- [ ] Is the loop count in toast messages helpful or distracting?
- [ ] Should it show current count differently?

**Excel Output:**
- [ ] Is the Assessment_Log sheet professional looking?
- [ ] Are column widths appropriate?
- [ ] Is the data easy to read?

**Workflow:**
- [ ] Is the two-form approach (Session → Assessment) intuitive?
- [ ] Should they be combined into one form?
- [ ] Is anything confusing?

### ✅ Test 5 Feedback:

**Positive:**
```
(What worked well?)




```

**Needs Improvement:**
```
(What could be better?)




```

**Suggestions:**
```
(Any ideas for refinement?)




```

---

## 🧪 Test 6: Edge Cases

**Goal:** Test unusual scenarios

### 6.1 Very Long Text
- [ ] Fill remarks with 300+ characters
- [ ] Submit
- [ ] Check Excel: Text wraps correctly?

### 6.2 Many Loops
- [ ] Click "↻" 50+ times
- [ ] Check if tracking handles large numbers

### 6.3 No Interactions
- [ ] Upload file
- [ ] Don't click any refresh buttons (0 loops)
- [ ] Submit session and assessment
- [ ] Question Loops should be **0** ✅

### 6.4 Close Modal Accidentally
- [ ] Assessment Modal opens
- [ ] Fill some data
- [ ] Click X or click outside modal
- [ ] Confirmation dialog appears?
- [ ] If yes, click OK to close
- [ ] Data is lost (expected, no draft save yet)

### ✅ Test 6 Results:

**Issues Found:**
```
(Describe any problems with edge cases)




```

---

## 📊 Overall Assessment

### What Works Well ✅

```
(List everything that worked perfectly)




```

### Issues Found 🐛

```
(List any bugs or problems)




```

### Suggested Improvements 💡

```
(List any desired refinements or changes)




```

---

## 🎯 Final Decision

After testing Phase 1, I want to:

- [ ] **Proceed to Phase 2** - Phase 1 works well, ready for more features
- [ ] **Refine Phase 1** - Need adjustments before continuing
- [ ] **Production Use** - Phase 1 is sufficient for my needs

**Specific requests for next steps:**
```
(What would you like to happen next?)




```

---

## 📸 Screenshots (Optional)

If you encountered issues, screenshots help:
- Assessment Modal
- Excel sheets
- Browser console errors
- Backend terminal errors

---

**Testing Started:** ____________  
**Testing Completed:** ____________  
**Total Time:** ____________  
**Overall Result:** ☐ Pass | ☐ Partial | ☐ Fail

---

**Thank you for testing Phase 1!** 🎉

Your feedback will help us decide whether to:
1. Move to Phase 2 (Bias Detection + Interventions)
2. Refine Phase 1 based on your feedback
3. Consider Phase 1 complete for your needs
