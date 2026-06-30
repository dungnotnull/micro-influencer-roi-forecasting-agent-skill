---
name: micro-influencer-roi-forecasting__sub-roi-forecaster
description: Sub-skill of micro-influencer-roi-forecasting — Forecast reach, conversions and ROI with attribution assumptions and confidence range.
---

## Purpose
Generate data-driven forecasts of campaign performance across multiple attribution models. Provide confidence intervals based on uncertainty in inputs. Score campaigns against named frameworks. Transparently surface all assumptions for devil's advocate review.

## Procedure

### Step 1: Gather Inputs

Collect from previous stages:
- Campaign context from `sub-campaign-intake`
- Effective reach from `sub-fraud-screener`
- Platform benchmarks from `SECOND-KNOWLEDGE-BRAIN.md`

### Step 2: Calculate Reach Forecasts

```python
def forecast_reach(campaign_context, effective_reach):
    """
    Generate reach estimates across scenarios (conservative, base, optimistic).
    """
    base_impressions = effective_reach

    # Scenario parameters
    scenarios = {
        "conservative": {
            "viral_multiplier": 1.0,      # No organic lift
            "algorithm_boost": 0.9,       # Slight underperformance
            "completion_rate": 0.5        # 50% of viewers watch full content
        },
        "base": {
            "viral_multiplier": 1.2,      # 20% organic lift
            "algorithm_boost": 1.0,       # Platform baseline
            "completion_rate": 0.65       # Industry average
        },
        "optimistic": {
            "viral_multiplier": 1.8,      # Strong organic lift
            "algorithm_boost": 1.3,       # Content resonates, gets boost
            "completion_rate": 0.8        # Highly engaging content
        }
    }

    forecasts = {}
    for scenario, params in scenarios.items():
        adjusted_reach = (
            base_impressions *
            params["viral_multiplier"] *
            params["algorithm_boost"]
        )
        fully_engaged_reach = adjusted_reach * params["completion_rate"]

        forecasts[scenario] = {
            "impressions": round(adjusted_reach),
            "fully_engaged_viewers": round(fully_engaged_reach),
            "parameters_used": params
        }

    return forecasts
```

### Step 3: Model Conversion Funnels

```python
def forecast_conversions(reach_forecasts, campaign_context):
    """
    Apply conversion funnel modeling to generate conversion estimates.
    """
    baseline_conversion_rate = campaign_context.get("expected_baseline_conversion_rate", 0.02)

    # Influencer lift multiplier based on content format and trust
    influencer_lift_multipliers = {
        "video": 1.8,        # Video has higher persuasive power
        "reel": 1.6,         # Short-form video, good engagement
        "post": 1.3,         # Static post, moderate lift
        "story": 1.4,        # Ephemeral, high urgency
        "livestream": 2.2,   # Real-time, highest trust
        "carousel": 1.5,     # Educational, good for consideration
        "series": 2.0        # Repeated exposure, compounding effect
    }

    content_format = campaign_context.get("content_format", "post")
    lift_multiplier = influencer_lift_multipliers.get(content_format, 1.3)

    conversion_forecasts = {}

    for scenario, reach_data in reach_forecasts.items():
        fully_engaged = reach_data["fully_engaged_viewers"]

        # Apply influencer lift to baseline rate
        effective_conversion_rate = baseline_conversion_rate * lift_multiplier

        # Scenario-specific conversion rate adjustments
        if scenario == "conservative":
            effective_conversion_rate *= 0.7  # Assume lower lift
        elif scenario == "optimistic":
            effective_conversion_rate *= 1.3  # Assume higher lift

        conversions = fully_engaged * effective_conversion_rate

        conversion_forecasts[scenario] = {
            "conversions": round(conversions),
            "conversion_rate": round(effective_conversion_rate, 4),
            "lift_multiplier_applied": lift_multiplier,
            "baseline_rate_used": baseline_conversion_rate
        }

    return conversion_forecasts
```

### Step 4: Apply Attribution Models

