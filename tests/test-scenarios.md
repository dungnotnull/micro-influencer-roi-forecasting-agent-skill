# tests/test-scenarios.md — Micro-influencer ROI Forecasting & Measurement

Scenario-based tests for `micro-influencer-roi-forecasting` (idea #208). Minimum 5; 7 provided (incl. degraded-mode and insufficient-input edge cases).

### Scenario 1: Pricing a deal
- **User input:** "Creator wants $2k, is it worth it?"
- **Expected harness behavior:** Screens fraud, forecasts ROI vs benchmarks, recommends fair price.
- **Frameworks exercised:** Marketing attribution models (last-click, MMM, incrementality), Engagement-quality / fraud detection, CPM/CPE/CPA & earned-media-value pricing
- **Quality gate under test:** Fraud screen runs before ROI.
- **Pass criteria:** scored output produced, gate enforced, every dimension evidence-linked or assumption-marked, prioritized roadmap included.
### Scenario 2: Fake followers
- **User input:** "This creator's followers look fake"
- **Expected harness behavior:** Runs engagement-quality detection, adjusts reach.
- **Frameworks exercised:** Marketing attribution models (last-click, MMM, incrementality), Engagement-quality / fraud detection, CPM/CPE/CPA & earned-media-value pricing
- **Quality gate under test:** Effective reach discounts fraud.
- **Pass criteria:** scored output produced, gate enforced, every dimension evidence-linked or assumption-marked, prioritized roadmap included.
### Scenario 3: Measurement setup
- **User input:** "How do I track conversions?"
- **Expected harness behavior:** Designs UTM/code + incrementality plan.
- **Frameworks exercised:** Marketing attribution models (last-click, MMM, incrementality), Engagement-quality / fraud detection, CPM/CPE/CPA & earned-media-value pricing
- **Quality gate under test:** Measurement plan precedes spend.
- **Pass criteria:** scored output produced, gate enforced, every dimension evidence-linked or assumption-marked, prioritized roadmap included.
### Scenario 4: Disclosure
- **User input:** "Do they need to say #ad?"
- **Expected harness behavior:** Applies FTC disclosure rules.
- **Frameworks exercised:** Marketing attribution models (last-click, MMM, incrementality), Engagement-quality / fraud detection, CPM/CPE/CPA & earned-media-value pricing
- **Quality gate under test:** Compliance check mandatory before launch.
- **Pass criteria:** scored output produced, gate enforced, every dimension evidence-linked or assumption-marked, prioritized roadmap included.
### Scenario 5: Portfolio choice
- **User input:** "10 creators, pick the best 3"
- **Expected harness behavior:** Ranks by forecast ROI and audience-fit.
- **Frameworks exercised:** Marketing attribution models (last-click, MMM, incrementality), Engagement-quality / fraud detection, CPM/CPE/CPA & earned-media-value pricing
- **Quality gate under test:** Ranking shows assumptions and confidence.
- **Pass criteria:** scored output produced, gate enforced, every dimension evidence-linked or assumption-marked, prioritized roadmap included.
### Scenario 6: Degraded mode (offline)
- **User input:** any of the above with WebSearch/WebFetch unavailable.
- **Expected behavior:** skill falls back to `SECOND-KNOWLEDGE-BRAIN.md`, explicitly signals degraded mode, and still enforces all gates.
- **Pass criteria:** no fabricated live data; degradation disclosed.

### Scenario 7: Insufficient input
- **User input:** a vague one-line request missing key fields.
- **Expected behavior:** intake sub-skill asks targeted clarifying questions instead of assuming.
- **Pass criteria:** no scored output until required inputs are gathered.

### Scenario 8: Multi-platform campaign
- **User input:** "Creator is active on TikTok, Instagram Reels, and YouTube Shorts. Which should we sponsor?"
- **Expected harness behavior:** Analyzes cross-platform audience overlap, engagement quality differences by platform, and recommends platform-specific budget allocation.
- **Frameworks exercised:** Marketing attribution models (cross-platform), CPM/CPE/CPA & earned-media-value pricing (platform-specific benchmarks), Funnel/AARRR & conversion modeling
- **Quality gate under test:** Platform-specific recommendations with evidence-based rationale.
- **Pass criteria:** scored output produced, platform comparison with evidence, gate enforced, roadmap includes platform-priority actions.

### Scenario 9: International compliance complexity
- **User input:** "UK-based creator, US-based brand, targeting EU audience. What disclosure rules apply?"
- **Expected harness behavior:** Applies FTC (US), CMA (UK), and EU/U.K. GDPR considerations; flags jurisdiction conflicts; recommends disclosure language per region.
- **Frameworks exercised:** FTC disclosure & ad-compliance standards (multi-jurisdiction), CPM/CPE/CPA & earned-media-value pricing (regional pricing differences)
- **Quality gate under test:** Compliance check catches multi-jurisdiction exposure.
- **Pass criteria:** compliance gate triggered, regional requirements documented, assumptions explicit about legal scope.

### Scenario 10: High engagement but suspicious patterns
- **User input:** "Creator has 12% engagement rate but comments feel repetitive and followers spiked in one week."
- **Expected harness behavior:** Fraud screener flags engagement pod/bot patterns; adjusts effective reach downward; provides diagnostic signals.
- **Frameworks exercised:** Engagement-quality / fraud detection, Marketing attribution models (attribution to fake vs real), CPM/CPE/CPA & earned-media-value pricing (price adjustment)
- **Quality gate under test:** Fraud detection overrides surface metrics.
- **Pass criteria:** fraud screen produces diagnostic, effective reach discounted, transparency about uncertainty.

### Scenario 11: Celebrity vs micro-influencer trade-off
- **User input:** "We have budget for one mid-tier celebrity (500k followers, 1.5% engagement) OR ten micro-influencers (10k each, 6% engagement). Which is better?"
- **Expected harness behavior:** Runs comparative forecast with reach overlap, incrementality assumptions, and risk diversification; presents both scenarios with confidence ranges.
- **Frameworks exercised:** Marketing attribution models (incrementality, MMM), CPM/CPE/CPA & earned-media-value pricing (efficiency comparison), Funnel/AARRR & conversion modeling
- **Quality gate under test:** Devil's advocate challenges concentration risk.
- **Pass criteria:** both scenarios scored, assumptions explicit about overlap, roadmap addresses risk mitigation.

### Scenario 12: Budget-constrained with high aspirations
- **User input:** "We only have $500 but want 10,000 conversions. Is this realistic?"
- **Expected harness behavior:** Honest feasibility check using benchmarks; shows required CPA vs realistic CPA; proposes budget reallocation or goal adjustment with alternatives.
- **Frameworks exercised:** CPM/CPE/CPA & earned-media-value pricing (benchmark comparisons), Funnel/AARRR & conversion modeling (conversion math)
- **Quality gate under test:** Honest assessment over false optimism.
- **Pass criteria:** feasibility documented, gap quantified, alternatives presented, no false promises.

### Scenario 13: Platform-specific algorithm quirks
- **User input:** "This creator's TikToks go viral but Instagram Stories average 200 views. Should we pay the same for both formats?"
- **Expected harness behavior:** Distinguishes platform-algorithm-driven reach vs owned-audience reach; prices by effective CPM per format; recommends format strategy.
- **Frameworks exercised:** CPM/CPE/CPA & earned-media-value pricing (format-specific valuation), Engagement-quality / fraud detection (viral vs stable engagement)
- **Quality gate under test:** Pricing reflects format-specific realities.
- **Pass criteria:** format-specific pricing with rationale, recommendation addresses portfolio balance.

### Scenario 14: Long-term partnership vs one-off
- **User input:** "Creator wants $3k/month retainer for 6 months. We usually do one-off $500 posts. Which delivers better ROI?"
- **Expected harness behavior:** Models compounding effects (audience familiarity, brand alignment, discount for bulk), risks (creative fatigue, creator burnout), and presents NPV comparison.
- **Frameworks exercised:** Marketing attribution models (multi-touch, decay curves), CPM/CPE/CPA & earned-media-value pricing (volume discounts, long-term value)
- **Quality gate under test:** Long-term assumptions explicit about diminishing returns.
- **Pass criteria:** both models scored, long-term assumptions documented, roadmap includes milestone reviews.

### Scenario 15: Product-market fit mismatch
- **User input:** "Creator's audience is Gen Z skater culture. Our product is enterprise B2B software. Will this work?"
- **Expected harness behavior:** Audience-fit analysis flags misalignment; suggests alternative creators or content repositioning; honest assessment of conversion probability.
- **Frameworks exercised:** Funnel/AARRR & conversion modeling (awareness-to-conversion leakage), CPM/CPE/CPA & earned-media-value pricing (efficiency penalty for misalignment)
- **Quality gate under test:** Honest call on low-probability conversions.
- **Pass criteria:** misalignment flagged, alternatives proposed, no false optimism, roadmap addresses pivot options.

### Scenario 16: Negative sentiment creator
- **User input:** "Creator has great engagement but recently posted controversial takes. Brand safety concern?"
- **Expected harness behavior:** Brand-safety assessment, sentiment analysis guidance, contingency planning for association risk; includes insurance/clause recommendations.
- **Frameworks exercised:** FTC disclosure & ad-compliance standards (brand safety provisions), Engagement-quality / fraud detection (sentiment quality vs engagement rate)
- **Quality gate under test:** Risk assessment precedes recommendation.
- **Pass criteria:** risk flagged with probability, mitigation options in roadmap, assumptions about brand threshold explicit.

### Scenario 17: Data access limitations
- **User input:** "Creator won't share insights data. Can we still measure ROI?"
- **Expected harness behavior:** Proposes proxy measurement (landing pages, promo codes, platform analytics), acknowledges uncertainty increase, provides lower-confidence forecasts.
- **Frameworks exercised:** Marketing attribution models (proxy-based), Funnel/AARRR & conversion modeling (measurement gaps)
- **Quality gate under test:** Transparency about data limitations.
- **Pass criteria:** proxy methods proposed, confidence range widened appropriately, limitations documented in assumptions.

### Scenario 18: Saturated niche with creator overlap
- **User input:** "Five competitors already sponsored this creator. Will our campaign stand out or blend in?"
- **Expected harness behavior:** Competitive sponsor frequency analysis, differentiation recommendations, creative format guidance to avoid fatigue.
- **Frameworks exercised:** Marketing attribution models (competitive interference), CPM/CPE/CPA & earned-media-value pricing (saturation discount)
- **Quality gate under test:** Honest assessment of diminishing returns from over-sponsorship.
- **Pass criteria:** frequency documented, differentiation in roadmap, pricing reflects saturation penalty.

## Regression Checklist
- [ ] All gates enforced on every path (compliance).
- [ ] Scores trace to citations or explicit assumptions.
- [ ] Devil's-advocate review present.
- [ ] Roadmap prioritized by impact × effort.
- [ ] Disclaimer present where applicable.
- [ ] All 18 scenarios documented with pass criteria.
- [ ] Multi-jurisdiction compliance tested.
- [ ] Edge cases (budget mismatch, product-fit, brand safety) covered.
