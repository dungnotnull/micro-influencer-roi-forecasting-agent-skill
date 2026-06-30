# Micro-Influencer ROI Forecasting & Measurement

> Forecasts and measures micro-influencer campaign ROI using real engagement, fraud screening, and attribution models.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Phase: Production Ready](https://img.shields.io/badge/Phase-Production%20Ready-brightgreen)](https://github.com/dungnotnull/micro-influencer-roi-forecasting-agent-skill)
[![Skill: Claude Code](https://img.shields.io/badge/Skill-Claude%20Code-blue)](https://claude.com/claude-code)

## Overview

Brands overpay for micro-influencers based on vanity metrics and fake engagement. This skill screens for fraud, forecasts realistic reach/conversions/ROI, sets fair sponsorship pricing, and designs measurement—grounded in marketing-measurement and media-mix standards.

### What It Does

- **Fraud Screening**: Detects fake followers, engagement pods, and bot activity using 5 detection algorithms
- **ROI Forecasting**: Multi-model attribution (last-click, position-based, time-decay, incrementality) with confidence intervals
- **Compliance Verification**: FTC endorsement guides, UK CMA, GDPR, and platform-specific policy checks
- **Fair Pricing**: Benchmark-based pricing recommendations with negotiation talking points
- **Measurement Design**: UTM parameters, promo codes, pixel events, and incrementality testing setup

### Key Features

- **Production-Ready**: Real implementations across 5 sub-skills with detailed procedures
- **Evidence-Driven**: Every claim cites a framework or explicit assumption
- **Quality Gates**: Compliance check and devil's-advocate review before output
- **Comprehensive Testing**: 18 test scenarios including adversarial edge cases
- **Cluster Integration**: Shared interfaces for reuse across marketing-content-branding cluster

## How It Works

The harness follows a disciplined 6-stage workflow:

1. **Intake**: Capture campaign parameters through structured inquiry with validation and completeness scoring
2. **Evidence Sync**: Load knowledge brain; refresh with live search when available
3. **Gate**: Compliance check—verify regulatory/disclosure requirements; halt on violation
4. **Score**: Multi-dimensional scoring against named frameworks with confidence ranges
5. **Challenge**: Devil's-advocate review—actively argue against your own conclusions
6. **Synthesize**: Generate scored report with prioritized roadmap and fair pricing recommendation

### Evaluation Frameworks

All scoring is grounded in world-renowned, citable frameworks:

- **Marketing Attribution Models**: Last-click, Media Mix Modeling (MMM), Incrementality Testing
- **Engagement Quality / Fraud Detection**: Bot detection, engagement pod identification
- **CPM/CPE/CPA & Earned Media Value**: Industry pricing benchmarks and fair value calculation
- **Funnel/AARRR & Conversion Modeling**: Awareness-to-revenue pipeline analysis
- **FTC Disclosure & Ad Compliance**: Regulatory adherence across jurisdictions

## Installation

### Prerequisites

- Claude Code (latest version)
- Python 3.8+ (for knowledge updater pipeline)
- Optional: crawl4ai for knowledge pipeline automation

### Setup

1. Clone this repository
2. Copy to your Claude skills directory:
   ```bash
   cp -r micro-influencer-roi-forecasting ~/.claude/skills/
   ```
3. Invoke the skill in Claude Code:
   ```
   /micro-influencer-roi-forecasting
   ```

### Knowledge Pipeline (Optional)

To enable automated knowledge updates:

```bash
cd tools/knowledge_updater
pip install -r requirements.txt
python knowledge_updater.py
```

Set up weekly cron:
```bash
0 9 * * 1 cd /path/to/skills && python tools/knowledge_updater.py
```

## Usage

### Basic Invocation

Ask Claude Code to analyze an influencer campaign:

```
"Creator @jane_fitness wants $2000 for an Instagram Reel promoting our protein powder. Is this worth it? Our target CPA is $15 and average order value is $50."
```

### What to Expect

The skill will:

1. Ask clarifying questions about campaign parameters (if needed)
2. Run fraud screening on the creator's engagement metrics
3. Forecast ROI across multiple attribution models with confidence intervals
4. Verify compliance (FTC disclosure, UK CMA, GDPR, platform policies)
5. Provide a scored report with:
   - Composite score and confidence level
   - Dimension scores (engagement authenticity, audience fit, forecast ROI, attribution rigor, disclosure compliance, measurement readiness)
   - Findings (strengths, gaps, risks)
   - Prioritized roadmap ranked by impact × effort
   - Fair pricing recommendation with negotiation talking points
   - Full sources and assumptions

### Example Output

```markdown
# Campaign Analysis: @jane_fitness — Protein Powder Promotion

## Summary & Headline Score
- **Composite Score**: 72/100
- **Confidence**: 68%
- **Recommendation**: Proceed with minor adjustments

## Dimension Scores
| Dimension | Score | Evidence/Assumption |
|-----------|-------|---------------------|
| Engagement Authenticity | 58/100 | 40% effective reach discount due to engagement anomalies |
| Audience Fit | 82/100 | Strong alignment with fitness-interested audience |
| Forecast ROI | 65/100 | 35% base case ROI under incrementality attribution |
| Attribution Rigor | 50/100 | Wide confidence interval (+/- 40 percentage points) |
| Disclosure Compliance | Pending | Awaiting compliance check results |
| Measurement Readiness | 75/100 | UTM and promo code strategy defined |

## Pricing Recommendation
- **Quoted Price**: $2,000
- **Recommended Fair Price**: $1,750
- **Verdict**: Slightly Overpriced (14% above fair value)

## Prioritized Roadmap
| Priority | Action | Impact | Effort | Category |
|----------|--------|--------|--------|----------|
| 1 | Deploy UTM tracking and promo codes | 10 | 4 | Foundational |
| 2 | Resolve compliance blocking issues | 10 | 3 | Foundational |
| 3 | Configure conversion pixel events | 9 | 5 | Foundational |
| 4 | Negotiate creator pricing | 8 | 3 | Quick Win |

## Sources & Assumptions
- FTC Endorsement Guides: Disclosures 101
- UK CMA Influencer Marketing Guidance
- Instagram micro-influencer CPM benchmarks ($35/1000 impressions)
- Assumption: 65% incrementality rate (35% of conversions would happen anyway)
```

## Sub-Skills

The skill consists of 5 production-ready sub-skills:

### 1. Campaign Intake (`sub-campaign-intake`)
Captures niche, platform, creator metrics, budget, product economics, and conversion goals through structured inquiry with validation and completeness scoring.

### 2. Fraud Screener (`sub-fraud-screener`)
Detects fake/low-quality engagement using 5 algorithms:
- Follower-following ratio check
- Engagement rate vs benchmark deviation
- Comment quality analysis
- Follower growth velocity check
- Content-engagement consistency

### 3. ROI Forecaster (`sub-roi-forecaster`)
Forecasts reach, conversions, and ROI using:
- Multi-scenario modeling (conservative, base, optimistic)
- Multi-model attribution (last-click, position-based, time-decay, incrementality)
- Confidence interval calculation
- Dimension scoring against named frameworks

### 4. Compliance Check (`sub-compliance-check`)
Verifies:
- FTC Endorsement Guides (US)
- UK CMA Guidelines (UK)
- GDPR data protection (EU)
- Platform-specific policies (Instagram, TikTok, YouTube)

### 5. Measurement Roadmap (`sub-measurement-roadmap`)
Designs:
- UTM parameter strategy
- Promo code system
- Pixel event tracking
- Incrementality testing
- Fair pricing recommendations

## Testing

Comprehensive test coverage with 18 scenarios:

- **Core scenarios** (7): Pricing, fraud, measurement, disclosure, portfolio choice, degraded mode, insufficient input
- **Adversarial scenarios** (11): Multi-platform, international compliance, suspicious engagement, celebrity vs micro, budget constraints, platform quirks, long-term partnerships, product-market fit, brand safety, data limitations, saturated niche

Run tests:
```bash
cd tests
# Verify all 18 scenarios are documented with pass criteria
```

## Documentation

- `PROJECT-detail.md` — Full technical specification
- `PROJECT-DEVELOPMENT-PHASE-TRACKING.md` — Phase-by-phase development tracking
- `docs/integration-cross-skill-wiring.md` — Cross-skill integration patterns
- `SECOND-KNOWLEDGE-BRAIN.md` — Living domain knowledge base

## Integration with Other Skills

This skill defines shared interfaces for cluster reuse:

- **Shared Campaign Intake**: Common intake pattern for marketing skills
- **Shared Multi-Dimensional Scoring**: Reusable scoring framework
- **Shared Prioritized Roadmap**: Common roadmap generation pattern

Integration points:
- Content calendar optimizer (timing and format recommendations)
- Brand voice auditor (voice compliance constraints)
- Budget simulator (scenario modeling inputs)

## Limitations & Disclaimers

**This skill provides informational analysis only and is not professional legal, financial, tax, or accounting advice.**

- Compliance recommendations should be verified with qualified legal counsel
- ROI forecasts are estimates based on available data and assumptions
- Fraud detection uses heuristics; sophisticated fraud may evade detection
- Platform policies change; verify current terms before campaign launch
- Incrementality measurements require holdout tests; assumptions used when testing unavailable

## Contributing

Contributions welcome! Areas for enhancement:

1. Additional platform policy checks (LinkedIn, Pinterest, Twitch)
2. More fraud detection algorithms (content similarity analysis, timing patterns)
3. Geographic pricing benchmarks (beyond US/UK/EU)
4. Multi-creator portfolio optimization
5. Real-time platform API integration

## Development Phases

All phases (0-5) complete:

- ✅ **Phase 0**: Research & Skill Architecture
- ✅ **Phase 1**: Core Sub-Skills (5 production-ready implementations)
- ✅ **Phase 2**: Main Harness + Quality Gates
- ✅ **Phase 3**: SECOND-KNOWLEDGE-BRAIN Pipeline
- ✅ **Phase 4**: Testing & Validation (18 comprehensive scenarios)
- ✅ **Phase 5**: Integration & Cross-Skill Wiring

## License

MIT License — see LICENSE file for details.

## Acknowledgments

Built with:
- Claude Code (Anthropic)
- FTC Endorsement Guides: Disclosures 101 for Social Media Influencers
- UK CMA Influencer Marketing Guidance
- Industry benchmarks from Influencer Marketing Hub

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=dungnotnull/micro-influencer-roi-forecasting-agent-skill&type=Date)](https://star-history.com/#dungnotnull/micro-influencer-roi-forecasting-agent-skill&Date)

---

**Made with ❤️ for data-driven influencer marketing**

*Idea #208 · Cluster: Marketing, Content & Branding*