```python
def forecast_by_attribution_model(conversion_forecasts, campaign_context):
    """
    Generate forecasts across multiple attribution models.
    """
    attribution_window_days = campaign_context.get("attribution_window_days", 7)

    # Attribution model parameters (based on industry research)
    attribution_models = {
        "last_click": {
            "description": "100% credit to influencer for immediate conversions",
            "immediate_credit": 1.0,
            "delayed_credit": 0.0,
            "halflife_days": 0,
            "industry_usage": "Simple, common in direct-response"
        },
        "position_based": {
            "description": "40% credit first touch, 40% last touch, 20% middle",
            "immediate_credit": 0.6,  # Assume influencer is often first or last
            "delayed_credit": 0.2,
            "halflife_days": attribution_window_days / 2,
            "industry_usage": "Balanced view of full funnel"
        },
        "time_decay": {
            "description": "Credit decays exponentially over time",
            "immediate_credit": 0.7,
            "delayed_credit": 0.3,
            "halflife_days": attribution_window_days / 3,
            "industry_usage": "Accounts for recency effect"
        },
        "incrementality": {
            "description": "Only conversions that wouldn't happen otherwise",
            "immediate_credit": 0.5,  # Assume 50% incremental for micro-influencers
            "delayed_credit": 0.15,
            "halflife_days": attribution_window_days,
            "industry_usage": "Most rigorous, requires holdout testing"
        }
    }

    attribution_forecasts = {}

    for model_name, model_params in attribution_models.items():
        model_forecasts = {}

        for scenario, conv_data in conversion_forecasts.items():
            base_conversions = conv_data["conversions"]

            # Apply attribution model
            attributed_conversions = (
                base_conversions * model_params["immediate_credit"] +
                base_conversions * model_params["delayed_credit"]
            )

            model_forecasts[scenario] = {
                "attributed_conversions": round(attributed_conversions),
                "unattributed_conversions": round(base_conversions - attributed_conversions),
                "attribution_percentage": model_params["immediate_credit"] + model_params["delayed_credit"]
            }

        attribution_forecasts[model_name] = {
            "model_description": model_params["description"],
            "industry_usage": model_params["industry_usage"],
            "forecasts_by_scenario": model_forecasts
        }

    return attribution_forecasts
```

### Step 5: Calculate ROI & Economic Metrics

```python
def calculate_roi(attribution_forecasts, campaign_context):
    """
    Calculate ROI across all models and scenarios.
    """
    total_budget = campaign_context.get("total_budget", 0)
    conversion_value = campaign_context.get("conversion_value_per_action", 0)

    roi_results = {}

    for model_name, model_data in attribution_forecasts.items():
        model_roi = {}

        for scenario, forecast in model_data["forecasts_by_scenario"].items():
            attributed_conversions = forecast["attributed_conversions"]
            revenue = attributed_conversions * conversion_value
            profit = revenue - total_budget

            roi = (profit / max(1, total_budget)) * 100  # ROI as percentage
            roas = revenue / max(1, total_budget)  # Return on Ad Spend

            model_roi[scenario] = {
                "attributed_conversions": attributed_conversions,
                "revenue": round(revenue, 2),
                "profit": round(profit, 2),
                "roi_percentage": round(roi, 2),
                "roas": round(roas, 2),
                "cpa": round(total_budget / max(1, attributed_conversions), 2),  # Cost per acquisition
                "break_even_conversions": round(total_budget / max(1, conversion_value)),
                "is_profitable": profit > 0
            }

        roi_results[model_name] = model_roi

    return roi_results
```

### Step 6: Calculate Confidence Intervals

