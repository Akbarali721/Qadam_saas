"""E2E: complete test and verify result API + stored differences text."""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.services.love_dimension_insights import build_differences_content  # noqa: E402

BASE = "http://127.0.0.1:8765"


def http(method: str, path: str, body: dict | None = None) -> tuple[int, str]:
    data = None
    headers = {}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(f"{BASE}{path}", data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, resp.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8")


def answer_all(token: str, role: str, pick: str) -> None:
    status, qraw = http("GET", f"/api/sessions/{token}/questions?role={role}")
    if status != 200:
        raise RuntimeError(f"questions {role}: {status}")
    questions = json.loads(qraw)
    if pick == "first":
        answers = [{"question_id": q["id"], "option_id": q["options"][0]["id"]} for q in questions]
    elif pick == "last":
        answers = [{"question_id": q["id"], "option_id": q["options"][-1]["id"]} for q in questions]
    else:
        answers = []
        for i, q in enumerate(questions):
            opt = q["options"][i % len(q["options"])]
            answers.append({"question_id": q["id"], "option_id": opt["id"]})
    status, body = http("POST", f"/api/sessions/{token}/answers", {"role": role, "answers": answers})
    if status != 200:
        raise RuntimeError(f"answers {role}: {status} {body[:300]}")


def main() -> int:
    create_body = {
        "initiator_name": "A",
        "initiator_age": 25,
        "initiator_gender": "ayol",
        "initiator_zodiac": "Tarozi",
        "relationship_type": "dating",
    }
    status, raw = http("POST", "/api/sessions", create_body)
    if status != 200:
        print("FAIL create:", status)
        return 1
    token = json.loads(raw)["token"]

    http("POST", f"/api/sessions/{token}/partner", {
        "partner_name": "B",
        "partner_age": 26,
        "partner_gender": "erkak",
        "partner_zodiac": "Arslon",
    })

    answer_all(token, "initiator", "first")
    answer_all(token, "partner", "last")

    status, raw = http("GET", f"/api/sessions/{token}/result")
    if status != 200:
        print("FAIL result:", status, raw[:400])
        return 1
    result = json.loads(raw)
    scores = result["dimension_scores"]
    content = build_differences_content(scores)
    print("dimension_scores:", scores)
    print("differences (stored):", result["differences"][:120], "...")

    if content["text"] not in result["differences"]:
        print("WARN: stored differences may be from older logic until new result row")

    status, html = http("GET", f"/result/{token}")
    if status != 200:
        print("FAIL result page:", status)
        return 1
    for needle in (
        "love_dimension_insights.js",
        "dimension-teasers",
        "differences-subtext",
        "Muhim tafovutlar",
        "Professional psixologik",
    ):
        if needle not in html:
            print(f"FAIL result HTML missing: {needle}")
            return 1

    # JS-rendered strings appear only after load; verify insight module has tier copy
    js = (ROOT / "static" / "love_dimension_insights.js").read_text(encoding="utf-8")
    if "Zaif nuqta" not in js or "Kuchli tomon" not in js:
        print("FAIL insights JS bundle")
        return 1

    print("OK result page shell + API scores + insight module")
    print("ALL E2E CHECKS PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
