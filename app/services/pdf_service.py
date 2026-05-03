from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from html import escape
from io import BytesIO
from pathlib import Path
from typing import Any

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    ListFlowable,
    ListItem,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app import crud, models
from app.services.mbti_profiles import generate_mbti_result, get_mbti_profile
from app.services.payment_service import PAYMENT_APPROVED

FOOTER_TEXT = "Bu tahlil umumiy o‘zini anglash va rivojlanish uchun mo‘ljallangan."
SUPPORTED_TEST_TYPES = {"love", "mbti", "stress"}

DIMENSION_LABELS = {
    "communication": "Muloqot",
    "trust": "Ishonch",
    "attention": "E’tibor",
    "emotional_closeness": "Hissiy yaqinlik",
}

STRESS_DIMENSION_LABELS = {
    "emotional_pressure": "Hissiy bosim",
    "sleep_energy": "Uyqu va energiya",
    "work_pressure": "Ish/o‘qish bosimi",
    "relationship_pressure": "Munosabatlar bosimi",
    "overthinking": "Ortiqcha o‘ylash",
}

STRESS_LEVEL_TITLES = {
    "low": "Past stress",
    "medium": "O‘rtacha stress",
    "high": "Yuqori stress",
}


@dataclass(frozen=True)
class PremiumReport:
    test_type: str
    test_name: str
    session_token: str
    result_url: str
    user_name: str
    date_text: str
    summary: str
    score_label: str
    strong_sides: list[str]
    weak_sides: list[str]
    main_risk: str
    recommendations: list[str]
    seven_day_plan: list[str]
    conclusion: str

    def as_context(self) -> dict[str, Any]:
        return {
            "test_type": self.test_type,
            "test_name": self.test_name,
            "session_token": self.session_token,
            "result_url": self.result_url,
            "user_name": self.user_name,
            "date_text": self.date_text,
            "summary": self.summary,
            "score_label": self.score_label,
            "strong_sides": self.strong_sides,
            "weak_sides": self.weak_sides,
            "main_risk": self.main_risk,
            "recommendations": self.recommendations,
            "seven_day_plan": self.seven_day_plan,
            "conclusion": self.conclusion,
        }


def is_supported_test_type(test_type: str) -> bool:
    return test_type in SUPPORTED_TEST_TYPES


def result_url_for(test_type: str, token: str) -> str:
    if test_type == "love":
        return f"/result/{token}"
    if test_type == "mbti":
        return f"/mbti/result/{token}"
    return f"/stress/result/{token}"


def is_pdf_allowed(session: Any) -> bool:
    return bool(session.is_premium) and session.payment_status == PAYMENT_APPROVED


def _date_text(value: datetime | None) -> str:
    date_value = value or datetime.utcnow()
    return date_value.strftime("%Y-%m-%d")


def _label(key: str, labels: dict[str, str]) -> str:
    return labels.get(key, key.replace("_", " "))


def _sorted_dimensions(scores: dict[str, int]) -> list[tuple[str, int]]:
    return sorted(scores.items(), key=lambda item: item[1], reverse=True)


