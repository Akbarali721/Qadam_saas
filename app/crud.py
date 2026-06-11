from datetime import datetime
import json
import logging
import random
from uuid import uuid4

from sqlalchemy import func, select
from sqlalchemy.orm import Session
from sqlalchemy.orm import selectinload

from app import models, schemas
from app.seeds import mbti_questions, question_seeds, stress_questions
from app.services.result_text import (
    build_advice,
    build_differences_text,
    build_result_summary,
    build_zodiac_summary,
)
from app.services.scoring import calculate_pair_scores

ALLOWED_DIMENSIONS: set[str] = {
    "communication",
    "trust",
    "attention",
    "emotional_closeness",
    "future_vision",
    "boundaries",
    "responsibility",
}
ALLOWED_GENDER_TARGETS: set[str] = {"female", "male", "both"}
UZBEK_ZODIACS: tuple[str, ...] = (
    "Qo‘y",
    "Buzoq",
    "Egizaklar",
    "Qisqichbaqa",
    "Arslon",
    "Sunbula",
    "Tarozi",
    "Chayon",
    "O‘qotar",
    "Tog‘ echkisi",
    "Qovg‘a",
    "Baliq",
)

RELATIONSHIP_TYPES: tuple[str, ...] = ("married", "friends", "dating")
SESSION_QUESTION_COUNT = question_seeds.SESSION_QUESTION_COUNT
LOVE_FUNNEL_ABANDONED_AFTER_MINUTES = 30
BALANCE_DIMENSIONS: tuple[str, ...] = (
    "communication",
    "trust",
    "emotional_closeness",
    "attention",
    "future_vision",
    "boundaries",
    "responsibility",
)
MBTI_DIMENSIONS: tuple[str, ...] = ("IE", "NS", "TF", "PJ")
MBTI_POLES: tuple[str, ...] = ("I", "E", "N", "S", "T", "F", "P", "J")

QUESTION_SETS: dict[str, list[question_seeds.QuestionSeed]] = {
    "married": question_seeds.QUESTIONS_MARRIED,
    "friends": question_seeds.QUESTIONS_FRIENDS,
    "dating": question_seeds.QUESTIONS_DATING,
}

PRODUCT_SEEDS: tuple[dict[str, str | int | bool], ...] = (
    {
        "slug": "love",
        "title": "Love Test",
        "name": "Love Test",
        "description": "Two-person compatibility flow that is live today.",
        "status": "active",
        "is_active": True,
        "sort_order": 1,
        "public_path": "/",
        "admin_path": "/admin/questions",
    },
    {
        "slug": "mbti",
        "title": "MBTI",
        "name": "MBTI",
        "description": "Simple 10-question personality test with a 4-letter result.",
        "status": "active",
        "is_active": True,
        "sort_order": 2,
        "public_path": "/mbti/start",
        "admin_path": "#",
    },
    {
        "slug": "stress",
        "title": "Stress Test",
        "name": "Stress Test",
        "description": "10-question stress assessment with practical recommendations.",
        "status": "active",
        "is_active": True,
        "sort_order": 3,
        "public_path": "/stress/start",
        "admin_path": "#",
    },
)


def _validate_relationship_type(value: str) -> str:
    normalized = value.strip()
    if normalized not in RELATIONSHIP_TYPES:
        raise ValueError("relationship_type must be one of: married, friends, dating")
    return normalized


def _validate_gender_target(gender_target: str) -> str:
    normalized = gender_target.strip()
    if normalized not in ALLOWED_GENDER_TARGETS:
        raise ValueError("Gender target must be one of: female, male, both")
    return normalized


def _validate_zodiac(zodiac: str) -> str:
    normalized = zodiac.strip()
    if normalized not in UZBEK_ZODIACS:
        raise ValueError("Invalid zodiac value")
    return normalized


def _optional_zodiac(zodiac: str | None) -> str | None:
    if zodiac is None:
        return None
    normalized = zodiac.strip()
    if not normalized:
        return None
    return _validate_zodiac(normalized)


def _derive_respondent_gender(initiator_gender: str) -> str:
    normalized = initiator_gender.strip().lower()
    if normalized == "ayol":
        return "male"
    return "female"


def _generate_unique_session_token(db: Session) -> str:
    while True:
        token = uuid4().hex
        existing = db.execute(
            select(models.Session).where(models.Session.token == token),
        ).scalar_one_or_none()
        if existing is None:
            return token


