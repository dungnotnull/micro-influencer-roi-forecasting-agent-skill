---
name: micro-influencer-roi-forecasting__sub-compliance-check
description: Sub-skill of micro-influencer-roi-forecasting — Verify FTC/platform disclosure and ad-policy compliance for the planned content.
---

## Purpose
Systematically verify regulatory compliance, disclosure requirements, and platform policy adherence for influencer campaigns. Act as a quality gate before measurement roadmap generation. **IMPORTANT:** This is informational analysis only, not professional legal advice.

## Procedure

### Step 1: Determine Applicable Jurisdictions

```yaml
jurisdiction_analysis:
  campaign_regions:
    - region: string
      country_code: string
      disclosure_requirements: object
      data_protection_laws: list
      advertising_standards: list
  multi_jurisdiction:
    applies: boolean
    primary_jurisdiction: string
    secondary_jurisdictions: list
    most_strict_standard_applies: boolean
```

### Step 2: Apply FTC Endorsement Guidelines (United States)

**Framework:** FTC Endorsement Guides: Disclosures 101 for Social Media Influencers

#### Checklist 2.1: Material Connection Disclosure

```python
def check_ftc_disclosure_material_connection(campaign_context):
    """
    Verify material connection (payment, free product, etc.) is disclosed.
    """
    checks = {
        "material_connection_exists": {
            "check": "Is there a financial relationship, free product, or other benefit?",
            "result": campaign_context.get("total_budget", 0) > 0 or campaign_context.get("free_product_provided", False),
            "severity": "informational"
        },
        "disclosure_planned": {
            "check": "Has creator agreed to disclose the relationship?",
            "result": campaign_context.get("creator_disclosure_agreement", False),
            "severity": "critical"
        },
        "disclosure_placement": {
            "check": "Is disclosure in a hard-to-miss location (beginning of content, not buried)?",
            "result": campaign_context.get("disclosure_location") in ["beginning", "prominent"],
            "severity": "high"
        },
        "disclosure_clarity": {
            "check": "Is disclosure clear and unambiguous (not #ad hidden in hashtag soup)?",
            "result": campaign_context.get("disclosure_method") in ["verbal", "text_overlay", "clear_hashtag"],
            "severity": "high"
        },
        "disclosure_language": {
            "check": "Is disclosure in same language as content?",
            "result": campaign_context.get("disclosure_language_match", True),
            "severity": "medium"
        }
    }

    return checks
```

#### Checklist 2.2: Truth-in-Advertising

```python
def check_ftc_truth_in_advertising(campaign_context):
    """
    Verify claims made in content are truthful and substantiated.
    """
    checks = {
        "product_claims_substantiated": {
            "check": "Are product performance claims backed by evidence?",
            "result": campaign_context.get("claims_substantiation_documented", False),
            "severity": "high"
        },
        "no_deceptive_omissions": {
            "check": "Are material limitations or conditions disclosed?",
            "result": campaign_context.get("limitations_disclosed", False),
            "severity": "high"
        },
        "testimonial_authenticity": {
            "check": "Are testimonials based on real user experience?",
            "result": campaign_context.get("testimonial_source", "creator") == "creator",
            "severity": "high"
        },
        "no_false_endorsements": {
            "check": "Does creator actually use/like the product?",
            "result": campaign_context.get("creator_genuine_interest", True),
            "severity": "critical"
        }
    }

    return checks
```

### Step 3: Apply UK CMA Guidelines (United Kingdom)

**Framework:** Competition and Markets Authority (CMA) Influencer Marketing Guidance

