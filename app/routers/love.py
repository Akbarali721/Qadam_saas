import json

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session as DbSession

from app import crud, models, schemas
from app.core.database import get_db
from app.core.templates import templates
from app.services import pdf_service

router = APIRouter(tags=["love"])


@router.get("/", response_class=HTMLResponse)
def index_page(request: Request):
    return templates.TemplateResponse(request=request, name="love/index.html")


@router.get("/share/{token}", response_class=HTMLResponse)
def share_page(request: Request, token: str, db: DbSession = Depends(get_db)):
    session = crud.get_session_by_token(db=db, token=token)
    if session is None:
        raise HTTPException(status_code=404, detail="Sessiya topilmadi")
    state = crud.get_session_quiz_state(db=db, session=session)
    if not state["initiator_answered"]:
        return RedirectResponse(url=f"/quiz/init/{token}", status_code=303)
    base = str(request.base_url).rstrip("/")
    return templates.TemplateResponse(
        request=request,
        name="love/share.html",
        context={
            "token": token,
            "initiator_name": session.initiator_name,
            "partner_start_url": f"{base}/start/{token}",
            "initiator_questions_url": f"{base}/questions.html?token={token}&role=initiator",
        },
    )


@router.get("/start/{token}", response_class=HTMLResponse)
def partner_landing_page(request: Request, token: str, db: DbSession = Depends(get_db)):
    session = crud.get_session_by_token(db=db, token=token)
    if session is None:
        raise HTTPException(status_code=404, detail="Sessiya topilmadi")
    return templates.TemplateResponse(
        request=request,
        name="love/partner.html",
        context={
            "token": token,
            "initiator_name": session.initiator_name,
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
