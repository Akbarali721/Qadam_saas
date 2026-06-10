import json
import logging

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session as DbSession

from app import crud, models, schemas
from app.core.database import SessionLocal, get_db
from app.core.templates import templates
from app.services import pdf_service, telegram_service
from app.services.product_events_service import record_love_product_event
from app.services.telegram_notify import (
    notify_love_user1_premium_unlocked,
    notify_user1_test_completed,
    resolve_public_base_url,
    user1_telegram_id,
)

router = APIRouter(tags=["love"])
logger = logging.getLogger(__name__)

LOVE_INVITE_SHARE_TEXT = "Munosabat testini birga ishlab ko‘raylik 💞"


def _apply_tg_id_to_session_create(
    payload: schemas.SessionCreate,
    tg_id: str | None,
) -> schemas.SessionCreate:
    raw = (tg_id or "").strip()
    if not raw.isdigit():
        return payload
    if payload.creator_telegram_id:
        return payload
    return payload.model_copy(
        update={
            "creator_telegram_id": raw,
            "initiator_telegram_id": raw,
        },
    )


def _should_notify_user1_after_submit(
    *,
    completed: bool,
    session: models.Session,
    db: DbSession,
) -> bool:
    if not completed:
        return False
    state = crud.get_session_quiz_state(db=db, session=session)
    return bool(state["initiator_answered"] and state["partner_answered"])


async def _notify_initiator_partner_completed(token: str, fallback_base_url: str) -> None:
    """Ikkala tomon tugagach User1 ga bir marta Telegram; xatoliklar natija oqimini buzmaydi."""
    logger.info("Telegram notify task started token=%s fallback_base_url=%s", token, fallback_base_url)
    db = SessionLocal()
    try:
        session = crud.get_session_by_token(db, token)
        if session is None:
            logger.warning("Telegram notify skipped: session not found token=%s", token)
            return
        state = crud.get_session_quiz_state(db=db, session=session)
        has_result = crud.get_result_by_session_id(db=db, session_id=session.id) is not None
        logger.info(
            "Telegram notify pre-check token=%s session_id=%s status=%s "
            "creator_telegram_id=%s initiator_telegram_id=%s payment_status=%s "
            "initiator_answered=%s partner_answered=%s completion_notify_sent=%s has_result=%s",
            token,
            session.id,
            session.status,
            session.creator_telegram_id,
            session.initiator_telegram_id,
            session.payment_status,
            state["initiator_answered"],
            state["partner_answered"],
            getattr(session, "completion_notify_sent", False),
            has_result,
        )
        if getattr(session, "completion_notify_sent", False):
            logger.info("Telegram notify skipped: already sent token=%s", token)
            return
        if session.status != "completed":
            logger.warning(
                "Telegram notify skipped: status not completed token=%s status=%s",
                token,
                session.status,
            )
            return
        if not state["partner_answered"]:
            logger.warning("Telegram notify skipped: partner not answered token=%s", token)
            return
        if not state["initiator_answered"]:
            logger.warning("Telegram notify skipped: initiator not answered token=%s", token)
            return
        raw_id = user1_telegram_id(session)
        if not raw_id:
            logger.warning(
                "Telegram notify skipped: no User1 telegram id token=%s "
                "creator_telegram_id=%s initiator_telegram_id=%s",
                token,
                session.creator_telegram_id,
                session.initiator_telegram_id,
            )
            return
        try:
            telegram_int = int(raw_id)
        except ValueError:
            logger.warning("Invalid creator_telegram_id=%s token=%s", raw_id, token)
            return
        logger.info(
            "Telegram notify sending token=%s session_id=%s chat_id=%s",
            token,
            session.id,
            raw_id,
        )
        try:
            ok = await notify_user1_test_completed(
                telegram_int,
                token,
                fallback_base_url=fallback_base_url,
            )
        except Exception:
            logger.exception(
                "Telegram notify_user1_test_completed failed token=%s chat_id=%s",
                token,
                raw_id,
            )
            return
        if ok:
            session.completion_notify_sent = True
            db.commit()
            logger.info("Telegram notify marked sent token=%s session_id=%s", token, session.id)
        else:
            logger.warning(
                "Telegram notify API returned failure token=%s chat_id=%s",
                token,
                raw_id,
            )
    except Exception:
        logger.exception("notify initiator partner completed task failed token=%s", token)
    finally:
        db.close()


