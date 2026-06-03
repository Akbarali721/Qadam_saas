from datetime import datetime
from typing import Optional

import json

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.product import Product
from app.models.platform import PlatformUser, ProductEvent, ProductSession


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    token: Mapped[str] = mapped_column(String(128), unique=True, index=True, nullable=False)
    creator_telegram_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    initiator_telegram_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    partner_telegram_id: Mapped[str | None] = mapped_column(String(64), nullable=True)

    initiator_name: Mapped[str] = mapped_column(String(120), nullable=False, server_default="")
    initiator_age: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    initiator_gender: Mapped[str] = mapped_column(String(16), nullable=False, server_default="erkak")
    initiator_zodiac: Mapped[str | None] = mapped_column(String(40), nullable=True)
    respondent_gender: Mapped[str] = mapped_column(String(16), nullable=False, server_default="female")

    partner_name: Mapped[str] = mapped_column(String(120), nullable=False, server_default="")
    partner_age: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    partner_gender: Mapped[str] = mapped_column(String(16), nullable=False, server_default="")
    partner_zodiac: Mapped[str | None] = mapped_column(String(40), nullable=True)

    respondent_zodiac: Mapped[str | None] = mapped_column(String(40), nullable=True)

    relationship_type: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        server_default="married",
    )

    answers_initiator: Mapped[str] = mapped_column(Text(), nullable=False, server_default="{}")
    answers_partner: Mapped[str] = mapped_column(Text(), nullable=False, server_default="{}")
    questions_json: Mapped[str] = mapped_column(Text(), nullable=False, server_default="[]")
    is_premium: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="0")
    payment_status: Mapped[str] = mapped_column(String(16), nullable=False, default="none", server_default="none")
    result_view_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
    premium_interest_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
    completion_notify_sent: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="0",
    )

    status: Mapped[str] = mapped_column(String(32), nullable=False, server_default="started")
    current_question_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        server_default=func.now(),
        nullable=False,
    )
    started_at: Mapped[datetime | None] = mapped_column(DateTime(), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(), nullable=True)
    last_activity_at: Mapped[datetime | None] = mapped_column(DateTime(), nullable=True)
    answered_at: Mapped[datetime | None] = mapped_column(DateTime(), nullable=True)

    answers: Mapped[list["Answer"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan",
    )
    result: Mapped[Optional["Result"]] = relationship(
        back_populates="session",
        uselist=False,
        cascade="all, delete-orphan",
    )


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    text: Mapped[str] = mapped_column(String(500), nullable=False)
    order: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    dimension: Mapped[str] = mapped_column(String(64), nullable=False, server_default="communication")
    gender_target: Mapped[str] = mapped_column(
        Enum("male", "female", "both", name="question_gender_target"),
        nullable=False,
        server_default="both",
    )
    relationship_type: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        server_default="married",
    )

    options: Mapped[list["Option"]] = relationship(
        back_populates="question",
        cascade="all, delete-orphan",
    )
    answers: Mapped[list["Answer"]] = relationship(back_populates="question")


class Option(Base):
    __tablename__ = "options"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"), nullable=False)
    text: Mapped[str] = mapped_column(String(500), nullable=False)
    value: Mapped[int] = mapped_column(Integer, nullable=False)

    question: Mapped[Question] = relationship(back_populates="options")
    answers: Mapped[list["Answer"]] = relationship(back_populates="option")

    @property
    def weight(self) -> int:
        return self.value


class Answer(Base):
    __tablename__ = "answers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"), nullable=False)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"), nullable=False)
    option_id: Mapped[int] = mapped_column(ForeignKey("options.id"), nullable=False)

    session: Mapped[Session] = relationship(back_populates="answers")
    question: Mapped[Question] = relationship(back_populates="answers")
    option: Mapped[Option] = relationship(back_populates="answers")


class Result(Base):
    __tablename__ = "results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"), unique=True, nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    dimension_scores: Mapped[str] = mapped_column(String(2000), nullable=False, server_default="{}")
    summary: Mapped[str] = mapped_column(String(500), nullable=False)
    advice: Mapped[str] = mapped_column(String(500), nullable=False, server_default="")
    differences: Mapped[str] = mapped_column(String(2000), nullable=False, server_default="")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        server_default=func.now(),
        nullable=False,
    )

    session: Mapped[Session] = relationship(back_populates="result")

    @property
    def dimension_scores_dict(self) -> dict[str, int]:
        try:
            parsed = json.loads(self.dimension_scores)
        except json.JSONDecodeError:
            return {}
        if not isinstance(parsed, dict):
            return {}
        return {str(key): int(value) for key, value in parsed.items()}


class MbtiQuestion(Base):
    __tablename__ = "mbti_questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    text: Mapped[str] = mapped_column(String(500), nullable=False)
    dimension: Mapped[str] = mapped_column(String(2), nullable=False, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="1")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        server_default=func.now(),
        nullable=False,
    )

    options: Mapped[list["MbtiOption"]] = relationship(
        back_populates="question",
        cascade="all, delete-orphan",
    )