def _get_love_report(db: Session, token: str) -> PremiumReport | None:
    session = crud.get_session_by_token(db=db, token=token)
    if session is None:
        return None

    result = crud.get_result_by_session_id(db=db, session_id=session.id)
    if result is None:
        result = crud.ensure_result_for_session(db=db, session=session)
    if result is None:
        return None

    payload = crud.build_result_payload_from_row(result=result)
    scores = payload["dimension_scores"]
    if not scores:
        scores = {"communication": payload["total_score"]}
    sorted_scores = _sorted_dimensions(scores)
    strong = [key for key, value in sorted_scores if value >= 60] or [sorted_scores[0][0]]
    weak = [key for key, value in sorted_scores if value < 55] or [sorted_scores[-1][0]]
    strongest = _label(strong[0], DIMENSION_LABELS)
    weakest = _label(weak[0], DIMENSION_LABELS)
    names = " va ".join(
        name for name in [session.initiator_name, session.partner_name] if name
    ) or "Foydalanuvchi"

    return PremiumReport(
        test_type="love",
        test_name="Sevgi moslik testi",
        session_token=token,
        result_url=result_url_for("love", token),
        user_name=names,
        date_text=_date_text(result.created_at),
        summary=(
            f"Moslik ko‘rsatkichi {payload['total_score']}%. Bu natija munosabatda "
            f"{strongest.lower()} tayanch bo‘la olishini, {weakest.lower()} esa ongli e’tibor "
            "talab qiladigan nozik nuqta ekanini ko‘rsatadi."
        ),
        score_label=f"{payload['total_score']}% - {payload['summary']}",
        strong_sides=[
            f"{strongest} yo‘nalishida sizlarda iliqlik va bir-biringizni tushunishga tayyorlik bor.",
            "Kelishmovchilikdan keyin aloqani tiklash imkoniyatingiz yaxshi, agar suhbatni cho‘zib yubormasangiz.",
            "Munosabatda kichik e’tibor va samimiy so‘zlar tez ijobiy ta’sir beradi.",
        ],
        weak_sides=[
            f"{weakest} bo‘yicha kutishlar ochiq aytilmasa, mayda ranjishlar yig‘ilishi mumkin.",
            "Charchoq yoki shoshilinch vaziyatda ohang keskinlashib, asl niyat noto‘g‘ri tushunilishi ehtimoli bor.",
            "Muammo paytida kim haq ekanidan ko‘ra, ikkingiz nimani his qilayotganingizni aniqlash muhim.",
        ],
        main_risk=(
            f"Asosiy xavf {weakest.lower()} mavzusida gapni ichda olib yurish yoki sherik "
            "o‘zi tushunib oladi deb kutishdan boshlanadi. Bu holat yaqinlik bor joyda ham masofa paydo qilishi mumkin."
        ),
        recommendations=[
            "Haftasiga kamida bir marta 20 daqiqalik telefonsiz suhbat qiling.",
            "Tanqid o‘rniga “men shunday his qildim” shaklida gapirishga kelishing.",
            "Kutilmalarni oldindan ayting: vaqt, e’tibor, yordam va shaxsiy chegaralar haqida aniq so‘zlashing.",
            "Kelishmovchilikdan keyin yarashish marosimini yarating: qisqa quchoqlash, choy, yoki sokin sayr.",
        ],
        seven_day_plan=[
            "1-kun: Har biringiz munosabatda qadrlaydigan 3 narsani ayting.",
            "2-kun: Telefonsiz 20 daqiqa suhbat qiling va faqat tinglashga harakat qiling.",
            "3-kun: Bir-biringizga kichik, lekin aniq yordam bering.",
            "4-kun: Oxirgi ranjishlardan birini ayblamasdan muhokama qiling.",
            "5-kun: Birga yoqimli xotira yoki reja haqida gaplashing.",
            "6-kun: “Menga sendan kerak bo‘ladigani...” jumlasini davom ettiring.",
            "7-kun: Haftadagi eng yaxshi o‘zgarishni ayting va keyingi odatni tanlang.",
        ],
        conclusion=(
            "Sizlarning natijangiz munosabatda imkoniyat borligini ko‘rsatadi. Eng katta o‘sish "
            "bir-biringizni tuzatishga urinishdan emas, hislarni xavfsiz va aniq ifodalashdan boshlanadi."
        ),
    )


def _get_mbti_report(db: Session, token: str) -> PremiumReport | None:
    session = db.execute(
        select(models.MbtiSession).where(models.MbtiSession.token == token),
    ).scalar_one_or_none()
    if session is None or not session.result_type:
        return None

    result_type = session.result_type
    profile = get_mbti_profile(result_type)
    content = generate_mbti_result(result_type)
    title = str(content.get("title") or profile.get("title") or "Shaxsiyat profili")
    strengths = [str(item) for item in content.get("strengths", [])][:4]
    career = [str(item) for item in content.get("career", [])]
    weaknesses = [str(item) for item in content.get("weaknesses", [])][:4]

    return PremiumReport(
        test_type="mbti",
        test_name="MBTI shaxsiyat testi",
        session_token=token,
        result_url=result_url_for("mbti", token),
        user_name="Foydalanuvchi",
        date_text=_date_text(session.finished_at or session.created_at),
        summary=(
            f"Sizning MBTI natijangiz {result_type} - {title}. Bu profil qaror qabul qilish, "
            "muloqot va ish uslubingizdagi tabiiy yo‘nalishlarni ko‘rsatadi."
        ),
        score_label=f"{result_type} - {title}",
        strong_sides=strengths
        or [
            "Vaziyatni o‘z uslubingizda tahlil qilish va muhim narsani tez ajratish.",
            "Ichki mezonlarga tayanib qaror qabul qilish.",
        ],
        weak_sides=weaknesses
        or [
            "Kuchli tomon haddan tashqari ishlatilsa charchoq paydo bo‘lishi mumkin.",
            "Fikr va ehtiyojlarni boshqalarga aniqroq tushuntirish foydali.",
        ],
        main_risk=(
            "Asosiy o‘sish nuqtasi - kuchli tomoningizni haddan tashqari ishlatib yubormaslik. "
            "Sizga mos ritm, chegaralar va aniq ustuvorliklar bo‘lsa, natijangiz ancha barqaror bo‘ladi."
        ),
        recommendations=[
            "Kuchli tomoningizni har kuni bitta aniq ishda ongli ishlating.",
            "Muloqotda taxmin qildirish o‘rniga niyat va kutishingizni ochiq ayting.",
            "Mos kasb yo‘nalishlarini tanlashda qiziqish, energiya va muhit omillarini birga baholang.",
            career[1] if len(career) > 1 else "Ish muhitida mustaqillik va aniq mas’uliyat balansini qidiring.",
        ],
        seven_day_plan=[
            "1-kun: Natijangizdagi 3 kuchli tomonni yozing va misol bilan tasdiqlang.",
            "2-kun: Sizni charchatadigan 3 vaziyatni belgilang.",
            "3-kun: Bir suhbatda fikringizni qisqa, aniq va muloyim aytishni mashq qiling.",
            "4-kun: Mos kasb yoki loyiha ro‘yxatini tuzing.",
            "5-kun: Bitta zaif joyni yaxshilash uchun kichik odat tanlang.",
            "6-kun: Ish yoki o‘qish kuningizni energiyangizga qarab rejalang.",
            "7-kun: Haftalik kuzatuvdan bitta xulosa va keyingi qadamni yozing.",
        ],
        conclusion=(
            "MBTI natijasi sizni qolipga solish uchun emas, balki o‘zingizga mos muhit va odatlarni "
            "tanlash uchun kerak. O‘z uslubingizni tushunsangiz, qarorlar ham, muloqot ham yengillashadi."
        ),
    )


