import logging
import os
from urllib.parse import quote

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session as DbSession

from app.admin_auth import verify_admin_token
from app.core.database import get_db
from app.services import payment_service
from app.services.telegram_notify import resolve_public_base_url

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin/api", tags=["admin-api"])


def _absolute_url(public_base: str, path: str) -> str:
    if public_base:
        return f"{public_base}{path}"
    return path


def _pending_payment_item(
    session: payment_service.PaymentSession,
    *,
    public_base: str,
    admin_token: str,
) -> dict[str, object]:
    result_url = _absolute_url(public_base, session.result_url)
    dashboard_path = (
        f"/admin/dashboard?token={quote(admin_token, safe='')}"
        f"&session_token={quote(session.token, safe='')}"
    )
    return {
        "test_type": session.test_type or session.title,
        "token": session.token,
        "payment_status": session.payment_status,
        "is_premium": session.is_premium,
        "creator_telegram_id": session.creator_telegram_id,
        "result_url": result_url,
        "admin_dashboard_url": _absolute_url(public_base, dashboard_path),
    }


@router.get("/stats")
def admin_api_stats(
    db: DbSession = Depends(get_db),
    _admin: None = Depends(verify_admin_token),
) -> dict[str, int]:
    stats = payment_service.get_admin_api_stats(db=db)
    logger.info("Admin API stats requested %s", stats)
    return stats


@router.get("/pending-payments")
def admin_api_pending_payments(
    request: Request,
    db: DbSession = Depends(get_db),
    _admin: None = Depends(verify_admin_token),
) -> list[dict[str, object]]:
    public_base = resolve_public_base_url(
        fallback_base_url=str(request.base_url).rstrip("/"),
    )
    admin_token = (os.getenv("ADMIN_TOKEN") or "").strip()
    pending = payment_service.list_pending_payment_sessions(db=db)
    items = [
        _pending_payment_item(session, public_base=public_base, admin_token=admin_token)
        for session in pending
    ]
    logger.info("Admin API pending-payments count=%s", len(items))
    return items
