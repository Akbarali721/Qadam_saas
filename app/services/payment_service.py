from dataclasses import dataclass
from datetime import datetime
import logging

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app import models
from app.services import stats_service

logger = logging.getLogger(__name__)

PAYMENT_NONE = "none"
PAYMENT_PENDING = "pending"
PAYMENT_APPROVED = "approved"
PAYMENT_REJECTED = "rejected"
VALID_PAYMENT_STATUSES = {
    PAYMENT_NONE,
    PAYMENT_PENDING,
    PAYMENT_APPROVED,
    PAYMENT_REJECTED,
}


@dataclass(frozen=True)
class PaymentSession:
    product: str
    token: str
    title: str
    result_url: str
    created_at: datetime | None
    payment_status: str
    is_premium: bool
    user_name: str = ""
    pdf_url: str = ""
    test_type: str = ""
    creator_telegram_id: str | None = None


SESSION_MODELS = (
    ("love", "Love", models.Session, "/result/{token}"),
    ("mbti", "MBTI", models.MbtiSession, "/mbti/result/{token}"),
    ("stress", "Stress", models.StressSession, "/stress/result/{token}"),
)


def get_payment_session(db: Session, session_token: str):
    for _slug, _title, model, _result_path in SESSION_MODELS:
        session = db.execute(
            select(model).where(model.token == session_token),
        ).scalar_one_or_none()
        if session is not None:
            return session
    return None


def _display_name(row) -> str:
    initiator_name = getattr(row, "initiator_name", "") or ""
    partner_name = getattr(row, "partner_name", "") or ""
    names = [name for name in (initiator_name.strip(), partner_name.strip()) if name]
    if names:
        return " / ".join(names)
    return "-"


def _payment_session_from_row(slug: str, title: str, result_path: str, row) -> PaymentSession:
    creator_id = getattr(row, "creator_telegram_id", None)
    return PaymentSession(
        product=title,
        token=row.token,
        title=slug,
        result_url=result_path.format(token=row.token),
        created_at=getattr(row, "created_at", None),
        payment_status=row.payment_status,
        is_premium=bool(row.is_premium),
        user_name=_display_name(row),
        pdf_url=f"/pdf/{slug}/{row.token}",
        test_type=slug,
        creator_telegram_id=creator_id.strip() if creator_id else None,
    )


def _count_payment_status(db: Session, model, status: str) -> int:
    return int(
        db.execute(
            select(func.count(model.id)).where(model.payment_status == status),
        ).scalar_one()
        or 0,
    )


def _count_sessions(db: Session, model) -> int:
    return int(db.execute(select(func.count(model.id))).scalar_one() or 0)


def get_admin_api_stats(db: Session) -> dict[str, int]:
    love_stats = stats_service.get_product_stats(db=db, product_slug="love")
    return {
        "love_sessions_total": love_stats["total_sessions"],
        "love_completed_pairs": love_stats["finished_sessions"],
        "love_premium_pending": _count_payment_status(db, models.Session, PAYMENT_PENDING),
        "love_premium_approved": _count_payment_status(db, models.Session, PAYMENT_APPROVED),
        "mbti_sessions_total": _count_sessions(db, models.MbtiSession),
        "mbti_premium_pending": _count_payment_status(db, models.MbtiSession, PAYMENT_PENDING),
        "mbti_premium_approved": _count_payment_status(db, models.MbtiSession, PAYMENT_APPROVED),
        "stress_sessions_total": _count_sessions(db, models.StressSession),
        "stress_premium_pending": _count_payment_status(db, models.StressSession, PAYMENT_PENDING),
        "stress_premium_approved": _count_payment_status(db, models.StressSession, PAYMENT_APPROVED),
    }


def find_payment_session_by_token(db: Session, session_token: str) -> PaymentSession | None:
    normalized_token = session_token.strip()
    if not normalized_token:
        return None

    for slug, title, model, result_path in SESSION_MODELS:
        row = db.execute(
            select(model).where(model.token == normalized_token),
        ).scalar_one_or_none()
        if row is not None:
            return _payment_session_from_row(slug=slug, title=title, result_path=result_path, row=row)
    return None


def set_payment_requested(db: Session, session_token: str):
    session = get_payment_session(db=db, session_token=session_token)
    if session is None:
        return None
    if session.payment_status == PAYMENT_APPROVED and session.is_premium:
        return session
    session.payment_status = PAYMENT_PENDING
    db.commit()
    db.refresh(session)
    logger.info(
        "set_payment_requested token=%s payment_status=%s is_premium=%s",
        session.token,
        session.payment_status,
        session.is_premium,
    )
    return session


def approve_payment(db: Session, session_token: str):
    session = get_payment_session(db=db, session_token=session_token)
    if session is None:
        return None
    session.payment_status = PAYMENT_APPROVED
    session.is_premium = True
    db.commit()
    db.refresh(session)
    logger.info(
        "approve_payment token=%s payment_status=%s is_premium=%s",
        session.token,
        session.payment_status,
        session.is_premium,
    )
    return session


def reject_payment(db: Session, session_token: str):
    session = get_payment_session(db=db, session_token=session_token)
    if session is None:
        return None
    session.payment_status = PAYMENT_REJECTED
    session.is_premium = False
    db.commit()
    db.refresh(session)
    return session


def list_pending_payment_sessions(db: Session) -> list[PaymentSession]:
    pending: list[PaymentSession] = []
    for slug, title, model, result_path in SESSION_MODELS:
        rows = db.execute(
            select(model).where(model.payment_status == PAYMENT_PENDING),
        ).scalars()
        for row in rows:
            pending.append(_payment_session_from_row(slug=slug, title=title, result_path=result_path, row=row))
    pending.sort(key=lambda item: item.created_at or datetime.min, reverse=True)
    return pending
