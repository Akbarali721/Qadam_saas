"""Verify dimension insight tiers and differences copy."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.services.love_dimension_insights import (  # noqa: E402
    build_differences_content,
    get_dimension_insight,
    score_tier,
)

JS_PATH = ROOT / "static" / "love_dimension_insights.js"


def test_score_tiers() -> None:
    assert score_tier(100) == "high"
    assert score_tier(80) == "high"
    assert score_tier(79) == "mid"
    assert score_tier(50) == "mid"
    assert score_tier(49) == "low"


def test_communication_high() -> None:
    insight = get_dimension_insight("communication", 88)
    assert insight["status_label"] == "Kuchli tomon"
    assert "muloqot yaxshi" in insight["explanation"].lower()
    assert "men shunday his qildim" in insight["recommendation"]


def test_trust_low() -> None:
    insight = get_dimension_insight("trust", 30)
    assert insight["status_label"] == "Zaif nuqta"
    assert "ehtiyotkorlik" in insight["explanation"].lower()


def test_differences_no_gaps() -> None:
    scores = {
        "communication": 88,
        "trust": 100,
        "attention": 100,
        "emotional_closeness": 88,
    }
    content = build_differences_content(scores)
    assert content["has_gaps"] is False
    assert "keskin tafovutlar ko‘rinmadi" in content["text"]


def test_differences_with_gaps() -> None:
    scores = {
        "communication": 40,
        "trust": 100,
        "attention": 65,
        "emotional_closeness": 88,
    }
    content = build_differences_content(scores)
    assert content["has_gaps"] is True
    assert "Muloqot" in content["text"]
    assert "E’tibor" in content["text"]
    assert content["subtext"]
    assert "Men ba’zan shunday his qilaman" in content["recommendation"]


def test_js_bundle() -> None:
    text = JS_PATH.read_text(encoding="utf-8")
    assert "Professional" not in text  # unrelated
    assert "getDimensionInsight" in text
    assert "Kuchli tomon" in text
    assert "Hissiy yaqinlik" in text
    assert "buildDifferencesContent" in text


def main() -> int:
    test_score_tiers()
    test_communication_high()
    test_trust_low()
    test_differences_no_gaps()
    test_differences_with_gaps()
    test_js_bundle()
    print("ALL INSIGHT TESTS PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
