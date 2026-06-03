from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import func, select
from sqlalchemy.orm import Session as DbSession

from app import crud, models
from app.admin_auth import verify_admin_token
from app.core.database import get_db
from app.core.templates import templates
from app.services import payment_service
from app.services.stats_service import PRODUCT_SLUGS, get_love_test_funnel_stats, get_product_stats

router = APIRouter(tags=["admin-dashboard"])


def _admin_stats_context(db: DbSession) -> dict[str, object]:
    product_stats = {
        product_slug: get_product_stats(db=db, product_slug=product_slug)
        for product_slug in PRODUCT_SLUGS
    }
    love_stats = product_stats["love"]
    total_questions = db.execute(select(func.count(models.Question.id))).scalar_one() or 0
    return {
        "product_stats": product_stats,
        "love_test_funnel": get_love_test_funnel_stats(db=db),
        "total_questions": int(total_questions),
        "total_sessions": love_stats["total_sessions"],
        "completed_sessions": love_stats["finished_sessions"],
        "today_sessions": love_stats["today_sessions"],
    }


@router.get("/admin", response_class=HTMLResponse)
@router.get("/admin/", response_class=HTMLResponse)
@router.get("/admin/dashboard", response_class=HTMLResponse)
def admin_dashboard(
    request: Request,
    db: DbSession = Depends(get_db),
    _admin: None = Depends(verify_admin_token),
):
    context = _admin_stats_context(db)
    session_token = (request.query_params.get("session_token") or "").strip()
    context["products"] = crud.list_products(db=db)
    context["pending_payments"] = payment_service.list_pending_payment_sessions(db=db)
    context["session_token_query"] = session_token
    context["searched_payment_session"] = (
        payment_service.find_payment_session_by_token(db=db, session_token=session_token)
        if session_token
        else None
    )
    context["search_not_found"] = bool(session_token and context["searched_payment_session"] is None)
    return templates.TemplateResponse(
        request=request,
        name="admin/dashboard.html",
        context=context,
    )


@router.get("/admin/questions", response_class=HTMLResponse)
def admin_questions(
    request: Request,
    db: DbSession = Depends(get_db),
    _admin: None = Depends(verify_admin_token),
):
    return templates.TemplateResponse(
        request=request,
        name="admin.html",
        context={
            **_admin_stats_context(db),
            "result_views": "-",
            "premium_interest_clicks": "-",
            "premium_interest_rate": "-",
        },
    )
