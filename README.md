# 🎓 Clarity Coach - Multi-Domain Socratic Coaching System

**Version:** 4.0 (Self & Business Clarity Integration)
**Status:** ✅ **Production Ready**
**Last Update:** February 11, 2026

---

## 🌟 **What is Clarity Coach?**

Clarity Coach is an AI-powered multi-domain coaching platform based on the **Socratic method**. Instead of providing direct answers, the system guides users through targeted questions to develop independent understanding.

### Three Coaching Domains

| Domain | Icon | Description | Sessions |
|--------|------|-------------|----------|
| **Math Clarity** | 📐 | Socratic math tutoring for grades 7-13 | Single session |
| **Business Clarity** | 💼 | Business decisions & automation strategy | 1-2 sessions per topic |
| **Self Clarity** | 🧘 | Personal reflection & self-discovery | 5-10 sessions |

### Core Philosophy

> *"I cannot teach anyone anything, I can only make them think."* - Socrates

---

## 🆕 **Version 4.0 - What's New?**

### Added Features
- ✅ **Self Clarity Coach** - Personal reflection with multi-session tracking
- ✅ **Business Clarity Coach** - Business consulting with Socratic questions
- ✅ **Domain Selector** - Beautiful UI to choose coaching domain
- ✅ **Session Management** - File-based persistence across sessions
- ✅ **Full German UI** - Complete German language interface

### Existing Features (Math Clarity)
- ✅ **3-Level Progressive Hints** - Socratic → Guided → Specific
- ✅ **Smart Visual Hints** - AI chooses best visualization automatically
- ✅ **Approach Checker** - Feedback without revealing solution
- ✅ **Self-Sufficiency Score** - Learning autonomy tracking (1-5)

