---
name: micro-influencer-roi-forecasting__sub-fraud-screener
description: Sub-skill of micro-influencer-roi-forecasting — Detect fake/low-quality engagement and adjust effective-reach estimates.
---

## Purpose
Systematically evaluate creator and engagement authenticity using multiple detection algorithms. Adjust effective-reach estimates downward when indicators suggest bot activity, engagement pods, or purchased followers. Provide transparency about uncertainty in fraud assessment.

## Procedure

### Step 1: Collect Engagement Metrics

Gather the following metrics from creator profiles and recent content:

```yaml
engagement_profile:
  follower_count: number
  following_count: number
  post_count: number
  average_likes_per_post: number
  average_comments_per_post: number
  average_shares_per_post: number
  average_views_per_video: number
  engagement_rate: number  # (likes+comments+shares) / followers
  follower_growth_rate_30d: number  # % change in last 30 days
  follower_growth_rate_90d: number  # % change in last 90 days
  recent_post_frequency: number  # posts per week (last 4 weeks)
  content_consistency_score: number  # similarity analysis of recent posts
```

### Step 2: Execute Fraud Detection Algorithms

#### Algorithm 1: Follower-Following Ratio Check

```python
def detect_follow_anomaly(follower_count, following_count):
    """
    Real creators typically have follower:following ratios > 10:1 for micro-influencers.
    Ratios below 2:1 often indicate follow-for-follow behavior or bot networks.
    """
    ratio = follower_count / max(1, following_count)

    if ratio < 2:
        return {
            "signal": "follow_anomaly",
            "severity": "high",
            "confidence": 0.85,
            "indicator": f"Low follower:following ratio ({ratio:.1f}:1) suggests follow-for-follow or bot activity",
            "effective_reach_discount": 0.4  # discount by 40%
        }
    elif ratio < 5:
        return {
            "signal": "follow_anomaly",
            "severity": "medium",
            "confidence": 0.60,
            "indicator": f"Moderate follower:following ratio ({ratio:.1f}:1) warrants investigation",
            "effective_reach_discount": 0.2  # discount by 20%
        }
    else:
        return {"signal": "follow_anomaly", "severity": "none", "effective_reach_discount": 0}
```

#### Algorithm 2: Engagement Rate vs Benchmark Deviation

```python
def detect_engagement_anomaly(engagement_rate, follower_count, platform):
    """
    Compare actual engagement rate against platform-specific benchmarks for follower tier.
    Engagement rates >3x benchmark often indicate purchase or pods.
    """
    benchmark = get_platform_benchmark(platform, follower_count)
    deviation_ratio = engagement_rate / benchmark

    if deviation_ratio > 5:
        return {
            "signal": "engagement_inflation",
            "severity": "critical",
            "confidence": 0.92,
            "indicator": f"Engagement rate ({engagement_rate:.1%}) is {deviation_ratio:.1f}x platform benchmark — strong signal of purchased engagement or pods",
            "effective_reach_discount": 0.6
        }
    elif deviation_ratio > 3:
        return {
            "signal": "engagement_inflation",
            "severity": "high",
            "confidence": 0.75,
            "indicator": f"Engagement rate ({engagement_rate:.1%}) is {deviation_ratio:.1f}x platform benchmark — likely artificial inflation",
            "effective_reach_discount": 0.4
        }
    elif deviation_ratio > 2:
        return {
            "signal": "engagement_inflation",
            "severity": "medium",
            "confidence": 0.55,
            "indicator": f"Engagement rate ({engagement_rate:.1%}) is {deviation_ratio:.1f}x platform benchmark — warrants investigation",
            "effective_reach_discount": 0.25
        }
    else:
        return {"signal": "engagement_inflation", "severity": "none", "effective_reach_discount": 0}
```

#### Algorithm 3: Comment Quality Analysis

