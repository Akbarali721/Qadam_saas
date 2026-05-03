import json
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import func
from sqlalchemy.orm import Session as DbSession

from app import crud, models, schemas
from app.admin_auth import verify_admin_token
from app.database import get_db

router = APIRouter(tags=["pages"])

BASE_DIR = Path(__file__).resolve().parent.parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@router.get("/", response_class=HTMLResponse)
def index_page(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@router.get("/share/{token}", response_class=HTMLResponse)
def share_page(request: Request, token: str, db: DbSession = Depends(get_db)):
    session = crud.get_session_by_token(db=db, token=token)
    if session is None:
        raise HTTPException(status_code=404, detail="Sessiya topilmadi")
    state = crud.get_session_quiz_state(db=db, session=session)
    if not state["initiator_answered"]:
        return RedirectResponse(url=f"/quiz/init/{token}", status_code=303)
    base = str(request.base_url).rstrip("/")
    return templates.TemplateResponse(
        request=request,
        name="share.html",
        context={
            "token": token,
            "initiator_name": session.initiator_name,
            "partner_start_url": f"{base}/start/{token}",
            "initiator_questions_url": f"{base}/questions.html?token={token}&role=initiator",
        },
    )


@router.get("/start/{token}", response_class=HTMLResponse)
def partner_landing_page(request: Request, token: str, db: DbSession = Depends(get_db)):
    session = crud.get_session_by_token(db=db, token=token)
    if session is None:
        raise HTTPException(status_code=404, detail="Sessiya topilmadi")
    return templates.TemplateResponse(
        request=request,
        name="partner.html",
        context={
            "token": token,
            "initiator_name": session.initiator_name,
        },
    )


@router.get("/questions.html", response_class=HTMLResponse)
def questions_page(request: Request, db: DbSession = Depends(get_db)):
    token = request.query_params.get("token", "")
    role = request.query_params.get("role", "")
    questions_payload: list[dict] = []
    if token:
        session = crud.get_session_by_token(db=db, token=token)
        if session is not None:
            questions_payload = [
                schemas.QuestionRead.model_validate(question).model_dump()
                for question in crud.get_session_questions(db=db, session=session)
            ]
    return templates.TemplateResponse(
        request=request,
        name="questions.html",
        context={
            "token": token,
            "role": role,
            "questions": questions_payload,
            "questions_json": json.dumps(questions_payload, ensure_ascii=False),
        },
    )


@router.get("/quiz/init/{token}")
def initiator_quiz_page(token: str):
    return RedirectResponse(
        url=f"/questions.html?token={token}&role=initiator",
        status_code=303,
    )


@router.get("/result.html", response_class=HTMLResponse)
def result_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={"token": "", "is_premium": False},
    )


@router.get("/result/{token}", response_class=HTMLResponse)
def result_page_by_token(request: Request, token: str, db: DbSession = Depends(get_db)):
    session = crud.get_session_by_token(db=db, token=token)
    if session is None:
        raise HTTPException(status_code=404, detail="Sessiya topilmadi")
    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={"token": token, "is_premium": session.is_premium},
    )


def _admin_stats_context(db: DbSession) -> dict[str, int | str]:
    """Return safe dashboard metrics for admin page."""
    try:
        today = datetime.utcnow().date().isoformat()
        total_questions = db.query(func.count(models.Question.id)).scalar() or 0
        total_sessions = db.query(func.count(models.Session.id)).scalar() or 0
        completed_sessions = (
            db.query(func.count(models.Session.id))
            .filter(models.Session.status == "completed")
            .scalar()
            or 0
        )
        today_sessions = (
            db.query(func.count(models.Session.id))
            .filter(func.date(models.Session.created_at) == today)
            .scalar()
            or 0
        )
        result_views = db.query(func.coalesce(func.sum(models.Session.result_view_count), 0)).scalar() or 0
        premium_interest_clicks = (
            db.query(func.coalesce(func.sum(models.Session.premium_interest_count), 0)).scalar()
            or 0
        )
        premium_interest_rate = (
            (int(premium_interest_clicks) / int(result_views)) * 100
            if int(result_views) > 0
            else 0
        )
        return {
            "total_questions": int(total_questions),
            "total_sessions": int(total_sessions),
            "completed_sessions": int(completed_sessions),
            "today_sessions": int(today_sessions),
            "result_views": int(result_views),
            "premium_interest_clicks": int(premium_interest_clicks),
            "premium_interest_rate": f"{premium_interest_rate:.1f}%",
        }
    except Exception:
        # MVP-safe fallback: keep page render working even if stats query fails.
        return {
            "total_questions": "-",
            "total_sessions": "-",
            "completed_sessions": "-",
            "today_sessions": "-",
            "result_views": "-",
            "premium_interest_clicks": "-",
            "premium_interest_rate": "-",
        }


@router.get("/admin", response_class=HTMLResponse)
@router.get("/admin/", response_class=HTMLResponse)
def admin_page(
    request: Request,
    db: DbSession = Depends(get_db),
    _admin: None = Depends(verify_admin_token),
):
    return templates.TemplateResponse(
        request=request,
        name="admin.html",
        context=_admin_stats_context(db),
    )