```python
def check_uk_cma_compliance(campaign_context):
    """
    Verify UK-specific disclosure requirements.
    """
    checks = {
        "ad_identification_clear": {
            "check": "Is content clearly identifiable as an ad (label 'Ad', 'Advertisement', or 'Sponsored')?",
            "result": campaign_context.get("uk_ad_label_used", False),
            "severity": "critical"
        },
        "disclosure_before_engagement": {
            "check": "Is disclosure visible before user engages (likes, shares)?",
            "result": campaign_context.get("disclosure_placement", "") == "beginning",
            "severity": "high"
        },
        "no_ambiguous_labels": {
            "check": "Are ambiguous terms like 'sp', 'spon', 'collab' avoided?",
            "result": campaign_context.get("ambiguous_terms_avoided", True),
            "severity": "high"
        },
        "gift_threshold_declared": {
            "check": "For gifts > £50, is disclosure clear?",
            "result": campaign_context.get("gift_value", 0) <= 50 or campaign_context.get("gift_disclosed", False),
            "severity": "medium"
        }
    }

    return checks
```

### Step 4: Apply EU/U.K. GDPR Considerations

```python
def check_data_protection_compliance(campaign_context):
    """
    Verify data protection compliance for influencer campaigns.
    """
    checks = {
        "data_minimization": {
            "check": "Is only necessary data collected from audience?",
            "result": campaign_context.get("data_collection_minimal", True),
            "severity": "medium"
        },
        "consent_mechanism": {
            "check": "Is clear consent obtained for data collection?",
            "result": campaign_context.get("user_consent_obtained", False),
            "severity": "high"
        },
        "tracking_transparency": {
            "check": "Are tracking methods disclosed to users?",
            "result": campaign_context.get("tracking_disclosed", False),
            "severity": "medium"
        },
        "right_to_withdraw": {
            "check": "Can users opt-out of data collection?",
            "result": campaign_context.get("opt_out_available", False),
            "severity": "medium"
        }
    }

    return checks
```

### Step 5: Apply Platform-Specific Policies

#### Instagram (Meta)

```python
def check_instagram_policy(campaign_context):
    """
    Verify Instagram/Meta branded content policy compliance.
    """
    checks = {
        "branded_content_tool_used": {
            "check": "Is Meta's Branded Content Ad tool used?",
            "result": campaign_context.get("instagram_branded_tool_enabled", False),
            "severity": "medium"
        },
        "brand_account_tagged": {
            "check": "Is brand account properly tagged?",
            "result": campaign_context.get("instagram_brand_tag", "") != "",
            "severity": "low"
        },
        "no_policy_violating_content": {
            "check": "Does content comply with Instagram Community Guidelines?",
            "result": campaign_context.get("content_policy_check", "unknown"),
            "severity": "high"
        }
    }

    return checks
```

#### TikTok

```python
def check_tiktok_policy(campaign_context):
    """
    Verify TikTok promotional content policy compliance.
    """
    checks = {
        "disclosure_conspicuous": {
            "check": "Is disclosure in video itself, not just caption?",
            "result": campaign_context.get("tiktok_video_disclosure", False),
            "severity": "high"
        },
        "hashtag_disclosure_adequate": {
            "check": "If hashtag used, is it #ad, #advertisement, or #sponsored (not ambiguous)?",
            "result": campaign_context.get("tiktok_hashtag_type", "") in ["#ad", "#advertisement", "#sponsored"],
            "severity": "high"
        },
        "no_minors_targeting": {
            "check": "Does campaign comply with TikTok's minor protection policies?",
            "result": campaign_context.get("target_audience_age_min", 18) >= 13,
            "severity": "critical"
        }
    }

    return checks
```

#### YouTube

```python
def check_youtube_policy(campaign_context):
    """
    Verify YouTube paid content disclosure compliance.
    """
    checks = {
        "video_disclosure": {
            "check": "Is payment disclosure in both video AND description?",
            "result": campaign_context.get("youtube_video_disclosure", False) and campaign_context.get("youtube_description_disclosure", False),
            "severity": "high"
        },
        "paid_content_label": {
            "check": "Is 'Includes paid promotion' label checked?",
            "result": campaign_context.get("youtube_paid_label_checked", False),
            "severity": "medium"
        }
    }

    return checks
```

