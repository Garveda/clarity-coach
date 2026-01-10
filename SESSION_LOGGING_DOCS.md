# 📊 Session Logging System Documentation

**Version:** 1.0  
**Date:** January 10, 2026  
**Feature:** Automatic Excel logging of Clarity Coach sessions

---

## 🎯 **Overview**

The Session Logging System automatically tracks and records every Clarity Coach usage session in an Excel file (`Clarity_Coach_Session_Log.xlsx`). This provides valuable analytics and tracking capabilities for educational monitoring.

---

## 📋 **Excel Structure**

### **File Location:**
```
C:\Users\admin\Desktop\Sonstiges\HMS_PROJEKT\clarity-coach\Clarity_Coach_Session_Log.xlsx
```

### **Sheet Name:**
`Session_Log`

### **Column Structure (21 columns):**

| Column | Field Name | Type | Description |
|--------|------------|------|-------------|
| A | Session_ID | Auto | Format: YYYYMMDD-### (e.g., "20260110-001") |
| B | Datum | Auto | Date of session (YYYY-MM-DD) |
| C | Uhrzeit | Auto | Time of session (HH:MM:SS) |
| D | Benutzer_Name | **Required** | Student's name |
| E | Klasse | **Required** | Class (e.g., "10a") |
| F | Schule | **Required** | School name |
| G | Fach | **Required** | Subject (Mathematik, Physik, etc.) |
| H | Thema | **Required** | Topic (e.g., "Quadratische Gleichungen") |
| I | Aufgabentyp | Optional | Type of task |
| J | Schwierigkeitsgrad | **Required** | Difficulty (Leicht/Mittel/Anspruchsvoll) |
| K | Datei_Name | Auto | Uploaded file name |
| L | Datei_Typ | Auto | File type (PDF/JPG/PNG/TXT) |
| M | Anzahl_Aufgaben | Auto | Number of main tasks |
| N | Anzahl_Teilaufgaben | Auto | Total number of subtasks |
| O | Visualisierungen_Genutzt | Auto | Count of visualizations used |
| P | Animationen_Genutzt | Auto | Count of animations used |
| Q | Grafiken_Genutzt | Auto | Count of graphs created |
| R | Lösungen_Angezeigt | Auto | Count of solutions viewed |
| S | Feedback | Optional | User feedback (Helpful/Needs Clarification) |
| T | Sitzungsdauer_Minuten | Auto | Session duration in minutes |
| U | Notizen | Optional | Additional notes |

---

## 🚀 **How It Works**

### **1. Session Start**
- User uploads a file (PDF, image, or text)
- File name and type are automatically captured
- Session timer starts

### **2. During Session**
- User interacts with tasks (visualizations, animations, graphs, solutions)
- Each button click is automatically tracked
- Usage statistics are updated in real-time

### **3. Session End (Form Appears)**
- After file analysis completes, a form automatically pops up
- User fills in required information:
  - Personal info (name, class, school)
  - Subject and topic
  - Difficulty level
  - Optional notes
- Pre-filled automatically:
  - File name and type
  - Task counts
  - Button usage statistics
  - Session duration

### **4. Data Saved to Excel**
- On form submission, data is sent to backend
- Backend appends new row to Excel file
- Unique Session ID is generated
- User receives confirmation toast

---

## 🎨 **User Interface**

### **Session Form (Modal)**

The form appears automatically after file analysis and includes:

#### **Section 1: Personal Information**
- Benutzer Name (required)
- Klasse (required)
- Schule (required)
- Fach (required dropdown)
  - Mathematik
  - Physik
  - Chemie
  - Biologie
  - Informatik
  - Sonstiges

#### **Section 2: Task Information**
- Thema (required)
- Aufgabentyp (optional)
- Schwierigkeitsgrad (required dropdown)
  - Leicht
  - Mittel
  - Anspruchsvoll
- Feedback (optional dropdown)
  - Helpful
  - Needs Clarification
  - Keine Angabe

#### **Section 3: Additional Information**
- Notizen (optional textarea)

#### **Actions**
- **Abbrechen** button: Close form without saving
- **Sitzung protokollieren** button: Submit and save to Excel

