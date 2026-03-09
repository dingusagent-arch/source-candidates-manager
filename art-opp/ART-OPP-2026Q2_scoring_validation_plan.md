ART-OPP-2026Q2 — Scoring Variants & Validation Plan

Baseline formula
- base = 50
- base += 10 * len(matched_tags)
- base += 20 if candidate.priority == 'high'
- base -= deadline_penalty (see below)
- score = clamp(base, 0, 100)

Variants
- Variant A (Conservative)
  - base = 40
  - +8 per matched_tag
  - +25 for high priority
  - deadline penalty: -1 per day if deadline < 30 days
- Variant B (Recall-oriented)
  - base = 30
  - +12 per matched_tag
  - +10 for high priority
  - deadline penalty: -0.5 per day under 30
  - location boost: +10 if within 50km
- Variant C (Strict-fit)
  - base = 50
  - +15 per matched_tag
  - +40 if exact match to artist primary practice
  - hard filter: exclude if fee < profile.min_fee

Edge rules
- Past deadline -> score = 0
- requires_in_person + unknown artist location -> -30
- duplicate -> merge and keep highest score

Validation (50-sample blind test)
- Human raters (3) rate 1-5 relevance
- Compute Precision@10, Recall@50, MAP, Kendall Tau vs median human
- Acceptance thresholds: Precision@10 >= 0.6, Kendall Tau >= 0.5, triage time reduction >= 30%
- If thresholds unmet: tune tag weights / priority bonuses; re-run

Weekly report metrics
- Weekly processed candidates
- Avg triage time/item
- Precision@10, Recall@50, MAP
- Approval->Follow-up rate
- Duplicates detected
- New tags added
- Open defects
