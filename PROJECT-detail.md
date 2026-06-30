# PROJECT-detail.md — Micro-influencer ROI Forecasting & Measurement

## Executive Summary
`micro-influencer-roi-forecasting` is a harness skill in the **Marketing, Content & Branding** cluster (idea #208). Forecasts and measures micro-influencer campaign ROI using real engagement, fraud screening and attribution models. It executes a research-first, framework-grounded workflow that ends in a multi-dimensional score and a prioritized, effort/impact-ranked improvement roadmap.

> **Disclaimer:** This skill provides informational analysis only and is **not** professional legal, financial, tax or accounting advice. Verify with a licensed professional before acting.

## Problem Statement
Brands overpay for micro-influencers based on vanity metrics and fake engagement. This skill screens for fraud, forecasts realistic reach/conversions and ROI, sets fair sponsorship pricing, and designs measurement, grounded in marketing-measurement and media-mix standards.

## Target Users & Use Cases
- Practitioners, learners and small teams who need an expert-grade, evidence-based analysis without hiring a specialist.
- Trigger examples:
  - "Creator wants $2k, is it worth it?" → the skill runs its full harness and returns a scored deliverable.
  - "This creator's followers look fake" → the skill runs its full harness and returns a scored deliverable.
  - "How do I track conversions?" → the skill runs its full harness and returns a scored deliverable.
  - "Do they need to say #ad?" → the skill runs its full harness and returns a scored deliverable.
  - "10 creators, pick the best 3" → the skill runs its full harness and returns a scored deliverable.

## Harness Architecture
```
User input
   │
   ▼
[Stage 1 Intake]  sub-campaign-intake
   │
   ▼
[Stage 2 Research]  SECOND-KNOWLEDGE-BRAIN.md + WebSearch/WebFetch
   │
   ▼
[Stage 3 Gate]  sub-compliance-check
   │
   ▼
[Stage 4 Scoring]  sub-roi-forecaster  → score vs frameworks
   │
   ▼
[Stage 5 Challenge]  devil's-advocate review
   │
   ▼
[Stage 6 Synthesis]  sub-measurement-roadmap  → scored report + roadmap
```

## Full Sub-Skill Catalog
### `sub-campaign-intake`
- **Purpose:** Capture niche, platform, creator metrics, budget, product economics and conversion goal.
- **Inputs:** structured fields from prior stages / user.
- **Outputs:** structured record consumed by the next stage.
- **Tools:** Read, WebSearch/WebFetch (as needed).
- **Quality gate:** outputs are complete, evidence-linked, and assumptions are explicit.
### `sub-fraud-screener`
- **Purpose:** Detect fake/low-quality engagement and adjust effective-reach estimates.
- **Inputs:** structured fields from prior stages / user.
- **Outputs:** structured record consumed by the next stage.
- **Tools:** Read, WebSearch/WebFetch (as needed).
- **Quality gate:** outputs are complete, evidence-linked, and assumptions are explicit.
### `sub-roi-forecaster`
- **Purpose:** Forecast reach, conversions and ROI with attribution assumptions and confidence range.
- **Inputs:** structured fields from prior stages / user.
- **Outputs:** structured record consumed by the next stage.
- **Tools:** Read, WebSearch/WebFetch (as needed).
- **Quality gate:** outputs are complete, evidence-linked, and assumptions are explicit.
### `sub-compliance-check`
- **Purpose:** Verify FTC/platform disclosure and ad-policy compliance for the planned content.
- **Inputs:** structured fields from prior stages / user.
- **Outputs:** structured record consumed by the next stage.
- **Tools:** Read, WebSearch/WebFetch (as needed).
- **Quality gate:** outputs are complete, evidence-linked, and assumptions are explicit.
### `sub-measurement-roadmap`
- **Purpose:** Design tracking (codes/UTMs/incrementality) and a fair-pricing recommendation.
- **Inputs:** structured fields from prior stages / user.
- **Outputs:** structured record consumed by the next stage.
- **Tools:** Read, WebSearch/WebFetch (as needed).
- **Quality gate:** outputs are complete, evidence-linked, and assumptions are explicit.

## Evaluation Frameworks
1. **Marketing attribution models (last-click, MMM, incrementality)** — Frameworks for assigning conversions to influencer touchpoints and measuring true incremental lift.
2. **Engagement-quality / fraud detection** — Methods to detect fake followers, pods and bot engagement vs authentic reach.
3. **CPM/CPE/CPA & earned-media-value pricing** — Standard influencer pricing and value benchmarks for fair sponsorship rates.
4. **Funnel/AARRR & conversion modeling** — Mapping influencer impact across awareness-to-revenue stages.
5. **FTC disclosure & ad-compliance standards** — Required sponsorship disclosure rules affecting compliant campaign design.

## Scoring Dimensions
- Engagement authenticity
- Audience-fit
- Forecast ROI
- Attribution rigor
- Disclosure compliance
- Measurement readiness

Each dimension is scored 0–100 (or 1–5) with an explicit rationale and at least one cited source or stated assumption. The composite score is a transparent weighted aggregate; weights are disclosed.

## Skill File Format Specification
- Frontmatter: `name` (= `micro-influencer-roi-forecasting`), `description` (one line).
- Required sections: Role & Persona, Workflow (Harness Flow), Sub-skills Available, Tools, Output Format, Quality Gates.

## E2E Execution Flow
1. Parse request; classify the task and detect missing inputs (ask targeted questions).
2. Run intake sub-skill → structured profile.
3. Sync evidence from the knowledge brain; refresh via WebSearch/WebFetch when available; otherwise signal degraded mode.
4. Run the compliance gate — **halt and route out** on red flags.
5. Score against frameworks; record evidence per dimension.
6. Devil's-advocate pass: challenge weakest assumptions, seek disconfirming evidence.
7. Synthesize the deliverable: scored report + prioritized roadmap (effort × impact).
8. Run quality gates; only then present output.

## SECOND-KNOWLEDGE-BRAIN Integration
- Sources: ArXiv (cs.SI, econ.GN) + the authoritative domain sources listed in `CLAUDE.md`.
- Crawl config and append format are defined in `tools/knowledge_updater.py` and `SECOND-KNOWLEDGE-BRAIN.md`.

## Supporting Tools Spec — `knowledge_updater.py`
- **Inputs:** crawl query list (below), source URLs, last-run timestamp.
- **Outputs:** appended, de-duplicated, date-stamped entries in `SECOND-KNOWLEDGE-BRAIN.md`.
- **Schedule:** weekly cron.
- **Crawl queries:** `influencer marketing ROI measurement 2026`, `fake engagement bot detection influencer`, `incrementality testing influencer lift`, `micro influencer pricing benchmark`

## Quality Gates (must all pass before output)
- Every scored dimension cites a source or states an assumption.
- The applicable safety/compliance gate has passed.
- The devil's-advocate review has been performed and its objections addressed.
- The roadmap items are prioritized by effort × impact and are actionable.
- Evidence hierarchy respected (systematic review > meta-analysis > RCT/standard > expert opinion > blog).

## Test Scenarios
1. **Pricing a deal** — *User:* "Creator wants $2k, is it worth it?" → *Skill:* Screens fraud, forecasts ROI vs benchmarks, recommends fair price. (**Gate:** Fraud screen runs before ROI.)
2. **Fake followers** — *User:* "This creator's followers look fake" → *Skill:* Runs engagement-quality detection, adjusts reach. (**Gate:** Effective reach discounts fraud.)
3. **Measurement setup** — *User:* "How do I track conversions?" → *Skill:* Designs UTM/code + incrementality plan. (**Gate:** Measurement plan precedes spend.)
4. **Disclosure** — *User:* "Do they need to say #ad?" → *Skill:* Applies FTC disclosure rules. (**Gate:** Compliance check mandatory before launch.)
5. **Portfolio choice** — *User:* "10 creators, pick the best 3" → *Skill:* Ranks by forecast ROI and audience-fit. (**Gate:** Ranking shows assumptions and confidence.)

## Key Design Decisions
1. Research-first: no scored claim without a citation or explicit assumption.
2. Framework-grounded: scoring uses only the named world-renowned frameworks above.
3. Composable sub-skills (≥3) with explicit gates between stages.
4. Self-improving knowledge brain via the crawl pipeline.
5. Graceful degradation when WebSearch/WebFetch are unavailable.
