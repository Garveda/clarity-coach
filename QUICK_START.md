# Clarity Coach - Quick Start Guide

## 🚀 Starting the Application

### Step 1: Start Backend
```bash
cd clarity-coach-main/backend
../backend/venv/Scripts/activate
uvicorn main:app --reload
```
✅ Backend running on: http://127.0.0.1:8000

### Step 2: Start Frontend
```bash
cd clarity-coach-main
npm run dev
```
✅ Frontend running on: http://localhost:5173/

---

## 📱 Using the Application

### 1. Upload a Document
- Click the upload area or drag & drop
- **Supported formats:** PDF, JPG, PNG
- **Max size:** 12 MB

### 2. Three Action Buttons Per Subtask

#### 🟣 Visualisierung anzeigen (Purple)
**Shows:** Key facts, concepts, formulas, and approach hints
- Given information
- What we're looking for
- Relevant formulas
- Strategic hints

#### 🔴 Animation erstellen (Pink)
**Shows:** Interactive step-by-step animation
- Automatic playback
- Smooth GSAP animations
- Beautiful KaTeX math rendering
- Replay button available

#### 🔵 Lösung anzeigen (Blue)
**Shows:** Complete solution
- Step-by-step working
- Full mathematical proof
- LaTeX-formatted equations

---

## 🎨 Features

### Visualizations
- Structured key facts
- Bullet points with LaTeX
- Organized sections
- No solution spoilers

### Animations
- **Instant rendering** (no waiting!)
- **Animation types:**
  - fadeIn - Smooth appearance
  - scale - Growing/shrinking
  - bounce - Bouncing effect
  - highlight - Yellow flash
  - transform - Rotation + scale
- **Interactive:** Replay anytime
- **Professional:** GSAP-powered

### Solutions
- Complete step-by-step
- Mathematical proofs
- LaTeX equations
- Explanations in German

---

## 🔧 Technical Stack

### Frontend
- Vue 3
- Vite
- GSAP (animations)
- KaTeX (math rendering)
- vue-sonner (toasts)

### Backend
- FastAPI
- OpenAI GPT-4o-mini
- PyMuPDF (PDF processing)
- Python 3.14

---

## 📊 Current Status

✅ Backend: Running on port 8000  
✅ Frontend: Running on port 5173  
✅ All features: Working  
✅ No installation required: Browser-based animations  

---

## 🐛 Troubleshooting

### Backend not starting?
```bash
cd clarity-coach-main/backend
pip install -r requirements.txt
```

### Frontend not starting?
```bash
cd clarity-coach-main
npm install
```

### Animations not showing?
- Check browser console for errors
- Ensure GSAP is installed: `npm list gsap`
- Clear browser cache and reload

### Upload failing?
- Check file size (max 12 MB)
- Ensure file format is PDF, JPG, or PNG
- Check backend console for errors

---

## 💡 Tips

1. **Upload Quality:** Higher resolution images = better text recognition
2. **File Format:** PDF works best for multiple pages
3. **Replay:** Use the replay button to watch animations again
4. **Copy LaTeX:** Right-click equations to copy LaTeX code
5. **Feedback:** Use the "Hilfreich" / "Noch unklar" buttons

---

## 📝 Environment

- **OS:** Windows 10
- **Python:** 3.14
- **Node.js:** Latest
- **Browsers:** Chrome, Firefox, Edge, Safari

---

## 🎯 Next Steps

1. ✅ Start both servers
2. ✅ Open http://localhost:5173/
3. ✅ Upload a math problem
4. ✅ Try all three buttons!
5. ✅ Enjoy the animations!

---

**Need help?** Check the CHANGELOG.md for detailed changes.