### Step 6: Aggregate Compliance Status

```python
def aggregate_compliance_status(all_checks):
    """
    Combine all jurisdiction and platform checks into overall status.
    """
    severity_weights = {
        "critical": 1000,
        "high": 100,
        "medium": 10,
        "low": 1,
        "informational": 0
    }

    failed_criticals = []
    failed_highs = []
    warnings = []

    for category, checks in all_checks.items():
        for check_name, check_data in checks.items():
            if not check_data["result"]:
                severity = check_data["severity"]

                if severity == "critical":
                    failed_criticals.append(f"{category}.{check_name}")
                elif severity == "high":
                    failed_highs.append(f"{category}.{check_name}")
                elif severity in ["medium", "low"]:
                    warnings.append(f"{category}.{check_name}")

    # Determine overall status
    if failed_criticals:
        overall_status = "BLOCKING_ISSUES"
        can_proceed = False
    elif failed_highs:
        overall_status = "CRITICAL_ISSUES"
        can_proceed = False
    elif warnings:
        overall_status = "WARNINGS"
        can_proceed = True
    else:
        overall_status = "COMPLIANT"
        can_proceed = True

    return {
        "overall_status": overall_status,
        "can_proceed_to_measurement": can_proceed,
        "blocking_issues": failed_criticals + failed_highs,
        "warnings": warnings,
        "passed_checks_count": sum(len([c for c in checks.values() if c["result"]]) for checks in all_checks.values()),
        "total_checks_count": sum(len(checks) for checks in all_checks.values())
    }
```

### Step 7: Generate Remediation Guidance

```python
def generate_compliance_remediation(compliance_status):
    """
    Provide specific actions to resolve compliance issues.
    """
    remediation_actions = []

    issue_mapping = {
        "disclosure_planned": [
            "Obtain written agreement from creator to disclose material connection",
            "Add disclosure requirement to creator contract terms"
        ],
        "disclosure_placement": [
            "Move disclosure to beginning of content (first 3 seconds for video, top for posts)",
            "Ensure disclosure is not buried in caption or description"
        ],
        "disclosure_clarity": [
            "Use clear language: 'Advertisement', 'Sponsored', 'Paid partnership'",
            "Avoid ambiguous terms: 'sp', 'spon', 'collab', 'thanks'",
            "For video, include verbal disclosure or text overlay",
            "For posts, use #Ad or #Sponsored at the beginning of caption"
        ],
        "product_claims_substantiated": [
            "Document evidence for all performance claims",
            "Provide clinical studies, tests, or reliable sources for assertions",
            "Avoid superlative claims ('best', 'world's leading') without proof"
        ],
        "no_false_endorsements": [
            "Ensure creator has actually used/experienced the product",
            "Document creator's genuine interest/experience with product",
            "Avoid scripted testimonials that don't reflect creator's opinion"
        ],
        "ad_identification_clear": [
            "Use 'Ad', 'Advertisement', or 'Sponsored' label for UK audiences",
            "Place label at beginning of content, not end",
            "Ensure label is in English (same language as content)"
        ],
        "consent_mechanism": [
            "Implement clear opt-in for data collection",
            "Provide link to privacy policy",
            "Allow users to withdraw consent"
        ]
    }

    for issue in compliance_status["blocking_issues"]:
        for key, actions in issue_mapping.items():
            if key in issue:
                remediation_actions.extend([{"issue": issue, "action": action} for action in actions])

    return remediation_actions
```

### Step 8: Generate Structured Output