```python
def calculate_confidence_intervals(roi_results, fraud_assessment):
    """
    Generate confidence ranges based on input uncertainty.
    """
    # Base uncertainty from scenario spread (conservative to optimistic)
    # Additional uncertainty from fraud assessment

    confidence_intervals = {}

    for model_name, scenarios in roi_results.items():
        conservative = scenarios["conservative"]
        optimistic = scenarios["optimistic"]
        base_case = scenarios["base"]

        # Calculate standard deviation estimate from scenario spread
        std_estimate = (optimistic["roi_percentage"] - conservative["roi_percentage"]) / 4  # Rule of thumb

        # Fraud adjustment increases uncertainty
        fraud_penalty = fraud_assessment.get("composite_score", 0) * 20  # Up to 20% additional uncertainty

        # 95% confidence interval (approximately ±2 standard deviations)
        ci_lower = base_case["roi_percentage"] - 2 * std_estimate - fraud_penalty
        ci_upper = base_case["roi_percentage"] + 2 * std_estimate + fraud_penalty

        confidence_intervals[model_name] = {
            "base_roi": base_case["roi_percentage"],
            "confidence_interval_95": {
                "lower": round(ci_lower, 2),
                "upper": round(ci_upper, 2)
            },
            "confidence_interval_80": {
                "lower": round(base_case["roi_percentage"] - 1.28 * std_estimate - fraud_penalty/2, 2),
                "upper": round(base_case["roi_percentage"] + 1.28 * std_estimate + fraud_penalty/2, 2)
            },
            "uncertainty_sources": [
                "Scenario parameter uncertainty (viral, algorithm, completion rates)",
                "Fraud assessment uncertainty",
                "Attribution model selection bias",
                "Conversion rate variation by content quality",
                "Market condition changes between forecast and execution"
            ]
        }

    return confidence_intervals
```

### Step 7: Score Against Frameworks

```python
def score_against_frameworks(roi_results, confidence_intervals, campaign_context):
    """
    Score campaign across multiple dimensions using named frameworks.
    """
    scores = {}

    # Framework 1: Engagement Quality / Fraud Detection
    fraud_score = calculate_fraud_quality_score(fraud_assessment)
    scores["engagement_authenticity"] = fraud_score

    # Framework 2: CPM/CPE/CPA & Earned Media Value
    pricing_score = calculate_pricing_efficiency_score(roi_results, campaign_context)
    scores["pricing_efficiency"] = pricing_score

    # Framework 3: Funnel/AARRR & Conversion Modeling
    conversion_score = calculate_conversion_score(roi_results, campaign_context)
    scores["conversion_quality"] = conversion_score

    # Framework 4: Marketing Attribution Models
    attribution_score = calculate_attribution_rigor_score(confidence_intervals)
    scores["attribution_rigor"] = attribution_score

    # Framework 5: FTC Disclosure & Ad Compliance
    # This is handled in sub-compliance-check, so we note its absence here
    scores["compliance_status"] = "pending_compliance_check"

    return scores

def calculate_fraud_quality_score(fraud_assessment):
    """Score based on fraud assessment from screener."""
    composite = fraud_assessment.get("composite_score", 0.5)
    # Invert: lower fraud = higher quality
    quality_score = (1 - composite) * 100
    return round(quality_score, 1)

def calculate_pricing_efficiency_score(roi_results, campaign_context):
    """Score based on pricing efficiency vs benchmarks."""
    base_roi = roi_results.get("incrementality", {}).get("base", {}).get("roi_percentage", 0)

    # Score based on ROI tiers
    if base_roi > 200:
        return 95  # Excellent efficiency
    elif base_roi > 100:
        return 80  # Good efficiency
    elif base_roi > 50:
        return 60  # Acceptable efficiency
    elif base_roi > 0:
        return 40  # Low efficiency
    else:
        return 20  # Poor efficiency

def calculate_conversion_score(roi_results, campaign_context):
    """Score based on conversion quality and likelihood."""
    base_cpa = roi_results.get("incrementality", {}).get("base", {}).get("cpa", 999999)
    target_cpa = campaign_context.get("target_cpa_max_acceptable", base_cpa * 1.2)

    if base_cpa <= target_cpa:
        return 85
    elif base_cpa <= target_cpa * 1.2:
        return 65
    elif base_cpa <= target_cpa * 1.5:
        return 45
    else:
        return 25

def calculate_attribution_rigor_score(confidence_intervals):
    """Score based on attribution confidence."""
    # Wider intervals = lower rigor score
    ci_width = (
        confidence_intervals.get("incrementality", {}).get("confidence_interval_95", {}).get("upper", 100) -
        confidence_intervals.get("incrementality", {}).get("confidence_interval_95", {}).get("lower", 0)
    )

    if ci_width < 30:
        return 90  # High confidence, narrow interval
    elif ci_width < 60:
        return 70  # Moderate confidence
    elif ci_width < 100:
        return 50  # Low confidence
    else:
        return 30  # Very low confidence
```

