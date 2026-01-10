# Clarity Coach - Quick Reference Card

**Version:** 2.0 | **Date:** Jan 10, 2026 | **Status:** ✅ Ready

---

## 🚀 **Start Commands**

### Backend:
```bash
cd clarity-coach-main/backend
.\venv\Scripts\Activate.ps1
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### Frontend:
```bash
cd clarity-coach-main
npm run dev
```

### Access:
- **Frontend:** http://localhost:5173/
- **Backend:** http://127.0.0.1:8000
- **Health Check:** http://127.0.0.1:8000/health

---

## 🎯 **Four Buttons**

| Button | Color | Function | Time |
|--------|-------|----------|------|
| **Visualisierung anzeigen** | 🟣 Purple | Key facts & concepts | 3-6s |
| **Animation erstellen** | 🩷 Pink | Step-by-step animation | 10-15s |
| **Grafik erstellen** | 🟢 Green | Interactive graph | 5-10s |
| **Lösung anzeigen** | 🔵 Blue | Complete solution | 3-6s |

---

## 📊 **Supported Files**

- **Text:** .txt
- **PDF:** .pdf (max 12 MB)
- **Images:** .jpg, .jpeg, .png

**Processing Time:** 5-30 seconds depending on file type

---

## ⚡ **Quick Troubleshooting**

### Upload Hanging?
1. Check backend terminal for `[ERROR]` messages
2. Verify OpenAI API key in `backend/.env`
3. Try with simple `test.txt` file first
4. Check browser console (F12) for errors

### Backend Not Starting?
```bash
cd backend
.\venv\Scripts\pip install -r requirements.txt
```

### Frontend Not Starting?
```bash
npm install
npm run dev
```

### Graph Showing "Not Applicable"?
- This is normal for abstract tasks (e.g., "f'(x) = 0")
- Graph only works for concrete functions (e.g., "x² - 4")

---

## 📁 **Key Files**

| File | Purpose |
|------|---------|
| `backend/main.py` | All backend logic |
| `src/components/ClarityCoach.vue` | All frontend logic |
| `backend/.env` | OpenAI API key (keep secret!) |
| `COMPLETE_SUMMARY.md` | Full documentation |
| `CHANGELOG.md` | All changes made |

---

## 🎨 **Design Theme**

- **Primary:** #1e3a5f (Navy)
- **Secondary:** #2c5f8d (Blue)
- **Accent:** #3b82f6 (Bright Blue)
- **Success:** #10b981 (Green)
- **Language:** German
- **Style:** Professional & Clean

---

## 🔧 **Tech Stack**

**Backend:** FastAPI + OpenAI GPT-4o-mini + Plotly  
**Frontend:** Vue 3 + Vite + KaTeX + GSAP + Plotly.js  
**Math:** KaTeX for rendering, LaTeX syntax  
**Graphs:** Plotly (backend) → Plotly.js (frontend)

---

## ✅ **Feature Checklist**

- [x] Upload (PDF/Image/Text)
- [x] Task Analysis with German output
- [x] Socratic Questions (cycleable)
- [x] Visualizations (structured facts)
- [x] Animations (GSAP-based)
- [x] Graphs (Plotly interactive)
- [x] Solutions (LaTeX formatted)
- [x] Feedback buttons
- [x] Professional design
- [x] Error handling
- [x] Timeout protection (120s)

---

## 📞 **Emergency Fixes**

### Restart Everything:
```bash
# Stop all (Ctrl+C in terminals)
# Then:
cd clarity-coach-main/backend
.\venv\Scripts\python.exe -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
# New terminal:
cd clarity-coach-main
npm run dev
```

### Reset Application:
1. Close browsers
2. Stop servers (Ctrl+C)
3. Restart servers
4. Open fresh browser window
5. Clear browser cache if needed (Ctrl+Shift+Del)

---

## 🎓 **Example Test**

**Create `test.txt`:**
```
Aufgabe 1: Löse x^2 = 4
```

**Expected:**
- Analysis completes in ~5 seconds
- Shows "Quadratische Gleichungen"
- Socratic questions about the equation
- All 4 buttons work:
  - Visualization shows key facts
  - Animation shows step-by-step
  - Graph shows parabola with nullstellen
  - Solution shows x = ±2

---

**For more details, see `COMPLETE_SUMMARY.md`** 📚
