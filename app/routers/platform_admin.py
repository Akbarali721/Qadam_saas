from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session as DbSession

from app import crud
from app.admin_auth import verify_admin_token
from app.core.database import get_db
from app.core.templates import templates
from app.services import stats_service

router = APIRouter(tags=["platform-admin"])


@router.get("/admin/products", response_class=HTMLResponse)
def admin_products(
    request: Request,
    db: DbSession = Depends(get_db),
    _admin: None = Depends(verify_admin_token),
):
    return templates.TemplateResponse(
        request=request,
        name="admin/products.html",
        context={
            "products": crud.list_products(db=db),
            "product_stats": stats_service.get_all_product_stats(db=db),
        },
    )


@router.get("/admin/sessions", response_class=HTMLResponse)
def admin_sessions(
    request: Request,
    db: DbSession = Depends(get_db),
    _admin: None = Depends(verify_admin_token),
):
    sessions = (
        stats_service.platform_session_rows(db=db, limit=50)
        + stats_service.legacy_love_session_rows(db=db, limit=50)
    )
    sessions.sort(key=lambda row: row["created_at"], reverse=True)
    return templates.TemplateResponse(
        request=request,
        name="admin/sessions.html",
        context={"sessions": sessions[:50]},
    )


@router.get("/admin/events", response_class=HTMLResponse)
def admin_events(
    request: Request,
    db: DbSession = Depends(get_db),
    _admin: None = Depends(verify_admin_token),
):
    return templates.TemplateResponse(
        request=request,
        name="admin/events.html",
        context={"events": stats_service.latest_events(db=db, limit=50)},
    )
