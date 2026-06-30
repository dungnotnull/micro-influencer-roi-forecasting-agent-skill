---
name: micro-influencer-roi-forecasting__sub-measurement-roadmap
description: Sub-skill of micro-influencer-roi-forecasting — Design tracking (codes/UTMs/incrementality) and a fair-pricing recommendation.
---

## Purpose
Synthesize all prior analysis into a comprehensive measurement roadmap. Design tracking infrastructure that enables accurate attribution, recommend fair pricing based on forecasts, and provide prioritized action items. All recommendations must be evidence-linked and assumptions must be explicit.

## Procedure

### Step 1: Synthesize Prior Stage Outputs

Collect from previous stages:
- Campaign context from `sub-campaign-intake`
- Fraud assessment from `sub-fraud-screener`
- ROI forecasts from `sub-roi-forecaster`
- Compliance status from `sub-compliance-check`

### Step 2: Design Tracking Infrastructure

#### 2.1 UTM Parameter Strategy

```python
def design_utm_strategy(campaign_context):
    """
    Generate UTM parameters for accurate campaign tracking.
    """
    utm_template = {
        "utm_source": {
            "value": campaign_context.get("primary_platform"),
            "purpose": "Identify traffic origin platform"
        },
        "utm_medium": {
            "value": "influencer",
            "purpose": "Distinguish from other paid media"
        },
        "utm_campaign": {
            "value": f"{campaign_context.get('campaign_name', 'campaign')}_{campaign_context.get('creator_handle', 'creator')}",
            "purpose": "Group conversions by campaign-creator pair"
        },
        "utm_content": {
            "value": campaign_context.get("content_format", "post"),
            "purpose": "Track performance by content format"
        },
        "utm_term": {
            "value": "",  # Optional for keyword tracking
            "purpose": "Track by specific term if applicable"
        }
    }

    # Generate full tracking URLs for each placement
    tracking_urls = []
    base_url = campaign_context.get("destination_url", "")

    placements = ["bio_link", "story_link", "post_caption", "video_description", "comment_pin"]

    for placement in placements:
        params = "&".join([f"{k}={v['value']}" for k, v in utm_template.items() if v["value"]])
        tracking_urls.append({
            "placement": placement,
            "full_url": f"{base_url}?{params}",
            "utm_parameters": utm_template
        })

    return {
        "strategy": "UTM-based attribution with placement granularity",
        "base_parameters": utm_template,
        "tracking_urls": tracking_urls
    }
```

#### 2.2 Promo Code Design

```python
def design_promo_codes(campaign_context):
    """
    Generate unique promo codes for tracking and attribution.
    """
    creator_handle = campaign_context.get("creator_handle", "creator").replace("@", "")
    campaign_name = campaign_context.get("campaign_name", "campaign").replace(" ", "")[:8].upper()

    # Generate code variants for testing
    code_templates = [
        f"{creator_handle[:10].upper()}10",    # 10% discount
        f"{creator_handle[:10].upper()}15",    # 15% discount
        f"{creator_handle[:10].upper()}20",    # 20% discount
        f"{campaign_name}_{creator_handle[:5].upper()}"  # Custom code
    ]

    promo_codes = []
    for template in code_templates:
        promo_codes.append({
            "code": template,
            "discount_percentage": int(template[-2:]) if template[-2:].isdigit() else 0,
            "purpose": "Track conversions and incentivize action",
            "attribution_strength": "high"  # Direct link between code and conversion
        })

    return {
        "strategy": "Unique promo codes per creator for high-confidence attribution",
        "codes": promo_codes,
        "implementation_requirements": [
            "Configure discount in e-commerce/platform backend",
            "Set code expiration date",
            "Track code usage in analytics platform"
        ]
    }
```

#### 2.3 Pixel & Event Tracking

