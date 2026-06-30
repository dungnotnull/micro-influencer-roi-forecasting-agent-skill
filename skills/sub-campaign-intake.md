---
name: micro-influencer-roi-forecasting__sub-campaign-intake
description: Sub-skill of micro-influencer-roi-forecasting — Capture niche, platform, creator metrics, budget, product economics and conversion goal.
---

## Purpose
Systematically capture all required campaign parameters through structured inquiry, validation, and normalization. Ensures the harness never proceeds without critical inputs, and surfaces assumptions transparently when information is incomplete.

## Procedure

### Step 1: Initialize Intake Session
Create a fresh intake context with the following structure:

```yaml
intake_session:
  session_id: generated_uuid
  timestamp: current_datetime
  user_inputs: []
  derived_fields: []
  quality_flags:
    completeness_score: 0.0
    missing_critical_fields: []
    assumptions_made: []
    confidence_level: 0.0
```

### Step 2: Collect Required Fields

For each required field, follow this pattern:
1. **Check if already provided** in user input or prior context
2. **If not present**, ask a targeted question
3. **Validate** the response (type, range, format)
4. **Normalize** to standard format
5. **Flag assumptions** if value is estimated vs provided

#### Required Field Set

**Category: Campaign Basics**
- `campaign_name` (string) — Human-readable identifier
- `campaign_objective` (enum) — awareness, consideration, conversion, retention, advocacy
- `primary_product_service` (string) — What is being promoted
- `product_category` (string) — Industry/niche classification
- `target_launch_date` (date) — When campaign goes live

**Category: Creator & Platform**
- `creator_handle` (string) — @username or profile URL
- `primary_platform` (enum) — instagram, tiktok, youtube, twitch, linkedin, pinterest, twitter
- `secondary_platforms` (list of enum) — Additional platforms if multi-platform
- `creator_tier` (enum) — nano (1k-10k), micro (10k-50k), mid (50k-500k), macro (500k-1M), celebrity (1M+)
- `content_format` (enum) — post, reel, story, video, livestream, carousel, series

**Category: Audience & Market**
- `target_audience_description` (string) — Freeform description of ideal audience
- `primary_geography` (list of countries/regions) — Where audience is located
- `audience_age_range` (range) — Target age bracket(s)
- `b2c_or_b2b` (enum) — b2c, b2b, b2b2c

**Category: Budget & Economics**
- `total_budget` (number) — Available spend in campaign currency
- `currency` (string) — ISO 4217 currency code
- `pricing_proposal` (object) — Creator's quoted rate if provided
  - `quoted_amount` (number)
  - `pricing_model` (enum) — flat_fee, cpm, cpe, cpa, hybrid, revshare
  - `deliverables` (list) — What creator commits to produce
- `target_cpa_max_acceptable` (number) — Maximum cost per acquisition willing to pay

**Category: Conversion Goals**
- `primary_conversion_action` (enum) — purchase, lead_form, signup, app_install, visit, video_view, engagement, custom
- `conversion_value_per_action` (number) — Expected revenue/value per conversion
- `attribution_window_days` (number) — Days to attribute post-click/post-view conversions
- `expected_baseline_conversion_rate` (number) — Current conversion rate without influencer

**Category: Measurement & Constraints**
- `has_pixel_analytics` (boolean) — Can brand track via pixel/analytics platform?
- `creator_provides_insights` (boolean) — Will creator share platform insights?
- `compliance_regions` (list) — Jurisdictions where campaign will run
- `brand_sensitivity_level` (enum) — low, medium, high — tolerance for controversy
- `excluded_content_themes` (list) — Topics creator must avoid

#### Field Validation Rules

