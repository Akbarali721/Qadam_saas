import os

from sqlalchemy import text
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.crud import (
    ensure_mbti_questions_seeded,
    ensure_products_seeded,
    ensure_relationship_questions_seeded,
    ensure_stress_questions_seeded,
)
from app.core.config import BASE_DIR
from app.core.database import Base, SessionLocal, engine
from app.core.migrations import run_platform_startup_migrations
from app.routers import admin, admin_dashboard, love, mbti, payment, pdf, platform_admin, stress


app = FastAPI(title="Qadam API")

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    try:
        body = await request.json()
    except Exception:
        body = None
    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors(),
            "received_body": body,
        },
    )


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
    run_platform_startup_migrations(engine)
    _run_lightweight_migrations()
    db = SessionLocal()
    try:
        ensure_products_seeded(db)
        ensure_relationship_questions_seeded(db)
        ensure_mbti_questions_seeded(db)
        ensure_stress_questions_seeded(db)
    finally:
        db.close()
    _print_startup_diagnostics()


def _print_startup_diagnostics() -> None:
    print(f"[startup] cwd={os.getcwd()}", flush=True)
    print(f"[startup] imported_app={__name__}:app file={__file__} app_id={id(app)}", flush=True)
    print("[startup] registered routes:", flush=True)
    for route in sorted(app.routes, key=lambda item: (getattr(item, "path", ""), getattr(item, "name", ""))):
        methods = ",".join(sorted(getattr(route, "methods", []) or [])) or "-"
        print(f"[startup] route {methods} {route.path} name={route.name}", flush=True)


