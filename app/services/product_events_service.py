"""Minimal product event tracking for the Qadam platform."""
from __future__ import annotations

import json
import logging
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session as DbSession

from app import models

logger = logging.getLogger(__name__)

LOVE_PRODUCT_SLUG = "love"


def _love_product_id(db: DbSession) -> int | None:
    product = db.execute(
        select(models.Product).where(models.Product.slug == LOVE_PRODUCT_SLUG),
    ).scalar_one_or_none()
    return product.id if product else None


def get_or_create_love_product_session(db: DbSession, *, session_token: str) -> models.ProductSession | None:
    product_id = _love_product_id(db)
    if product_id is None:
        return None
    existing = db.execute(
        select(models.ProductSession).where(
            models.ProductSession.product_id == product_id,
            models.ProductSession.token == session_token,
        ),
    ).scalar_one_or_none()
    if existing is not None:
        return existing
    row = models.ProductSession(
        product_id=product_id,
        token=session_token,
        status="created",
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def record_love_product_event(
    db: DbSession,
    *,
    session_token: str,
    event_type: str,
    metadata: dict[str, Any] | None = None,
) -> bool:
    """Record a love-test analytics event. Safe to call; failures are logged only."""
    product_id = _love_product_id(db)
    if product_id is None:
        logger.warning("Skipping love event %s: product not seeded", event_type)
        return False
    try:
        product_session = get_or_create_love_product_session(db, session_token=session_token)
        if product_session is None:
            return False
        db.add(
            models.ProductEvent(
                product_id=product_id,
                session_id=product_session.id,
                event_type=event_type,
                metadata_json=json.dumps(metadata or {}, ensure_ascii=False),
            ),
        )
        db.commit()
        return True
    except Exception:
        logger.exception("Failed to record love event %s token=%s", event_type, session_token)
        db.rollback()
        return False
