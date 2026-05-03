from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session as DbSession

from app.core.database import get_db
from app.services import pdf_service

router = APIRouter(prefix="/pdf", tags=["pdf"])


@router.get("/{test_type}/{session_token}")
def download_pdf_report(
    test_type: str,
    session_token: str,
    db: DbSession = Depends(get_db),
) -> Response:
    if not pdf_service.is_supported_test_type(test_type):
        raise HTTPException(status_code=404, detail="Test type not found")

    session = pdf_service.get_session_for_pdf(db=db, test_type=test_type, token=session_token)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    if not pdf_service.is_pdf_allowed(session):
        raise HTTPException(status_code=403, detail="Premium payment is not approved")

    report = pdf_service.build_premium_report(db=db, test_type=test_type, token=session_token)
    if report is None:
        raise HTTPException(status_code=404, detail="Result not found")

    pdf_bytes = pdf_service.generate_pdf_bytes(report)
    filename = f"qadam-{test_type}-{session_token[:10]}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
