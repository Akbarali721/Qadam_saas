from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session as DbSession

from app import crud
from app.admin_auth import verify_admin_token
from app.core.database import get_db
from app.services import telegram_service

router = APIRouter(prefix="/telegram", tags=["telegram"])


@router.post("/set-webhook", dependencies=[Depends(verify_admin_token)])
def set_telegram_webhook(request: Request) -> dict[str, str | bool]:
    fallback_base_url = str(request.base_url).rstrip("/")
    webhook_url = telegram_service.webapp_url("/telegram/webhook", fallback_base_url=fallback_base_url)
    ok, message = telegram_service.set_webhook(webhook_url=webhook_url)
    if not ok:
        raise HTTPException(status_code=400, detail=message)
    return {"ok": True, "webhook_url": webhook_url}


def _chat_id_from_message(message: dict) -> str:
    chat = message.get("chat") or {}
    chat_id = chat.get("id")
    return str(chat_id) if chat_id is not None else ""


def _sender_id_from_message(message: dict) -> str:
    sender = message.get("from") or {}
    sender_id = sender.get("id")
    return str(sender_id) if sender_id is not None else ""


def _start_payload(text: str) -> str:
    parts = text.split(maxsplit=1)
    if len(parts) < 2:
        return ""
    return parts[1].strip()


@router.post("/webhook")
async def telegram_webhook(request: Request, db: DbSession = Depends(get_db)) -> dict[str, bool]:
    update = await request.json()
    message = update.get("message") or {}
    text = (message.get("text") or "").strip()
    chat_id = _chat_id_from_message(message)
    sender_id = _sender_id_from_message(message)

    if not chat_id or not text.startswith("/start"):
        return {"ok": True}

    payload = _start_payload(text)
    fallback_base_url = str(request.base_url).rstrip("/")

    if payload.startswith("love_partner_"):
        token = payload.removeprefix("love_partner_").strip()
        session = crud.get_session_by_token(db=db, token=token)
        if session is None:
            telegram_service.send_message(
                chat_id=chat_id,
                text="Bu taklif havolasi topilmadi yoki eskirgan.",
            )
            return {"ok": True}

        if sender_id:
            crud.set_partner_telegram_id(db=db, session=session, telegram_id=sender_id)

        telegram_service.send_love_partner_invite_message(
            chat_id=chat_id,
            token=token,
            initiator_name=session.initiator_name,
            partner_telegram_id=sender_id,
            fallback_base_url=fallback_base_url,
        )
        return {"ok": True}

    telegram_service.send_message(
        chat_id=chat_id,
        text="Love testni boshlash uchun tugmani bosing.",
        reply_markup={
            "inline_keyboard": [
                [
                    {
                        "text": "Love testni boshlash",
                        "web_app": {
                            "url": telegram_service.webapp_url("/", fallback_base_url=fallback_base_url),
                        },
                    },
                ],
            ],
        },
    )
    return {"ok": True}