def _parse_question_ids_blob(raw: str | None) -> list[int]:
    if not raw or raw.strip() in ("", "[]"):
        return []
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return []
    if not isinstance(parsed, list):
        return []
    out: list[int] = []
    for item in parsed:
        try:
            out.append(int(item))
        except (TypeError, ValueError):
            continue
    return out


def _build_balanced_question_ids_for_relationship(
    db: Session,
    relationship_type: str,
    respondent_gender: str,
    target_count: int = SESSION_QUESTION_COUNT,
) -> list[int]:
    rel = _validate_relationship_type(relationship_type)

    if target_count < 1:
        raise ValueError("target_count must be >= 1")

    # First, prefer relationship-specific questions with respondent-aware targeting.
    primary_questions = get_questions_with_options(
        db=db,
        randomized=False,
        respondent_gender=respondent_gender,
        relationship_type=rel,
    )
    pool_by_id: dict[int, models.Question] = {q.id: q for q in primary_questions}

    # If needed, widen to relationship-specific questions regardless of target.
    if len(pool_by_id) < target_count:
        rel_questions = get_questions_with_options(
            db=db,
            randomized=False,
            respondent_gender=None,
            relationship_type=rel,
        )
        for question in rel_questions:
            pool_by_id.setdefault(question.id, question)

    pool = list(pool_by_id.values())
    if len(pool) < target_count:
        raise ValueError(f"Questions pool must contain at least {target_count} items")

    by_dimension: dict[str, list[models.Question]] = {dim: [] for dim in BALANCE_DIMENSIONS}
    extras: list[models.Question] = []
    for question in pool:
        if question.dimension in by_dimension:
            by_dimension[question.dimension].append(question)
        else:
            extras.append(question)

    selected_ids: list[int] = []
    selected_set: set[int] = set()
    dims = list(BALANCE_DIMENSIONS)
    per_dim_base = target_count // len(dims)
    remainder = target_count % len(dims)

    # Balanced sampling first (equal chunks + simple remainder distribution).
    for idx, dim in enumerate(dims):
        need = per_dim_base + (1 if idx < remainder else 0)
        bucket = by_dimension.get(dim, [])
        random.shuffle(bucket)
        for question in bucket[:need]:
            if question.id not in selected_set:
                selected_set.add(question.id)
                selected_ids.append(question.id)

    if len(selected_ids) < target_count:
        leftovers = [q for q in pool if q.id not in selected_set]
        random.shuffle(leftovers)
        for question in leftovers:
            selected_set.add(question.id)
            selected_ids.append(question.id)
            if len(selected_ids) >= target_count:
                break

    if len(selected_ids) < target_count:
        raise ValueError(f"Could not select {target_count} questions for this session")
    return selected_ids[:target_count]


def get_session_questions(db: Session, session: models.Session) -> list[models.Question]:
    respondent_gender = (
        session.respondent_gender
        if session.respondent_gender in ("male", "female")
        else _derive_respondent_gender(session.initiator_gender)
    )
    stored_ids = _parse_question_ids_blob(session.questions_json)
    if not stored_ids:
        stored_ids = _build_balanced_question_ids_for_relationship(
            db=db,
            relationship_type=session.relationship_type,
            respondent_gender=respondent_gender,
            target_count=SESSION_QUESTION_COUNT,
        )
        session.questions_json = json.dumps(stored_ids)
        db.commit()
        db.refresh(session)

    if not stored_ids:
        return []

    rows = db.execute(
        select(models.Question)
        .options(selectinload(models.Question.options))
        .where(models.Question.id.in_(stored_ids)),
    ).scalars().all()
    by_id = {row.id: row for row in rows}
    return [by_id[qid] for qid in stored_ids if qid in by_id]


logger = logging.getLogger(__name__)


def _utcnow() -> datetime:
    return datetime.utcnow()


def _effective_last_activity(session: models.Session) -> datetime:
    return session.last_activity_at or session.started_at or session.created_at


def _count_session_answers(session: models.Session) -> int:
    return len(_parse_answer_blob(session.answers_initiator)) + len(
        _parse_answer_blob(session.answers_partner),
    )


