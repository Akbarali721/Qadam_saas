from datetime import datetime, time, timedelta
from typing import Any, TypedDict

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session as DbSession

from app import models


PRODUCT_SLUGS = ("love", "mbti", "stress")


class ProductStats(TypedDict):
    slug: str
    total_sessions: int
    finished_sessions: int
    today_sessions: int
    conversion_rate: float


class LatestEvent(TypedDict):
    id: int
    product_slug: str
    session_token: str | None
    event_type: str
    metadata_json: str
    created_at: datetime


def _today_window() -> tuple[datetime, datetime]:
    today = datetime.utcnow().date()
    start = datetime.combine(today, time.min)
    return start, start + timedelta(days=1)


def _product_id_for_slug(db: DbSession, product_slug: str) -> int | None:
    return db.execute(
        select(models.Product.id).where(models.Product.slug == product_slug),
    ).scalar_one_or_none()


def _platform_total_sessions(db: DbSession, product_slug: str) -> int:
    product_id = _product_id_for_slug(db=db, product_slug=product_slug)
    if product_id is None:
        return 0
    return int(
        db.execute(
            select(func.count(models.ProductSession.id)).where(
                models.ProductSession.product_id == product_id,
            ),
        ).scalar_one()
        or 0,
    )


def _platform_finished_sessions(db: DbSession, product_slug: str) -> int:
    product_id = _product_id_for_slug(db=db, product_slug=product_slug)
    if product_id is None:
        return 0
    return int(
        db.execute(
            select(func.count(models.ProductSession.id)).where(
                models.ProductSession.product_id == product_id,
                or_(
                    models.ProductSession.status.in_(("finished", "completed")),
                    models.ProductSession.finished_at.is_not(None),
                ),
            ),
        ).scalar_one()
        or 0,
    )


def _platform_today_sessions(db: DbSession, product_slug: str) -> int:
    product_id = _product_id_for_slug(db=db, product_slug=product_slug)
    if product_id is None:
        return 0
    start, end = _today_window()
    return int(
        db.execute(
            select(func.count(models.ProductSession.id)).where(
                models.ProductSession.product_id == product_id,
                models.ProductSession.created_at >= start,
                models.ProductSession.created_at < end,
            ),
        ).scalar_one()
        or 0,
    )


def total_sessions(db: DbSession, product_slug: str) -> int:
    if product_slug != "love":
        return _platform_total_sessions(db=db, product_slug=product_slug)
    return int(db.execute(select(func.count(models.Session.id))).scalar_one() or 0)


def finished_sessions(db: DbSession, product_slug: str) -> int:
    if product_slug != "love":
        return _platform_finished_sessions(db=db, product_slug=product_slug)
    return int(
        db.execute(
            select(func.count(models.Session.id)).where(models.Session.status == "completed"),
        ).scalar_one()
        or 0,
    )


def today_sessions(db: DbSession, product_slug: str) -> int:
    if product_slug != "love":
        return _platform_today_sessions(db=db, product_slug=product_slug)

    start, end = _today_window()
    return int(
        db.execute(
            select(func.count(models.Session.id)).where(
                models.Session.created_at >= start,
                models.Session.created_at < end,
            ),
        ).scalar_one()
        or 0,
    )


def conversion_rate(db: DbSession, product_slug: str) -> float:
    total = total_sessions(db=db, product_slug=product_slug)
    if total == 0:
        return 0.0
    finished = finished_sessions(db=db, product_slug=product_slug)
    return round((finished / total) * 100, 1)


def get_product_stats(db: DbSession, product_slug: str) -> ProductStats:
    normalized_slug = product_slug.strip().lower()
    return {
        "slug": normalized_slug,
        "total_sessions": total_sessions(db=db, product_slug=normalized_slug),
        "finished_sessions": finished_sessions(db=db, product_slug=normalized_slug),
        "today_sessions": today_sessions(db=db, product_slug=normalized_slug),
        "conversion_rate": conversion_rate(db=db, product_slug=normalized_slug),
    }


def get_all_product_stats(db: DbSession) -> dict[str, ProductStats]:
    return {
        product_slug: get_product_stats(db=db, product_slug=product_slug)
        for product_slug in PRODUCT_SLUGS
    }


def latest_events(db: DbSession, limit: int = 20) -> list[LatestEvent]:
    rows = db.execute(
        select(models.ProductEvent, models.Product.slug, models.ProductSession.token)
        .join(models.Product, models.Product.id == models.ProductEvent.product_id)
        .outerjoin(
            models.ProductSession,
            models.ProductSession.id == models.ProductEvent.session_id,
        )
        .order_by(models.ProductEvent.created_at.desc(), models.ProductEvent.id.desc())
        .limit(limit),
    ).all()
    return [
        {
            "id": event.id,
            "product_slug": product_slug,
            "session_token": session_token,
            "event_type": event.event_type,
            "metadata_json": event.metadata_json,
            "created_at": event.created_at,
        }
        for event, product_slug, session_token in rows
    ]


def platform_session_rows(db: DbSession, limit: int = 50) -> list[dict[str, Any]]:
    rows = db.execute(
        select(models.ProductSession, models.Product.slug)
        .join(models.Product, models.Product.id == models.ProductSession.product_id)
        .order_by(models.ProductSession.created_at.desc(), models.ProductSession.id.desc())
        .limit(limit),
    ).all()
    return [
        {
            "id": session.id,
            "product_slug": product_slug,
            "user_id": session.user_id,
            "token": session.token,
            "status": session.status,
            "created_at": session.created_at,
            "finished_at": session.finished_at,
        }
        for session, product_slug in rows
    ]


def legacy_love_session_rows(db: DbSession, limit: int = 50) -> list[dict[str, Any]]:
    sessions = db.execute(
        select(models.Session)
        .order_by(models.Session.created_at.desc(), models.Session.id.desc())
        .limit(limit),
    ).scalars().all()
    return [
        {
            "id": session.id,
            "product_slug": "love",
            "user_id": None,
            "token": session.token,
            "status": session.status,
            "created_at": session.created_at,
            "finished_at": session.answered_at,
        }
        for session in sessions
    ]
