from datetime import datetime, timezone
import unittest

from src.scoring.engine import ScoringConfig, score_opportunity


class TestScoringEngine(unittest.TestCase):
    def setUp(self) -> None:
        self.now = datetime(2026, 3, 1, tzinfo=timezone.utc)
        self.config = ScoringConfig(
            preferred_disciplines=("Painting", "Mixed Media"),
            preferred_cities=("Boston", "Providence"),
            trusted_sources=("TrustedFoundation",),
        )

    def test_high_fit_low_fee_recent_deadline(self) -> None:
        opp = {
            "fee_usd": 0,
            "deadline": "2026-03-05T12:00:00Z",
            "discipline": "Painting",
            "city": "Boston",
            "source": "TrustedFoundation",
        }
        result = score_opportunity(opp, self.config, now=self.now)

        self.assertEqual(result["score_breakdown"]["fee"], 20)
        self.assertEqual(result["score_breakdown"]["deadline"], 15)
        self.assertEqual(result["score_breakdown"]["discipline_fit"], 25)
        self.assertEqual(result["score_breakdown"]["location_fit"], 10)
        self.assertEqual(result["score_breakdown"]["source_confidence"], 7)
        self.assertEqual(result["score_total"], 77)

    def test_expired_deadline_penalty(self) -> None:
        opp = {
            "fee_usd": 10,
            "deadline": "2026-02-15T12:00:00Z",
            "discipline": "Photography",
            "city": "Chicago",
            "source": "Unknown",
        }
        result = score_opportunity(opp, self.config, now=self.now)
        self.assertEqual(result["score_breakdown"]["deadline"], -100)
        self.assertLess(result["score_total"], -80)


if __name__ == "__main__":
    unittest.main()