```python
def design_pixel_tracking(campaign_context):
    """
    Define pixel events to track for conversion attribution.
    """
    primary_conversion = campaign_context.get("primary_conversion_action", "purchase")

    event_definitions = {
        "purchase": {
            "standard_events": ["Purchase", "CompleteRegistration"],
            "custom_events": ["InfluencerCampaignPurchase"],
            "parameters": ["value", "currency", "content_ids", "content_name", "num_items"],
            "attribution_window": campaign_context.get("attribution_window_days", 7)
        },
        "lead_form": {
            "standard_events": ["Lead", "CompleteRegistration"],
            "custom_events": ["InfluencerCampaignLead"],
            "parameters": ["value", "currency", "lead_type", "industry"],
            "attribution_window": campaign_context.get("attribution_window_days", 14)  # Longer for leads
        },
        "signup": {
            "standard_events": ["CompleteRegistration", "SignUp"],
            "custom_events": ["InfluencerCampaignSignup"],
            "parameters": ["value", "currency", "user_type"],
            "attribution_window": campaign_context.get("attribution_window_days", 7)
        },
        "app_install": {
            "standard_events": ["Install", "MobileAppInstall"],
            "custom_events": ["InfluencerCampaignInstall"],
            "parameters": ["app_id", "package_name", "app_version"],
            "attribution_window": campaign_context.get("attribution_window_days", 3)  # Shorter for apps
        }
    }

    definition = event_definitions.get(primary_conversion, event_definitions["purchase"])

    return {
        "conversion_action": primary_conversion,
        "standard_events_to_track": definition["standard_events"],
        "custom_events_to_create": definition["custom_events"],
        "parameters_to_capture": definition["parameters"],
        "attribution_window_days": definition["attribution_window"],
        "implementation_checklist": [
            f"Place pixel on confirmation page for {primary_conversion}",
            f"Configure {definition['standard_events'][0]} event fire",
            f"Test custom event: {definition['custom_events'][0]}",
            f"Validate parameters: {', '.join(definition['parameters'][:3])}",
            f"Set attribution window to {definition['attribution_window']} days"
        ]
    }
```

#### 2.4 Incrementality Testing Design

```python
def design_incrementality_test(campaign_context, roi_forecasts):
    """
    Design holdout test to measure true incremental lift.
    """
    # Incrementality is most valuable for campaigns with >$10k budget
    budget = campaign_context.get("total_budget", 0)

    if budget < 5000:
        recommendation = {
            "test_recommended": False,
            "rationale": "Budget below incrementality testing threshold (<$5k). Cost of test exceeds value of insights.",
            "alternative": "Use geo-based or time-based comparison instead"
        }
    else:
        recommendation = {
            "test_recommended": True,
            "test_design": {
                "method": "geo_holdout" if campaign_context.get("target_audience_description", "").lower().find("national") > -1 else "time_based",
                "holdout_percentage": 20,  # 20% of audience sees no influencer content
                "test_duration_weeks": 2,
                "power_analysis": {
                    "minimum_detectable_effect": "15% lift",
                    "statistical_power": 0.8,
                    "significance_level": 0.05
                },
                "measurement_protocol": {
                    "test_group": "Sees influencer content",
                    "control_group": "Sees brand's other marketing but no influencer content",
                    "primary_metric": campaign_context.get("primary_conversion_action", "purchase"),
                    "lift_calculation": "(test_group_rate - control_group_rate) / control_group_rate"
                }
            },
            "implementation_requirements": [
                "Audience segmentation capability",
                "Ability to suppress influencer ads for holdout group",
                "Sufficient sample size in both groups"
            ]
        }

    return recommendation
```

### Step 3: Generate Fair Pricing Recommendation

