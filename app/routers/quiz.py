from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session as DbSession

from app import crud, models, schemas
from app.database import get_db

router = APIRouter()


@router.post("/api/sessions", response_model=schemas.SessionCreateRead, tags=["sessions"])
def create_session(
    request: Request,
    payload: schemas.SessionCreate,
    db: DbSession = Depends(get_db),
) -> schemas.SessionCreateRead:
    session = crud.create_session(db=db, payload=payload)
    base = str(request.base_url).rstrip("/")
    token = session.token
    share_page_url = f"{base}/share/{token}"
    partner_join_url = f"{base}/start/{token}"
    initiator_questions_url = f"{base}/questions.html?token={token}&role=initiator"
    return schemas.SessionCreateRead(
        **schemas.SessionRead.model_validate(session).model_dump(),
        share_url=partner_join_url,
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
def unlock_premium(token: str, db: DbSession = Depends(get_db)) -> dict[str, bool | str]:
    session = crud.get_session_by_token(db=db, token=token)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    unlocked = crud.unlock_session_premium(db=db, session=session)
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
    return crud.get_session_questions(db=db, session=session)


@router.post("/api/sessions/{token}/answers", tags=["answers"])
def submit_answers(
    token: str,
    payload: schemas.AnswerSubmitRequest,
    db: DbSession = Depends(get_db),
) -> dict[str, str]:
    session = crud.get_session_by_token(db=db, token=token)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.status == "completed":
        raise HTTPException(status_code=409, detail="Test allaqachon yakunlangan")

    try:
        completed = crud.submit_session_answers(db=db, session=session, payload=payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {"status": "completed" if completed else "partial"}


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