@router.get("/", response_class=HTMLResponse)
def index_page(request: Request, tg_id: str | None = None):
    raw = (tg_id or request.query_params.get("tg_id") or "").strip()
    return templates.TemplateResponse(
        request=request,
        name="love/index.html",
        context={"tg_id": raw},
    )


@router.get("/share/{token}", response_class=HTMLResponse)
def share_page(request: Request, token: str, db: DbSession = Depends(get_db)):
    session = crud.get_session_by_token(db=db, token=token)
    if session is None:
        raise HTTPException(status_code=404, detail="Sessiya topilmadi")
    state = crud.get_session_quiz_state(db=db, session=session)
    if not state["initiator_answered"]:
        return RedirectResponse(url=f"/quiz/init/{token}", status_code=303)
    if not state["partner_registered"] and request.query_params.get("host") != "1":
        return RedirectResponse(url=f"/start/{token}", status_code=303)
    public_base = resolve_public_base_url(
        fallback_base_url=str(request.base_url).rstrip("/"),
    )
    share_page_url = f"{public_base}/share/{token}"
    partner_start_url = f"{public_base}/start/{token}"
    bot_invite_link = telegram_service.relationship_invite_deep_link(
        token=token,
        fallback_url=partner_start_url,
    )
    telegram_share_url = telegram_service.telegram_share_url(
        url=bot_invite_link,
        text=LOVE_INVITE_SHARE_TEXT,
    )
    return templates.TemplateResponse(
        request=request,
        name="love/share.html",
        context={
            "token": token,
            "initiator_name": session.initiator_name,
            "share_page_url": share_page_url,
            "partner_start_url": partner_start_url,
            "bot_invite_link": bot_invite_link,
            "telegram_share_url": telegram_share_url,
            "share_text": LOVE_INVITE_SHARE_TEXT,
            "initiator_questions_url": f"{public_base}/questions.html?token={token}&role=initiator",
        },
    )


@router.get("/start/{token}", response_class=HTMLResponse)
def partner_landing_page(
    request: Request,
    token: str,
    tg_id: int | None = None,
    partner_tg_id: int | None = None,
    db: DbSession = Depends(get_db),
):
    session = crud.get_session_by_token(db=db, token=token)
    if session is None:
        raise HTTPException(status_code=404, detail="Sessiya topilmadi")
    if tg_id is not None and not session.initiator_telegram_id:
        session.initiator_telegram_id = str(tg_id)
        db.commit()
        db.refresh(session)
    if partner_tg_id is not None:
        session = crud.set_partner_telegram_id(
            db=db,
            session=session,
            telegram_id=str(partner_tg_id),
        )
    return templates.TemplateResponse(
        request=request,
        name="love/partner.html",
        context={
            "token": token,
            "initiator_name": session.initiator_name,
        },
    )


@router.get("/premium/{token}")
def premium_webapp_entry(token: str):
    """Telegram inline tugma: premium blokiga yo‘naltirish (natija sahifasi)."""
    return RedirectResponse(url=f"/result/{token}", status_code=302)


