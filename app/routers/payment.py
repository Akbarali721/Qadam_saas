import logging
from typing import Any
from urllib.parse import quote

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session as DbSession

from app import models
from app.admin_auth import verify_admin_token
from app.core.config import ADMIN_CONTACT_URL, ADMIN_USERNAME
from app.core.database import get_db
from app.core.templates import templates
from app.services import payment_service
from app.services.telegram_notify import (
    notify_admin_premium_request,
    notify_love_user1_premium_unlocked,
)

router = APIRouter(prefix="/payment", tags=["payment"])
logger = logging.getLogger(__name__)


def _admin_contact_url(order_code: str) -> str | None:
    if ADMIN_CONTACT_URL:
        return ADMIN_CONTACT_URL
    if ADMIN_USERNAME:
        message = quote(
            f"Salom, men premium tahlilni olmoqchiman. Buyurtma kodim: {order_code}",
            safe="",
        )
        return f"https://t.me/{ADMIN_USERNAME}?text={message}"
    return None


def _wants_html_redirect(request: Request) -> bool:
    accept = request.headers.get("accept", "")
    if "text/html" in accept:
        return True
    content_type = (request.headers.get("content-type") or "").lower()
    return request.method == "POST" and "application/json" not in content_type


def _payment_response(request: Request, session) -> Any:
    if _wants_html_redirect(request):
        referer = request.headers.get("referer") or ""
        if "/admin" in referer:
            admin_token = request.query_params.get("token", "")
            dashboard_url = (
                f"/admin/dashboard?token={admin_token}" if admin_token else "/admin/dashboard"
            )
            return RedirectResponse(url=dashboard_url, status_code=303)
        if referer:
            return RedirectResponse(url=referer, status_code=303)
        if getattr(session, "token", None):
            return RedirectResponse(url=f"/result/{session.token}", status_code=303)
        return RedirectResponse(url="/", status_code=303)
    return {
        "status": "ok",
        "token": session.token,
        "payment_status": session.payment_status,
        "is_premium": bool(session.is_premium),
        "premium_unlocked": bool(session.is_premium),
    }


@router.post("/request/{session_token}")
def request_payment(
    session_token: str,
    request: Request,
    background_tasks: BackgroundTasks,
    db: DbSession = Depends(get_db),
) -> Any:
    existing = payment_service.get_payment_session(db=db, session_token=session_token)
    if existing is None:
        raise HTTPException(status_code=404, detail="Session not found")
    previous_status = existing.payment_status
    session = payment_service.set_payment_requested(db=db, session_token=session_token)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    logger.info(
        "Premium request created token=%s payment_status=%s is_premium=%s previous_status=%s",
        session.token,
        session.payment_status,
        session.is_premium,
        previous_status,
    )
    if (
        session.payment_status == payment_service.PAYMENT_PENDING
        and previous_status != payment_service.PAYMENT_PENDING
    ):
        background_tasks.add_task(
            notify_admin_premium_request,
            session.token,
            fallback_base_url=str(request.base_url).rstrip("/"),
        )
    if _wants_html_redirect(request):
        return RedirectResponse(url=f"/payment/pending/{session.token}", status_code=303)
    return _payment_response(request=request, session=session)


@router.get("/pending/{session_token}")
def pending_payment_page(
    session_token: str,
    request: Request,
    db: DbSession = Depends(get_db),
) -> Any:
    payment_session = payment_service.find_payment_session_by_token(
        db=db,
        session_token=session_token,
    )
    if payment_session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return templates.TemplateResponse(
        request=request,
        name="payment/pending.html",
        context={
            "payment": payment_session,
            "admin_contact_url": _admin_contact_url(payment_session.token),
        },
    )


@router.post("/approve/{session_token}", dependencies=[Depends(verify_admin_token)])
def approve_payment(
    session_token: str,
    request: Request,
    background_tasks: BackgroundTasks,
    db: DbSession = Depends(get_db),
) -> Any:
    session = payment_service.approve_payment(db=db, session_token=session_token)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    logger.info(
        "Payment approved token=%s payment_status=%s is_premium=%s "
        "creator_telegram_id=%s initiator_telegram_id=%s",
        session.token,
        session.payment_status,
        session.is_premium,
        getattr(session, "creator_telegram_id", None),
        getattr(session, "initiator_telegram_id", None),
    )
    if isinstance(session, models.Session):
        background_tasks.add_task(
            notify_love_user1_premium_unlocked,
            session_token,
            fallback_base_url=str(request.base_url).rstrip("/"),
        )
    return _payment_response(request=request, session=session)


@router.post("/reject/{session_token}", dependencies=[Depends(verify_admin_token)])
def reject_payment(
    session_token: str,
    request: Request,
    db: DbSession = Depends(get_db),
) -> Any:
    session = payment_service.reject_payment(db=db, session_token=session_token)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return _payment_response(request=request, session=session)