class MbtiOption(Base):
    __tablename__ = "mbti_options"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("mbti_questions.id"), nullable=False, index=True)
    text: Mapped[str] = mapped_column(String(500), nullable=False)
    pole: Mapped[str] = mapped_column(String(1), nullable=False, index=True)
    score: Mapped[int] = mapped_column(Integer, nullable=False)

    question: Mapped[MbtiQuestion] = relationship(back_populates="options")


class MbtiSession(Base):
    __tablename__ = "mbti_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    token: Mapped[str] = mapped_column(String(128), unique=True, index=True, nullable=False)
    selected_question_ids: Mapped[str] = mapped_column(Text(), nullable=False, server_default="[]")
    current_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
    answers_json: Mapped[str] = mapped_column(Text(), nullable=False, server_default="{}")
    result_type: Mapped[str | None] = mapped_column(String(4), nullable=True)
    is_premium: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="0")
    payment_status: Mapped[str] = mapped_column(String(16), nullable=False, default="none", server_default="none")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        server_default=func.now(),
        nullable=False,
    )
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(), nullable=True)


class StressQuestion(Base):
    __tablename__ = "stress_questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    text: Mapped[str] = mapped_column(String(500), nullable=False, unique=True)
    dimension: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="1")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        server_default=func.now(),
        nullable=False,
    )

    options: Mapped[list["StressOption"]] = relationship(
        back_populates="question",
        cascade="all, delete-orphan",
    )
    answers: Mapped[list["StressAnswer"]] = relationship(back_populates="question")


class StressOption(Base):
    __tablename__ = "stress_options"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("stress_questions.id"), nullable=False, index=True)
    text: Mapped[str] = mapped_column(String(500), nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)

    question: Mapped[StressQuestion] = relationship(back_populates="options")
    answers: Mapped[list["StressAnswer"]] = relationship(back_populates="option")


class StressSession(Base):
    __tablename__ = "stress_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    token: Mapped[str] = mapped_column(String(128), unique=True, index=True, nullable=False)
    selected_question_ids: Mapped[str] = mapped_column(Text(), nullable=False, server_default="[]")
    current_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
    is_premium: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="0")
    payment_status: Mapped[str] = mapped_column(String(16), nullable=False, default="none", server_default="none")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        server_default=func.now(),
        nullable=False,
    )
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(), nullable=True)

    answers: Mapped[list["StressAnswer"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan",
    )
    result: Mapped[Optional["StressResult"]] = relationship(
        back_populates="session",
        uselist=False,
        cascade="all, delete-orphan",
    )


class StressAnswer(Base):
    __tablename__ = "stress_answers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("stress_sessions.id"), nullable=False, index=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("stress_questions.id"), nullable=False, index=True)
    option_id: Mapped[int] = mapped_column(ForeignKey("stress_options.id"), nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    dimension: Mapped[str] = mapped_column(String(64), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        server_default=func.now(),
        nullable=False,
    )

    session: Mapped[StressSession] = relationship(back_populates="answers")
    question: Mapped[StressQuestion] = relationship(back_populates="answers")
    option: Mapped[StressOption] = relationship(back_populates="answers")


class StressResult(Base):
    __tablename__ = "stress_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("stress_sessions.id"), unique=True, nullable=False)
    total_score: Mapped[int] = mapped_column(Integer, nullable=False)
    level: Mapped[str] = mapped_column(String(16), nullable=False)
    strongest_dimension: Mapped[str] = mapped_column(String(64), nullable=False)
    dimension_scores: Mapped[str] = mapped_column(String(2000), nullable=False, server_default="{}")
    explanation: Mapped[str] = mapped_column(String(700), nullable=False)
    recommendations: Mapped[str] = mapped_column(Text(), nullable=False, server_default="[]")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        server_default=func.now(),
        nullable=False,
    )

    session: Mapped[StressSession] = relationship(back_populates="result")

    @property
    def dimension_scores_dict(self) -> dict[str, int]:
        try:
            parsed = json.loads(self.dimension_scores)
        except json.JSONDecodeError:
            return {}
        if not isinstance(parsed, dict):
            return {}
        return {str(key): int(value) for key, value in parsed.items()}

    @property
    def recommendations_list(self) -> list[str]:
        try:
            parsed = json.loads(self.recommendations)
        except json.JSONDecodeError:
            return []
        if not isinstance(parsed, list):
            return []
        return [str(item) for item in parsed]


__all__ = [
    "Answer",
    "MbtiOption",
    "MbtiQuestion",
    "MbtiSession",
    "Option",
    "PlatformUser",
    "Product",
    "ProductEvent",
    "ProductSession",
    "Question",
    "Result",
    "Session",
    "StressAnswer",
    "StressOption",
    "StressQuestion",
    "StressResult",
    "StressSession",
]
