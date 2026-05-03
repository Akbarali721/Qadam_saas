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
from app.services import pdf_service
from app.services.mbti_profiles import generate_mbti_result, get_mbti_profile

router = APIRouter(tags=["mbti"])

SESSION_QUESTION_COUNT = 10
BALANCED_DIMENSIONS = ("IE", "NS", "TF", "PJ")
RESULT_PAIRS = (("I", "E"), ("N", "S"), ("T", "F"), ("P", "J"))


def _generate_token(db: DbSession) -> str:
    while True:
        token = uuid4().hex
        exists = db.execute(
            select(models.MbtiSession.id).where(models.MbtiSession.token == token),
        ).scalar_one_or_none()
        if exists is None:
            return token


def _get_mbti_session(db: DbSession, token: str) -> models.MbtiSession:
    session = db.execute(
        select(models.MbtiSession).where(models.MbtiSession.token == token),
    ).scalar_one_or_none()
    if session is None:
        raise HTTPException(status_code=404, detail="MBTI sessiya topilmadi")
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


def _parse_answers(raw: str) -> dict[str, int]:
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    if not isinstance(parsed, dict):
        return {}
    answers: dict[str, int] = {}
    for question_id, option_id in parsed.items():
        try:
            answers[str(int(question_id))] = int(option_id)
        except (TypeError, ValueError):
            continue
    return answers


def _active_questions(db: DbSession) -> list[models.MbtiQuestion]:
    questions = list(
        db.execute(
            select(models.MbtiQuestion)
            .where(models.MbtiQuestion.is_active.is_(True))
            .options(selectinload(models.MbtiQuestion.options)),
        )
        .scalars()
        .all(),
    )
    return [question for question in questions if len(question.options) == 4]


def _select_question_ids(db: DbSession) -> list[int]:
    questions = _active_questions(db)
    if len(questions) < SESSION_QUESTION_COUNT:
        raise HTTPException(status_code=500, detail="MBTI savollari yetarli emas")

    by_dimension: dict[str, list[models.MbtiQuestion]] = {
        dimension: [] for dimension in BALANCED_DIMENSIONS
    }
    for question in questions:
        if question.dimension in by_dimension:
            by_dimension[question.dimension].append(question)

    selected: list[models.MbtiQuestion] = []
    selected_ids: set[int] = set()
    for dimension in BALANCED_DIMENSIONS:
        bucket = by_dimension.get(dimension, [])
        random.shuffle(bucket)
        for question in bucket[:2]:
            selected.append(question)
            selected_ids.add(question.id)

    remaining = [question for question in questions if question.id not in selected_ids]
    random.shuffle(remaining)
    selected.extend(remaining[: max(0, SESSION_QUESTION_COUNT - len(selected))])

    if len(selected) < SESSION_QUESTION_COUNT:
        raise HTTPException(status_code=500, detail="MBTI savollarini tanlash imkonsiz")

    random.shuffle(selected)
    return [question.id for question in selected[:SESSION_QUESTION_COUNT]]


def _get_question(db: DbSession, question_id: int) -> models.MbtiQuestion:
    question = db.execute(
        select(models.MbtiQuestion)
        .where(models.MbtiQuestion.id == question_id)
        .options(selectinload(models.MbtiQuestion.options)),
    ).scalar_one_or_none()
    if question is None:
        raise HTTPException(status_code=404, detail="MBTI savoli topilmadi")
    return question


def _calculate_result(db: DbSession, answers: dict[str, int]) -> str:
    scores = {letter: 0 for pair in RESULT_PAIRS for letter in pair}
    option_ids = list(answers.values())
    if not option_ids:
        return "INTP"

    options = db.execute(
        select(models.MbtiOption).where(models.MbtiOption.id.in_(option_ids)),
    ).scalars()
    for option in options:
        scores[option.pole] += option.score

    return "".join(first if scores[first] >= scores[second] else second for first, second in RESULT_PAIRS)


@router.get("/mbti/start", response_class=HTMLResponse)
def mbti_start_page(request: Request):
    return templates.TemplateResponse(request=request, name="mbti/start.html")


