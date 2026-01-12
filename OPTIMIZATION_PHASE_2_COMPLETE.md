# Clarity Coach Optimization - Phase 2 Complete

**Date:** 2026-01-12
**Status:** ✅ PHASE 2.1 COMPLETE (Smart Visual System)

---

## Summary of Changes

### ✅ NEW: Unified Smart Visual Button ("💡 Visuelle Hilfe")

**Replaces 3 separate buttons** (Visualisierung, Animation, Grafik) with **1 intelligent button** that:
1. Analyzes the task type (polynomial, derivative, integral, etc.)
2. Considers student progress (time stuck, hints used)
3. Auto-selects the best visual aid (graph, animation, or key facts)
4. Provides reason for selection

---

## New Files Created

### `src/services/visualHintService.js`

The **SmartVisualHintService** that intelligently selects visualizations:

```javascript
// Task type detection patterns
const TASK_PATTERNS = {
  extremwert: /extremwert|maximum|minimum|hochpunkt|tiefpunkt/i,
  ableitung: /ableitung|f['′]|differenzier|steigung/i,
  integral: /integral|∫|stammfunktion/i,
  nullstelle: /nullstelle|x.*=.*0|löse.*gleichung/i,
  polynom: /polynom|x\^[2-9]|quadrat|kubisch/i,
  // ... more patterns
}

// Selection logic
selectBestVisual(context) {
  // Polynomial tasks → Graph
  if (taskTypes.includes('polynom') || taskTypes.includes('extremwert')) {
    return VISUAL_TYPES.GRAPH
  }
  
  // Derivative tasks → Animation when stuck, otherwise Graph
  if (taskTypes.includes('ableitung')) {
    return stuckLevel >= 2 ? VISUAL_TYPES.ANIMATION : VISUAL_TYPES.GRAPH
  }
  
  // Integral tasks → Animation
  if (taskTypes.includes('integral')) {
    return VISUAL_TYPES.ANIMATION
  }
  
  // ... more logic
}
```

---

## Feature Flag Configuration

**Updated `src/config/featureFlags.js`:**

```javascript
FEATURE_FLAGS = {
  legacyVisualButtons: false,  // DISABLED - Old 3-button system
  smartVisualHint: true,       // ACTIVE - Unified smart button
}
```

**To rollback** (show 3 separate buttons again):
```javascript
legacyVisualButtons: true,
smartVisualHint: false,
```

---

## UI Changes

### Before (3 buttons):
```
[Visualisierung anzeigen] [Animation erstellen] [Grafik erstellen]
```

### After (1 smart button):
```
[💡 Visuelle Hilfe] [🤔 Hilfestellung]
```

---

## Visual Type Selection Logic

| Task Type | Default Visual | When Stuck (3+ min) |
|-----------|---------------|---------------------|
| Polynomial (x², x³) | 📊 Graph | 📊 Graph |
| Extremwert | 📊 Graph | 🎬 Animation |
| Derivative | 📊 Graph (tangent) | 🎬 Animation |
| Integral | 🎬 Animation | 🎬 Animation |
| Trigonometry | 🎬 Animation | 🎬 Animation |
| Linear | 📊 Graph | 📊 Graph |
| Exponential | 📊 Graph | 📊 Graph |
| General | 💡 Key Facts | 🎬 Animation |

---

## Smart Visual Box Design

The visual display changes color based on type:

| Type | Color Scheme | Badge |
|------|-------------|-------|
| Graph | Green (emerald) | "Interaktiv" |
| Animation | Pink (rose) | "Animiert" |
| Key Facts | Indigo (violet) | "Fakten" |

Each visual box shows:
- **Title** with emoji indicator
- **Type badge** showing what kind of visual
- **Reason** explaining why this visual was selected
- **Content** (graph, animation, or formatted facts)

---

## Tracking & Assessment

New tracking fields added:

```javascript
usageStats = {
  // ... existing fields
  smartVisuals: 0,        // Total unified visuals requested
  visualTypes: []         // ['graph', 'animation', 'key_facts', ...]
}
```

---

## Files Modified

| File | Changes |
|------|---------|
| `src/components/ClarityCoach.vue` | Added smart visual system, feature flag conditionals |
| `src/config/featureFlags.js` | Enabled smartVisualHint, disabled legacy |
| `src/services/visualHintService.js` | NEW - Smart selection service |

---

## Technical Details

### State Variables Added
```javascript
const smartVisuals = ref([])          // Visual data per subtask
const smartVisualLoading = ref([])    // Loading states
const smartVisualTypes = ref([])      // What type was shown
const previousVisuals = ref([])       // Track previous visuals
const subtaskStartTime = ref([])      // When subtask was viewed
```

### New Functions
- `requestSmartVisual()` - Main entry point
- `getSmartVisualTitle()` - Get German title
- `getSmartVisualBadge()` - Get badge text
- `renderSmartGraph()` - Render Plotly graph
- `playSmartAnimation()` - Play GSAP animation
- `replaySmartAnimation()` - Replay animation

---

## Next Steps (Phase 2.2)

### Pending: Replace Plotly with Lightweight Alternative

**Current bundle size issue:**
- `plotly.js-dist-min`: ~2.35MB

**Options:**
1. **Recharts** (~300KB) - React-based, would need adaptation for Vue
2. **Chart.js** (~200KB) - Framework agnostic, good option
3. **Canvas API** (~0KB) - Native, most lightweight
4. **uPlot** (~25KB) - Ultra lightweight, good for functions

**Recommendation:** Use **Chart.js** or custom **Canvas API** for function plots.

---

## Testing Checklist

- [ ] Upload a PDF and verify single "💡 Visuelle Hilfe" button appears
- [ ] Click button on polynomial task → Should show Graph
- [ ] Click button on derivative task → Should show Graph or Animation
- [ ] Wait 3+ minutes, click again → May switch to Animation
- [ ] Click "Andere Visualisierung" → Should show different type
- [ ] Verify color-coded visual boxes appear correctly
- [ ] Check that reason text explains why visual was chosen

---

**Phase 2.1 Status: ✅ COMPLETE**

*Pending: Phase 2.2 (Replace Plotly)*
