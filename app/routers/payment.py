from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session as DbSession

from app.admin_auth import verify_admin_token
from app.core.database import get_db
from app.services import payment_service

router = APIRouter(prefix="/payment", tags=["payment"])


def _wants_html_redirect(request: Request) -> bool:
    accept = request.headers.get("accept", "")
    return "text/html" in accept


def _payment_response(request: Request, session) -> Any:
    if _wants_html_redirect(request):
        return RedirectResponse(
            url=request.headers.get("referer") or "/",
            status_code=303,
        )
    return {
        "status": "ok",
        "token": session.token,
        "payment_status": session.payment_status,
        "is_premium": bool(session.is_premium),
    }


@router.post("/request/{session_token}")
def request_payment(
    session_token: str,
    request: Request,
    db: DbSession = Depends(get_db),
) -> Any:
    session = payment_service.set_payment_requested(db=db, session_token=session_token)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return _payment_response(request=request, session=session)


@router.post("/approve/{session_token}", dependencies=[Depends(verify_admin_token)])
def approve_payment(
    session_token: str,
    request: Request,
    db: DbSession = Depends(get_db),
) -> Any:
    session = payment_service.approve_payment(db=db, session_token=session_token)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return _payment_response(request=request, session=session)


@router.post("/reject/{session_token}", dependencies=[Depends(verify_admin_token)])
def reject_payment(
    session_token: str,
    request: Request,
    db: DbSession = Depends(get_db),
) -> Any:
    session = payment_service.reject_payment(db=db, session_token=session_token)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return _payment_response(request=request, session=session)
