import hmac
import os

from fastapi import Header, HTTPException, Query, status

from app.core.config import load_environment


def verify_admin_token(
    token: str | None = Query(default=None),
    x_admin_token: str | None = Header(default=None, alias="X-Admin-Token"),
) -> None:
    load_environment()
    admin_token = os.getenv("ADMIN_TOKEN")
    if not admin_token:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="ADMIN_TOKEN is not configured",
        )

    provided_token = x_admin_token or token
    if not provided_token or not hmac.compare_digest(provided_token, admin_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )
