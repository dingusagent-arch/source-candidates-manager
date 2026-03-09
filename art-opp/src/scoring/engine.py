"""Minimal rule-based scoring engine for ART-OPP opportunities."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, Mapping, Tuple


@dataclass(frozen=True)
class ScoringConfig:
    preferred_disciplines: Tuple[str, ...] = ()
    preferred_cities: Tuple[str, ...] = ()
    trusted_sources: Tuple[str, ...] = ()


def _parse_datetime(value: str) -> datetime:
    """Parse ISO-ish datetime into timezone-aware UTC datetime."""
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _days_until(deadline_iso: str, now: datetime) -> int:
    deadline = _parse_datetime(deadline_iso)
    return (deadline - now).days


def score_opportunity(
    opp: Mapping[str, object], config: ScoringConfig, now: datetime | None = None
) -> Dict[str, object]:
    """Return deterministic score + explainable breakdown.

    Required keys in opp: fee_usd, deadline, discipline, city, source.
    """
    now = now or datetime.now(timezone.utc)

    fee_usd = float(opp.get("fee_usd", 0))
    discipline = str(opp.get("discipline", "")).lower()
    city = str(opp.get("city", "")).lower()
    source = str(opp.get("source", "")).lower()

    preferred_disciplines = {d.lower() for d in config.preferred_disciplines}
    preferred_cities = {c.lower() for c in config.preferred_cities}
    trusted_sources = {s.lower() for s in config.trusted_sources}

    breakdown: Dict[str, float] = {}

    # Rule 1: Fee
    if fee_usd == 0:
        breakdown["fee"] = 20
    elif fee_usd <= 25:
        breakdown["fee"] = 10
    elif fee_usd <= 50:
        breakdown["fee"] = 3
    else:
        breakdown["fee"] = -10

    # Rule 2: Deadline window
    days = _days_until(str(opp["deadline"]), now)
    if days < 0:
        breakdown["deadline"] = -100
    elif days <= 7:
        breakdown["deadline"] = 15
    elif days <= 30:
        breakdown["deadline"] = 8
    else:
        breakdown["deadline"] = 2

    # Rule 3: Discipline fit
    breakdown["discipline_fit"] = 25 if discipline in preferred_disciplines else 0

    # Rule 4: Location fit
    breakdown["location_fit"] = 10 if city in preferred_cities else 0

    # Rule 5: Source confidence
    breakdown["source_confidence"] = 7 if source in trusted_sources else 0

    total = sum(breakdown.values())
    return {"score_total": total, "score_breakdown": breakdown}
