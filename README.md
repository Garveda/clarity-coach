# 🎓 Clarity Coach - Sokratisches Mathematik-Lernsystem

**Version:** 3.0 (UI/UX Optimization Complete)  
**Status:** ✅ **Production Ready**  
**Letzte Aktualisierung:** 12. Januar 2026

---

## 🌟 **Was ist Clarity Coach?**

Clarity Coach ist eine KI-gestützte Mathematik-Lernplattform, die auf der **sokratischen Methode** basiert. Anstatt direkte Lösungen zu zeigen, führt das System Schüler durch gezielte Fragen und progressive Hilfestellungen zu eigenständigem Verständnis.

### Kernphilosophie

> *"Ich kann niemandem etwas beibringen, ich kann ihn nur zum Denken anregen."* - Sokrates

---

## 🆕 **Version 3.0 - Was ist neu?**

### Entfernt (Anti-Patterns)
- ❌ **Lösungs-Button entfernt** - Direkte Lösungen widersprechen dem sokratischen Ansatz

### Neue Features
- ✅ **3-Stufen-Hilfestellungen** - Sokratisch → Anleitend → Spezifisch
- ✅ **Smart Visual Hint** - KI wählt beste Visualisierung automatisch
- ✅ **Ansatz-Prüfung** - Feedback ohne Lösung zu verraten
- ✅ **Selbstständigkeits-Score** - Tracking der Lernautonomie (1-5)
- ✅ **Feature Flags** - Sichere Feature-Aktivierung

---

## 🚀 **Quick Start**

### **Voraussetzungen**
- Python 3.10+
- Node.js 18+
- OpenAI API Key

### **Installation**

```bash
# 1. Backend einrichten
cd clarity-coach-main/backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 2. .env Datei erstellen
echo "OPENAI_API_KEY=sk-your-key-here" > .env

# 3. Frontend installieren
cd ..
npm install
```

### **Starten**

**Terminal 1 - Backend:**
```bash
cd clarity-coach-main/backend
.\venv\Scripts\Activate.ps1
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd clarity-coach-main
npm run dev
```

**Öffnen:** http://localhost:5173/

---

## 🎨 **Hauptfunktionen**

### **Lernhilfen**

| Feature | Beschreibung |
|---------|--------------|
| 🤔 **Sokratische Fragen** | Leitfragen die zum Nachdenken anregen |
| 💡 **Progressive Hilfestellungen** | 3-Stufen-System ohne Lösung zu verraten |
| 📊 **Visuelle Hilfe** | Grafiken, Animationen, Keyfacts |
| ✓ **Ansatz-Prüfung** | Konstruktives Feedback zum Lösungsweg |

### **Hilfestellungs-System**

```
Stufe 1: Sokratisch    → "Welche Eigenschaft hat f'(x) an Extremstellen?"
Stufe 2: Anleitend     → "Berechne f'(x) und setze sie gleich null."
Stufe 3: Spezifisch    → "Bei f(x)=x³-3x² ist f'(x)=3x²-6x"
```

### **Selbstständigkeits-Score**

| Hilfe | Score | Bewertung |
|-------|-------|-----------|
| 0 | ★★★★★ | Eigenständig |
| 1-2 | ★★★★☆ | Minimal unterstützt |
| 3-5 | ★★★☆☆ | Moderat unterstützt |
| 6-8 | ★★☆☆☆ | Stark unterstützt |
| 9+ | ★☆☆☆☆ | Intensive Betreuung |

---

## 📁 **Unterstützte Dateien**

- **PDF** (bis 12 MB)
- **Bilder** (.jpg, .jpeg, .png)
- **Text** (.txt)

---

## 🛠️ **Tech Stack**

**Backend:**
- FastAPI (Python)
- OpenAI GPT-4o-mini
- Chart.js (Grafiken)
- PyMuPDF (PDF)

**Frontend:**
- Vue 3 (Composition API)
- Vite
- KaTeX (LaTeX)
- GSAP (Animationen)

