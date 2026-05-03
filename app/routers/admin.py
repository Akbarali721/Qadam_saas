from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DbSession

from app import crud, models, schemas
from app.admin_auth import verify_admin_token
from app.database import get_db

router = APIRouter(tags=["admin"], dependencies=[Depends(verify_admin_token)])


@router.get("/api/admin/questions", response_model=list[schemas.QuestionRead])
def admin_list_questions(db: DbSession = Depends(get_db)) -> list[models.Question]:
    try:
        return crud.admin_list_questions(db=db)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/api/admin/questions", response_model=schemas.QuestionRead)
def admin_create_question(
    payload: schemas.AdminQuestionCreate,
    db: DbSession = Depends(get_db),
) -> models.Question:
    try:
        return crud.admin_create_question(db=db, payload=payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.put("/api/admin/questions/{question_id}", response_model=schemas.QuestionRead)
def admin_update_question(
    question_id: int,
    payload: schemas.AdminQuestionUpdate,
    db: DbSession = Depends(get_db),
) -> models.Question:
    try:
        return crud.admin_update_question(db=db, question_id=question_id, payload=payload)
    except ValueError as exc:
        if str(exc) == "Question not found":
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.delete("/api/admin/questions/{question_id}")
def admin_delete_question(
    question_id: int,
    db: DbSession = Depends(get_db),
) -> dict[str, str]:
    try:
        crud.admin_delete_question(db=db, question_id=question_id)
    except ValueError as exc:
        if str(exc) == "Question not found":
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"status": "ok"}
