import json
import random
from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import select
from sqlalchemy.orm import Session as DbSession
from sqlalchemy.orm import selectinload

from app import models
from app.core.database import get_db
from app.core.templates import templates
from app.data.stress_result_profiles import (
    DIMENSION_LABELS,
    PREMIUM_TEASER_COPY,
    PREMIUM_TEASER_ITEMS,
    STRESS_LEVEL_PROFILES,
    build_stress_result_view,
    get_area_profile,
)
from app.seeds.stress_questions import STRESS_DIMENSIONS
from app.services import pdf_service

router = APIRouter(tags=["stress"])

SESSION_QUESTION_COUNT = 10


def _generate_token(db: DbSession) -> str:
    while True:
        token = uuid4().hex
        exists = db.execute(
            select(models.StressSession.id).where(models.StressSession.token == token),
        ).scalar_one_or_none()
        if exists is None:
            return token


def _get_stress_session(db: DbSession, token: str) -> models.StressSession:
    session = db.execute(
        select(models.StressSession)
        .where(models.StressSession.token == token)
        .options(selectinload(models.StressSession.result)),
    ).scalar_one_or_none()
    if session is None:
        raise HTTPException(status_code=404, detail="Stress test sessiyasi topilmadi")
    return session


def _parse_id_list(raw: str) -> list[int]:
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return []
    if not isinstance(parsed, list):
        return []
    ids: list[int] = []
    for item in parsed:
        try:
            ids.append(int(item))
        except (TypeError, ValueError):
            continue
    return ids


def _active_questions(db: DbSession) -> list[models.StressQuestion]:
    questions = list(
        db.execute(
            select(models.StressQuestion)
            .where(models.StressQuestion.is_active.is_(True))
            .options(selectinload(models.StressQuestion.options)),
        )
        .scalars()
        .all(),
    )
    return [question for question in questions if len(question.options) == 4]


def _select_question_ids(db: DbSession) -> list[int]:
    questions = _active_questions(db)
    if len(questions) < SESSION_QUESTION_COUNT:
        raise HTTPException(status_code=500, detail="Stress test savollari yetarli emas")

    by_dimension: dict[str, list[models.StressQuestion]] = {
        dimension: [] for dimension in STRESS_DIMENSIONS
    }
    for question in questions:
        if question.dimension in by_dimension:
            by_dimension[question.dimension].append(question)

    selected: list[models.StressQuestion] = []
    selected_ids: set[int] = set()
    for dimension in STRESS_DIMENSIONS:
        bucket = by_dimension.get(dimension, [])
        random.shuffle(bucket)
        for question in bucket[:2]:
            selected.append(question)
            selected_ids.add(question.id)

    remaining = [question for question in questions if question.id not in selected_ids]
    random.shuffle(remaining)
    selected.extend(remaining[: max(0, SESSION_QUESTION_COUNT - len(selected))])

    if len(selected) < SESSION_QUESTION_COUNT:
        raise HTTPException(status_code=500, detail="Stress test savollarini tanlash imkonsiz")

    random.shuffle(selected)
    return [question.id for question in selected[:SESSION_QUESTION_COUNT]]


def _get_question(db: DbSession, question_id: int) -> models.StressQuestion:
    question = db.execute(
        select(models.StressQuestion)
        .where(models.StressQuestion.id == question_id)
        .options(selectinload(models.StressQuestion.options)),
    ).scalar_one_or_none()
    if question is None:
        raise HTTPException(status_code=404, detail="Stress test savoli topilmadi")
    return question


def _answered_question_ids(db: DbSession, session_id: int) -> set[int]:
    rows = db.execute(
        select(models.StressAnswer.question_id).where(models.StressAnswer.session_id == session_id),
    ).scalars()
    return {int(question_id) for question_id in rows}


def _level_for_score(total_score: int) -> str:
    if total_score <= 10:
        return "low"
    if total_score <= 20:
        return "medium"
    return "high"


def _calculate_and_store_result(db: DbSession, session: models.StressSession) -> models.StressResult:
    existing = db.execute(
        select(models.StressResult).where(models.StressResult.session_id == session.id),
    ).scalar_one_or_none()
    if existing is not None:
        return existing

    answers = list(
        db.execute(
            select(models.StressAnswer).where(models.StressAnswer.session_id == session.id),
        )
        .scalars()
        .all(),
    )
    if len(answers) < SESSION_QUESTION_COUNT:
        raise HTTPException(status_code=400, detail="Stress test hali yakunlanmagan")

    dimension_scores = {dimension: 0 for dimension in STRESS_DIMENSIONS}
    total_score = 0
    for answer in answers:
        total_score += answer.score
        if answer.dimension in dimension_scores:
            dimension_scores[answer.dimension] += answer.score

    level = _level_for_score(total_score)
    strongest_dimension = max(dimension_scores, key=lambda dimension: dimension_scores[dimension])
    level_profile = STRESS_LEVEL_PROFILES[level]
    area_profile, _ = get_area_profile(strongest_dimension)
    result = models.StressResult(
        session_id=session.id,
        total_score=total_score,
        level=level,
        strongest_dimension=strongest_dimension,
        dimension_scores=json.dumps(dimension_scores, ensure_ascii=False, sort_keys=True),
        explanation=level_profile["description"],
        recommendations=json.dumps(area_profile["advice"], ensure_ascii=False),
    )
    session.finished_at = datetime.utcnow()
    db.add(result)
    db.commit()
    db.refresh(result)
    return result


