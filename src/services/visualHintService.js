/**
 * Smart Visual Hint Service
 * 
 * Intelligently selects the best visual aid based on:
 * - Task type (polynomial, derivative, integral, geometry, etc.)
 * - Student progress (time stuck, attempts made)
 * - Learner type preference (visual, analytical, experimental)
 * 
 * @file visualHintService.js
 * @created 2026-01-12
 */

// Visual hint types
export const VISUAL_TYPES = {
  GRAPH: 'graph',           // Interactive Plotly graph
  ANIMATION: 'animation',   // Step-by-step GSAP animation
  KEY_FACTS: 'key_facts',   // Structured visualization of facts
  FORMULA: 'formula',       // Formula breakdown with KaTeX
  DIAGRAM: 'diagram'        // Concept diagram
};

// Task type detection patterns
const TASK_PATTERNS = {
  extremwert: /extremwert|maximum|minimum|hochpunkt|tiefpunkt|extremstelle/i,
  ableitung: /ableitung|f['′]|differenzier|steigung|tangente/i,
  integral: /integral|∫|stammfunktion|fläche.*unter/i,
  nullstelle: /nullstelle|x.*=.*0|löse.*gleichung|wurzel/i,
  polynom: /polynom|x\^[2-9]|quadrat|kubisch|grad/i,
  kurvendiskussion: /kurvendiskussion|wendepunkt|monotonie|symmetrie/i,
  grenzwert: /grenzwert|limes|lim|konvergenz/i,
  geometry: /dreieck|kreis|rechteck|fläche|umfang|winkel|pythagoras/i,
  linear: /linear|gerade|y.*=.*mx|steigungsdreieck/i,
  exponential: /exponential|e\^|wachstum|zerfall|halbwertszeit/i,
  logarithmus: /logarithm|ln|log|natürlich/i,
  trigonometrie: /sin|cos|tan|sinus|cosinus|tangens/i
};

/**
 * Detect the type of mathematical task from text
 * @param {string} taskText - The task description
 * @param {string} topic - The topic name
 * @returns {string[]} Array of detected task types
 */
export function detectTaskTypes(taskText, topic = '') {
  const fullText = `${taskText} ${topic}`.toLowerCase();
  const detectedTypes = [];
  
  for (const [type, pattern] of Object.entries(TASK_PATTERNS)) {
    if (pattern.test(fullText)) {
      detectedTypes.push(type);
    }
  }
  
  return detectedTypes.length > 0 ? detectedTypes : ['general'];
}

/**
 * Calculate how stuck the student might be
 * @param {object} studentProgress - Progress tracking data
 * @returns {number} Stuck level from 0 (not stuck) to 3 (very stuck)
 */
export function calculateStuckLevel(studentProgress) {
  const { timeSpent = 0, hintsUsed = 0, questionsViewed = 0 } = studentProgress;
  
  let stuckLevel = 0;
  
  // Time-based stuck detection
  if (timeSpent > 300) stuckLevel += 2;      // 5+ minutes
  else if (timeSpent > 120) stuckLevel += 1; // 2+ minutes
  
  // Hint-based detection
  if (hintsUsed >= 2) stuckLevel += 1;
  
  // Question cycling detection
  if (questionsViewed >= 3) stuckLevel += 1;
  
  return Math.min(stuckLevel, 3);
}

/**
 * Main service class for smart visual hint selection
 */
class SmartVisualHintService {
  constructor() {
    this.visualCache = new Map();
    this.usageLog = [];
  }
  
  /**
   * Intelligently select the best visual aid for a given context
   * @param {object} context - Task and student context
   * @returns {object} Visual hint configuration
   */
  selectBestVisual(context) {
    const {
      taskText = '',
      subtaskText = '',
      topic = '',
      learnerType = 'visual',
      studentProgress = {},
      previousVisuals = []
    } = context;
    
    // Detect task types
    const taskTypes = detectTaskTypes(`${taskText} ${subtaskText}`, topic);
    const stuckLevel = calculateStuckLevel(studentProgress);
    
    // Decision logic based on task type and student state
    let selectedType = VISUAL_TYPES.KEY_FACTS; // Default
    let reason = 'Standard visual aid selection';
    
    // ============================================================
    // TASK TYPE BASED SELECTION
    // ============================================================
    
    // Polynomial/Function tasks → Graph is most helpful
    if (taskTypes.includes('polynom') || 
        taskTypes.includes('extremwert') || 
        taskTypes.includes('nullstelle') ||
        taskTypes.includes('kurvendiskussion')) {
      selectedType = VISUAL_TYPES.GRAPH;
      reason = 'Funktionsgraph zeigt Nullstellen, Extrema und Verlauf';
    }
    
    // Derivative tasks → Animation shows step-by-step transformation
    else if (taskTypes.includes('ableitung')) {
      if (stuckLevel >= 2) {
        selectedType = VISUAL_TYPES.ANIMATION;
        reason = 'Schrittweise Animation der Ableitungsregeln';
      } else {
        selectedType = VISUAL_TYPES.GRAPH;
        reason = 'Graph mit Tangente verdeutlicht Steigung';
      }
    }
    
    // Integral tasks → Animation or Graph
    else if (taskTypes.includes('integral')) {
      selectedType = VISUAL_TYPES.ANIMATION;
      reason = 'Animation zeigt Flächeninhalt unter der Kurve';
    }
    
    // Trigonometric tasks → Animation with unit circle
    else if (taskTypes.includes('trigonometrie')) {
      selectedType = VISUAL_TYPES.ANIMATION;
      reason = 'Einheitskreis-Animation verdeutlicht Zusammenhänge';
    }
    
    // Exponential/Logarithmic → Graph best
    else if (taskTypes.includes('exponential') || taskTypes.includes('logarithmus')) {
      selectedType = VISUAL_TYPES.GRAPH;
      reason = 'Funktionsverlauf zeigt Wachstum/Zerfall';
    }
    
    // Linear equations → Graph with points
    else if (taskTypes.includes('linear')) {
      selectedType = VISUAL_TYPES.GRAPH;
      reason = 'Gerade mit markierten Punkten';
    }
    
    // Geometry → Key facts with diagram description
    else if (taskTypes.includes('geometry')) {
      selectedType = VISUAL_TYPES.KEY_FACTS;
      reason = 'Schlüsselfakten und geometrische Beziehungen';
    }
    
    // Limit/Convergence → Animation
    else if (taskTypes.includes('grenzwert')) {
      selectedType = VISUAL_TYPES.ANIMATION;
      reason = 'Animation zeigt Konvergenzverhalten';
    }
    
    // ============================================================
    // LEARNER TYPE ADJUSTMENTS
    // ============================================================
    
    if (learnerType === 'analytical' && selectedType === VISUAL_TYPES.ANIMATION) {
      // Analytical learners might prefer key facts
      if (stuckLevel < 2) {
        selectedType = VISUAL_TYPES.KEY_FACTS;
        reason += ' (Angepasst für analytischen Lerntyp)';
      }
    }
    
    if (learnerType === 'experimental' && selectedType === VISUAL_TYPES.KEY_FACTS) {
      // Experimental learners prefer interactive graphs
      selectedType = VISUAL_TYPES.GRAPH;
      reason += ' (Angepasst für experimentellen Lerntyp)';
    }
    
    // ============================================================
    // STUCK LEVEL ADJUSTMENTS
    // ============================================================
    
    // If very stuck and hasn't seen animation, show animation
    if (stuckLevel >= 3 && !previousVisuals.includes(VISUAL_TYPES.ANIMATION)) {
      selectedType = VISUAL_TYPES.ANIMATION;
      reason = 'Schrittweise Animation für besseres Verständnis (du bist länger hier)';
    }
    
    // ============================================================
    // AVOID REPETITION
    // ============================================================
    
    // If already seen this type, try a different one
    if (previousVisuals.length > 0 && previousVisuals[previousVisuals.length - 1] === selectedType) {
      const alternatives = [VISUAL_TYPES.GRAPH, VISUAL_TYPES.ANIMATION, VISUAL_TYPES.KEY_FACTS];
      const available = alternatives.filter(t => !previousVisuals.includes(t));
      if (available.length > 0) {
        selectedType = available[0];
        reason = 'Alternative Visualisierung für neue Perspektive';
      }
    }
    
    // Log the selection
    this.logSelection(context, selectedType, reason);
    
    return {
      type: selectedType,
      reason,
      taskTypes,
      stuckLevel,
      endpoint: this.getEndpointForType(selectedType)
    };
  }
  
  /**
   * Get the backend endpoint for a visual type
   * @param {string} visualType - The visual type
   * @returns {string} Backend endpoint path
   */
  getEndpointForType(visualType) {
    const endpoints = {
      [VISUAL_TYPES.GRAPH]: '/plot',
      [VISUAL_TYPES.ANIMATION]: '/animate',
      [VISUAL_TYPES.KEY_FACTS]: '/visualize',
      [VISUAL_TYPES.FORMULA]: '/visualize',
      [VISUAL_TYPES.DIAGRAM]: '/visualize'
    };
    return endpoints[visualType] || '/visualize';
  }
  
  /**
   * Get German name for visual type
   * @param {string} visualType - The visual type
   * @returns {string} German label
   */
  getVisualLabel(visualType) {
    const labels = {
      [VISUAL_TYPES.GRAPH]: '📊 Interaktive Grafik',
      [VISUAL_TYPES.ANIMATION]: '🎬 Schrittweise Animation',
      [VISUAL_TYPES.KEY_FACTS]: '💡 Schlüsselfakten',
      [VISUAL_TYPES.FORMULA]: '📐 Formelübersicht',
      [VISUAL_TYPES.DIAGRAM]: '📝 Konzeptdiagramm'
    };
    return labels[visualType] || '💡 Visuelle Hilfe';
  }
  
  /**
   * Log selection for analytics
   * @private
   */
  logSelection(context, selectedType, reason) {
    this.usageLog.push({
      timestamp: new Date().toISOString(),
      taskTypes: detectTaskTypes(context.taskText, context.topic),
      selectedType,
      reason,
      learnerType: context.learnerType,
      stuckLevel: calculateStuckLevel(context.studentProgress)
    });
    
    // Keep only last 100 entries
    if (this.usageLog.length > 100) {
      this.usageLog.shift();
    }
  }
  
  /**
   * Get visual type statistics for assessment
   * @returns {object} Usage statistics
   */
  getUsageStats() {
    const stats = {
      total: this.usageLog.length,
      byType: {},
      byTaskType: {}
    };
    
    this.usageLog.forEach(entry => {
      // Count by visual type
      stats.byType[entry.selectedType] = (stats.byType[entry.selectedType] || 0) + 1;
      
      // Count by task type
      entry.taskTypes.forEach(tt => {
        stats.byTaskType[tt] = (stats.byTaskType[tt] || 0) + 1;
      });
    });
    
    return stats;
  }
  
  /**
   * Cache a rendered visual
   * @param {string} key - Cache key (taskId + subtaskId)
   * @param {object} visual - The rendered visual data
   */
  cacheVisual(key, visual) {
    // Limit cache size
    if (this.visualCache.size >= 20) {
      const firstKey = this.visualCache.keys().next().value;
      this.visualCache.delete(firstKey);
    }
    this.visualCache.set(key, {
      visual,
      timestamp: Date.now()
    });
  }
  
  /**
   * Get cached visual if available
   * @param {string} key - Cache key
   * @returns {object|null} Cached visual or null
   */
  getCachedVisual(key) {
    const cached = this.visualCache.get(key);
    if (cached) {
      // Invalidate after 30 minutes
      if (Date.now() - cached.timestamp < 30 * 60 * 1000) {
        return cached.visual;
      }
      this.visualCache.delete(key);
    }
    return null;
  }
  
  /**
   * Clear all cached visuals
   */
  clearCache() {
    this.visualCache.clear();
  }
}

// Export singleton instance
export const visualHintService = new SmartVisualHintService();

export default visualHintService;