def _run_lightweight_migrations() -> None:
    if engine.dialect.name != "sqlite":
        return

    with engine.begin() as connection:
        session_columns = connection.execute(text("PRAGMA table_info(sessions)")).mappings().all()
        session_column_names = {column["name"] for column in session_columns}
        if "initiator_name" not in session_column_names:
            connection.execute(
                text(
                    "ALTER TABLE sessions ADD COLUMN initiator_name VARCHAR(120) "
                    "NOT NULL DEFAULT ''",
                ),
            )
        if "initiator_age" not in session_column_names:
            connection.execute(
                text(
                    "ALTER TABLE sessions ADD COLUMN initiator_age INTEGER "
                    "NOT NULL DEFAULT 0",
                ),
            )
        if "initiator_zodiac" not in session_column_names:
            connection.execute(
                text("ALTER TABLE sessions ADD COLUMN initiator_zodiac VARCHAR(40)"),
            )
        if "initiator_gender" not in session_column_names:
            connection.execute(
                text(
                    "ALTER TABLE sessions ADD COLUMN initiator_gender VARCHAR(16) "
                    "NOT NULL DEFAULT 'erkak'",
                ),
            )
        if "respondent_gender" not in session_column_names:
            connection.execute(
                text(
                    "ALTER TABLE sessions ADD COLUMN respondent_gender VARCHAR(16) "
                    "NOT NULL DEFAULT 'female'",
                ),
            )
        if "respondent_zodiac" not in session_column_names:
            connection.execute(
                text("ALTER TABLE sessions ADD COLUMN respondent_zodiac VARCHAR(40)"),
            )
        if "relationship_type" not in session_column_names:
            connection.execute(
                text(
                    "ALTER TABLE sessions ADD COLUMN relationship_type VARCHAR(32) "
                    "NOT NULL DEFAULT 'married'",
                ),
            )
        if "partner_name" not in session_column_names:
            connection.execute(
                text(
                    "ALTER TABLE sessions ADD COLUMN partner_name VARCHAR(120) "
                    "NOT NULL DEFAULT ''",
                ),
            )
        if "partner_age" not in session_column_names:
            connection.execute(
                text(
                    "ALTER TABLE sessions ADD COLUMN partner_age INTEGER NOT NULL DEFAULT 0",
                ),
            )
        if "partner_gender" not in session_column_names:
            connection.execute(
                text(
                    "ALTER TABLE sessions ADD COLUMN partner_gender VARCHAR(16) "
                    "NOT NULL DEFAULT ''",
                ),
            )
        if "partner_zodiac" not in session_column_names:
            connection.execute(
                text("ALTER TABLE sessions ADD COLUMN partner_zodiac VARCHAR(40)"),
            )
        if "answers_initiator" not in session_column_names:
            connection.execute(
                text(
                    "ALTER TABLE sessions ADD COLUMN answers_initiator TEXT "
                    "NOT NULL DEFAULT '{}'",
                ),
            )
        if "answers_partner" not in session_column_names:
            connection.execute(
                text(
                    "ALTER TABLE sessions ADD COLUMN answers_partner TEXT "
                    "NOT NULL DEFAULT '{}'",
                ),
            )
        if "questions_json" not in session_column_names:
            connection.execute(
                text(
                    "ALTER TABLE sessions ADD COLUMN questions_json TEXT "
                    "NOT NULL DEFAULT '[]'",
                ),
            )
        if "is_premium" not in session_column_names:
            connection.execute(
                text(
                    "ALTER TABLE sessions ADD COLUMN is_premium BOOLEAN "
                    "NOT NULL DEFAULT 0",
                ),
            )
        if "payment_status" not in session_column_names:
            connection.execute(
                text(
                    "ALTER TABLE sessions ADD COLUMN payment_status VARCHAR(16) "
                    "NOT NULL DEFAULT 'none'",
                ),
            )
        if "result_view_count" not in session_column_names:
            connection.execute(
                text(
                    "ALTER TABLE sessions ADD COLUMN result_view_count INTEGER "
                    "NOT NULL DEFAULT 0",
                ),
            )
        if "premium_interest_count" not in session_column_names:
            connection.execute(
                text(
                    "ALTER TABLE sessions ADD COLUMN premium_interest_count INTEGER "
                    "NOT NULL DEFAULT 0",
                ),
            )
        connection.execute(
            text("UPDATE sessions SET payment_status = 'approved' WHERE is_premium = 1"),
        )

        connection.execute(text("UPDATE sessions SET status = 'created' WHERE status = 'new'"))
        connection.execute(text("UPDATE sessions SET status = 'completed' WHERE status = 'answered'"))
        connection.execute(
            text(
                "UPDATE sessions SET respondent_gender = CASE "
                "WHEN initiator_gender = 'ayol' THEN 'male' "
                "ELSE 'female' END",
            ),
        )

        columns = connection.execute(text("PRAGMA table_info(questions)")).mappings().all()
        column_names = {column["name"] for column in columns}
        if "dimension" not in column_names:
            connection.execute(
                text(
                    "ALTER TABLE questions ADD COLUMN dimension VARCHAR(64) "
                    "NOT NULL DEFAULT 'communication'",
                ),
            )
        if "gender_target" not in column_names:
            connection.execute(
                text(
                    "ALTER TABLE questions ADD COLUMN gender_target VARCHAR(16) "
                    "NOT NULL DEFAULT 'both'",
                ),
            )
        if "relationship_type" not in column_names:
            connection.execute(
                text(
                    "ALTER TABLE questions ADD COLUMN relationship_type VARCHAR(32) "
                    "NOT NULL DEFAULT 'married'",
                ),
            )

        result_columns = connection.execute(text("PRAGMA table_info(results)")).mappings().all()
        result_column_names = {column["name"] for column in result_columns}
        if "dimension_scores" not in result_column_names:
            connection.execute(
                text(
                    "ALTER TABLE results ADD COLUMN dimension_scores VARCHAR(2000) "
                    "NOT NULL DEFAULT '{}'",
                ),
            )
        if "advice" not in result_column_names:
            connection.execute(
                text(
                    "ALTER TABLE results ADD COLUMN advice VARCHAR(500) "
                    "NOT NULL DEFAULT ''",
                ),
            )
        if "differences" not in result_column_names:
            connection.execute(
                text(
                    "ALTER TABLE results ADD COLUMN differences VARCHAR(2000) "
                    "NOT NULL DEFAULT ''",
                ),
            )

        mbti_session_columns = connection.execute(text("PRAGMA table_info(mbti_sessions)")).mappings().all()
        mbti_session_column_names = {column["name"] for column in mbti_session_columns}
        if "is_premium" not in mbti_session_column_names:
            connection.execute(
                text(
                    "ALTER TABLE mbti_sessions ADD COLUMN is_premium BOOLEAN "
                    "NOT NULL DEFAULT 0",
                ),
            )
        if "payment_status" not in mbti_session_column_names:
            connection.execute(
                text(
                    "ALTER TABLE mbti_sessions ADD COLUMN payment_status VARCHAR(16) "
                    "NOT NULL DEFAULT 'none'",
                ),
            )
        connection.execute(
            text("UPDATE mbti_sessions SET payment_status = 'approved' WHERE is_premium = 1"),
        )

        stress_session_columns = connection.execute(text("PRAGMA table_info(stress_sessions)")).mappings().all()
        stress_session_column_names = {column["name"] for column in stress_session_columns}
        if "is_premium" not in stress_session_column_names:
            connection.execute(
                text(
                    "ALTER TABLE stress_sessions ADD COLUMN is_premium BOOLEAN "
                    "NOT NULL DEFAULT 0",
                ),
            )
        if "payment_status" not in stress_session_column_names:
            connection.execute(
                text(
                    "ALTER TABLE stress_sessions ADD COLUMN payment_status VARCHAR(16) "
                    "NOT NULL DEFAULT 'none'",
                ),
            )
        connection.execute(
            text("UPDATE stress_sessions SET payment_status = 'approved' WHERE is_premium = 1"),
        )

        # Keep previously seeded datasets compatible with the current dimension set.
        connection.execute(
            text(
                "UPDATE questions SET dimension = 'emotional_closeness' "
                "WHERE dimension = 'emotional_openness'",
            ),
        )
        connection.execute(
            text(
                "UPDATE questions SET dimension = 'attention' "
                "WHERE dimension = 'conflict_style'",
            ),
        )
        connection.execute(
            text("UPDATE questions SET gender_target = 'both' WHERE gender_target IS NULL"),
        )
        connection.execute(
            text("UPDATE questions SET gender_target = 'female' WHERE \"order\" = 3"),
        )
        connection.execute(
            text("UPDATE questions SET gender_target = 'male' WHERE \"order\" = 4"),
        )
        connection.execute(
            text("UPDATE questions SET gender_target = 'both' WHERE \"order\" IN (1, 2, 5)"),
        )

        # Keep default seed dataset in Uzbek for already existing databases.
        connection.execute(
            text(
                "UPDATE questions SET text = "
                "'Siz hislaringiz haqida bir-biringiz bilan qanchalik ochiq gaplashasiz?' "
                "WHERE \"order\" = 1",
            ),
        )
        connection.execute(
            text(
                "UPDATE questions SET text = 'Siz juftingizga qanchalik ishonasiz?' "
                "WHERE \"order\" = 2",
            ),
        )
        connection.execute(
            text(
                "UPDATE questions SET text = "
                "'Sizga nozik o‘y-fikrlaringizni bo‘lishish qanchalik oson?' "
                "WHERE \"order\" = 3",
            ),
        )
        connection.execute(
            text(
                "UPDATE questions SET text = "
                "'Kelishmovchilik chiqqanda odatda qanday yo‘l tutasiz?' "
                "WHERE \"order\" = 4",
            ),
        )
        connection.execute(
            text(
                "UPDATE questions SET text = "
                "'Bir-biringizdan kutgan narsalarni qanchalik aniq aytasiz?' "
                "WHERE \"order\" = 5",
            ),
        )
        connection.execute(
            text(
                "UPDATE options SET text = 'Deyarli gaplashmaymiz' "
                "WHERE question_id IN (SELECT id FROM questions WHERE \"order\" = 1) AND value = 1",
            ),
        )
        connection.execute(
            text(
                "UPDATE options SET text = 'Ba''zan, faqat muhim paytlarda' "
                "WHERE question_id IN (SELECT id FROM questions WHERE \"order\" = 1) AND value = 2",
            ),
        )
        connection.execute(
            text(
                "UPDATE options SET text = 'Ko‘pincha, yetarli darajada gaplashamiz' "
                "WHERE question_id IN (SELECT id FROM questions WHERE \"order\" = 1) AND value = 3",
            ),
        )
        connection.execute(
            text(
                "UPDATE options SET text = 'Har kuni deyarli juda ochiq gaplashamiz' "
                "WHERE question_id IN (SELECT id FROM questions WHERE \"order\" = 1) AND value = 4",
            ),
        )
        connection.execute(
            text(
                "UPDATE options SET text = 'Ko‘p holatda shubhalanaman' "
                "WHERE question_id IN (SELECT id FROM questions WHERE \"order\" = 2) AND value = 1",
            ),
        )
        connection.execute(
            text(
                "UPDATE options SET text = 'Ba''zi vaziyatlarda ishonaman' "
                "WHERE question_id IN (SELECT id FROM questions WHERE \"order\" = 2) AND value = 2",
            ),
        )
        connection.execute(
            text(
                "UPDATE options SET text = 'Asosan ishonaman' "
                "WHERE question_id IN (SELECT id FROM questions WHERE \"order\" = 2) AND value = 3",
            ),
        )
        connection.execute(
            text(
                "UPDATE options SET text = 'To‘liq ishonaman' "
                "WHERE question_id IN (SELECT id FROM questions WHERE \"order\" = 2) AND value = 4",
            ),
        )
        connection.execute(
            text(
                "UPDATE options SET text = 'Bunday mavzulardan qochaman' "
                "WHERE question_id IN (SELECT id FROM questions WHERE \"order\" = 3) AND value = 1",
            ),
        )
        connection.execute(
            text(
                "UPDATE options SET text = 'Faqat so‘rashsa aytaman' "
                "WHERE question_id IN (SELECT id FROM questions WHERE \"order\" = 3) AND value = 2",
            ),
        )
        connection.execute(
            text(
                "UPDATE options SET text = 'Kerak bo‘lsa bo‘lishaman' "
                "WHERE question_id IN (SELECT id FROM questions WHERE \"order\" = 3) AND value = 3",
            ),
        )
        connection.execute(
            text(
                "UPDATE options SET text = 'Bemalol aytaman, o‘zimni xavfsiz his qilaman' "
                "WHERE question_id IN (SELECT id FROM questions WHERE \"order\" = 3) AND value = 4",
            ),
        )
        connection.execute(
            text(
                "UPDATE options SET text = 'Gapni yopib, uzoqlashib ketamiz' "
                "WHERE question_id IN (SELECT id FROM questions WHERE \"order\" = 4) AND value = 1",
            ),
        )
        connection.execute(
            text(
                "UPDATE options SET text = 'Muammoning bir qismini hal qilamiz' "
                "WHERE question_id IN (SELECT id FROM questions WHERE \"order\" = 4) AND value = 2",
            ),
        )
        connection.execute(
            text(
                "UPDATE options SET text = 'Gaplashib, ko‘pini hal qilamiz' "
                "WHERE question_id IN (SELECT id FROM questions WHERE \"order\" = 4) AND value = 3",
            ),
        )
        connection.execute(
            text(
                "UPDATE options SET text = 'Sokin va hurmat bilan to‘liq hal qilamiz' "
                "WHERE question_id IN (SELECT id FROM questions WHERE \"order\" = 4) AND value = 4",
            ),
        )
        connection.execute(
            text(
                "UPDATE options SET text = 'Ko‘pincha noaniq qoladi' "
                "WHERE question_id IN (SELECT id FROM questions WHERE \"order\" = 5) AND value = 1",
            ),
        )
        connection.execute(
            text(
                "UPDATE options SET text = 'Ba''zan aniq, ba''zan taxmin qilamiz' "
                "WHERE question_id IN (SELECT id FROM questions WHERE \"order\" = 5) AND value = 2",
            ),
        )
        connection.execute(
            text(
                "UPDATE options SET text = "
                "'Asosan aniq, kamdan-kam tushunmovchilik bo‘ladi' "
                "WHERE question_id IN (SELECT id FROM questions WHERE \"order\" = 5) AND value = 3",
            ),
        )
        connection.execute(
            text(
                "UPDATE options SET text = 'Doim aniq va tushunarli aytamiz' "
                "WHERE question_id IN (SELECT id FROM questions WHERE \"order\" = 5) AND value = 4",
            ),
        )


@app.get("/health", tags=["system"])
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}

app.include_router(love.router)
app.include_router(mbti.router)
app.include_router(stress.router)
app.include_router(payment.router)
app.include_router(pdf.router)
app.include_router(admin_dashboard.router)
app.include_router(platform_admin.router)
app.include_router(admin.router)
