"""Telegram bildirishnomalar — Love test: User2 tugagach User1 ga xabar."""

from __future__ import annotations

import asyncio
import logging
import os
from urllib.parse import quote

from app import models
from app.core import config
from app.services import payment_service
from app.services import telegram_service

logger = logging.getLogger(__name__)


def user1_telegram_id(session) -> str | None:
    """User1 Telegram ID: creator_telegram_id, keyin initiator_telegram_id."""
    raw = getattr(session, "creator_telegram_id", None) or getattr(
        session, "initiator_telegram_id", None
    )
    return raw.strip() if raw else None


def resolve_public_base_url(*, fallback_base_url: str = "") -> str:
    """HTTPS public URL (Render). Bo‘sh bo‘lsa request.base_url ishlatiladi."""
    for candidate in (
        config.BASE_URL,
        config.WEBAPP_BASE_URL,
        fallback_base_url,
    ):
        if candidate:
            return str(candidate).rstrip("/")
    return ""


def notify_user1_test_completed_sync(
    telegram_id: int,
    token: str,
    *,
    fallback_base_url: str = "",
) -> bool:
    """User1 ga natija tugmasi bilan xabar yuboradi. Xatolikda False va log."""
    public_base = resolve_public_base_url(fallback_base_url=fallback_base_url)
    if not public_base:
        logger.warning(
            "Telegram notify skipped: BASE_URL / WEBAPP_BASE_URL empty and no fallback (token=%s)",
            token,
        )
        return False

    chat_id = str(telegram_id)
    result_url = f"{public_base}/result/{token}"

    reply_markup = {
        "inline_keyboard": [
            [{"text": "Natijani ko‘rish", "url": result_url}],
        ],
    }

    logger.info(
        "Telegram notify API call event=test_completed token=%s chat_id=%s result_url=%s public_base=%s",
        token,
        chat_id,
        result_url,
        public_base,
    )
    ok, err = telegram_service.send_message(
        chat_id=chat_id,
        text="Sherigingiz testni yakunladi. Natijani ko‘rish uchun tugmani bosing.",
        reply_markup=reply_markup,
    )
    if ok:
        logger.info(
            "Telegram notify success event=test_completed token=%s chat_id=%s result_url=%s",
            token,
            chat_id,
            result_url,
        )
    else:
        logger.warning(
            "Telegram notify failed event=test_completed token=%s chat_id=%s result_url=%s detail=%s",
            token,
            chat_id,
            result_url,
            err,
        )
    return ok


def notify_user1_premium_unlocked_sync(
    telegram_id: int,
    token: str,
    *,
    fallback_base_url: str = "",
) -> bool:
    """Admin premium ochganda User1 ga xabar."""
    public_base = resolve_public_base_url(fallback_base_url=fallback_base_url)
    if not public_base:
        logger.warning(
            "Telegram premium notify skipped: BASE_URL empty (token=%s)",
            token,
        )
        return False

    chat_id = str(telegram_id)
    result_url = f"{public_base}/result/{token}?premium=1"
    reply_markup = {
        "inline_keyboard": [
            [{"text": "Premium natijani ko‘rish", "url": result_url}],
        ],
    }
    logger.info(
        "Telegram premium notify API call token=%s chat_id=%s result_url=%s public_base=%s",
        token,
        chat_id,
        result_url,
        public_base,
    )
    ok, err = telegram_service.send_message(
        chat_id=chat_id,
        text="🎉 Premium tahlil ochildi. To‘liq natijani ko‘rishingiz mumkin.",
        reply_markup=reply_markup,
    )
    if ok:
        logger.info(
            "Telegram notify success event=premium_unlocked token=%s chat_id=%s result_url=%s",
            token,
            chat_id,
            result_url,
        )
    else:
        logger.warning(
            "Telegram notify failed event=premium_unlocked token=%s chat_id=%s result_url=%s detail=%s",
            token,
            chat_id,
            result_url,
            err,
        )
    return ok


async def notify_user1_premium_unlocked(
    telegram_id: int,
    token: str,
    *,
    fallback_base_url: str = "",
) -> bool:
    return await asyncio.to_thread(
        notify_user1_premium_unlocked_sync,
        telegram_id,
        token,
        fallback_base_url=fallback_base_url,
    )


