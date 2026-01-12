# Visual Features Audit Report

**Generated:** 2026-01-12
**Project:** Clarity Coach
**Purpose:** UI/UX Optimization & Feature Consolidation

---

## Executive Summary

The Clarity Coach currently has **4 buttons per subtask**, causing:
1. **Philosophical conflict**: "Lösung anzeigen" contradicts Socratic method
2. **Feature bloat**: 3 separate visual features (Visualization + Animation + Graph)
3. **Performance issues**: Heavy Plotly library (~2MB)
4. **UI overload**: Too many options confuse learners

---

## Current Button Structure (Per Subtask)

| Button | German Label | Function | Status |
|--------|-------------|----------|--------|
| 1 | Visualisierung anzeigen | Shows key facts | ✅ Keep (Consolidate) |
| 2 | Animation erstellen | Step-by-step animation | ✅ Keep (Consolidate) |
| 3 | Grafik erstellen | Interactive Plotly graph | ✅ Keep (Consolidate) |
| 4 | **Lösung anzeigen** | **Shows full solution** | ❌ **REMOVE** |

---

## Feature 1: Visualization ("Visualisierung anzeigen")

### Location
- **Frontend:** `src/components/ClarityCoach.vue` (lines 131-140, 873-928)
- **Backend:** `backend/main.py` → `/visualize` endpoint (lines 449-525)

### Implementation
- Uses GPT-4o-mini to generate structured key facts
- No external libraries (pure text/HTML)
- Renders with KaTeX for math notation

### Bundle Size Impact
- **Frontend:** ~0KB (uses existing KaTeX)
- **Backend:** 0KB (GPT API only)

### Performance
- **Load time:** ~2-4 seconds (API dependent)
- **Very lightweight** ✅

### Usage Tracking
```javascript
usageStats.value.visualizations++  // Tracked ✅
```

---

## Feature 2: Animation ("Animation erstellen")

### Location
- **Frontend:** `src/components/ClarityCoach.vue` (lines 143-153, 933-1126)
- **Backend:** `backend/main.py` → `/animate` endpoint (lines 531-638)

### Implementation
- Uses GPT-4o-mini to generate JSON animation data
- Frontend renders with **GSAP** (lightweight) + **KaTeX**
- Browser-based animations (Canvas/SVG)

### Bundle Size Impact
- **Frontend:** ~60KB (GSAP is lightweight)
- **Backend:** 0KB (GPT API only)

### Performance
- **Load time:** ~2-4 seconds (API dependent)
- **Render time:** Instant (GSAP is fast)
- **Lightweight** ✅

### Usage Tracking
```javascript
usageStats.value.animations++  // Tracked ✅
```

---

## Feature 3: Graph ("Grafik erstellen")

### Location
- **Frontend:** `src/components/ClarityCoach.vue` (lines 155-166, 1130-1240)
- **Backend:** `backend/main.py` → `/plot` endpoint (lines 644-944)

### Implementation
- Uses GPT-4o-mini to analyze task for plottability
- Backend generates Plotly figure with NumPy
- Frontend renders with `plotly.js-dist-min`

### Bundle Size Impact
- **Frontend:** ~2.35MB (plotly.js-dist-min) ⚠️ HEAVY
- **Backend:** ~50MB (numpy, plotly) in Python env

### Performance
- **Load time:** ~3-6 seconds (calculation + API)
- **Initial bundle:** 2MB+ adds significant load time ⚠️
- **Heavy** ❌

### Usage Tracking
```javascript
usageStats.value.graphs++  // Tracked ✅
```

---

## Feature 4: Solution ("Lösung anzeigen") - **TO BE REMOVED**

### Location
- **Frontend:** `src/components/ClarityCoach.vue` (lines 169-179, 815-868)
- **Backend:** `backend/main.py` → `/solve` endpoint (lines 252-341)

### Implementation
- Uses GPT-4o-mini to generate complete solution
- Renders with KaTeX for math notation

### Bundle Size Impact
- **Frontend:** ~0KB (uses existing KaTeX)
- **Backend:** 0KB (GPT API only)

### **PROBLEM**
- ❌ **Directly contradicts Socratic method**
- ❌ Students skip problem-solving process
- ❌ Makes assessment impossible (did they learn or just click?)
- ❌ Creates learned helplessness

### Usage Tracking
```javascript
usageStats.value.solutions++  // Tracked ✅ (but shouldn't exist)
```

---

## Bundle Size Analysis

### Current State (package.json)

```json
{
  "dependencies": {
    "gsap": "^3.14.2",           // ~60KB - Keep ✅
    "katex": "^0.16.25",          // ~300KB - Required ✅
    "plotly.js-dist-min": "^2.35.3",  // ~2.35MB - HEAVY ⚠️
    "vue": "^3.5.24",             // ~40KB - Core
    "vue-sonner": "^2.0.9"        // ~10KB - Toast
  }
}
```

### Total Visual Dependencies
| Library | Size | Verdict |
|---------|------|---------|
| plotly.js-dist-min | ~2.35MB | ❌ Replace with Recharts |
| gsap | ~60KB | ✅ Keep |
| katex | ~300KB | ✅ Required |
| **Total** | **~2.7MB** | Reduce to ~400KB |

---

## Assessment Impact Analysis

### Current Tracking (Session Log)
```typescript
visualisierungen_genutzt: number;  // ✅ Tracked
animationen_genutzt: number;        // ✅ Tracked
grafiken_genutzt: number;           // ✅ Tracked
loesungen_angezeigt: number;        // ❌ Should not exist
```

### Missing Metrics (Need to Add)
- Self-sufficiency score
- Hint levels used (Socratic → Directive → Specific)
- Time to solution without hints
- Visual aid effectiveness rating

---

## Recommendations

### Phase 1: Immediate Cleanup
1. ❌ **DELETE** `/solve` endpoint in backend
2. ❌ **REMOVE** "Lösung anzeigen" button from frontend
3. ❌ **REMOVE** `solutions` ref and related code
4. ✅ **KEEP** all tracking for remaining features

### Phase 2: Feature Consolidation
1. Replace 3 visual buttons with 1 "💡 Visual Hint" button
2. Smart system selects best visual aid based on:
   - Task type (polynomial, geometry, etc.)
   - Time stuck
   - Learner type
3. Replace Plotly (~2MB) with Recharts (~300KB) or Canvas

### Phase 3: Smart Enhancements
1. Add Progressive Hint System (3 levels)
2. Add Smart Approach Checker
3. Update session tracking for new metrics

---

## Files to Modify

### Frontend (ClarityCoach.vue)
- Remove lines 169-179 (solution button)
- Remove lines 815-868 (toggleSolution function)
- Remove `solutions` and `solutionLoading` refs
- Remove solution-related CSS
- Add new VisualHintService

### Backend (main.py)
- Remove lines 252-341 (`/solve` endpoint)
- Add `/hint` endpoint (progressive hints)
- Add `/check-approach` endpoint

### Package.json
- Remove `plotly.js-dist-min`
- Add `recharts` (if using React) or use Canvas API

---

## Expected Outcomes

| Metric | Before | After |
|--------|--------|-------|
| Buttons per subtask | 4 | 3 (or 1 unified) |
| Bundle size (visuals) | ~2.7MB | ~400KB |
| Load time | ~5s | ~2s |
| Socratic compliance | ❌ Violated | ✅ Preserved |
| Assessment clarity | Unclear | Clear metrics |

---

**Next Step:** Proceed with Phase 1 - Remove Solution Button