```python
validation_rules = {
    "total_budget": {
        "type": "number",
        "min": 0,
        "max": 10000000,
        "required": True
    },
    "primary_platform": {
        "type": "enum",
        "values": ["instagram", "tiktok", "youtube", "twitch", "linkedin", "pinterest", "twitter"],
        "required": True
    },
    "target_launch_date": {
        "type": "date",
        "min": "today",
        "max": "today+365",
        "required": False
    },
    "expected_baseline_conversion_rate": {
        "type": "number",
        "min": 0,
        "max": 1,
        "default": 0.02  # 2% if not provided
    }
}
```

### Step 3: Derive Additional Fields

After collection, derive these fields automatically:

```yaml
derived_fields:
  estimated_impressions:
    formula: "creator_followers * platform_engagement_rate * content_visibility_factor"
    source: platform_benchmarks
  estimated_cpm:
    formula: "quoted_amount / (estimated_impressions / 1000)"
    source: calculated
  breakeven_conversion_rate:
    formula: "quoted_amount / (conversion_value_per_action * estimated_impressions)"
    source: calculated
  pricing_vs_benchmark:
    formula: "quoted_amount / benchmark_pricing_for_tier_platform_format"
    source: SECOND-KNOWLEDGE-BRAIN.md
```

### Step 4: Calculate Completeness Score

```python
completeness_score = (
    critical_fields_provided / total_critical_fields * 0.6 +
    important_fields_provided / total_important_fields * 0.3 +
    optional_fields_provided / total_optional_fields * 0.1
)
```

Critical fields (blocking if missing): campaign_objective, creator_handle, primary_platform, total_budget, primary_conversion_action, conversion_value_per_action

### Step 5: Generate Structured Output

Produce the following JSON-serializable output for downstream stages:

```json
{
  "intake_session": {
    "session_id": "uuid",
    "timestamp": "ISO8601",
    "completeness_score": 0.85,
    "confidence_level": 0.75
  },
  "campaign_context": {
    "basics": {...},
    "creator_platform": {...},
    "audience_market": {...},
    "budget_economics": {...},
    "conversion_goals": {...},
    "measurement_constraints": {...}
  },
  "derived_metrics": {
    "estimated_impressions": 45000,
    "estimated_cpm": 44.44,
    "breakeven_conversion_rate": 0.0089,
    "pricing_vs_benchmark": 1.15
  },
  "quality_flags": {
    "missing_critical_fields": ["attribution_window_days"],
    "assumptions_made": [
      {
        "field": "expected_baseline_conversion_rate",
        "assumed_value": 0.02,
        "reason": "not provided, using industry default"
      }
    ],
    "validation_warnings": [],
    "blocking_issues": []
  }
}
```

## Quality Gates

### Gate 1: Critical Field Completeness
- **Check:** All critical fields have non-null values
- **Pass:** `completeness_score >= 0.6` (60% of critical fields)
- **Fail:** Request missing fields from user before proceeding

### Gate 2: Data Consistency
- **Check:** No contradictory values (e.g., target_launch_date < today)
- **Pass:** Zero validation errors at error level
- **Fail:** Present contradictions for resolution

### Gate 3: Value Reasonableness
- **Check:** Numerical values within plausible ranges based on benchmarks
- **Pass:** No values exceed 5x benchmark extremes
- **Fail:** Flag outliers for confirmation

## Outputs

### Primary Output
Structured campaign context object (see Step 5) passed to `sub-fraud-screener`.

### Secondary Outputs
- Completeness report shown to user
- List of assumptions to be surfaced in final deliverable
- Blocking issues preventing progression to analysis

## Error Handling

**Error: Creator handle not found on platform**
- Log error in quality_flags.validation_warnings
- Mark creator_handle as "unverified"
- Proceed with analysis but flag in assumptions

**Error: Platform API rate limited during validation**
- Fall back to manual verification request
- Add to quality_flags.validation_warnings
- Proceed with user-provided data but mark as unverified

**Error: Currency conversion unavailable**
- Request user specify budget in USD or major currency
- Add to quality_flags.validation_warnings
- Proceed but note currency assumptions in final report