def _dropoff_question_index(session: models.Session) -> int:
    if session.current_question_index > 0:
        return session.current_question_index
    init_count = len(_parse_answer_blob(session.answers_initiator))
    partner_count = len(_parse_answer_blob(session.answers_partner))
    progress = max(init_count, partner_count)
    return max(progress - 1, 0)


def touch_session_activity(
    session: models.Session,
    *,
    status: str | None = None,
    question_index: int | None = None,
) -> None:
    now = _utcnow()
    session.last_activity_at = now
    if status is not None and session.status != "completed":
        session.status = status
    if question_index is not None:
        session.current_question_index = max(question_index, 0)


def mark_session_quiz_started(db: Session, session: models.Session) -> None:
    if session.status == "completed":
        return
    now = _utcnow()
    if session.started_at is None:
        session.started_at = now
    session.last_activity_at = now
    if session.status in ("created", "started", "partner_started"):
        session.status = "in_progress"
    db.commit()
    db.refresh(session)


def update_session_quiz_progress(
    db: Session,
    session: models.Session,
    *,
    question_index: int,
) -> None:
    if session.status == "completed":
        return
    touch_session_activity(
        session,
        status="in_progress",
        question_index=question_index,
    )
    db.commit()
    db.refresh(session)


def mark_session_completed(session: models.Session) -> None:
    now = _utcnow()
    session.status = "completed"
    session.answered_at = now
    session.completed_at = now
    session.last_activity_at = now