---

## 📚 **Dokumentation**

| Dokument | Beschreibung |
|----------|--------------|
| [USER_GUIDE.md](USER_GUIDE.md) | Benutzerhandbuch |
| [TESTING_GUIDE.md](TESTING_GUIDE.md) | Test-Checkliste |
| [OPTIMIZATION_COMPLETE_SUMMARY.md](OPTIMIZATION_COMPLETE_SUMMARY.md) | Optimierungs-Zusammenfassung |
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | Schnellreferenz |

---

## 🔧 **Konfiguration**

### Feature Flags (`src/config/featureFlags.js`)

```javascript
export const FEATURE_FLAGS = {
  showSolutionButton: false,      // ENTFERNT
  smartVisualHint: true,          // AKTIV
  progressiveHints: true,         // AKTIV
  smartApproachChecker: true,     // AKTIV
  trackSelfSufficiency: true,     // AKTIV
}
```

---

## 🐛 **Fehlerbehebung**

### Upload hängt?
1. Backend-Terminal auf Fehler prüfen
2. `.env` Datei mit API-Key vorhanden?
3. Server neustarten

### Keine Grafik möglich?
- Bei abstrakten Aufgaben ohne konkrete Funktion
- System zeigt dann Keyfacts oder Animation

### Session speichern schlägt fehl?
1. Excel-Datei existiert?
2. Excel-Datei geschlossen?
3. Schreibrechte vorhanden?

---

## 📊 **Projektstruktur**

```
clarity-coach-main/
├── backend/
│   ├── main.py              # FastAPI Server
│   ├── requirements.txt     # Python Dependencies
│   └── .env                 # API Keys (nicht committen!)
├── src/
│   ├── components/
│   │   ├── ClarityCoach.vue # Hauptkomponente
│   │   ├── SessionForm.vue  # Sitzungsformular
│   │   └── ...
│   ├── config/
│   │   └── featureFlags.js  # Feature-Toggles
│   └── services/
│       └── visualHintService.js # Smart Visual Logic
├── USER_GUIDE.md            # Benutzerhandbuch
├── TESTING_GUIDE.md         # Test-Anleitung
└── README.md                # Diese Datei
```

---

## ✅ **Changelog v3.0**

### Hinzugefügt
- Progressive 3-Stufen-Hilfestellungen
- Smart Visual Hint System
- Ansatz-Prüfung mit KI-Feedback
- Selbstständigkeits-Score Tracking
- Feature Flags System
- Umfassende Dokumentation

### Entfernt
- Lösungs-Button (widerspricht Sokrates-Methode)
- Legacy Visual Buttons (durch Smart System ersetzt)

### Verbessert
- Bundle-Größe reduziert (~80%)
- Ladezeiten verbessert
- Excel-Export erweitert

---

## 🎓 **Pädagogischer Ansatz**

Clarity Coach folgt dem **konstruktivistischen Lernparadigma**:

1. **Aktives Lernen** - Schüler konstruieren Wissen selbst
2. **Scaffolding** - Unterstützung wird schrittweise reduziert
3. **Zone der proximalen Entwicklung** - Hilfe auf richtigem Niveau
4. **Metakognition** - Reflexion über eigenen Lernprozess

---

## 📞 **Support**

1. Dokumentation lesen: [USER_GUIDE.md](USER_GUIDE.md)
2. Tests durchführen: [TESTING_GUIDE.md](TESTING_GUIDE.md)
3. Terminal-Logs prüfen
4. Server neustarten

---

## 🌟 **Credits**

- **KI-Modell:** OpenAI GPT-4o-mini
- **Mathe-Rendering:** KaTeX
- **Animationen:** GSAP
- **Grafiken:** Chart.js
- **Frontend:** Vue 3
- **Backend:** FastAPI

---

**Clarity Coach v3.0** - Sokratisches Lernen mit KI 🎓

*Entwickelt für eigenständiges Denken und tiefes Verständnis.*