```python
def detect_comment_quality(comments_sample):
    """
    Analyze a sample of recent comments for authenticity signals.
    """
    total_comments = len(comments_sample)
    authentic_signals = {
        "generic_phrases": 0,
        "emoji_only": 0,
        "repetitive_patterns": 0,
        "spam_keywords": 0,
        "contextual_relevance": 0
    }

    spam_keywords = ["buy followers", "get more likes", "follow back", "check my page"]
    generic_phrases = ["nice pic", "great", "cool", "awesome", "love it", "amazing"]

    for comment in comments_sample:
        text = comment.lower().strip()

        # Check for emoji-only comments
        if all(char in emoji_set for char in text):
            authentic_signals["emoji_only"] += 1

        # Check for generic phrases
        if any(phrase in text for phrase in generic_phrases):
            authentic_signals["generic_phrases"] += 1

        # Check for spam keywords
        if any(kw in text for kw in spam_keywords):
            authentic_signals["spam_keywords"] += 1

        # Check for contextual relevance (has context beyond emoji/generic)
        words = text.split()
        if len(words) > 4 and not any(phrase in text for phrase in generic_phrases):
            authentic_signals["contextual_relevance"] += 1

    # Calculate quality score
    inauthentic_ratio = (
        authentic_signals["emoji_only"] +
        authentic_signals["generic_phrases"] +
        authentic_signals["spam_keywords"]
    ) / max(1, total_comments)

    if inauthentic_ratio > 0.7:
        return {
            "signal": "low_quality_comments",
            "severity": "high",
            "confidence": 0.85,
            "indicator": f"{inauthentic_ratio:.0%} of comments appear low-quality (emoji-only, generic, or spam)",
            "effective_reach_discount": 0.35
        }
    elif inauthentic_ratio > 0.4:
        return {
            "signal": "low_quality_comments",
            "severity": "medium",
            "confidence": 0.65,
            "indicator": f"{inauthentic_ratio:.0%} of comments appear low-quality",
            "effective_reach_discount": 0.2
        }
    else:
        return {"signal": "low_quality_comments", "severity": "none", "effective_reach_discount": 0}
```

#### Algorithm 4: Follower Growth Velocity Check

```python
def detect_growth_anomaly(growth_30d, growth_90d, follower_count):
    """
    Sudden follower spikes often indicate bot purchases or pod joins.
    Compare recent growth to historical velocity.
    """
    avg_daily_growth_30d = growth_30d / 30
    avg_daily_growth_90d = growth_90d / 90

    # Normalize by follower count to account for tier differences
    normalized_velocity_30d = avg_daily_growth_30d / max(1, follower_count)
    normalized_velocity_90d = avg_daily_growth_90d / max(1, follower_count)

    velocity_spike = normalized_velocity_30d / max(0.0001, normalized_velocity_90d)

    if velocity_spike > 10 and avg_daily_growth_30d > 100:
        return {
            "signal": "unnatural_growth",
            "severity": "critical",
            "confidence": 0.88,
            "indicator": f"Follower growth velocity spiked {velocity_spike:.0f}x recently — suggests bot purchase or pod join",
            "effective_reach_discount": 0.5
        }
    elif velocity_spike > 5 and avg_daily_growth_30d > 50:
        return {
            "signal": "unnatural_growth",
            "severity": "high",
            "confidence": 0.72,
            "indicator": f"Follower growth velocity elevated {velocity_spike:.0f}x — investigate for artificial growth",
            "effective_reach_discount": 0.3
        }
    else:
        return {"signal": "unnatural_growth", "severity": "none", "effective_reach_discount": 0}
```

#### Algorithm 5: Content-Engagement Consistency

```python
def detect_content_engagement_mismatch(engagement_profile):
    """
    High-quality content typically shows consistent engagement across posts.
    High variance may indicate selective boost/promotion of specific posts.
    """
    # This would require per-post engagement data
    # Placeholder for variance analysis implementation
    return {
        "signal": "content_engagement_mismatch",
        "severity": "none",
        "confidence": 0.0,
        "indicator": "Insufficient per-post data for variance analysis",
        "effective_reach_discount": 0
    }
```

### Step 3: Calculate Composite Fraud Score

Aggregate all signals into a composite assessment:

