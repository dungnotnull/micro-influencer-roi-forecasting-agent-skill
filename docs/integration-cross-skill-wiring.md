# Integration & Cross-Skill Wiring

## Purpose

This document defines the shared interfaces and patterns that enable `micro-influencer-roi-forecasting` and sibling skills in the `marketing-content-branding` cluster to reuse common sub-skills for intake, scoring, and roadmap generation.

## Cluster Overview

**Cluster:** Marketing, Content & Branding

**Skills in cluster:**
- `micro-influencer-roi-forecasting` (idea #208) — Influencer campaign ROI forecasting
- `content-calendar-optimizer` — Editorial planning and timing optimization
- `brand-voice-auditor` — Brand voice consistency and guideline compliance
- `campaign-budget-simulator` — Budget scenario modeling and allocation

## Shared Sub-Skill Contracts

### 1. Intake Pattern (`shared-campaign-intake`)

All skills require structured campaign context before analysis. The intake sub-skill normalizes this pattern.

**Standardized Interface:**

```yaml
inputs:
  user_request: string
  existing_context: object (optional)

outputs:
  campaign_context:
    brand: string
    industry: string
    primary_goal: enum (awareness, consideration, conversion, retention, advocacy)
    target_audience:
      demographics: object
      psychographics: object
      geography: list
    budget:
      total: number
      currency: string
      timeframe: string
    timeline:
      start_date: string
      end_date: string
    constraints:
      compliance_regions: list
      brand_sensitivity: enum (low, medium, high)
      excluded_platforms: list
    success_metrics:
      primary_kpi: string
      secondary_kpis: list
      targets: object
  quality_flags:
    completeness_score: number (0-1)
    missing_critical_fields: list
    assumptions_made: list
  meta:
    intake_timestamp: string
    confidence: number (0-1)
```

**Reuse Pattern:**
- Each skill can extend the base with skill-specific fields (e.g., influencer-specific for this skill)
- Quality gate: `completeness_score >= 0.7` before proceeding to analysis

### 2. Scoring Framework (`shared-multi-dimensional-scoring`)

All skills produce multi-dimensional scores against named frameworks.

**Standardized Interface:**

```yaml
inputs:
  campaign_context: object (from intake)
  framework_definitions:
    - name: string
      dimensions:
        - dimension_name: string
          weight: number
          scoring_method: string
          evidence_sources: list
  analysis_data: object (skill-specific)

outputs:
  composite_score:
    value: number (0-100)
    confidence: number (0-1)
    methodology: string
  dimension_scores:
    - dimension: string
      score: number (0-100)
      weight: number
      contribution: number
      evidence:
        - source: string
          relevance: number
          citation: string
      assumptions:
        - statement: string
          likelihood: number
          impact_if_wrong: string
  quality_flags:
    evidence_coverage: number (0-1)
    assumption_risk: number (0-1)
    framework_alignment: number (0-1)
  meta:
    scoring_timestamp: string
    frameworks_applied: list
    devil_advocate_review: object
```

**Reuse Pattern:**
- Each skill defines its own frameworks and dimensions
- Devil's advocate review is mandatory across all skills
- Evidence hierarchy must be respected (primary research > industry benchmarks > assumptions)

### 3. Roadmap Generation (`shared-prioritized-roadmap`)

All skills produce actionable roadmaps ranked by impact × effort.

**Standardized Interface:**

```yaml
inputs:
  campaign_context: object (from intake)
  scoring_results: object (from scoring)
  gaps_identified: list
  constraints: object

outputs:
  roadmap:
    - priority: number (1 = highest)
      action_title: string
      impact_score: number (1-10)
      effort_score: number (1-10)
      impact_effort_product: number
      category: enum (quick_win, major_bet, foundational, cleanup)
      rationale: string
      dependencies: list
      timeframe_estimate: string
      owner_suggestion: string
      success_criteria: string
      citations:
        - source: string
          relevance: string
    execution_summary:
      total_actions: number
      quick_wins: number
      major_bets: number
      estimated_implementable_quick_wins: number
    meta:
      generation_timestamp: string
      prioritization_method: string
```

**Reuse Pattern:**
- Impact × effort matrix is standard across cluster
- Categories enable cross-skill portfolio planning
- Dependencies support orchestration across multiple concurrent campaigns

## Cross-Skill Integration Points

### Integration 1: Influencer ROI ↔ Content Calendar

**Data Flow:**
1. `micro-influencer-roi-forecasting` identifies optimal posting windows and content types
2. `content-calendar-optimizer` receives these as constraints for editorial planning
3. Feedback loop: calendar availability informs influencer availability and pricing

**Shared Data Schema:**
```yaml
content_optimization_signals:
  optimal_posting_windows:
    - platform: string
      day_of_week: string
      time_range: string
      expected_lift: number
      evidence_source: string
  content_format_recommendations:
    - format: string
      expected_engagement_multiplier: number
      platform_fit: list
  resource_constraints:
    - creator_id: string
      availability_windows: list
      lead_time_required: number
```

### Integration 2: Influencer ROI ↔ Brand Voice

**Data Flow:**
1. `brand-voice-auditor` establishes voice guidelines and red flags
2. `micro-influencer-roi-forecasting` uses voice constraints as compliance gates
3. Creative guidance ensures ROI forecasts don't compromise brand integrity

**Shared Data Schema:**
```yaml
brand_voice_constraints:
  tone_guidelines:
    - attribute: string
      acceptable_range: list
      examples_violating: list
  terminology_rules:
    required_phrases: list
    forbidden_phrases: list
    industry_specific_glossary: object
  visual_style:
    palette_constraints: list
    logo_placement_rules: list
  compliance_flags:
    - rule_id: string
      severity: enum (block, warn, advisory)
      auto_check_available: boolean
```

### Integration 3: Influencer ROI ↔ Budget Simulator

**Data Flow:**
1. `campaign-budget-simulator` runs what-if scenarios on budget allocation
2. `micro-influencer-roi-forecasting` provides per-creator ROI estimates as inputs
3. Combined view: optimal budget × optimal creator selection

**Shared Data Schema:**
```yaml
budget_allocation_inputs:
  scenarios:
    - scenario_id: string
      creator_portfolio: list
      budget_allocation:
        - creator_id: string
          amount: number
          justification: string
      assumed_attribution_model: string
      expected_total_roi: number
      risk_factors: list
  sensitivity_analysis:
    - variable: string
      range: [number, number]
      impact_on_roi: object
```

## Implementation Status

### Phase 5 Tasks

- [x] Document shared-sub-skill interfaces (intake, scoring, roadmap)
- [x] Define cross-skill integration points (content calendar, brand voice, budget simulator)
- [x] Create shared data schemas for integration points
- [x] Document data flow and feedback loops between skills
- [ ] Implement version 1 of shared intake sub-skill (extracted from existing implementations)
- [ ] Implement version 1 of shared scoring framework (extracted from existing implementations)
- [ ] Implement version 1 of shared roadmap generator (extracted from existing implementations)
- [ ] Create integration tests that validate cross-skill data handoffs
- [ ] Document orchestration patterns for multi-skill workflows

## Next Steps for Cluster Maturity

1. **Extract shared sub-skills** — Refactor existing skill-specific implementations into shared, parameterizable versions
2. **Create integration layer** — Build lightweight orchestrator that can call multiple skills and merge results
3. **Standardize error handling** — Define common error types and recovery patterns across cluster
4. **Create cluster-level test suite** — End-to-end tests that validate cross-skill workflows
5. **Document cluster playbooks** — User-facing guides for common multi-skill use cases

## Version History

- **v1.0** (2025-06-30) — Initial integration documentation for Phase 5 completion
