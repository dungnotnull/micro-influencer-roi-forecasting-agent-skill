# CLAUDE.md — Micro-influencer ROI Forecasting & Measurement

**Skill name:** `micro-influencer-roi-forecasting`
**Source idea:** #208 (ideas.md)
**Cluster:** Marketing, Content & Branding (`marketing-content-branding`)
**Tagline:** Forecasts and measures micro-influencer campaign ROI using real engagement, fraud screening and attribution models.
**Current phase:** Phase 4 — Testing & Validation (initial build complete)

## Problem This Skill Solves
Brands overpay for micro-influencers based on vanity metrics and fake engagement. This skill screens for fraud, forecasts realistic reach/conversions and ROI, sets fair sponsorship pricing, and designs measurement, grounded in marketing-measurement and media-mix standards.

## Harness Flow Summary
1. **Intake** → `sub-campaign-intake` gathers structured inputs.
2. **Research / evidence sync** → consult `SECOND-KNOWLEDGE-BRAIN.md`; refresh via WebSearch/WebFetch when available.
3. **Gate** → compliance check (`sub-compliance-check`) runs before analysis.
4. **Analysis / scoring** → `sub-roi-forecaster` scores against the named frameworks.
5. **Challenge** → devil's-advocate review stress-tests assumptions and evidence.
6. **Synthesize** → `sub-measurement-roadmap` produces the scored deliverable + prioritized roadmap.

**Compliance gate:** `sub-compliance-check` (or the embedded compliance step) MUST pass before the final deliverable is emitted. Output is informational, not professional/legal/financial advice.

## Sub-skills
- `skills/sub-campaign-intake.md` — Capture niche, platform, creator metrics, budget, product economics and conversion goal.
- `skills/sub-fraud-screener.md` — Detect fake/low-quality engagement and adjust effective-reach estimates.
- `skills/sub-roi-forecaster.md` — Forecast reach, conversions and ROI with attribution assumptions and confidence range.
- `skills/sub-compliance-check.md` — Verify FTC/platform disclosure and ad-policy compliance for the planned content.
- `skills/sub-measurement-roadmap.md` — Design tracking (codes/UTMs/incrementality) and a fair-pricing recommendation.

## Evaluation Frameworks (world-renowned, citable)
- **Marketing attribution models (last-click, MMM, incrementality)** — Frameworks for assigning conversions to influencer touchpoints and measuring true incremental lift.
- **Engagement-quality / fraud detection** — Methods to detect fake followers, pods and bot engagement vs authentic reach.
- **CPM/CPE/CPA & earned-media-value pricing** — Standard influencer pricing and value benchmarks for fair sponsorship rates.
- **Funnel/AARRR & conversion modeling** — Mapping influencer impact across awareness-to-revenue stages.
- **FTC disclosure & ad-compliance standards** — Required sponsorship disclosure rules affecting compliant campaign design.

## Tools Required
- `WebSearch`, `WebFetch` — live evidence and trend updates (graceful degradation to the knowledge brain when unavailable).
- `Read`, `Write` — load the knowledge brain; emit the deliverable.
- `Bash` — run `tools/knowledge_updater.py` (crawl4ai pipeline).

## Knowledge Sources
- **ArXiv / academic categories:** cs.SI, econ.GN
- [Journal of Marketing / JMR](https://www.ama.org/journal-of-marketing/) — Peer-reviewed influencer/attribution research.
- [Influencer Marketing Hub benchmarks](https://influencermarketinghub.com/) — Pricing and ROI benchmarks.
- [FTC endorsement guides](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers) — Disclosure compliance rules.
- [Platform creator/insights docs](https://creators.instagram.com/) — Engagement metric definitions.
- [Nielsen / MMM research](https://www.nielsen.com/) — Media-mix and incrementality methodology.

## Supporting Tools
- `tools/knowledge_updater.py` — crawl4ai + WebSearch pipeline that grows `SECOND-KNOWLEDGE-BRAIN.md` (recommended weekly cron).

## Active Development Tasks
- [x] Scaffold all required deliverables
- [x] Define frameworks, sub-skills and scoring dimensions
- [x] Author knowledge brain v1 and crawl pipeline
- [ ] Expand knowledge brain via first scheduled crawl
- [ ] Add adversarial/edge-case test scenarios beyond the initial 5

## Related Root Docs
- `PROJECT-detail.md` — full technical spec
- `PROJECT-DEVELOPMENT-PHASE-TRACKING.md` — phase roadmap
- `SECOND-KNOWLEDGE-BRAIN.md` — living domain knowledge base