def _get_stress_report(db: Session, token: str) -> PremiumReport | None:
    session = db.execute(
        select(models.StressSession)
        .where(models.StressSession.token == token)
        .options(selectinload(models.StressSession.result)),
    ).scalar_one_or_none()
    if session is None or session.result is None:
        return None

    result = session.result
    scores = result.dimension_scores_dict
    source = _label(result.strongest_dimension, STRESS_DIMENSION_LABELS)
    level_title = STRESS_LEVEL_TITLES.get(result.level, result.level)

    signs = {
        "low": [
            "Vaqti-vaqti bilan charchoq bo‘lishi mumkin, lekin tiklanish imkoniyati yaxshi.",
            "Stress belgilari ko‘proq qisqa muddatli va boshqariladigan ko‘rinadi.",
        ],
        "medium": [
            "Uyqu, diqqat yoki kayfiyatda tebranishlar sezila boshlashi mumkin.",
            "Mayda vazifalar ham og‘ir tuyulsa, bu organizm tanaffus so‘rayotganidan darak.",
        ],
        "high": [
            "Tanada zo‘riqish, tez charchash, jahldorlik yoki ichki bezovtalik kuchayishi mumkin.",
            "Tiklanish vaqtini kechiktirish stressni yanada chuqurlashtirishi ehtimoli bor.",
        ],
    }

    return PremiumReport(
        test_type="stress",
        test_name="Stress darajasi testi",
        session_token=token,
        result_url=result_url_for("stress", token),
        user_name="Foydalanuvchi",
        date_text=_date_text(result.created_at),
        summary=(
            f"Natijangiz: {level_title}. Umumiy ball {result.total_score}/30. "
            f"Eng ko‘p bosim {source.lower()} yo‘nalishida yig‘ilgan."
        ),
        score_label=f"{result.total_score}/30 - {level_title}",
        strong_sides=[
            "Stress manbasini aniqlashning o‘zi tiklanish uchun muhim birinchi qadam.",
            "Sizga kichik, muntazam odatlar katta o‘zgarish berishi mumkin.",
            "Yuklamani qismlarga ajratish orqali bosimni boshqarish imkoniyatingiz bor.",
        ],
        weak_sides=signs.get(result.level, signs["medium"]),
        main_risk=(
            f"Asosiy manba - {source.lower()}. Bu soha nazoratsiz qolsa, stress boshqa yo‘nalishlarga "
            "ham tarqalib, uyqu, energiya va munosabatlarga ta’sir qilishi mumkin."
        ),
        recommendations=[
            "Bugungi vazifalarni eng muhim 3 ta ishgacha qisqartiring.",
            "Kechqurun ekran, ish yoki o‘qish mavzusidan kamida 30 daqiqa uzoqlashing.",
            "Kuniga 10 daqiqa sekin nafas, yurish yoki sokin tanaffus kiriting.",
            "Bosim berayotgan mavzuni ishonchli odam bilan aniq gaplashib oling.",
        ],
        seven_day_plan=[
            "1-kun: Stress manbalarini yozing va eng kuchlisini belgilang.",
            "2-kun: 10 daqiqa sokin yurish yoki nafas mashqini bajaring.",
            "3-kun: Rejangizdan bitta ortiqcha vazifani olib tashlang.",
            "4-kun: Uyqudan oldin 30 daqiqa ekran tanaffusi qiling.",
            "5-kun: Tanangizdagi zo‘riqish joylarini sezib, qisqa cho‘zilish qiling.",
            "6-kun: Ishonchli odamga hozir sizga nima og‘irligini ayting.",
            "7-kun: Qaysi odat yengillik berganini tanlab, keyingi haftaga qoldiring.",
        ],
        conclusion=(
            "Stress natijasi sizni qo‘rqitish uchun emas, organizm signalini vaqtida eshitish uchun. "
            "Kichik, izchil tiklanish odatlari bosimni kamaytiradi va energiyani qaytaradi."
        ),
    )


