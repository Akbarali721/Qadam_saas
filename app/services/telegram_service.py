from __future__ import annotations

import json
import logging
import os
from urllib.parse import quote
from urllib import request as urlrequest

from app.core.config import TELEGRAM_BOT_USERNAME, TELEGRAM_BOT_TOKEN, WEBAPP_BASE_URL, load_environment

logger = logging.getLogger(__name__)


def _bot_token() -> str:
    load_environment()
    return TELEGRAM_BOT_TOKEN or os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("BOT_TOKEN") or ""


def bot_token_configured() -> bool:
    return bool(_bot_token())


def bot_username() -> str:
    load_environment()
    return (
        TELEGRAM_BOT_USERNAME
        or os.getenv("TELEGRAM_BOT_USERNAME", "")
        or os.getenv("BOT_USERNAME", "")
        or "qadam_loyihaBot"
    ).lstrip("@")


def webapp_base_url(fallback_base_url: str = "") -> str:
    load_environment()
    return (WEBAPP_BASE_URL or os.getenv("WEBAPP_BASE_URL", "") or os.getenv("APP_BASE_URL", "") or fallback_base_url).rstrip("/")


def webapp_url(path: str, fallback_base_url: str = "") -> str:
    base = webapp_base_url(fallback_base_url=fallback_base_url)
    if not base:
        return path
    return f"{base}{path if path.startswith('/') else f'/{path}'}"


REL_INVITE_PREFIX = "rel_invite_"
LEGACY_LOVE_PARTNER_PREFIX = "love_partner_"


def relationship_invite_deep_link(*, token: str, fallback_url: str = "") -> str:
    """Telegram bot deep-link for partner invite: t.me/<bot>?start=rel_invite_<token>"""
    username = bot_username()
    if not username:
        return fallback_url or webapp_url(f"/start/{token}")
    return f"https://t.me/{username}?start={REL_INVITE_PREFIX}{token}"


def love_partner_deep_link(*, token: str, fallback_url: str) -> str:
    """Backward-compatible alias for relationship_invite_deep_link."""
    return relationship_invite_deep_link(token=token, fallback_url=fallback_url)


def parse_relationship_invite_token(payload: str) -> str | None:
    for prefix in (REL_INVITE_PREFIX, LEGACY_LOVE_PARTNER_PREFIX):
        if payload.startswith(prefix):
            return payload.removeprefix(prefix).strip()
    return None


def telegram_share_url(*, url: str, text: str) -> str:
    return f"https://t.me/share/url?url={quote(url, safe='')}&text={quote(text)}"


def _post_telegram_method(method: str, payload: dict) -> tuple[bool, str]:
    bot_token = _bot_token()
    if not bot_token:
        return False, "Telegram bot token sozlanmagan."
    data = json.dumps(payload).encode("utf-8")
    req = urlrequest.Request(
        url=f"https://api.telegram.org/bot{bot_token}/{method}",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlrequest.urlopen(req, timeout=10) as response:
            body = json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        return False, f"Telegram xabar yuborishda xatolik: {exc}"

    if not body.get("ok"):
        detail = str(body.get("description") or "Telegram xabarni qabul qilmadi.")
        logger.warning("Telegram API %s failed: %s", method, detail)
        return False, detail
    logger.info("Telegram API %s success", method)
    return True, "ok"


def set_webhook(*, webhook_url: str) -> tuple[bool, str]:
    return _post_telegram_method("setWebhook", {"url": webhook_url})


def send_message(*, chat_id: str, text: str, reply_markup: dict | None = None) -> tuple[bool, str]:
    payload: dict = {"chat_id": chat_id, "text": text}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    ok, detail = _post_telegram_method("sendMessage", payload)
    if ok:
        logger.info("Telegram sendMessage OK chat_id=%s", chat_id)
    else:
        logger.warning("Telegram sendMessage FAILED chat_id=%s detail=%s", chat_id, detail)
    return ok, detail


def send_love_partner_invite_message(
    *,
    chat_id: str,
    token: str,
    initiator_name: str,
    partner_telegram_id: str = "",
    fallback_base_url: str = "",
) -> tuple[bool, str]:
    path = f"/start/{token}"
    if partner_telegram_id:
        path = f"{path}?partner_tg_id={quote(partner_telegram_id)}"
    url = webapp_url(path, fallback_base_url=fallback_base_url)
    return send_message(
        chat_id=chat_id,
        text=(
            f"💌 {initiator_name or 'Sevgan insoningiz'} sizni Love testga taklif qildi.\n\n"
            "Anketani to‘ldirish va testni yechish uchun tugmani bosing."
        ),
        reply_markup={
            "inline_keyboard": [
                [
                    {
                        "text": "Testni yechish",
                        "web_app": {"url": url},
                    },
                ],
            ],
        },
    )