---

## 🔧 **Technical Implementation**

### **Backend Components**

#### **1. Excel Template Creator**
**File:** `backend/create_excel_template.py`

Creates the initial Excel file with:
- Styled header row (navy blue background, white text)
- Proper column widths
- Freeze panes on first row
- Border styling
- Example data row

**Usage:**
```bash
cd backend
.\venv\Scripts\python.exe create_excel_template.py
```

#### **2. Session Logging Endpoint**
**Endpoint:** `POST /log-session`  
**File:** `backend/main.py`

**Request Body:**
```json
{
  "benutzer_name": "Max Mustermann",
  "klasse": "10a",
  "schule": "Gymnasium Beispiel",
  "fach": "Mathematik",
  "thema": "Quadratische Gleichungen",
  "aufgabentyp": "Gleichungen lösen",
  "schwierigkeitsgrad": "Mittel",
  "datei_name": "aufgabe.pdf",
  "datei_typ": "PDF",
  "anzahl_aufgaben": 1,
  "anzahl_teilaufgaben": 3,
  "visualisierungen_genutzt": 2,
  "animationen_genutzt": 1,
  "grafiken_genutzt": 0,
  "loesungen_angezeigt": 3,
  "feedback": "Helpful",
  "sitzungsdauer_minuten": 15.5,
  "notizen": "Gute Fortschritte"
}
```

**Response:**
```json
{
  "success": true,
  "session_id": "20260110-001",
  "message": "Session erfolgreich protokolliert",
  "row": 2
}
```

#### **3. Dependencies Added**
```txt
openpyxl  # Excel file manipulation
```

---

### **Frontend Components**

#### **1. SessionForm Component**
**File:** `src/components/SessionForm.vue`

**Features:**
- Professional modal design
- Form validation
- Real-time duration calculation
- Automatic pre-filling of usage stats
- Toast notifications for success/error

**Props:**
- `isOpen` (Boolean): Controls modal visibility
- `fileName` (String): Uploaded file name
- `fileType` (String): File extension
- `taskCount` (Number): Number of main tasks
- `subtaskCount` (Number): Total subtasks

**Events:**
- `@close`: Emitted when form is closed
- `@submitted`: Emitted with result data after successful submission

**Methods:**
- `updateUsageStats(stats)`: Updates visualization/animation/graph/solution counts

#### **2. ClarityCoach Integration**
**File:** `src/components/ClarityCoach.vue`

**Changes:**
1. Added SessionForm import
2. Added session tracking refs:
   ```javascript
   const showSessionForm = ref(false)
   const uploadedFileName = ref('')
   const uploadedFileType = ref('')
   const usageStats = ref({
     visualizations: 0,
     animations: 0,
     graphs: 0,
     solutions: 0
   })
   ```

3. Updated toggle functions to track usage:
   - `toggleSolution()` → increments `usageStats.solutions`
   - `toggleVisualization()` → increments `usageStats.visualizations`
   - `toggleAnimation()` → increments `usageStats.animations`
   - `toggleGraph()` → increments `usageStats.graphs`

4. Show form after analysis:
   ```javascript
   function handleAnalysisResult(data) {
     // ... existing code ...
     showSessionForm.value = true  // Show form
   }
   ```

#### **3. FileUpload Component Update**
**File:** `src/components/FileUpload.vue`

**Changes:**
- Emits file information with `analysis-started` event:
  ```javascript
  emit('analysis-started', {
    fileName: file.name,
    fileType: file.extension
  })
  ```

---

## 📊 **Data Flow**

```
1. User uploads file
   ↓
2. FileUpload captures file info
   ↓
3. ClarityCoach stores file info & starts tracking
   ↓
4. User interacts with buttons (tracked automatically)
   ↓
5. Analysis complete → SessionForm modal appears
   ↓
6. User fills form (pre-filled with auto data)
   ↓
7. Submit → POST /log-session
   ↓
8. Backend writes to Excel
   ↓
9. Success toast shown
```

---

## 🔐 **Security & Error Handling**

