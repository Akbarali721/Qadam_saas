from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, computed_field


class SessionCreate(BaseModel):
    initiator_name: str = Field(..., min_length=1, max_length=120)
    initiator_age: int = Field(..., ge=18, le=99)
    initiator_gender: str = Field(..., pattern="^(ayol|erkak)$")
    initiator_zodiac: str = Field(..., max_length=40)
    relationship_type: str = Field(
        ...,
        pattern="^(married|friends|dating)$",
        description="married=Er-xotin, friends=Tanishlar, dating=Uchrashuvdagilar",
    )
    creator_telegram_id: str | None = None
    initiator_telegram_id: str | None = None


class PartnerRegister(BaseModel):
    partner_name: str = Field(..., min_length=1, max_length=120)
    partner_age: int = Field(..., ge=18, le=99)
    partner_gender: str = Field(..., pattern="^(ayol|erkak)$")
    partner_zodiac: str = Field(..., max_length=40)
    partner_telegram_id: str | None = None


class SessionRead(BaseModel):
    id: int
    token: str
    initiator_name: str
    initiator_age: int
    initiator_gender: str
    initiator_zodiac: str | None
    relationship_type: str
    partner_name: str
    partner_age: int
    partner_gender: str
    partner_zodiac: str | None
    respondent_zodiac: str | None
    creator_telegram_id: str | None
    initiator_telegram_id: str | None
    partner_telegram_id: str | None
    is_premium: bool
    payment_status: str
    status: str
    created_at: datetime
    answered_at: datetime | None

    model_config = ConfigDict(from_attributes=True)

    @computed_field  # type: ignore[prop-decorator]
    @property
    def user1_telegram_id(self) -> str | None:
        """Telegram WebApp dan kelgan User1 ID (`initiator_telegram_id`)."""
        return self.initiator_telegram_id


class SessionStateRead(BaseModel):
    initiator_name: str
    partner_registered: bool
    initiator_answered: bool
    partner_answered: bool
    status: str


class SessionCreateRead(SessionRead):
    """share_url — hamkor uchun /start/{token} havolasi (eski klientlar uchun)."""

    share_url: str
    share_page_url: str
    partner_join_url: str
    initiator_questions_url: str


class OptionRead(BaseModel):
    id: int
    text: str
    weight: int

    model_config = ConfigDict(from_attributes=True)


class QuestionRead(BaseModel):
    id: int
    text: str
    order: int
    dimension: str
    gender_target: str
    relationship_type: str = "married"
    options: list[OptionRead]

    model_config = ConfigDict(from_attributes=True)


class AdminOptionInput(BaseModel):
    text: str
    value: int = Field(..., ge=1, le=4)


class AdminQuestionCreate(BaseModel):
    text: str
    order: int
    dimension: str
    gender_target: str = Field(default="both", pattern="^(female|male|both)$")
    relationship_type: str = Field(default="married", pattern="^(married|friends|dating)$")
    options: list[AdminOptionInput] = Field(..., min_length=4, max_length=4)


class AdminQuestionUpdate(BaseModel):
    text: str
    order: int
    dimension: str
    gender_target: str = Field(default="both", pattern="^(female|male|both)$")
    relationship_type: str = Field(default="married", pattern="^(married|friends|dating)$")
    options: list[AdminOptionInput] = Field(..., min_length=4, max_length=4)


class AnswerSubmitItem(BaseModel):
    question_id: int
    option_id: int


class AnswerSubmitRequest(BaseModel):
    role: str = Field(..., pattern="^(initiator|partner)$")
    answers: list[AnswerSubmitItem] = Field(..., min_length=1)


class ResultRead(BaseModel):
    score: int
    total_score: int
    dimension_scores: dict[str, int]
    summary: str
    advice: str
    differences: str
    initiator_zodiac: str | None
    partner_zodiac: str | None
    zodiac_summary: str