@router.post("/mbti/start")
def mbti_start(db: DbSession = Depends(get_db)):
    selected_question_ids = _select_question_ids(db)
    session = models.MbtiSession(
        token=_generate_token(db),
        selected_question_ids=json.dumps(selected_question_ids),
        current_index=0,
        answers_json="{}",
    )
    db.add(session)
    db.commit()
    return RedirectResponse(url=f"/mbti/question/{session.token}", status_code=303)


@router.get("/mbti/question/{token}", response_class=HTMLResponse)
def mbti_question_page(request: Request, token: str, db: DbSession = Depends(get_db)):
    session = _get_mbti_session(db=db, token=token)
    if session.result_type:
        return RedirectResponse(url=f"/mbti/result/{token}", status_code=303)

    selected_question_ids = _parse_id_list(session.selected_question_ids)
    if not selected_question_ids:
        raise HTTPException(status_code=500, detail="MBTI sessiyasida savollar topilmadi")

    if session.current_index >= len(selected_question_ids):
        answers = _parse_answers(session.answers_json)
        session.result_type = _calculate_result(db=db, answers=answers)
        session.finished_at = datetime.utcnow()
        db.commit()
        return RedirectResponse(url=f"/mbti/result/{token}", status_code=303)

    question = _get_question(db=db, question_id=selected_question_ids[session.current_index])
    return templates.TemplateResponse(
        request=request,
        name="mbti/question.html",
        context={
            "token": token,
            "question": question,
            "options": sorted(question.options, key=lambda option: option.id),
            "progress_current": session.current_index + 1,
            "progress_total": len(selected_question_ids),
        },
    )


@router.post("/mbti/answer/{token}")
async def mbti_submit_answer(request: Request, token: str, db: DbSession = Depends(get_db)):
    session = _get_mbti_session(db=db, token=token)
    if session.result_type:
        return RedirectResponse(url=f"/mbti/result/{token}", status_code=303)

    selected_question_ids = _parse_id_list(session.selected_question_ids)
    if not selected_question_ids or session.current_index >= len(selected_question_ids):
        return RedirectResponse(url=f"/mbti/result/{token}", status_code=303)

    current_question_id = selected_question_ids[session.current_index]
    question = _get_question(db=db, question_id=current_question_id)
    option_ids = {option.id for option in question.options}
    form = await request.form()
    try:
        option_id = int(str(form.get("option_id", "")).strip())
    except ValueError:
        option_id = 0

    if option_id not in option_ids:
        return templates.TemplateResponse(
            request=request,
            name="mbti/question.html",
            context={
                "token": token,
                "question": question,
                "options": sorted(question.options, key=lambda option: option.id),
                "progress_current": session.current_index + 1,
                "progress_total": len(selected_question_ids),
                "error": "Iltimos, javob variantini tanlang.",
            },
            status_code=400,
        )

    answers = _parse_answers(session.answers_json)
    answers[str(current_question_id)] = option_id
    session.answers_json = json.dumps(answers, ensure_ascii=False, sort_keys=True)
    session.current_index += 1

    if session.current_index >= len(selected_question_ids):
        session.result_type = _calculate_result(db=db, answers=answers)
        session.finished_at = datetime.utcnow()
        db.commit()
        return RedirectResponse(url=f"/mbti/result/{token}", status_code=303)

    db.commit()
    return RedirectResponse(url=f"/mbti/question/{token}", status_code=303)


@router.post("/mbti/question/{token}")
async def mbti_submit_answer_legacy(request: Request, token: str, db: DbSession = Depends(get_db)):
    return await mbti_submit_answer(request=request, token=token, db=db)


@router.get("/mbti/result/{token}", response_class=HTMLResponse)
def mbti_result_page(request: Request, token: str, db: DbSession = Depends(get_db)):
    session = _get_mbti_session(db=db, token=token)
    if not session.result_type:
        return RedirectResponse(url=f"/mbti/question/{token}", status_code=303)
    result_type = session.result_type
    premium = None
    if session.is_premium:
        report = pdf_service.build_premium_report(db=db, test_type="mbti", token=token)
        premium = report.as_context() if report else None
    return templates.TemplateResponse(
        request=request,
        name="mbti/result.html",
        context={
            "token": token,
            "is_premium": session.is_premium,
            "payment_status": session.payment_status,
            "result_type": result_type,
            "profile": get_mbti_profile(result_type),
            "result_content": generate_mbti_result(result_type),
            "premium": premium,
        },
    )