### Step 8: Generate Structured Output

```json
{
  "roi_forecast": {
    "recommended_model": "incrementality",
    "rationale_for_recommendation": "Incrementality model measures true lift, avoiding over-credit to influencer. Most rigorous for ROI decisions.",
    "scenarios": {
      "conservative": {
        "impressions": 36000,
        "conversions": 72,
        "revenue": 7200,
        "roi_percentage": -28.0,
        "roas": 0.72,
        "cpa": 13.89
      },
      "base": {
        "impressions": 45000,
        "conversions": 135,
        "revenue": 13500,
        "roi_percentage": 35.0,
        "roas": 1.35,
        "cpa": 7.41
      },
      "optimistic": {
        "impressions": 63000,
        "conversions": 252,
        "revenue": 25200,
        "roi_percentage": 152.0,
        "roas": 2.52,
        "cpa": 3.97
      }
    }
  },
  "attribution_model_comparison": {
    "last_click": {"base_roi": 52.5, "attribution_credit": 1.0},
    "position_based": {"base_roi": 42.0, "attribution_credit": 0.8},
    "time_decay": {"base_roi": 38.5, "attribution_credit": 0.7},
    "incrementality": {"base_roi": 35.0, "attribution_credit": 0.65}
  },
  "confidence_intervals": {
    "incrementality": {
      "base_roi": 35.0,
      "confidence_interval_95": {"lower": -5.0, "upper": 75.0},
      "confidence_interval_80": {"lower": 10.0, "upper": 60.0}
    }
  },
  "dimension_scores": {
    "engagement_authenticity": 58.0,
    "pricing_efficiency": 60.0,
    "conversion_quality": 85.0,
    "attribution_rigor": 50.0,
    "compliance_status": "pending_compliance_check"
  },
  "assumptions": [
    "Baseline conversion rate of 2% based on industry averages",
    "Influencer lift multiplier of 1.6 for Reel format",
    "Incrementality rate of 65% (assumes 35% of conversions would happen anyway)",
    "No significant market condition changes between forecast and execution",
    "Attribution window of 7 days for all credit calculations"
  ],
  "devil_advocate_prompts": [
    "What if conversions would have happened anyway (organic baseline)?",
    "What if fraud assessment missed sophisticated bot networks?",
    "What if platform algorithm changes reduce reach?",
    "What if competitor activity increases during campaign?",
    "What if conversion value per action is overestimated?"
  ]
}
```

## Quality Gates

### Gate 1: Minimum Input Validation
- **Check:** All required inputs present with reasonable values
- **Pass:** Budget, conversion value, effective reach all > 0
- **Fail:** Request missing data; cannot proceed without core economics

### Gate 2: Attribution Model Documentation
- **Check:** Every attribution model is documented with description and usage
- **Pass:** All models have clear rationale and industry context
- **Fail:** Add model documentation before proceeding

### Gate 3: Assumption Transparency
- **Check:** All material assumptions are explicitly listed
- **Pass:** Every assumption has rationale and uncertainty noted
- **Fail:** Missing assumption documentation; add before output

## Outputs

### Primary Output
ROI forecast object (see Step 8) passed to `sub-compliance-check`.

### Secondary Outputs
- Devil's advocate prompts for challenge stage
- Assumption list for final disclosure
- Attribution model comparison for user decision

## Error Handling

**Error: Insufficient data for forecasting**
- Use conservative defaults from benchmarks
- Flag all defaults in assumptions
- Increase uncertainty in confidence intervals

**Error: Conversion value not provided**
- Request user input; critical for ROI calculation
- If unavailable, provide ROI range per $100 conversion value
- Note limitation prominently in output

**Error: Attribution model parameters unavailable**
- Use documented defaults from SECOND-KNOWLEDGE-BRAIN.md
- Cite source for all parameters
- Note uncertainty in model-specific confidence intervals