@router.get("/stress", response_class=HTMLResponse)
def stress_index(request: Request):
    return templates.TemplateResponse(request=request, name="stress/start.html")


@router.get("/stress/start", response_class=HTMLResponse)
def stress_start_page(request: Request):
    return templates.TemplateResponse(request=request, name="stress/start.html")


@router.post("/stress/start")
def stress_start(db: DbSession = Depends(get_db)):
    selected_question_ids = _select_question_ids(db)
    session = models.StressSession(
        token=_generate_token(db),
        selected_question_ids=json.dumps(selected_question_ids),
        current_index=0,
    )
    db.add(session)
    db.commit()
    return RedirectResponse(url=f"/stress/question/{session.token}", status_code=303)


@router.get("/stress/question/{session_token}", response_class=HTMLResponse)
def stress_question_page(request: Request, session_token: str, db: DbSession = Depends(get_db)):
    session = _get_stress_session(db=db, token=session_token)
    if session.result is not None:
        return RedirectResponse(url=f"/stress/result/{session_token}", status_code=303)

    selected_question_ids = _parse_id_list(session.selected_question_ids)
    if not selected_question_ids:
        raise HTTPException(status_code=500, detail="Stress test sessiyasida savollar topilmadi")

    if session.current_index >= len(selected_question_ids):
        _calculate_and_store_result(db=db, session=session)
        return RedirectResponse(url=f"/stress/result/{session_token}", status_code=303)

    question = _get_question(db=db, question_id=selected_question_ids[session.current_index])
    return templates.TemplateResponse(
        request=request,
        name="stress/question.html",
        context={
            "token": session_token,
            "question": question,
            "options": sorted(question.options, key=lambda option: option.score),
            "progress_current": session.current_index + 1,
            "progress_total": len(selected_question_ids),
        },
    )


@router.post("/stress/question/{session_token}")
async def stress_submit_answer(request: Request, session_token: str, db: DbSession = Depends(get_db)):
    session = _get_stress_session(db=db, token=session_token)
    if session.result is not None:
        return RedirectResponse(url=f"/stress/result/{session_token}", status_code=303)

    selected_question_ids = _parse_id_list(session.selected_question_ids)
    if not selected_question_ids or session.current_index >= len(selected_question_ids):
        return RedirectResponse(url=f"/stress/result/{session_token}", status_code=303)

    current_question_id = selected_question_ids[session.current_index]
    question = _get_question(db=db, question_id=current_question_id)
    option_by_id = {option.id: option for option in question.options}
    form = await request.form()
    try:
        option_id = int(str(form.get("option_id", "")).strip())
    except ValueError:
        option_id = 0

    if option_id not in option_by_id:
        return templates.TemplateResponse(
            request=request,
            name="stress/question.html",
            context={
                "token": session_token,
                "question": question,
                "options": sorted(question.options, key=lambda option: option.score),
                "progress_current": session.current_index + 1,
                "progress_total": len(selected_question_ids),
                "error": "Iltimos, javob variantini tanlang.",
            },
            status_code=400,
        )

    answered_ids = _answered_question_ids(db=db, session_id=session.id)
    if current_question_id not in answered_ids:
        option = option_by_id[option_id]
        db.add(
            models.StressAnswer(
                session_id=session.id,
                question_id=question.id,
                option_id=option.id,
                score=option.score,
                dimension=question.dimension,
            ),
        )
    session.current_index += 1

    if session.current_index >= len(selected_question_ids):
        db.flush()
        _calculate_and_store_result(db=db, session=session)
        return RedirectResponse(url=f"/stress/result/{session_token}", status_code=303)

    db.commit()
    return RedirectResponse(url=f"/stress/question/{session_token}", status_code=303)


@router.get("/stress/result/{session_token}", response_class=HTMLResponse)
def stress_result_page(request: Request, session_token: str, db: DbSession = Depends(get_db)):
    session = _get_stress_session(db=db, token=session_token)
    result = session.result
    if result is None:
        selected_question_ids = _parse_id_list(session.selected_question_ids)
        if session.current_index < len(selected_question_ids):
            return RedirectResponse(url=f"/stress/question/{session_token}", status_code=303)
        result = _calculate_and_store_result(db=db, session=session)
    premium = None
    if session.is_premium:
        report = pdf_service.build_premium_report(db=db, test_type="stress", token=session_token)
        premium = report.as_context() if report else None

    result_view = build_stress_result_view(result)

    return templates.TemplateResponse(
        request=request,
        name="stress/result.html",
        context={
            "token": session_token,
            "is_premium": session.is_premium,
            "payment_status": session.payment_status,
            "result": result,
            "result_view": result_view,
            "level_profile": result_view["level_profile"],
            "area_profile": result_view["area_profile"],
            "area_found": result_view["area_found"],
            "max_score": result_view["max_score"],
            "overview_summary": result_view["overview_summary"],
            "hero_paragraphs": result_view["hero_paragraphs"],
            "strongest_area_title": result_view["strongest_area_title"],
            "dimension_scores": result.dimension_scores_dict,
            "dimension_labels": DIMENSION_LABELS,
            "premium": premium,
            "premium_teaser_items": PREMIUM_TEASER_ITEMS,
            "premium_teaser_copy": PREMIUM_TEASER_COPY,
        },
    )