---

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.10+
- Node.js 18+
- OpenAI API Key ([Get one here](https://platform.openai.com/api-keys))

### **Installation**

#### 1. Clone the Repository
```bash
git clone https://github.com/Garveda/clarity-coach.git
cd clarity-coach
```

#### 2. Setup Backend
```bash
cd backend
python -m venv venv

# Windows
.\venv\Scripts\Activate.ps1

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

#### 3. Configure Environment
```bash
# Copy example file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-key-here
```

#### 4. Setup Frontend
```bash
cd ..
npm install
```

### **Running the Application**

**Terminal 1 - Backend:**
```bash
cd backend
.\venv\Scripts\Activate.ps1  # or: source venv/bin/activate
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

**Terminal 2 - Frontend:**
```bash
npm run dev
```

**Open in Browser:** http://localhost:5173/

---

## 🎯 **How to Use**

### 1. Choose Your Domain
When you open the app, you'll see three coaching domains:
- 📐 **Math Clarity** - For mathematical problems
- 💼 **Business Clarity** - For business decisions
- 🧘 **Self Clarity** - For personal reflection

### 2. Math Clarity
1. Upload a math problem (PDF, image, or text)
2. Click on a task to explore it
3. Use **"💡 Hilfe"** for progressive hints (Level 1-3)
4. Use **"✓ Ansatz prüfen"** to check your approach
5. Get feedback without seeing the solution

### 3. Business Clarity
1. Select a topic (Automatisierung, Strategie, Betrieb, Wachstum)
2. Describe your business challenge
3. Answer the Socratic questions
4. Work through the decision systematically
5. Get clarity on next steps

### 4. Self Clarity
1. Share what's on your mind
2. Answer reflection questions
3. Continue over 5-10 sessions
4. Discover patterns and insights
5. Track recurring themes

---

## 🛠️ **Tech Stack**

### Backend
- **FastAPI** - Modern Python web framework
- **OpenAI GPT-4o-mini** - AI model for Socratic coaching
- **Python-dotenv** - Environment variable management
- **PyMuPDF** - PDF processing for Math Clarity

### Frontend
- **Vue 3** - Progressive JavaScript framework (Composition API)
- **Vite** - Next-generation frontend tooling
- **KaTeX** - Fast math typesetting
- **vue-sonner** - Toast notifications

### Data Storage
- **File-based sessions** - JSON files in `backend/sessions/`
- No database required for basic operation

---

## 📁 **Project Structure**

```
clarity-coach/
├── backend/
│   ├── main.py                      # Main FastAPI server
│   ├── prompts.py                   # Socratic prompts for all domains
│   ├── clarity_endpoints.py         # Self & Business Clarity APIs
│   ├── session_manager.py           # Session persistence
│   ├── requirements.txt             # Python dependencies
│   ├── .env.example                 # Environment template
│   └── sessions/                    # User session data
│       ├── self_clarity/            # Self Clarity sessions
│       └── business_clarity/        # Business Clarity sessions
├── src/
│   ├── components/
│   │   ├── DomainSelector.vue       # Domain selection UI
│   │   ├── ClarityCoach.vue         # Math Clarity component
│   │   ├── SelfClarityChat.vue      # Self Clarity chat
│   │   ├── BusinessClarityChat.vue  # Business Clarity chat
│   │   └── ...
│   ├── config/
│   │   └── featureFlags.js          # Feature toggles
│   └── services/
│       └── visualHintService.js     # Visual hint logic
├── optimization_prompts/            # Original prompt specifications
│   ├── math_clarity_prompt.md
│   ├── business_clarity_prompt.md
│   └── self_clarity_prompt.md
├── package.json                     # Node.js dependencies
├── .gitignore                       # Git ignore rules
└── README.md                        # This file
```

---

## 🎨 **Features by Domain**

### 📐 Math Clarity

| Feature | Description |
|---------|-------------|
| Progressive Hints | 3 levels without revealing solution |
| Approach Checker | Feedback on your solution path |
| Visual Hints | Graphs, animations, key facts |
| Self-Sufficiency Score | Track learning independence |

**Hint Levels:**
```
Level 1: Socratic    → "What property does f'(x) have at extrema?"
Level 2: Guided      → "Calculate f'(x) and set it equal to zero."
Level 3: Specific    → "For f(x)=x³-3x², f'(x)=3x²-6x"
```

### 💼 Business Clarity

| Feature | Description |
|---------|-------------|
| Topic Selection | Automation, Strategy, Operations, Growth |
| Socratic Questions | 8 question patterns for business thinking |
| Decision Framework | Systematic approach to complex decisions |
| Session Memory | Builds on previous conversations |

**Question Patterns:**
- Business Core Understanding
- Process Thinking
- Value Alignment
- Impact Assessment
- Resource Reality
- Priority Clarification
- Future Vision
- Decision Forcing

### 🧘 Self Clarity

| Feature | Description |
|---------|-------------|
| Multi-Session Journey | 5-10 sessions for deep reflection |
| Pattern Recognition | Discovers recurring themes |
| Contradiction Detection | Highlights inconsistencies |
| Insight Tracking | Records key discoveries |

**Session Progression:**
- Session 1-2: Explore current experiences
- Session 3-5: Identify patterns
- Session 6-8: Deep contradictions
- Session 9-10: Synthesize insights

---

## 🔧 **Configuration**

### Backend Environment (.env)
```bash
# Required
OPENAI_API_KEY=sk-your-key-here

# Optional
# PORT=8000
# HOST=127.0.0.1
```

### Frontend Feature Flags (src/config/featureFlags.js)
```javascript
export const FEATURE_FLAGS = {
  showSolutionButton: false,      // Removed (anti-pattern)
  smartVisualHint: true,          // Active
  progressiveHints: true,         // Active
  smartApproachChecker: true,     // Active
  trackSelfSufficiency: true,     // Active
}
```

---

## 📚 **API Endpoints**

### Math Clarity
- `POST /extract` - Upload and analyze math problems
- `POST /hint` - Get progressive hint (level 1-3)
- `POST /check-approach` - Check solution approach

### Self Clarity
- `POST /self-clarity` - Send message to Self Clarity coach
- `GET /self-clarity/session/{user_id}` - Get session status

### Business Clarity
- `POST /business-clarity` - Send message to Business Clarity coach
- `GET /business-clarity/session/{user_id}` - Get session status

---

## 🐛 **Troubleshooting**

### Backend Won't Start
1. Check if port 8000 is already in use
2. Verify `.env` file exists with valid OpenAI API key
3. Ensure all dependencies installed: `pip install -r requirements.txt`
4. Check Python version: `python --version` (need 3.10+)

### Frontend Won't Start
1. Check if port 5173 is already in use
2. Verify Node.js version: `node --version` (need 18+)
3. Try deleting `node_modules` and run `npm install` again
4. Clear npm cache: `npm cache clean --force`

### Domain Buttons Not Working
1. Hard refresh browser: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
2. Check browser console (F12) for JavaScript errors
3. Verify backend is running on http://127.0.0.1:8000

### OpenAI API Errors
1. Verify API key is valid and has credits
2. Check OpenAI service status
3. Ensure `.env` file is in `backend/` directory
4. Restart backend server after updating `.env`

---

## 📊 **Session Data**

Sessions are stored as JSON files in:
```
backend/sessions/
├── self_clarity/
│   └── {user_id}.json
└── business_clarity/
    └── {user_id}.json
```

**Session data includes:**
- Self Clarity: Session count, key insights, recurring themes, contradictions
- Business Clarity: Session count, decisions discussed, business context

To reset a session, delete the corresponding JSON file.

---

## 🌟 **Educational Approach**

Clarity Coach follows **constructivist learning principles**:

1. **Active Learning** - Users construct knowledge themselves
2. **Scaffolding** - Support is progressively reduced
3. **Zone of Proximal Development** - Help at the right level
4. **Metacognition** - Reflection on learning process
5. **Socratic Method** - Questions, not answers

---

## 📝 **Contributing**

This is a private educational project. For questions or suggestions, please contact the repository owner.

---

## 📄 **License**

Private project - All rights reserved.

---

## 🎓 **Credits**

- **AI Model:** OpenAI GPT-4o-mini
- **Math Rendering:** KaTeX
- **Frontend Framework:** Vue 3
- **Backend Framework:** FastAPI
- **Socratic Method:** Inspired by ancient Greek philosophy

---

## 📞 **Support**

1. Check documentation files in the repository
2. Review terminal logs for error messages
3. Ensure all prerequisites are installed
4. Try restarting both frontend and backend servers

---

**Clarity Coach v4.0** - Multi-Domain Socratic Coaching with AI 🎓

*Entwickelt für eigenständiges Denken und tiefes Verständnis.*
*Developed for independent thinking and deep understanding.*