async def notify_love_user1_premium_unlocked(token: str, *, fallback_base_url: str = "") -> None:
    from app.core.database import SessionLocal
    from app import crud

    logger.info("Telegram premium notify task started token=%s", token)
    db = SessionLocal()
    try:
        session = crud.get_session_by_token(db, token)
        if session is None:
            logger.warning("Telegram premium notify skipped: session not found token=%s", token)
            return
        if not session.is_premium:
            logger.warning(
                "Telegram premium notify skipped: not premium token=%s is_premium=%s payment_status=%s",
                token,
                session.is_premium,
                session.payment_status,
            )
            return
        raw_id = user1_telegram_id(session)
        logger.info(
            "Telegram premium notify target token=%s creator_telegram_id=%s initiator_telegram_id=%s user1_id=%s",
            token,
            session.creator_telegram_id,
            session.initiator_telegram_id,
            raw_id,
        )
        if not raw_id:
            logger.warning(
                "Telegram premium notify skipped: no User1 telegram id token=%s",
                token,
            )
            return
        try:
            telegram_int = int(raw_id)
        except ValueError:
            logger.warning("Invalid creator_telegram_id=%s token=%s", raw_id, token)
            return
        ok = await notify_user1_premium_unlocked(
            telegram_int,
            token,
            fallback_base_url=fallback_base_url,
        )
        if not ok:
            logger.warning(
                "Telegram premium notify task finished with failure token=%s chat_id=%s",
                token,
                raw_id,
            )
    except Exception:
        logger.exception("notify love user1 premium unlocked failed token=%s", token)
    finally:
        db.close()


async def notify_user1_test_completed(
    telegram_id: int,
    token: str,
    *,
    fallback_base_url: str = "",
) -> bool:
    return await asyncio.to_thread(
        notify_user1_test_completed_sync,
        telegram_id,
        token,
        fallback_base_url=fallback_base_url,
    )


def session_test_type(session) -> str:
    if isinstance(session, models.Session):
        return "Love"
    if isinstance(session, models.MbtiSession):
        return "MBTI"
    if isinstance(session, models.StressSession):
        return "Stress"
    return "Noma'lum"


def session_user_telegram_id(session) -> str | None:
    if isinstance(session, models.Session):
        return user1_telegram_id(session)
    return None


def notify_admin_premium_request_sync(
    session,
    *,
    fallback_base_url: str = "",
) -> bool:
    """Admin chatga yangi premium so‘rov haqida xabar (faqat ADMIN_CHAT_ID)."""
    token = getattr(session, "token", "")
    admin_chat_id = (config.ADMIN_CHAT_ID or "").strip()
    if not admin_chat_id:
        logger.warning(
            "Admin premium request notify skipped: ADMIN_CHAT_ID not configured token=%s",
            token,
        )
        return False

    admin_token = (os.getenv("ADMIN_TOKEN") or "").strip()
    if not admin_token:
        logger.warning(
            "Admin premium request notify skipped: ADMIN_TOKEN not configured token=%s",
            token,
        )
        return False

    public_base = resolve_public_base_url(fallback_base_url=fallback_base_url)
    if not public_base:
        logger.warning(
            "Admin premium request notify skipped: BASE_URL empty token=%s",
            token,
        )
        return False

    test_type = session_test_type(session)
    user_tg = session_user_telegram_id(session)
    payment_status = getattr(session, "payment_status", "") or ""
    dashboard_url = (
        f"{public_base}/admin/dashboard"
        f"?token={quote(admin_token, safe='')}"
        f"&session_token={quote(token, safe='')}"
    )
    text = (
        "💳 Yangi premium so‘rov\n\n"
        f"Test turi: {test_type}\n"
        f"Token: {token}\n"
        f"Telegram ID: {user_tg or '—'}\n"
        f"Holat: {payment_status}"
    )
    reply_markup = {
        "inline_keyboard": [
            [{"text": "Admin panelda ochish", "url": dashboard_url}],
        ],
    }

    logger.info(
        "Admin premium request notify API call token=%s chat_id=%s test_type=%s payment_status=%s",
        token,
        admin_chat_id,
        test_type,
        payment_status,
    )
    ok, err = telegram_service.send_message(
        chat_id=admin_chat_id,
        text=text,
        reply_markup=reply_markup,
    )
    if ok:
        logger.info(
            "Admin premium request notify sent token=%s chat_id=%s test_type=%s",
            token,
            admin_chat_id,
            test_type,
        )
    else:
        logger.warning(
            "Admin premium request notify failed token=%s chat_id=%s detail=%s",
            token,
            admin_chat_id,
            err,
        )
    return ok


async def notify_admin_premium_request(token: str, *, fallback_base_url: str = "") -> None:
    from app.core.database import SessionLocal

    logger.info("Admin premium request notify task started token=%s", token)
    db = SessionLocal()
    try:
        session = payment_service.get_payment_session(db=db, session_token=token)
        if session is None:
            logger.warning(
                "Admin premium request notify skipped: session not found token=%s",
                token,
            )
            return
        if session.payment_status != payment_service.PAYMENT_PENDING:
            logger.warning(
                "Admin premium request notify skipped: not pending token=%s payment_status=%s",
                token,
                session.payment_status,
            )
            return
        await asyncio.to_thread(
            notify_admin_premium_request_sync,
            session,
            fallback_base_url=fallback_base_url,
        )
    except Exception:
        logger.exception("Admin premium request notify task failed token=%s", token)
    finally:
        db.close()