def build_premium_report(db: Session, test_type: str, token: str) -> PremiumReport | None:
    if test_type == "love":
        return _get_love_report(db=db, token=token)
    if test_type == "mbti":
        return _get_mbti_report(db=db, token=token)
    if test_type == "stress":
        return _get_stress_report(db=db, token=token)
    return None


def get_session_for_pdf(db: Session, test_type: str, token: str):
    if test_type == "love":
        return crud.get_session_by_token(db=db, token=token)
    if test_type == "mbti":
        return db.execute(
            select(models.MbtiSession).where(models.MbtiSession.token == token),
        ).scalar_one_or_none()
    if test_type == "stress":
        return db.execute(
            select(models.StressSession).where(models.StressSession.token == token),
        ).scalar_one_or_none()
    return None


def _font_name() -> str:
    font_candidates = [
        Path("C:/Windows/Fonts/arial.ttf"),
        Path("C:/Windows/Fonts/calibri.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        Path("/Library/Fonts/Arial Unicode.ttf"),
    ]
    for path in font_candidates:
        if path.exists():
            font_name = "QadamUnicode"
            if font_name not in pdfmetrics.getRegisteredFontNames():
                pdfmetrics.registerFont(TTFont(font_name, str(path)))
            return font_name
    return "Helvetica"


def _paragraph(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(escape(text).replace("\n", "<br/>"), style)


def _bullet_list(items: list[str], style: ParagraphStyle) -> ListFlowable:
    return ListFlowable(
        [ListItem(_paragraph(item, style), leftIndent=4) for item in items],
        bulletType="bullet",
        start="circle",
        leftIndent=14,
        bulletFontName=style.fontName,
    )


def generate_pdf_bytes(report: PremiumReport) -> bytes:
    buffer = BytesIO()
    font = _font_name()
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "QadamTitle",
        parent=styles["Title"],
        fontName=font,
        fontSize=22,
        leading=28,
        textColor=colors.HexColor("#4f46e5"),
        alignment=TA_CENTER,
        spaceAfter=8,
    )
    subtitle_style = ParagraphStyle(
        "QadamSubtitle",
        parent=styles["Normal"],
        fontName=font,
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#475569"),
        alignment=TA_CENTER,
        spaceAfter=12,
    )
    heading_style = ParagraphStyle(
        "QadamHeading",
        parent=styles["Heading2"],
        fontName=font,
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#111827"),
        spaceBefore=10,
        spaceAfter=6,
    )
    body_style = ParagraphStyle(
        "QadamBody",
        parent=styles["BodyText"],
        fontName=font,
        fontSize=10.5,
        leading=16,
        textColor=colors.HexColor("#334155"),
        spaceAfter=6,
    )
    footer_style = ParagraphStyle(
        "QadamFooter",
        parent=styles["BodyText"],
        fontName=font,
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#64748b"),
        alignment=TA_CENTER,
    )

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=18 * mm,
        title=f"{report.test_name} - Qadam",
    )
    story = [
        _paragraph("Qadam Test Platform", title_style),
        _paragraph(
            f"{report.test_name} | {report.user_name} | {report.date_text}",
            subtitle_style,
        ),
        _paragraph("Qisqa xulosa", heading_style),
        _paragraph(report.summary, body_style),
        _paragraph("Score / result type", heading_style),
        _paragraph(report.score_label, body_style),
        _paragraph("Kuchli tomonlar", heading_style),
        _bullet_list(report.strong_sides, body_style),
        _paragraph("O‘sish kerak bo‘lgan joylar", heading_style),
        _bullet_list(report.weak_sides, body_style),
        _paragraph("Asosiy xavf yoki muammo nuqtasi", heading_style),
        _paragraph(report.main_risk, body_style),
        _paragraph("Amaliy tavsiyalar", heading_style),
        _bullet_list(report.recommendations, body_style),
        _paragraph("7 kunlik rivojlanish rejasi", heading_style),
        _bullet_list(report.seven_day_plan, body_style),
        _paragraph("Yakuniy xulosa", heading_style),
        _paragraph(report.conclusion, body_style),
        Spacer(1, 10),
        _paragraph(FOOTER_TEXT, footer_style),
    ]
    doc.build(story)
    return buffer.getvalue()
