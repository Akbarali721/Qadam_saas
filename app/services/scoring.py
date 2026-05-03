from app import models


def calculate_pair_scores(
    initiator_items: list[dict[str, int]],
    partner_items: list[dict[str, int]],
    questions_by_id: dict[int, models.Question],
    options_by_id: dict[int, models.Option],
) -> tuple[int, dict[str, int]]:
    initiator_map = {item["question_id"]: item["option_id"] for item in initiator_items}
    partner_map = {item["question_id"]: item["option_id"] for item in partner_items}

    per_question_scores: list[int] = []
    dimension_raw: dict[str, list[int]] = {}

    for qid, question in questions_by_id.items():
        initiator_oid = initiator_map.get(qid)
        partner_oid = partner_map.get(qid)
        if initiator_oid is None or partner_oid is None:
            continue

        initiator_option = options_by_id.get(initiator_oid)
        partner_option = options_by_id.get(partner_oid)
        if initiator_option is None or partner_option is None:
            raise ValueError("Noto‘g‘ri javoblar")
        if initiator_option.question_id != qid or partner_option.question_id != qid:
            raise ValueError("Noto‘g‘ri javoblar")

        val1 = int(initiator_option.value)
        val2 = int(partner_option.value)
        diff = abs(val1 - val2)
        score = 100 - diff * 25
        score = max(0, min(100, score))

        per_question_scores.append(score)
        dimension_raw.setdefault(question.dimension, []).append(score)

    if not per_question_scores:
        raise ValueError("Not enough answers to calculate compatibility")

    total_score = max(0, min(100, int(round(sum(per_question_scores) / len(per_question_scores)))))
    dimension_scores: dict[str, int] = {
        dim: max(0, min(100, int(round(sum(vals) / len(vals)))))
        for dim, vals in dimension_raw.items()
    }
    return total_score, dimension_scores
