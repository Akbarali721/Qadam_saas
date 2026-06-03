"""Generate static/love_dimension_insights.js from Python source."""
from __future__ import annotations

import json
from pathlib import Path

from app.services import love_dimension_insights as m

BASE = Path(__file__).resolve().parent.parent
data = {
    "order": list(m.DIMENSION_ORDER),
    "labels": m.DIMENSION_LABELS,
    "statusLabels": m.STATUS_LABELS,
    "insights": m.DIMENSION_INSIGHTS,
    "differencesHasGaps": m.DIFFERENCES_HAS_GAPS,
    "differencesNoGaps": m.DIFFERENCES_NO_GAPS,
}
payload = json.dumps(data, ensure_ascii=False)

js = f"""/* Auto-synced from app/services/love_dimension_insights.py */
(function () {{
  const DATA = {payload};

  function scoreTier(score) {{
    const n = Number(score);
    if (Number.isNaN(n)) return "low";
    if (n >= 80) return "high";
    if (n >= 50) return "mid";
    return "low";
  }}

  function dimensionLabel(key) {{
    return DATA.labels[key] || key;
  }}

  function formatDimensionList(names) {{
    if (!names.length) return "";
    if (names.length === 1) return names[0];
    if (names.length === 2) return `${{names[0]}} va ${{names[1]}}`;
    return `${{names.slice(0, -1).join(", ")}} va ${{names[names.length - 1]}}`;
  }}

  function getDimensionInsight(dimensionKey, score) {{
    const tier = scoreTier(score);
    const dimCopy = DATA.insights[dimensionKey] || DATA.insights.communication;
    const tierCopy = dimCopy[tier] || dimCopy.low;
    return {{
      dimension: dimensionKey,
      label: dimensionLabel(dimensionKey),
      score,
      tier,
      statusLabel: DATA.statusLabels[tier],
      explanation: tierCopy.explanation,
      recommendation: tierCopy.recommendation,
    }};
  }}

  function buildDifferencesContent(dimensionScores) {{
    const weakNames = DATA.order
      .filter((dim) => (dimensionScores[dim] ?? 0) < 80)
      .map((dim) => dimensionLabel(dim));
    if (weakNames.length) {{
      const namesText = formatDimensionList(weakNames);
      return {{
        hasGaps: true,
        text:
          `Natijada ${{namesText}} yo‘nalishlarida biroz farq seziladi. Bu yomon belgi emas — aksincha, aynan qaysi mavzularga e’tibor berish kerakligini ko‘rsatadi.`,
        subtext: DATA.differencesHasGaps.subtext,
        recommendation: DATA.differencesHasGaps.recommendation,
      }};
    }}
    return {{
      hasGaps: false,
      text: DATA.differencesNoGaps,
      subtext: "",
      recommendation: "",
    }};
  }}

  window.LoveDimensionInsights = {{
    order: DATA.order,
    scoreTier,
    dimensionLabel,
    getDimensionInsight,
    buildDifferencesContent,
  }};
}})();
"""

out = BASE / "static" / "love_dimension_insights.js"
out.write_text(js, encoding="utf-8")
print(f"wrote {out} ({len(js)} bytes)")