@router.get("/partner/complete/{token}", response_class=HTMLResponse)
def partner_complete_page(request: Request, token: str, db: DbSession = Depends(get_db)):
    session = crud.get_session_by_token(db=db, token=token)
    if session is None:
        raise HTTPException(status_code=404, detail="Sessiya topilmadi")
    state = crud.get_session_quiz_state(db=db, session=session)
    if not state["partner_answered"]:
        return RedirectResponse(url=f"/questions.html?token={token}&role=partner", status_code=303)
    user1_id = user1_telegram_id(session)
    message = (
        "Yakunlandi ✅ Natija saqlandi."
        if user1_id
        else "Yakunlandi ✅ Natija saqlandi. User1 Telegram orqali boshlamagan bo‘lsa, natijani ulashish uchun token kerak bo‘ladi."
    )
    return templates.TemplateResponse(
        request=request,
        name="love/partner_complete.html",
        context={
            "token": token,
            "message": message,
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
            crud.mark_session_quiz_started(db=db, session=session)
            questions_payload = [
                schemas.QuestionRead.model_validate(question).model_dump()
                for question in crud.get_session_questions(db=db, session=session)
            ]
    return templates.TemplateResponse(
        request=request,
        name="love/questions.html",
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
        name="love/result.html",
        context={"token": "", "is_premium": False, "payment_status": "none"},
    )


@router.get("/result/{token}", response_class=HTMLResponse)
def result_page_by_token(request: Request, token: str, db: DbSession = Depends(get_db)):
    session = crud.get_session_by_token(db=db, token=token)
    if session is None:
        raise HTTPException(status_code=404, detail="Sessiya topilmadi")
    premium = None
    if session.is_premium:
        report = pdf_service.build_premium_report(db=db, test_type="love", token=token)
        premium = report.as_context() if report else None
    return templates.TemplateResponse(
        request=request,
        name="love/result.html",
        context={
            "token": token,
            "is_premium": session.is_premium,
            "payment_status": session.payment_status,
            "premium": premium,
        },
    )


@router.post("/api/sessions", response_model=schemas.SessionCreateRead, tags=["sessions"])
def create_session(
    request: Request,
    payload: schemas.SessionCreate,
    db: DbSession = Depends(get_db),
) -> schemas.SessionCreateRead:
    tg_from_query = request.query_params.get("tg_id")
    payload = _apply_tg_id_to_session_create(payload, tg_from_query)
    logger.info(
        "create_session request tg_id_query=%s body_creator=%s body_initiator=%s",
        tg_from_query,
        payload.creator_telegram_id,
        payload.initiator_telegram_id,
    )
    session = crud.create_session(db=db, payload=payload)
    record_love_product_event(
        db,
        session_token=session.token,
        event_type="invite_created",
        metadata={"source": "love_create_session"},
    )
    logger.info(
        "Session created token=%s creator_telegram_id=%s initiator_telegram_id=%s",
        session.token,
        session.creator_telegram_id,
        session.initiator_telegram_id,
    )
    if not session.creator_telegram_id:
        logger.warning(
            "Session created without creator_telegram_id token=%s — User1 notify will not work",
            session.token,
        )
    public_base = resolve_public_base_url(
        fallback_base_url=str(request.base_url).rstrip("/"),
    )
    token = session.token
    share_page_url = f"{public_base}/share/{token}"
    partner_join_url = f"{public_base}/start/{token}"
    initiator_questions_url = f"{public_base}/questions.html?token={token}&role=initiator"
    return schemas.SessionCreateRead(
        **schemas.SessionRead.model_validate(session).model_dump(),
        share_url=share_page_url,
        share_page_url=share_page_url,
        partner_join_url=partner_join_url,
        initiator_questions_url=initiator_questions_url,
    )


@router.post("/create-session", response_model=schemas.SessionCreateRead, tags=["sessions"])
def create_session_alias(
    request: Request,
    payload: schemas.SessionCreate,
    db: DbSession = Depends(get_db),
) -> schemas.SessionCreateRead:
    return create_session(request=request, payload=payload, db=db)


@router.get("/api/sessions/{token}", response_model=schemas.SessionRead, tags=["sessions"])
def get_session(
    token: str,
    db: DbSession = Depends(get_db),
) -> models.Session:
    session = crud.get_session_by_token(db=db, token=token)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.get("/api/sessions/{token}/state", response_model=schemas.SessionStateRead, tags=["sessions"])
def get_session_state(token: str, db: DbSession = Depends(get_db)) -> schemas.SessionStateRead:
    session = crud.get_session_by_token(db=db, token=token)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    state = crud.get_session_quiz_state(db=db, session=session)
    return schemas.SessionStateRead(**state)


@router.post("/api/sessions/{token}/unlock-premium", tags=["sessions"])
def unlock_premium(
    token: str,
    request: Request,
    background_tasks: BackgroundTasks,
    db: DbSession = Depends(get_db),
) -> dict[str, bool | str]:
    session = crud.get_session_by_token(db=db, token=token)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    unlocked = crud.unlock_session_premium(db=db, session=session)
    background_tasks.add_task(
        notify_love_user1_premium_unlocked,
        token,
        fallback_base_url=str(request.base_url).rstrip("/"),
    )
    return {"ok": True, "token": unlocked.token, "is_premium": unlocked.is_premium}


@router.post("/api/sessions/{token}/partner", tags=["sessions"])
def register_partner(
    token: str,
    payload: schemas.PartnerRegister,
    db: DbSession = Depends(get_db),
) -> dict[str, str]:
    session = crud.get_session_by_token(db=db, token=token)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    try:
        crud.register_partner(db=db, session=session, payload=payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"status": "ok"}


@router.get(
    "/api/sessions/{token}/questions",
    response_model=list[schemas.QuestionRead],
    tags=["questions"],
)
def get_session_questions(
    token: str,
    db: DbSession = Depends(get_db),
) -> list[models.Question]:
    session = crud.get_session_by_token(db=db, token=token)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    crud.mark_session_quiz_started(db=db, session=session)
    return crud.get_session_questions(db=db, session=session)


@router.post("/api/sessions/{token}/progress", tags=["sessions"])
def update_session_progress(
    token: str,
    payload: schemas.SessionProgressUpdate,
    db: DbSession = Depends(get_db),
) -> dict[str, str]:
    session = crud.get_session_by_token(db=db, token=token)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.status == "completed":
        raise HTTPException(status_code=409, detail="Test allaqachon yakunlangan")
    crud.update_session_quiz_progress(
        db=db,
        session=session,
        question_index=payload.question_index,
    )
    return {"status": "ok"}


@router.post("/api/sessions/{token}/answers", tags=["answers"])
def submit_answers(
    token: str,
    payload: schemas.AnswerSubmitRequest,
    background_tasks: BackgroundTasks,
    request: Request,
    db: DbSession = Depends(get_db),
) -> dict[str, str]:
    session = crud.get_session_by_token(db=db, token=token)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.status == "completed":
        raise HTTPException(status_code=409, detail="Test allaqachon yakunlangan")

    role = payload.role.strip().lower()
    try:
        completed = crud.submit_session_answers(db=db, session=session, payload=payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    session = crud.get_session_by_token(db=db, token=token)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    state = crud.get_session_quiz_state(db=db, session=session)
    has_result = crud.get_result_by_session_id(db=db, session_id=session.id) is not None
    logger.info(
        "submit_answers token=%s session_id=%s role=%s completed=%s status=%s "
        "creator_telegram_id=%s initiator_telegram_id=%s payment_status=%s "
        "initiator_answered=%s partner_answered=%s has_result=%s",
        token,
        session.id,
        role,
        completed,
        session.status,
        session.creator_telegram_id,
        session.initiator_telegram_id,
        session.payment_status,
        state["initiator_answered"],
        state["partner_answered"],
        has_result,
    )

    if _should_notify_user1_after_submit(completed=completed, session=session, db=db):
        fallback_base = resolve_public_base_url(
            fallback_base_url=str(request.base_url).rstrip("/"),
        )
        logger.info(
            "Scheduling User1 Telegram notify token=%s session_id=%s role=%s public_base=%s",
            token,
            session.id,
            role,
            fallback_base or "(empty)",
        )
        background_tasks.add_task(
            _notify_initiator_partner_completed,
            token,
            str(request.base_url).rstrip("/"),
        )
    else:
        logger.info(
            "Skipping User1 Telegram notify token=%s completed=%s role=%s "
            "initiator_answered=%s partner_answered=%s",
            token,
            completed,
            role,
            state["initiator_answered"],
            state["partner_answered"],
        )

    return {"status": "completed" if completed else "partial"}


@router.post("/api/sessions/{token}/events/invite-share", tags=["sessions"])
def track_invite_share_clicked(token: str, db: DbSession = Depends(get_db)) -> dict[str, bool]:
    session = crud.get_session_by_token(db=db, token=token)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    recorded = record_love_product_event(
        db,
        session_token=token,
        event_type="invite_share_clicked",
        metadata={"channel": "telegram"},
    )
    return {"ok": recorded}


@router.get("/api/sessions/{token}/result", response_model=schemas.ResultRead, tags=["results"])
def get_session_result(
    token: str,
    db: DbSession = Depends(get_db),
) -> schemas.ResultRead:
    session = crud.get_session_by_token(db=db, token=token)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    result = crud.get_result_by_session_id(db=db, session_id=session.id)
    if result is None:
        result = crud.ensure_result_for_session(db=db, session=session)

    if result is None:
        state = crud.get_session_quiz_state(db=db, session=session)
        if not state["initiator_answered"] or not state["partner_answered"]:
            raise HTTPException(
                status_code=400,
                detail="Natija hali yo‘q: ikkala tomon ham savollarni tugatishi kerak.",
            )
        raise HTTPException(
            status_code=400,
            detail="Natija hisoblanmadi: javoblar bor, lekin result saqlanmadi.",
        )

    payload = crud.build_result_payload_from_row(result=result)
    crud.increment_result_view(db=db, session=session)
    return schemas.ResultRead(**payload)


@router.post("/api/sessions/{token}/premium-interest", tags=["results"])
def record_premium_interest(
    token: str,
    db: DbSession = Depends(get_db),
) -> dict[str, int | str]:
    session = crud.get_session_by_token(db=db, token=token)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    count = crud.record_premium_interest(db=db, session=session)
    return {"status": "ok", "premium_interest_count": count}