```python
def calculate_composite_fraud_score(signals):
    """
    Combine multiple fraud signals with severity weighting.
    """
    severity_weights = {"none": 0, "low": 0.25, "medium": 0.5, "high": 0.75, "critical": 1.0}

    weighted_sum = sum(
        severity_weights[s["severity"]] * s["confidence"]
        for s in signals
    )

    max_possible = sum(severity_weights["critical"] for _ in signals)

    composite_score = weighted_sum / max(1, max_possible)

    # Map to qualitative assessment
    if composite_score > 0.7:
        assessment = "critical_fraud_risk"
        recommendation = "strong_recommend_against"
    elif composite_score > 0.5:
        assessment = "high_fraud_risk"
        recommendation = "recommend_against_without_verification"
    elif composite_score > 0.3:
        assessment = "moderate_fraud_concern"
        recommendation = "proceed_with_caution_additional_verification"
    elif composite_score > 0.15:
        assessment = "low_fraud_concern"
        recommendation = "proceed_with_minor_discounts"
    else:
        assessment = "minimal_fraud_risk"
        recommendation = "proceed_confidently"

    return {
        "composite_score": round(composite_score, 3),
        "assessment": assessment,
        "recommendation": recommendation,
        "confidence": min(0.95, composite_score + 0.1)  # Higher confidence with more signals
    }
```

### Step 4: Calculate Effective Reach Adjustment

Apply the maximum discount across all signals (conservative approach):

```python
def calculate_effective_reach(signals, estimated_impressions):
    """
    Apply fraud discounts to estimated reach.
    Uses maximum discount across signals (conservative).
    """
    max_discount = max((s.get("effective_reach_discount", 0) for s in signals), default=0)

    effective_reach = estimated_impressions * (1 - max_discount)

    return {
        "original_estimated_impressions": estimated_impressions,
        "fraud_discount_applied": max_discount,
        "effective_reach": round(effective_reach),
        "effective_reach_percentage": round(1 - max_discount, 3)
    }
```

### Step 5: Generate Structured Output

```json
{
  "fraud_assessment": {
    "composite_score": 0.42,
    "assessment": "moderate_fraud_concern",
    "recommendation": "proceed_with_caution_additional_verification",
    "confidence": 0.52
  },
  "signals_detected": [
    {
      "signal": "engagement_inflation",
      "severity": "high",
      "confidence": 0.75,
      "indicator": "Engagement rate (8.2%) is 3.4x platform benchmark — likely artificial inflation",
      "effective_reach_discount": 0.4
    },
    {
      "signal": "low_quality_comments",
      "severity": "medium",
      "confidence": 0.65,
      "indicator": "48% of comments appear low-quality (emoji-only, generic, or spam)",
      "effective_reach_discount": 0.2
    }
  ],
  "effective_reach_adjustment": {
    "original_estimated_impressions": 45000,
    "fraud_discount_applied": 0.4,
    "effective_reach": 27000,
    "effective_reach_percentage": 0.6
  },
  "verification_recommendations": [
    "Request access to creator insights for verification",
    "Cross-reference follower growth with viral content history",
    "Sample comment sections manually for authenticity",
    "Check if creator is part of known engagement pods"
  ],
  "data_limitations": [
    "Comment quality based on 50-comment sample",
    "Follower growth analysis limited to 90-day window",
    "Platform benchmarks represent averages, niche-specific variation possible"
  ]
}
```

## Quality Gates

### Gate 1: Minimum Data Availability
- **Check:** At least follower count, engagement rate, and recent post data available
- **Pass:** Core metrics present
- **Fail:** Request creator profile URL and recent post samples from user

### Gate 2: Fraud Disclosure
- **Check:** All fraud signals and their impact are explicitly documented
- **Pass:** Every signal has severity, confidence, and discount documented
- **Fail:** Missing signal documentation; fail closed (assume maximum discount)

### Gate 3: Conservative Adjustment
- **Check:** Effective reach uses maximum (most conservative) discount across signals
- **Pass:** Discount application is conservative
- **Fail:** Over-optimistic adjustment; recalculate with max discount

## Outputs

### Primary Output
Fraud assessment object (see Step 5) passed to `sub-roi-forecaster`.

### Secondary Outputs
- List of specific fraud signals for user review
- Verification recommendations
- Data limitations and uncertainty disclosure

## Error Handling

**Error: Insufficient data for algorithm**
- Log limitation in data_limitations
- Skip algorithm but continue with others
- Increase overall uncertainty in final assessment

**Error: Platform API unavailable for benchmark comparison**
- Fall back to general benchmarks from SECOND-KNOWLEDGE-BRAIN.md
- Note benchmark source as "general platform averages"
- Proceed with lower confidence on engagement_inflation signal

**Error: Comment analysis blocked by rate limiting**
- Use smaller sample size
- Note limitation in data_limitations
- Proceed with reduced confidence on comment quality assessment
