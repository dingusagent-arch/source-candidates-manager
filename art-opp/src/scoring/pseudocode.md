# Rule-based scoring pseudocode

```text
function score(opportunity):
    score = 0
    breakdown = {}

    # Rule 1: Fee preference
    if fee_usd == 0:
        add +20
    else if fee_usd <= 25:
        add +10
    else if fee_usd <= 50:
        add +3
    else:
        add -10

    # Rule 2: Deadline urgency window
    days = days_until(deadline)
    if days < 0:
        add -100   # expired
    else if days <= 7:
        add +15
    else if days <= 30:
        add +8
    else:
        add +2

    # Rule 3: Discipline fit (simple keyword contains)
    if discipline in preferred_disciplines:
        add +25
    else:
        add +0

    # Rule 4: Location fit
    if city in preferred_cities:
        add +10

    # Rule 5: Source confidence
    if source in trusted_sources:
        add +7

    return {
      score_total: score,
      score_breakdown: breakdown
    }
```

This is intentionally deterministic and explainable. Tune constants after validation runs.