```python
def calculate_fair_pricing(campaign_context, roi_forecasts, fraud_assessment):
    """
    Recommend fair pricing based on forecasts and benchmarks.
    """
    quoted_price = campaign_context.get("pricing_proposal", {}).get("quoted_amount", 0)
    base_roi = roi_forecasts.get("incrementality", {}).get("base", {}).get("roi_percentage", 0)
    fraud_discount = fraud_assessment.get("effective_reach_adjustment", {}).get("fraud_discount_applied", 0)

    # Get pricing benchmarks from SECOND-KNOWLEDGE-BRAIN.md
    platform = campaign_context.get("primary_platform", "instagram")
    tier = campaign_context.get("creator_tier", "micro")
    content_format = campaign_context.get("content_format", "post")

    # Benchmark lookup (simplified - actual implementation queries knowledge brain)
    benchmark_cpm = get_benchmark_cpm(platform, tier, content_format)  # Returns $ per 1000 impressions

    estimated_impressions = campaign_context.get("derived_metrics", {}).get("estimated_impressions", 10000)
    effective_impressions = estimated_impressions * (1 - fraud_discount)

    # Calculate fair price based on benchmark CPM
    benchmark_based_price = (effective_impressions / 1000) * benchmark_cpm

    # Calculate price based on target ROI
    target_roi = 100  # 100% ROI (2x return)
    conversion_value = campaign_context.get("conversion_value_per_action", 50)
    target_cpa = conversion_value / (1 + target_roi / 100)

    forecasted_conversions = roi_forecasts.get("incrementality", {}).get("base", {}).get("conversions", 0)
    roi_based_price = forecasted_conversions * target_cpa

    # Take more conservative of the two methods
    recommended_price = min(benchmark_based_price, roi_based_price)

    # Generate recommendation
    if quoted_price <= recommended_price * 1.1:
        verdict = "FAIR_OR_UNDERPRICED"
        rationale = f"Quoted price (${quoted_price:,.0f}) is within 10% of our recommended fair price (${recommended_price:,.0f}). Proceed."
    elif quoted_price <= recommended_price * 1.5:
        verdict = "SLIGHTLY_OVERPRICED"
        rationale = f"Quoted price (${quoted_price:,.0f}) is {(quoted_price/recommended_price - 1)*100:.0f}% above our recommended fair price (${recommended_price:,.0f}). Consider negotiating."
    else:
        verdict = "SIGNIFICANTLY_OVERPRICED"
        rationale = f"Quoted price (${quoted_price:,.0f}) is {(quoted_price/recommended_price - 1)*100:.0f}% above our recommended fair price (${recommended_price:,.0f}). Strong recommend negotiating or seeking alternative creators."

    return {
        "pricing_verdict": verdict,
        "rationale": rationale,
        "quoted_price": quoted_price,
        "recommended_fair_price": round(recommended_price),
        "benchmark_based_pricing": {
            "benchmark_cpm": benchmark_cpm,
            "effective_impressions": round(effective_impressions),
            "calculated_price": round(benchmark_based_price)
        },
        "roi_based_pricing": {
            "target_roi_percentage": target_roi,
            "target_cpa": target_cpa,
            "forecasted_conversions": forecasted_conversions,
            "calculated_price": round(roi_based_price)
        },
        "negotiation_talking_points": [
            f"Based on {platform} {tier} benchmarks for {content_format}, fair CPM is ${benchmark_cpm:.2f}",
            f"After fraud adjustment ({fraud_discount:.0%} discount), effective reach is {round(effective_impressions):,} impressions",
            f"To achieve {target_roi}% ROI target, fair price is ${recommended_price:,.0f}",
            "Creator's engagement quality and audience fit should justify premium over benchmarks"
        ]
    }
```

### Step 4: Generate Prioritized Roadmap