def create_session(db: Session, payload: schemas.SessionCreate) -> models.Session:
    relationship_type = _validate_relationship_type(payload.relationship_type)
    respondent_gender = _derive_respondent_gender(payload.initiator_gender)
    questions_ids = _build_balanced_question_ids_for_relationship(
        db=db,
        relationship_type=relationship_type,
        respondent_gender=respondent_gender,
        target_count=SESSION_QUESTION_COUNT,
    )
    creator_telegram_id = (payload.creator_telegram_id or "").strip() or None
    initiator_telegram_id = (payload.initiator_telegram_id or "").strip() or None
    if not creator_telegram_id and initiator_telegram_id:
        creator_telegram_id = initiator_telegram_id
    if not initiator_telegram_id and creator_telegram_id:
        initiator_telegram_id = creator_telegram_id
    now = _utcnow()
    db_obj = models.Session(
        token=_generate_unique_session_token(db),
        creator_telegram_id=creator_telegram_id,
        initiator_telegram_id=initiator_telegram_id,
        initiator_name=payload.initiator_name.strip(),
        initiator_age=payload.initiator_age,
        initiator_gender=payload.initiator_gender,
        initiator_zodiac=_optional_zodiac(payload.initiator_zodiac),
        respondent_gender=respondent_gender,
        relationship_type=relationship_type,
        status="started",
        started_at=now,
        last_activity_at=now,
        current_question_index=0,
        answers_initiator="{}",
        answers_partner="{}",
        questions_json=json.dumps(questions_ids),
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    logger.info(
        "Saved session token=%s creator_telegram_id=%s initiator_telegram_id=%s",
        db_obj.token,
        db_obj.creator_telegram_id,
        db_obj.initiator_telegram_id,
    )
    return db_obj


def register_partner(
    db: Session,
    *,
    session: models.Session,
    payload: schemas.PartnerRegister,
) -> None:
    if session.partner_name.strip():
        raise ValueError("Hamkor allaqachon ro‘yxatdan o‘tgan")
    if payload.partner_telegram_id and not session.partner_telegram_id:
        session.partner_telegram_id = payload.partner_telegram_id
    session.partner_name = payload.partner_name.strip()
    session.partner_age = payload.partner_age
    session.partner_gender = payload.partner_gender
    z = _validate_zodiac(payload.partner_zodiac)
    session.partner_zodiac = z
    session.respondent_zodiac = z
    touch_session_activity(session, status="in_progress")
    db.commit()
    db.refresh(session)


def set_partner_telegram_id(db: Session, *, session: models.Session, telegram_id: str) -> models.Session:
    normalized = telegram_id.strip()
    if normalized and not session.partner_telegram_id:
        session.partner_telegram_id = normalized
        touch_session_activity(session)
        if session.status in ("created", "started"):
            session.status = "partner_started"
        db.commit()
        db.refresh(session)
    return session


def _parse_answer_blob(raw: str | None) -> list[dict[str, int]]:
    if not raw or raw.strip() in ("", "{}"):
        return []
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return []
    items = data.get("answers")
    if not isinstance(items, list):
        return []
    out: list[dict[str, int]] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        try:
            out.append(
                {
                    "question_id": int(item["question_id"]),
                    "option_id": int(item["option_id"]),
                },
            )
        except (KeyError, TypeError, ValueError):
            continue
    return out


def _answers_blob_complete(raw: str | None, expected: int) -> bool:
    return len(_parse_answer_blob(raw)) == expected


def build_pair_result_payload(db: Session, session: models.Session) -> dict:
    """Ikki tomon javoblari asosida moslik natijasini hisoblaydi."""
    initiator_items = _parse_answer_blob(session.answers_initiator)
    partner_items = _parse_answer_blob(session.answers_partner)
    if not initiator_items or not partner_items:
        raise ValueError("Natija uchun ikkala tomonning javoblari to‘liq bo‘lishi kerak")

    initiator_qids = {row["question_id"] for row in initiator_items}
    partner_qids = {row["question_id"] for row in partner_items}
    question_ids = initiator_qids | partner_qids
    option_ids = {row["option_id"] for row in initiator_items} | {
        row["option_id"] for row in partner_items
    }
    questions = db.execute(
        select(models.Question).where(models.Question.id.in_(question_ids)),
    ).scalars().all()
    q_by_id = {q.id: q for q in questions}
    options = db.execute(
        select(models.Option).where(models.Option.id.in_(option_ids)),
    ).scalars().all()
    opt_by_id = {o.id: o for o in options}

    total_score, dimension_scores = calculate_pair_scores(
        initiator_items=initiator_items,
        partner_items=partner_items,
        questions_by_id=q_by_id,
        options_by_id=opt_by_id,
    )
    diff_text = build_differences_text(dimension_scores)

    return {
        "score": total_score,
        "total_score": total_score,
        "dimension_scores": dimension_scores,
        "summary": build_result_summary(total_score),
        "advice": build_advice(total_score),
        "differences": diff_text,
        "initiator_zodiac": session.initiator_zodiac,
        "partner_zodiac": session.partner_zodiac or session.respondent_zodiac,
        "zodiac_summary": build_zodiac_summary(
            session.initiator_zodiac,
            session.partner_zodiac or session.respondent_zodiac,
        ),
    }


def _try_finalize_pair_session(db: Session, session: models.Session, expected_count: int) -> None:
    if not _answers_blob_complete(session.answers_initiator, expected_count):
        return
    if not _answers_blob_complete(session.answers_partner, expected_count):
        return
    existing = get_result_by_session_id(db=db, session_id=session.id)
    if existing is None:
        payload = build_pair_result_payload(db=db, session=session)
        db.add(
            models.Result(
                session_id=session.id,
                score=payload["total_score"],
                dimension_scores=json.dumps(payload["dimension_scores"], sort_keys=True),
                summary=payload["summary"],
                advice=payload["advice"],
                differences=payload["differences"],
            ),
        )
    mark_session_completed(session)


def ensure_result_for_session(db: Session, session: models.Session) -> models.Result | None:
    """Agar ikkala tomon javoblari to‘liq bo‘lsa, natijani yaratib qaytaradi."""
    existing = get_result_by_session_id(db=db, session_id=session.id)
    if existing is not None:
        return existing

    expected_count = expected_question_count(db=db, session=session)
    if not _answers_blob_complete(session.answers_initiator, expected_count):
        return None
    if not _answers_blob_complete(session.answers_partner, expected_count):
        return None

    payload = build_pair_result_payload(db=db, session=session)
    result = models.Result(
        session_id=session.id,
        score=payload["total_score"],
        dimension_scores=json.dumps(payload["dimension_scores"], sort_keys=True),
        summary=payload["summary"],
        advice=payload["advice"],
        differences=payload["differences"],
    )
    db.add(result)
    mark_session_completed(session)
    db.commit()
    db.refresh(session)
    return get_result_by_session_id(db=db, session_id=session.id)


def get_session_by_token(db: Session, token: str) -> models.Session | None:
    return db.execute(
        select(models.Session).where(models.Session.token == token),
    ).scalar_one_or_none()


def unlock_session_premium(db: Session, session: models.Session) -> models.Session:
    session.is_premium = True
    session.payment_status = "approved"
    db.commit()
    db.refresh(session)
    return session


def increment_result_view(db: Session, session: models.Session) -> int:
    session.result_view_count = (session.result_view_count or 0) + 1
    db.commit()
    db.refresh(session)
    return session.result_view_count


def record_premium_interest(db: Session, session: models.Session) -> int:
    session.premium_interest_count = (session.premium_interest_count or 0) + 1
    db.commit()
    db.refresh(session)
    return session.premium_interest_count


def get_questions_with_options(
    db: Session,
    *,
    randomized: bool = False,
    respondent_gender: str | None = None,
    relationship_type: str | None = None,
) -> list[models.Question]:
    order_clause = func.random() if randomized else models.Question.order
    query = (
        select(models.Question)
        .options(selectinload(models.Question.options))
        .order_by(order_clause)
    )
    if respondent_gender is not None:
        query = query.where(
            models.Question.gender_target.in_(("both", respondent_gender)),
        )
    if relationship_type is not None:
        rel = _validate_relationship_type(relationship_type)
        query = query.where(
            models.Question.relationship_type == rel,
        )
    return (
        db.execute(query)
        .scalars()
        .all()
    )


def _validate_dimension(dimension: str) -> str:
    normalized = dimension.strip()
    if normalized not in ALLOWED_DIMENSIONS:
        raise ValueError(
            "Dimension must be one of: communication, trust, attention, "
            "emotional_closeness, future_vision, boundaries, responsibility",
        )
    return normalized


def _validate_option_payload(options: list[schemas.AdminOptionInput]) -> None:
    if len(options) != 4:
        raise ValueError("Each question must have exactly 4 options")
    for option in options:
        if option.value < 1 or option.value > 4:
            raise ValueError("Each option value must be between 1 and 4")


def _validate_question_integrity(question: models.Question) -> None:
    if len(question.options) != 4:
        raise ValueError(f"Question {question.id} must have exactly 4 options")
    for option in question.options:
        if option.value < 1 or option.value > 4:
            raise ValueError(f"Question {question.id} has option value outside 1..4")
    _validate_dimension(question.dimension)
    _validate_gender_target(question.gender_target)


def ensure_relationship_questions_seeded(db: Session) -> None:
    """Munosabat turiga qarab savollar to‘plamini DB da mavjud qiladi (kam bo‘lsa qo‘shadi)."""
    for rel_type, seed_list in QUESTION_SETS.items():
        base = question_seeds.RELATIONSHIP_ORDER_BASE[rel_type]
        for index, question_data in enumerate(seed_list):
            global_order = base + index
            existing = db.execute(
                select(models.Question.id).where(models.Question.order == global_order),
            ).scalar_one_or_none()
            if existing is not None:
                continue

            options_data = question_data["options"]
            if len(options_data) != 4:
                raise ValueError("Each seeded question must have exactly 4 options")
            _validate_dimension(question_data["dimension"])
            _validate_gender_target(question_data["gender_target"])

            question = models.Question(
                text=question_data["text"],
                order=global_order,
                dimension=question_data["dimension"],
                gender_target=question_data["gender_target"],
                relationship_type=rel_type,
            )
            db.add(question)
            db.flush()

            for option_data in options_data:
                if option_data["weight"] < 1 or option_data["weight"] > 4:
                    raise ValueError("Each seeded option value must be between 1 and 4")
                db.add(
                    models.Option(
                        question_id=question.id,
                        text=option_data["text"],
                        value=option_data["weight"],
                    ),
                )

    db.commit()


def _validate_mbti_question_seed(question_data: mbti_questions.MbtiQuestionSeed) -> None:
    if question_data["dimension"] not in MBTI_DIMENSIONS:
        raise ValueError("MBTI question dimension must be one of: IE, NS, TF, PJ")
    options_data = question_data["options"]
    if len(options_data) != 4:
        raise ValueError("Each MBTI question must have exactly 4 options")
    for option_data in options_data:
        if option_data["pole"] not in MBTI_POLES:
            raise ValueError("MBTI option pole must be one of: I, E, N, S, T, F, P, J")
        if option_data["score"] not in (1, 2):
            raise ValueError("MBTI option score must be 1 or 2")


def ensure_mbti_questions_seeded(db: Session) -> None:
    for question_data in mbti_questions.MBTI_QUESTIONS:
        _validate_mbti_question_seed(question_data)
        existing = db.execute(
            select(models.MbtiQuestion)
            .where(
                models.MbtiQuestion.text == question_data["text"],
                models.MbtiQuestion.dimension == question_data["dimension"],
            )
            .options(selectinload(models.MbtiQuestion.options)),
        ).scalar_one_or_none()

        if existing is None:
            question = models.MbtiQuestion(
                text=question_data["text"],
                dimension=question_data["dimension"],
                is_active=True,
            )
            db.add(question)
            db.flush()
            for option_data in question_data["options"]:
                db.add(
                    models.MbtiOption(
                        question_id=question.id,
                        text=option_data["text"],
                        pole=option_data["pole"],
                        score=option_data["score"],
                    ),
                )
            continue

        existing.is_active = True
        existing.options.clear()
        db.flush()
        for option_data in question_data["options"]:
            db.add(
                models.MbtiOption(
                    question_id=existing.id,
                    text=option_data["text"],
                    pole=option_data["pole"],
                    score=option_data["score"],
                ),
            )

    db.commit()


def ensure_stress_questions_seeded(db: Session) -> None:
    stress_questions.ensure_stress_questions_seeded(db)


def ensure_products_seeded(db: Session) -> None:
    for product_data in PRODUCT_SEEDS:
        existing = db.execute(
            select(models.Product).where(models.Product.slug == product_data["slug"]),
        ).scalar_one_or_none()
        if existing is None:
            db.add(models.Product(**product_data))
            continue

        existing.title = str(product_data["title"])
        existing.name = str(product_data["name"])
        existing.description = str(product_data["description"])
        existing.status = str(product_data["status"])
        existing.is_active = bool(product_data["is_active"])
        existing.sort_order = int(product_data["sort_order"])
        existing.public_path = str(product_data["public_path"])
        existing.admin_path = str(product_data["admin_path"])
    db.commit()


def list_products(db: Session) -> list[models.Product]:
    return list(
        db.execute(
            select(models.Product).order_by(models.Product.sort_order, models.Product.id),
        ).scalars().all(),
    )


def get_result_by_session_id(db: Session, session_id: int) -> models.Result | None:
    return db.execute(
        select(models.Result)
        .options(selectinload(models.Result.session))
        .where(models.Result.session_id == session_id),
    ).scalar_one_or_none()


def build_result_payload_from_row(result: models.Result) -> dict:
    session = result.session
    partner_z = None
    if session is not None:
        partner_z = session.partner_zodiac or session.respondent_zodiac
    return {
        "score": result.score,
        "total_score": result.score,
        "dimension_scores": result.dimension_scores_dict,
        "summary": result.summary,
        "advice": result.advice,
        "differences": result.differences or "",
        "initiator_zodiac": session.initiator_zodiac if session else None,
        "partner_zodiac": partner_z,
        "zodiac_summary": build_zodiac_summary(
            session.initiator_zodiac if session else None,
            partner_z,
        ),
    }


def expected_question_count(db: Session, session: models.Session) -> int:
    return len(get_session_questions(db=db, session=session))


def get_session_quiz_state(db: Session, session: models.Session) -> dict[str, bool | str]:
    n = expected_question_count(db=db, session=session)
    return {
        "initiator_name": session.initiator_name,
        "partner_registered": bool(session.partner_name.strip()),
        "initiator_answered": _answers_blob_complete(session.answers_initiator, n),
        "partner_answered": _answers_blob_complete(session.answers_partner, n),
        "status": session.status,
    }


def submit_session_answers(
    db: Session,
    session: models.Session,
    payload: schemas.AnswerSubmitRequest,
) -> bool:
    role = payload.role.strip().lower()
    if role not in ("initiator", "partner"):
        raise ValueError("role initiator yoki partner bo‘lishi kerak")

    expected_questions = get_session_questions(db=db, session=session)
    for question in expected_questions:
        _validate_question_integrity(question)
    expected_question_ids = {question.id for question in expected_questions}
    submitted_question_ids = {item.question_id for item in payload.answers}
    n = len(expected_questions)

    if len(payload.answers) != n:
        raise ValueError(f"{n} ta savol javobi kutilmoqda")
    if submitted_question_ids != expected_question_ids:
        raise ValueError("Har bir savolga bitta javob kerak")

    if role == "partner" and not session.partner_name.strip():
        raise ValueError("Hamkor avval /start/{token} orqali anketa to‘ldirishi kerak")
    if role == "initiator" and _answers_blob_complete(session.answers_initiator, n):
        raise ValueError("Boshlovchi javoblari allaqachon yuborilgan")
    if role == "partner" and _answers_blob_complete(session.answers_partner, n):
        raise ValueError("Hamkor javoblari allaqachon yuborilgan")

    option_ids = [item.option_id for item in payload.answers]
    options = db.execute(
        select(models.Option).where(models.Option.id.in_(option_ids)),
    ).scalars().all()
    options_by_id = {option.id: option for option in options}
    if len(options_by_id) != len(set(option_ids)):
        raise ValueError("Ba'zi variantlar mavjud emas")

    for item in payload.answers:
        option = options_by_id[item.option_id]
        if option.question_id != item.question_id:
            raise ValueError("Variant savolga mos emas")

    blob = json.dumps(
        {
            "answers": [
                {"question_id": item.question_id, "option_id": item.option_id}
                for item in payload.answers
            ],
        },
        sort_keys=True,
    )
    if role == "initiator":
        session.answers_initiator = blob
    else:
        session.answers_partner = blob

    touch_session_activity(session, status="in_progress", question_index=n - 1)

    db.flush()
    _try_finalize_pair_session(db=db, session=session, expected_count=n)
    db.commit()
    db.refresh(session)
    ensure_result_for_session(db=db, session=session)
    return session.status == "completed"


def admin_list_questions(db: Session) -> list[models.Question]:
    questions = get_questions_with_options(db=db)
    for question in questions:
        _validate_question_integrity(question)
    return questions


def admin_create_question(db: Session, payload: schemas.AdminQuestionCreate) -> models.Question:
    dimension = _validate_dimension(payload.dimension)
    _validate_option_payload(payload.options)

    existing = db.execute(
        select(models.Question).where(models.Question.order == payload.order),
    ).scalar_one_or_none()
    if existing is not None:
        raise ValueError("Question order must be unique")

    question = models.Question(
        text=payload.text,
        order=payload.order,
        dimension=dimension,
        gender_target=_validate_gender_target(payload.gender_target),
        relationship_type=_validate_relationship_type(payload.relationship_type),
    )
    db.add(question)
    db.flush()

    for option in payload.options:
        db.add(
            models.Option(
                question_id=question.id,
                text=option.text,
                value=option.value,
            ),
        )

    db.commit()
    db.refresh(question)
    return db.execute(
        select(models.Question)
        .options(selectinload(models.Question.options))
        .where(models.Question.id == question.id),
    ).scalar_one()


def admin_update_question(
    db: Session,
    question_id: int,
    payload: schemas.AdminQuestionUpdate,
) -> models.Question:
    dimension = _validate_dimension(payload.dimension)
    _validate_option_payload(payload.options)

    question = db.execute(
        select(models.Question)
        .options(selectinload(models.Question.options))
        .where(models.Question.id == question_id),
    ).scalar_one_or_none()
    if question is None:
        raise ValueError("Question not found")

    conflicting = db.execute(
        select(models.Question)
        .where(models.Question.order == payload.order, models.Question.id != question_id),
    ).scalar_one_or_none()
    if conflicting is not None:
        raise ValueError("Question order must be unique")

    question.text = payload.text
    question.order = payload.order
    question.dimension = dimension
    question.gender_target = _validate_gender_target(payload.gender_target)
    question.relationship_type = _validate_relationship_type(payload.relationship_type)

    for old_option in list(question.options):
        db.delete(old_option)
    db.flush()

    for option in payload.options:
        db.add(
            models.Option(
                question_id=question.id,
                text=option.text,
                value=option.value,
            ),
        )

    db.commit()
    return db.execute(
        select(models.Question)
        .options(selectinload(models.Question.options))
        .where(models.Question.id == question.id),
    ).scalar_one()


def admin_delete_question(db: Session, question_id: int) -> None:
    question = db.execute(
        select(models.Question).where(models.Question.id == question_id),
    ).scalar_one_or_none()
    if question is None:
        raise ValueError("Question not found")
    db.delete(question)
    db.commit()