```json
{
  "compliance_assessment": {
    "overall_status": "CRITICAL_ISSUES",
    "can_proceed_to_measurement": false,
    "summary": "2 critical issues must be resolved before campaign launch",
    "timestamp": "2025-06-30T12:00:00Z"
  },
  "jurisdictions_covered": ["United States (FTC)", "United Kingdom (CMA)", "EU (GDPR)", "Instagram (Meta)"],
  "check_results": {
    "ftc_material_connection": {
      "disclosure_planned": {"result": false, "severity": "critical", "check": "Has creator agreed to disclose?"},
      "disclosure_placement": {"result": false, "severity": "high", "check": "Is disclosure in prominent location?"},
      "disclosure_clarity": {"result": true, "severity": "high", "check": "Is disclosure clear and unambiguous?"}
    },
    "ftc_truth_in_advertising": {
      "product_claims_substantiated": {"result": true, "severity": "high", "check": "Are claims substantiated?"},
      "no_false_endorsements": {"result": true, "severity": "critical", "check": "Does creator genuinely like product?"}
    },
    "uk_cma": {
      "ad_identification_clear": {"result": false, "severity": "critical", "check": "Is 'Ad' label used for UK?"}
    },
    "data_protection": {
      "consent_mechanism": {"result": true, "severity": "high", "check": "Is user consent obtained?"}
    },
    "instagram_policy": {
      "branded_content_tool_used": {"result": false, "severity": "medium", "check": "Is Meta Branded Content tool used?"}
    }
  },
  "blocking_issues": [
    "ftc_material_connection.disclosure_planned",
    "ftc_material_connection.disclosure_placement",
    "uk_cma.ad_identification_clear"
  ],
  "warnings": [
    "instagram_policy.branded_content_tool_used"
  ],
  "remediation_actions": [
    {
      "issue": "ftc_material_connection.disclosure_planned",
      "action": "Obtain written agreement from creator to disclose material connection"
    },
    {
      "issue": "ftc_material_connection.disclosure_placed",
      "action": "Move disclosure to beginning of content (first 3 seconds for video)"
    },
    {
      "issue": "uk_cma.ad_identification_clear",
      "action": "Use 'Advertisement' or 'Sponsored' label for UK audiences"
    }
  ],
  "disclaimer": "This compliance check is informational analysis only and is not professional legal advice. Consult with qualified legal counsel before campaign launch.",
  "resources": [
    {"title": "FTC Disclosures 101", "url": "https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers"},
    {"title": "UK CMA Influencer Marketing", "url": "https://www.gov.uk/government/publications/cma-reminds-influencers-and-brands-to-declare-ads/influencers-and-ads-cma-advice-online"},
    {"title": "Meta Branded Content Policies", "url": "https://www.facebook.com/business/help/1642118709328584"}
  ]
}
```

## Quality Gates

### Gate 1: Blocking Issues Resolution
- **Check:** No critical or high-severity compliance issues
- **Pass:** `can_proceed_to_measurement == true`
- **Fail:** Halt workflow; present remediation actions before proceeding

### Gate 2: Jurisdiction Coverage
- **Check:** All campaign jurisdictions have been assessed
- **Pass:** Every region in campaign_regions has compliance checks
- **Fail:** Request missing jurisdiction data; incomplete assessment

### Gate 3: Platform Policy Review
- **Check:** All platforms used have policy checks completed
- **Pass:** Primary and secondary platforms have policy verification
- **Fail:** Add platform-specific policy checks; incomplete coverage

## Outputs

### Primary Output
Compliance assessment object (see Step 8). **CRITICAL:** If `can_proceed_to_measurement == false`, the harness MUST halt before generating measurement roadmap.

### Secondary Outputs
- Remediation action list for issue resolution
- Regulatory resource links for user reference
- Compliance disclaimer (not legal advice)

## Error Handling

**Error: Unclear jurisdiction requirements**
- Apply most strict standard across all potential jurisdictions
- Flag uncertainty in warnings
- Recommend jurisdiction-specific legal consultation

**Error: Platform policy data unavailable**
- Document general platform best practices
- Note lack of current policy verification
- Advise manual review of platform terms

**Error: Conflicting requirements between jurisdictions**
- Apply most strict requirement (conservative approach)
- Document conflict for user awareness
- Suggest legal consultation for resolution
