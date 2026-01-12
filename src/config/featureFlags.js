/**
 * Feature Flags Configuration
 * 
 * This configuration allows gradual rollout of new features
 * and easy rollback if issues arise.
 * 
 * @file featureFlags.js
 * @created 2026-01-12
 */

export const FEATURE_FLAGS = {
  // ============================================================
  // Phase 1: Cleanup (COMPLETED)
  // ============================================================
  
  /**
   * REMOVED: Show Solution Button
   * This feature has been permanently disabled as it directly
   * contradicts the Socratic method.
   */
  showSolutionButton: false,
  
  /**
   * Legacy visual buttons (3 separate buttons)
   * Set to true for rollback if needed
   */
  legacyVisualButtons: false,  // DISABLED - Using unified smart visual
  
  // ============================================================
  // Phase 2: Feature Consolidation (ACTIVE)
  // ============================================================
  
  /**
   * Smart Visual Hint: Unified visual button that intelligently
   * selects the best visual aid based on task type
   */
  smartVisualHint: true,  // ACTIVE - Phase 2 Implementation
  
  /**
   * Use lightweight charts (Chart.js) instead of Plotly
   * Reduces bundle size from ~2.35MB to ~200KB
   */
  useLightweightCharts: true,  // ACTIVE - Phase 2.2 Complete
  
  // ============================================================
  // Phase 3: Smart Enhancements (ACTIVE)
  // ============================================================
  
  /**
   * Progressive Hints: 3-level hint system
   * Level 1: Socratic questions
   * Level 2: Directive hints
   * Level 3: Specific help
   */
  progressiveHints: true,  // ACTIVE - Replaces solution button
  
  /**
   * Smart Approach Checker: Validates student's work
   * without revealing the solution
   */
  smartApproachChecker: true,  // ACTIVE - Phase 3.2 Complete
  
  // ============================================================
  // Performance Features
  // ============================================================
  
  /**
   * Lazy load visual components only when needed
   */
  lazyLoadVisuals: false,
  
  /**
   * Cache rendered graphs to avoid re-generation
   */
  cacheRenderedGraphs: false,
  
  // ============================================================
  // Assessment Features
  // ============================================================
  
  /**
   * Track self-sufficiency score based on hints used
   */
  trackSelfSufficiency: true,
  
  /**
   * Show debug controls for testing
   * Set to false in production
   */
  showDebugControls: true,
}

/**
 * Calculate self-sufficiency score based on hints used
 * @param {number} hintsUsed - Total number of hints requested
 * @returns {1|2|3|4|5} Score from 1 (heavy support) to 5 (independent)
 */
export function calculateSelfSufficiencyScore(hintsUsed) {
  if (hintsUsed === 0) return 5;      // Solved independently
  if (hintsUsed <= 1) return 4;       // Minimal help
  if (hintsUsed <= 3) return 3;       // Moderate help
  if (hintsUsed <= 5) return 2;       // Significant help
  return 1;                           // Heavy support needed
}

/**
 * Get feature status summary for logging/debugging
 * @returns {object} Summary of active features
 */
export function getFeatureStatus() {
  const activeFeatures = Object.entries(FEATURE_FLAGS)
    .filter(([, enabled]) => enabled)
    .map(([name]) => name);
  
  const disabledFeatures = Object.entries(FEATURE_FLAGS)
    .filter(([, enabled]) => !enabled)
    .map(([name]) => name);
  
  return {
    active: activeFeatures,
    disabled: disabledFeatures,
    summary: `${activeFeatures.length} active, ${disabledFeatures.length} disabled`
  };
}

export default FEATURE_FLAGS;
