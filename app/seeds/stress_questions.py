from __future__ import annotations

from typing import TypedDict


STRESS_DIMENSIONS: tuple[str, ...] = (
    "emotional_pressure",
    "sleep_energy",
    "work_pressure",
    "relationship_pressure",
    "overthinking",
)


class StressOptionSeed(TypedDict):
    text: str
    score: int


class StressQuestionSeed(TypedDict):
    text: str
    dimension: str
    options: list[StressOptionSeed]


def _options(low: str, mild: str, medium: str, high: str) -> list[StressOptionSeed]:
    return [
        {"text": low, "score": 0},
        {"text": mild, "score": 1},
        {"text": medium, "score": 2},
        {"text": high, "score": 3},
    ]


STRESS_QUESTIONS: list[StressQuestionSeed] = [
    {
        "dimension": "emotional_pressure",
        "text": "So‘nggi kunlarda ichingizda bosim yoki siqilish qanchalik sezilyapti?",
        "options": _options("Deyarli sezilmayapti", "Ba'zan seziladi", "Ko‘p payt seziladi", "Deyarli doim bosim bor"),
    },
    {
        "dimension": "emotional_pressure",
        "text": "Mayda gap yoki holatlar kayfiyatingizga qanchalik tez ta’sir qilyapti?",
        "options": _options("Uncha ta’sir qilmaydi", "Ba'zan ta’sir qiladi", "Tez-tez ta’sir qiladi", "Juda tez ranjiyman yoki asabiylashaman"),
    },
    {
        "dimension": "emotional_pressure",
        "text": "O‘zingizni hissiy jihatdan to‘lib ketgandek his qilasizmi?",
        "options": _options("Yo‘q, o‘zimni barqaror his qilaman", "Ba'zan shunday bo‘ladi", "Ko‘pincha shunday his qilaman", "Deyarli har kuni ko‘tarish qiyin"),
    },
    {
        "dimension": "emotional_pressure",
        "text": "Xotirjam bo‘lish uchun odatdagidan ko‘proq vaqt kerak bo‘lyaptimi?",
        "options": _options("Yo‘q, tez tinchlanaman", "Ba'zan ko‘proq vaqt ketadi", "Ko‘pincha tinchlanish qiyin", "Uzoq vaqt tinchlana olmayman"),
    },
    {
        "dimension": "emotional_pressure",
        "text": "Kun davomida ichki bezovtalik yoki sababsiz xavotir paydo bo‘ladimi?",
        "options": _options("Deyarli yo‘q", "Kamdan-kam bo‘ladi", "Tez-tez bo‘ladi", "Deyarli doim bor"),
    },
    {
        "dimension": "emotional_pressure",
        "text": "Oxirgi paytda o‘zingizga nisbatan sabringiz kamayganini sezyapsizmi?",
        "options": _options("Yo‘q, odatdagidekman", "Biroz kamaygan", "Ancha kamaygan", "Juda kamaygan, o‘zimdan tez norozi bo‘laman"),
    },
    {
        "dimension": "sleep_energy",
        "text": "Uyqudan uyg‘onganda o‘zingizni qanchalik tetik his qilasiz?",
        "options": _options("Tetik va yengil", "Biroz charchoq bilan", "Ko‘pincha charchagan holda", "Deyarli doim holdan toygan holda"),
    },
    {
        "dimension": "sleep_energy",
        "text": "Kechasi uxlab qolish siz uchun qanchalik oson?",
        "options": _options("Oson uxlab qolaman", "Ba'zan cho‘ziladi", "Ko‘pincha qiyin", "Juda qiyin, uzoq vaqt aylantiradi"),
    },
    {
        "dimension": "sleep_energy",
        "text": "Kun davomida energiyangiz qanchalik tez tugaydi?",
        "options": _options("Odatda yetadi", "Kunning oxirida pasayadi", "Kunning o‘rtasidayoq kamayadi", "Ertalabdan charchoq seziladi"),
    },
    {
        "dimension": "sleep_energy",
        "text": "Dam olish kunlari ham charchoq qolayotganini sezasizmi?",
        "options": _options("Yo‘q, dam olsam tiklanaman", "Ba'zan qoladi", "Ko‘pincha qoladi", "Dam olsam ham tiklanmayman"),
    },
    {
        "dimension": "sleep_energy",
        "text": "Uyqu sifatingiz stress tufayli buzilayotgandek tuyuladimi?",
        "options": _options("Yo‘q", "Biroz", "Ancha", "Juda kuchli ta’sir qilyapti"),
    },
    {
        "dimension": "sleep_energy",
        "text": "Kundalik ishlarni boshlash uchun o‘zingizni majburlashga to‘g‘ri keladimi?",
        "options": _options("Yo‘q, tabiiy boshlayman", "Ba'zan", "Ko‘p kunlarda", "Deyarli har kuni"),
    },
    {
        "dimension": "work_pressure",
        "text": "Ish yoki o‘qishdagi vazifalar sizga qanchalik og‘ir tuyulyapti?",
        "options": _options("Boshqarish oson", "Biroz bosim bor", "Ancha og‘ir", "Juda og‘ir, yetib bo‘lmayapti"),
    },
    {
        "dimension": "work_pressure",
        "text": "Muddatlar yaqinlashganda tanangizda taranglik seziladimi?",
        "options": _options("Deyarli yo‘q", "Ba'zan seziladi", "Ko‘pincha seziladi", "Juda kuchli seziladi"),
    },
    {
        "dimension": "work_pressure",
        "text": "Bir vaqtning o‘zida ko‘p vazifa sizni qanchalik charchatadi?",
        "options": _options("Oson tartiblayman", "Biroz charchatadi", "Ancha charchatadi", "Juda charchatadi va bloklab qo‘yadi"),
    },
    {
        "dimension": "work_pressure",
        "text": "Xatoga yo‘l qo‘yishdan qo‘rqish ish unumdorligingizga ta’sir qilyaptimi?",
        "options": _options("Yo‘q", "Kam ta’sir qiladi", "Ko‘p ta’sir qiladi", "Juda kuchli to‘xtatib qo‘yadi"),
    },
    {
        "dimension": "work_pressure",
        "text": "Ish yoki o‘qish haqida bo‘sh vaqtda ham o‘ylab yurishingiz qanchalik ko‘p?",
        "options": _options("Kamdan-kam", "Ba'zan", "Ko‘pincha", "Deyarli doim xayolimda"),
    },
    {
        "dimension": "work_pressure",
        "text": "Mas’uliyatlar ko‘pligi sabab o‘zingizga vaqt qolmayotgandek tuyuladimi?",
        "options": _options("Yo‘q, muvozanat bor", "Ba'zan", "Ko‘pincha", "Ha, o‘zimga vaqt deyarli yo‘q"),
    },
    {
        "dimension": "relationship_pressure",
        "text": "Yaqin insonlar bilan muloqot sizni qanchalik charchatyapti?",
        "options": _options("Charchatmaydi", "Ba'zan charchatadi", "Ko‘pincha charchatadi", "Juda charchatadi, qochgim keladi"),
    },
    {
        "dimension": "relationship_pressure",
        "text": "Atrofdagilarning kutishlari sizga bosim bo‘lyaptimi?",
        "options": _options("Yo‘q", "Biroz", "Ancha", "Juda kuchli"),
    },
    {
        "dimension": "relationship_pressure",
        "text": "Kelishmovchiliklardan keyin uzoq vaqt ichingizda olib yurasizmi?",
        "options": _options("Yo‘q, tez qo‘yib yuboraman", "Ba'zan", "Ko‘pincha", "Juda uzoq vaqt"),
    },
    {
        "dimension": "relationship_pressure",
        "text": "O‘z ehtiyojingizni aytish o‘rniga boshqalarni ranjitmaslikka harakat qilasizmi?",
        "options": _options("Kamdan-kam", "Ba'zan", "Ko‘pincha", "Deyarli doim"),
    },
    {
        "dimension": "relationship_pressure",
        "text": "Yaqinlaringiz bilan gaplashgandan keyin o‘zingizni aybdor yoki charchagan his qilasizmi?",
        "options": _options("Deyarli yo‘q", "Ba'zan", "Ko‘pincha", "Deyarli har safar"),
    },
    {
        "dimension": "relationship_pressure",
        "text": "Sizga kerakli qo‘llab-quvvatlash yetmayotgandek tuyuladimi?",
        "options": _options("Yo‘q, yetarli", "Ba'zan yetmaydi", "Ko‘pincha yetmaydi", "Juda yetishmaydi"),
    },
    {
        "dimension": "overthinking",
        "text": "Bir voqeani qayta-qayta o‘ylab, tinmay tahlil qilasizmi?",
        "options": _options("Kamdan-kam", "Ba'zan", "Ko‘pincha", "Deyarli to‘xtata olmayman"),
    },
    {
        "dimension": "overthinking",
        "text": "Qaror qabul qilishdan oldin juda ko‘p ehtimollarni o‘ylab charchaysizmi?",
        "options": _options("Yo‘q, oson tanlayman", "Ba'zan", "Ko‘pincha", "Juda ko‘p, qaror qiyinlashadi"),
    },
    {
        "dimension": "overthinking",
        "text": "Kimdir javob bermasa, darhol turli taxminlar paydo bo‘ladimi?",
        "options": _options("Yo‘q, xotirjam kutaman", "Ba'zan", "Ko‘pincha", "Darhol eng yomonini o‘ylayman"),
    },
    {
        "dimension": "overthinking",
        "text": "Kechasi fikrlar oqimi uyquga xalal beradimi?",
        "options": _options("Deyarli yo‘q", "Ba'zan", "Ko‘pincha", "Juda ko‘p"),
    },
    {
        "dimension": "overthinking",
        "text": "O‘tmishdagi gaplaringiz yoki xatolaringizni ichingizda qayta ko‘rib chiqasizmi?",
        "options": _options("Kamdan-kam", "Ba'zan", "Ko‘pincha", "Juda tez-tez"),
    },
    {
        "dimension": "overthinking",
        "text": "Kelajakdagi noaniqliklar sizni qanchalik band qilib qo‘yadi?",
        "options": _options("Uncha band qilmaydi", "Biroz", "Ancha", "Juda kuchli, fikrim tinmaydi"),
    },
]