```python
def generate_prioritized_roadmap(synthesis_data):
    """
    Create impact × effort ranked action items.
    """
    actions = []

    # Action 1: Implement tracking infrastructure
    actions.append({
        "priority": 1,
        "action_title": "Deploy UTM tracking and promo codes",
        "impact_score": 10,
        "effort_score": 4,
        "impact_effort_product": 40,
        "category": "foundational",
        "rationale": "Without tracking, no attribution possible. High impact, moderate effort.",
        "dependencies": [],
        "timeframe_estimate": "1-2 days",
        "owner_suggestion": "Marketing Operations",
        "success_criteria": "UTM parameters live on all creator links; promo codes functional",
        "citations": ["SECOND-KNOWLEDGE-BRAIN.md: attribution_tracking_best_practices"]
    })

    # Action 2: Address compliance issues
    compliance_status = synthesis_data.get("compliance_assessment", {})
    if compliance_status.get("blocking_issues"):
        actions.append({
            "priority": 2,
            "action_title": "Resolve compliance blocking issues",
            "impact_score": 10,
            "effort_score": 3,
            "impact_effort_product": 30,
            "category": "foundational",
            "rationale": "Campaign cannot launch without compliance. Legal and reputational risk.",
            "dependencies": [],
            "timeframe_estimate": "2-3 days",
            "owner_suggestion": "Legal + Brand Manager",
            "success_criteria": "All critical/high compliance checks pass",
            "citations": ["FTC Disclosures 101", "UK CMA Guidelines"]
        })

    # Action 3: Negotiate pricing if overpriced
    pricing = synthesis_data.get("pricing_recommendation", {})
    if pricing.get("pricing_verdict") in ["SLIGHTLY_OVERPRICED", "SIGNIFICANTLY_OVERPRICED"]:
        actions.append({
            "priority": 3,
            "action_title": "Negotiate creator pricing",
            "impact_score": 8,
            "effort_score": 3,
            "impact_effort_product": 24,
            "category": "quick_win",
            "rationale": f"Creator asking {pricing.get('quoted_price', 0):,.0f} vs recommended {pricing.get('recommended_fair_price', 0):,.0f}. Negotiation could save ${(pricing.get('quoted_price', 0) - pricing.get('recommended_fair_price', 0)):,.0f}.",
            "dependencies": [],
            "timeframe_estimate": "1 day",
            "owner_suggestion": "Brand Manager",
            "success_criteria": "Agreed price within 10% of recommendation",
            "citations": ["SECOND-KNOWLEDGE-BRAIN.md: pricing_benchmarks"]
        })

    # Action 4: Set up pixel tracking
    actions.append({
        "priority": 4,
        "action_title": "Configure conversion pixel events",
        "impact_score": 9,
        "effort_score": 5,
        "impact_effort_product": 45,
        "category": "foundational",
        "rationale": "Pixel events enable post-view attribution. Critical for accurate ROI measurement.",
        "dependencies": [],
        "timeframe_estimate": "2-3 days",
        "owner_suggestion": "Marketing Operations + Development",
        "success_criteria": "All conversion events firing correctly in staging",
        "citations": ["SECOND-KNOWLEDGE-BRAIN.md: pixel_tracking_setup"]
    })

    # Action 5: Fraud monitoring setup
    fraud_assessment = synthesis_data.get("fraud_assessment", {})
    if fraud_assessment.get("composite_score", 0) > 0.3:
        actions.append({
            "priority": 5,
            "action_title": "Implement fraud monitoring checkpoints",
            "impact_score": 7,
            "effort_score": 4,
            "impact_effort_product": 28,
            "category": "major_bet",
            "rationale": f"Fraud risk score {fraud_assessment.get('composite_score', 0):.2f} suggests monitoring needed. Checkpoints detect quality issues early.",
            "dependencies": ["Deploy UTM tracking and promo codes"],
            "timeframe_estimate": "Ongoing (weekly during campaign)",
            "owner_suggestion": "Marketing Analytics",
            "success_criteria": "Weekly fraud score reports; alerts on anomalies",
            "citations": ["SECOND-KNOWLEDGE-BRAIN.md: fraud_detection_methods"]
        })

    # Action 6: Incrementality test (if budget warrants)
    if synthesis_data.get("incrementality_test", {}).get("test_recommended"):
        actions.append({
            "priority": 6,
            "action_title": "Execute incrementality holdout test",
            "impact_score": 9,
            "effort_score": 8,
            "impact_effort_product": 72,
            "category": "major_bet",
            "rationale": "Gold-standard measurement. High effort but provides true lift vs. baseline.",
            "dependencies": ["Deploy UTM tracking and promo codes", "Configure conversion pixel events"],
            "timeframe_estimate": f"{synthesis_data.get('incrementality_test', {}).get('test_design', {}).get('test_duration_weeks', 2)} weeks",
            "owner_suggestion": "Marketing Science + Analytics",
            "success_criteria": "Statistically significant lift measurement with 80% power",
            "citations": ["SECOND-KNOWLEDGE-BRAIN.md: incrementality_testing_design"]
        })

    # Sort by priority and return
    actions.sort(key=lambda x: x["priority"])

    return {
        "total_actions": len(actions),
        "quick_wins": len([a for a in actions if a["category"] == "quick_win"]),
        "major_bets": len([a for a in actions if a["category"] == "major_bet"]),
        "foundational": len([a for a in actions if a["category"] == "foundational"]),
        "estimated_implementable_quick_wins": len([a for a in actions if a["category"] == "quick_win"]),
        "actions": actions
    }
```

### Step 5: Generate Final Structured Output