### **Backend**
- ✅ Validates Excel file existence
- ✅ Validates Session_Log sheet existence
- ✅ Proper error messages via HTTPException
- ✅ File locking handled by openpyxl
- ✅ Automatic workbook closing

### **Frontend**
- ✅ Form validation (required fields)
- ✅ Network error handling
- ✅ Clear user feedback via toasts
- ✅ Modal can be closed without saving
- ✅ Data persists during session

---

## 📈 **Usage Analytics**

The Excel file enables tracking:

### **Student Analytics**
- Session frequency per student
- Average session duration
- Preferred difficulty levels
- Topic proficiency

### **Content Analytics**
- Most common topics
- Feature usage (visualizations vs solutions)
- Task complexity distribution
- File type preferences

### **Performance Analytics**
- Average completion times
- Feedback trends
- Success rates by difficulty

---

## 🛠️ **Setup Instructions**

### **1. Install Dependencies**
```bash
cd backend
.\venv\Scripts\pip install -r requirements.txt
```

### **2. Create Excel Template**
```bash
cd backend
.\venv\Scripts\python.exe create_excel_template.py
```

This creates:
```
C:\Users\admin\Desktop\Sonstiges\HMS_PROJEKT\clarity-coach\Clarity_Coach_Session_Log.xlsx
```

### **3. Restart Servers**
```bash
# Backend
cd backend
.\venv\Scripts\python.exe -m uvicorn main:app --reload

# Frontend
cd ..
npm run dev
```

### **4. Test**
1. Upload a file
2. Wait for analysis
3. Form appears automatically
4. Fill in required fields
5. Click "Sitzung protokollieren"
6. Check Excel file for new entry

---

## 🐛 **Troubleshooting**

### **Error: "Excel file not found"**
**Solution:** Run `create_excel_template.py` to create the file

### **Error: "Session_Log sheet not found"**
**Solution:** Re-run `create_excel_template.py` or manually create sheet

### **Error: "Permission denied"**
**Solution:** Close Excel file if it's open

### **Form doesn't appear**
**Solution:** Check browser console for errors, ensure backend is running

### **Data not saving**
**Solution:** Check backend terminal for errors, verify Excel file path

---

## 📝 **Example Session Entry**

```
Session_ID: 20260110-001
Datum: 2026-01-10
Uhrzeit: 14:30:15
Benutzer_Name: Max Mustermann
Klasse: 10a
Schule: Gymnasium Beispiel
Fach: Mathematik
Thema: Quadratische Gleichungen
Aufgabentyp: Gleichungen lösen
Schwierigkeitsgrad: Mittel
Datei_Name: aufgabe_quadratisch.pdf
Datei_Typ: PDF
Anzahl_Aufgaben: 1
Anzahl_Teilaufgaben: 3
Visualisierungen_Genutzt: 2
Animationen_Genutzt: 1
Grafiken_Genutzt: 0
Lösungen_Angezeigt: 3
Feedback: Helpful
Sitzungsdauer_Minuten: 15.5
Notizen: Gute Fortschritte beim Verständnis
```

---

## 🎯 **Benefits**

1. **Automatic Tracking** - No manual data entry required
2. **Comprehensive Data** - Captures all session details
3. **Easy Analysis** - Excel format for easy data analysis
4. **Educational Insights** - Track student progress and engagement
5. **Professional** - Clean, organized, standardized format
6. **Privacy-Conscious** - Data stored locally, not in cloud

---

## 🚀 **Future Enhancements**

Potential improvements:
- Export to CSV for data analysis
- Dashboard for visualizing statistics
- Automatic weekly/monthly reports
- Integration with learning management systems (LMS)
- Cloud backup option
- Multi-user support with authentication
- Advanced analytics (charts, trends)

---

## ✅ **System Status**

- ✅ Excel template created
- ✅ Backend endpoint implemented
- ✅ Frontend form designed
- ✅ Integration complete
- ✅ Automatic tracking enabled
- ✅ Error handling implemented
- ✅ Documentation complete

**Status:** Ready for use! 🎉

---

**For questions or issues, check the troubleshooting section or review the backend terminal logs.**