def _sync_stress_options(question, option_seeds: list[StressOptionSeed]) -> None:
    """Update StressOption rows in place; never delete options (user answers may reference them)."""
    from app import models

    by_score = {option.score: option for option in question.options}
    for option_data in option_seeds:
        score = option_data["score"]
        existing_option = by_score.get(score)
        if existing_option is None:
            question.options.append(
                models.StressOption(
                    text=option_data["text"],
                    score=score,
                ),
            )
        else:
            existing_option.text = option_data["text"]
            existing_option.score = score


def ensure_stress_questions_seeded(db) -> None:
    from sqlalchemy import select
    from sqlalchemy.orm import selectinload

    from app import models

    for question_data in STRESS_QUESTIONS:
        if question_data["dimension"] not in STRESS_DIMENSIONS:
            raise ValueError("Stress question dimension is invalid")
        if len(question_data["options"]) != 4:
            raise ValueError("Each stress question must have exactly 4 options")
        for option_data in question_data["options"]:
            if option_data["score"] not in (0, 1, 2, 3):
                raise ValueError("Stress option score must be 0, 1, 2 or 3")

        existing = db.execute(
            select(models.StressQuestion)
            .where(models.StressQuestion.text == question_data["text"])
            .options(selectinload(models.StressQuestion.options)),
        ).scalar_one_or_none()

        if existing is None:
            question = models.StressQuestion(
                text=question_data["text"],
                dimension=question_data["dimension"],
                is_active=True,
            )
            for option_data in question_data["options"]:
                question.options.append(
                    models.StressOption(
                        text=option_data["text"],
                        score=option_data["score"],
                    ),
                )
            db.add(question)
            continue

        existing.dimension = question_data["dimension"]
        existing.is_active = True
        _sync_stress_options(existing, question_data["options"])

    db.flush()
    db.commit()


if __name__ == "__main__":
    from app.core.database import Base, SessionLocal, engine

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        ensure_stress_questions_seeded(db)
        print(f"Seeded {len(STRESS_QUESTIONS)} stress questions.")
    finally:
        db.close()