```json
{
  "measurement_roadmap": {
    "tracking_strategy": {
      "utm_parameters": {
        "utm_source": "instagram",
        "utm_medium": "influencer",
        "utm_campaign": "summer2025_@jane_creator",
        "utm_content": "reel"
      },
      "promo_codes": [
        {"code": "JANECREATOR15", "discount": 15, "attribution_strength": "high"}
      ],
      "pixel_events": {
        "standard_events": ["Purchase"],
        "custom_events": ["InfluencerCampaignPurchase"],
        "attribution_window_days": 7
      }
    },
    "incrementality_testing": {
      "test_recommended": true,
      "method": "geo_holdout",
      "holdout_percentage": 20,
      "test_duration_weeks": 2
    },
    "pricing_recommendation": {
      "pricing_verdict": "SLIGHTLY_OVERPRICED",
      "quoted_price": 2000,
      "recommended_fair_price": 1750,
      "rationale": "Quoted price is 14% above recommended fair price. Consider negotiating.",
      "negotiation_talking_points": [
        "Based on Instagram micro benchmarks for Reel, fair CPM is $35",
        "After fraud adjustment (40% discount), effective reach is 27,000 impressions",
        "To achieve 100% ROI target, fair price is $1,750"
      ]
    }
  },
  "prioritized_roadmap": {
    "total_actions": 6,
    "quick_wins": 1,
    "major_bets": 2,
    "foundational": 3,
    "actions": [
      {
        "priority": 1,
        "action_title": "Deploy UTM tracking and promo codes",
        "impact_score": 10,
        "effort_score": 4,
        "category": "foundational",
        "timeframe_estimate": "1-2 days",
        "owner_suggestion": "Marketing Operations"
      }
    ]
  },
  "dimension_scores_summary": {
    "engagement_authenticity": 58.0,
    "pricing_efficiency": 60.0,
    "conversion_quality": 85.0,
    "attribution_rigor": 50.0,
    "compliance_status": "pending"
  },
  "key_findings": [
    "Fraud assessment reveals 40% effective reach discount due to engagement anomalies",
    "ROI forecast shows 35% base case ROI under incrementality attribution",
    "2 critical compliance issues must be resolved before launch",
    "Pricing 14% above fair market value based on benchmarks"
  ],
  "assumptions_summary": [
    "Baseline conversion rate of 2% based on industry averages",
    "Incrementality rate of 65% (35% of conversions would happen anyway)",
    "Fraud assessment based on 50-comment sample and 90-day growth window",
    "Platform benchmarks represent general averages, niche-specific variation possible"
  ],
  "disclaimer": "This analysis is informational only and is not professional legal, financial, or accounting advice. Verify with licensed professionals before acting."
}
```

## Quality Gates

### Gate 1: Roadmap Prioritization
- **Check:** All actions ranked by impact × effort
- **Pass:** Actions sorted and categorized (quick_win, major_bet, foundational)
- **Fail:** Recalculate priorities; add missing impact/effort scores

### Gate 2: Evidence Linkage
- **Check:** Every recommendation cites source or states assumption
- **Pass:** All claims backed by SECOND-KNOWLEDGE-BRAIN.md or explicit assumptions
- **Fail:** Add citations or assumption labels

### Gate 3: Actionability
- **Check:** Every roadmap action has success criteria and owner suggestion
- **Pass:** All actions implementable with clear accountability
- **Fail:** Add success criteria and owner suggestions

## Outputs

### Primary Output
Measurement roadmap object (see Step 5) — the final deliverable presented to user.

### Secondary Outputs
- Tracking infrastructure specifications for implementation
- Pricing recommendation with negotiation talking points
- Prioritized action list for execution

## Error Handling

**Error: Insufficient data for pricing recommendation**
- Use conservative benchmark pricing only
- Note inability to calculate ROI-based pricing
- Recommend creator-specific audit for accurate pricing

**Error: Compliance gate not passed**
- Do NOT generate measurement roadmap
- Return compliance assessment with remediation actions
- Halt workflow until compliance resolved

**Error: Fraud assessment indicates severe risk**
- Include fraud monitoring as priority 2 action
- Recommend reconsidering campaign engagement
- Note risk prominently in findings
