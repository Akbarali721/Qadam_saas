from __future__ import annotations

from typing import Any, TypedDict

STRESS_MAX_SCORE = 30

PREMIUM_TEASER_ITEMS: tuple[str, ...] = (
    "5 yo‘nalish bo‘yicha chuqur tahlil",
    "Stressingiz qaysi sohada kuchliroq ekanligi",
    "Uyqu, ish/o‘qish, munosabat, energiya va ortiqcha o‘ylash bo‘yicha alohida tahlil",
    "7 kunlik tiklanish rejasi",
    "Shaxsiy tavsiyalar",
    "PDF shaklida hisobot",
)

PREMIUM_TEASER_COPY = (
    "Premium tahlilda stressingiz qaysi yo‘nalishda kuchliroq ekanini, "
    "sizga mos 7 kunlik tiklanish rejasini va shaxsiy tavsiyalarni ko‘rasiz."
)


class StressLevelProfile(TypedDict):
    title: str
    description: str
    summary_line: str
    hero_notes: list[str]


class StressAreaProfile(TypedDict):
    title: str
    explanation: str
    signs: list[str]
    advice: list[str]


STRESS_LEVEL_PROFILES: dict[str, StressLevelProfile] = {
    "low": {
        "title": "Past stress",
        "description": (
            "Stress darajangiz hozircha past ko‘rinmoqda. Bu yaxshi holat, lekin barqaror "
            "energiyani saqlash uchun uyqu, dam olish va ish yuklamasini nazorat qilish muhim."
        ),
        "summary_line": "Hozircha stress nisbatan past, barqarorlikni saqlash muhim.",
        "hero_notes": [
            "Hozirgi javoblaringiz stress nisbatan boshqarilayotganini ko‘rsatadi.",
            "Kichik charchoq signallarini erta payqash va dam olish odatini saqlash foydali.",
        ],
    },
    "medium": {
        "title": "O‘rtacha stress",
        "description": (
            "Javoblaringiz stress bir nechta sohada sezila boshlaganini ko‘rsatadi. "
            "Bu bosqichda yuklamani tartiblash va tiklanish vaqtini oldindan rejalash muhim."
        ),
        "summary_line": "Stress bir nechta sohada sezila boshlagan, yuklamani tartiblash kerak.",
        "hero_notes": [
            "Bu bosqichda kichik odatlar va aniq chegaralar katta farq qiladi.",
            "Tiklanish vaqtini rejalashtirmasangiz, charchoq tez kuchayishi mumkin.",
        ],
    },
    "high": {
        "title": "Yuqori stress",
        "description": (
            "Javoblaringiz stress sizga sezilarli ta’sir qilayotganini ko‘rsatadi. Bunday holatda "
            "o‘zingizga bosimni kamaytirish, dam olishni rejalash va zarur bo‘lsa yaqin inson "
            "yoki mutaxassis bilan maslahatlashish foydali bo‘lishi mumkin."
        ),
        "summary_line": "Stress sezilarli ta’sir qilmoqda, yuklamani kamaytirish va dam olish muhim.",
        "hero_notes": [
            "O‘zingizni ayblamasdan, birinchi navbatda tanaffus va yordam so‘rashni ko‘rib chiqing.",
            "Agar bu holat davom etsa, yaqin inson yoki mutaxassis bilan gaplashish foydali bo‘lishi mumkin.",
        ],
    },
}

STRESS_AREA_PROFILES: dict[str, StressAreaProfile] = {
    "sleep_energy": {
        "title": "Uyqu va energiya",
        "explanation": (
            "Stress sizda ko‘proq uyqu sifati va kunlik energiya orqali sezilmoqda. "
            "Yetarlicha dam olgandek bo‘lsangiz ham, tanada charchoq, ertalab og‘ir uyg‘onish "
            "yoki kun davomida diqqat pasayishi kuzatilishi mumkin."
        ),
        "signs": [
            "Ertalab charchoq bilan uyg‘onish",
            "Kun davomida energiya tez tugashi",
            "Diqqatni jamlash qiyinlashishi",
        ],
        "advice": [
            "Uyqudan 30 daqiqa oldin telefonni chetga qo‘ying",
            "Kun davomida kamida 10 daqiqa sokin tanaffus qiling",
            "Kechqurun og‘ir fikrlarni qog‘ozga yozib qo‘ying",
        ],
    },
    "overthinking": {
        "title": "Ortiqcha o‘ylash",
        "explanation": (
            "Stress sizda ko‘proq fikrlar ko‘payishi, doimiy analiz va “nima bo‘lsa?” "
            "degan xavotirlar orqali namoyon bo‘lishi mumkin."
        ),
        "signs": [
            "Bir masalani qayta-qayta o‘ylash",
            "Qaror qabul qilishda qiynalish",
            "Dam olayotganda ham miyani to‘xtata olmaslik",
        ],
        "advice": [
            "Fikrlarni ichingizda aylantirmay, yozib chiqing",
            "Kunning eng muhim 1 ta ishini belgilang",
            "O‘zingiz nazorat qila oladigan narsalarga e’tibor bering",
        ],
    },
    "work_pressure": {
        "title": "Ish/o‘qish bosimi",
        "explanation": (
            "Stress sizda ko‘proq ish, o‘qish, mas’uliyat yoki vazifalar ko‘payishi "
            "orqali sezilmoqda."
        ),
        "signs": [
            "Vazifalar ko‘payib ketgandek tuyulishi",
            "Ishni boshlash qiyinlashishi",
            "Dam olganda ham ish haqida o‘ylash",
        ],
        "advice": [
            "Vazifalarni 3 ta kichik qadamga bo‘ling",
            "Eng og‘ir ishni kun boshida bajaring",
            "Har 60–90 daqiqada qisqa tanaffus qiling",
        ],
    },
    "relationship_pressure": {
        "title": "Munosabatlar",
        "explanation": (
            "Stress sizda odamlar bilan muloqot, tushunmovchilik yoki ichki gaplarni "
            "aytolmaslik orqali kuchayishi mumkin."
        ),
        "signs": [
            "Gaplashishdan qochish",
            "Mayda gaplarni ichga yutish",
            "Yaqin insonlar bilan tez ranjishish",
        ],
        "advice": [
            "Muhim gapni tinch vaqtda ayting",
            "Ayblashdan ko‘ra his-tuyg‘uni tushuntiring",
            "O‘zingizga ham, boshqalarga ham dam berishni o‘rganing",
        ],
    },
    "emotional_pressure": {
        "title": "Tana va charchoq",
        "explanation": (
            "Stress sizda ko‘proq tana charchog‘i, mushaklarda taranglik yoki umumiy "
            "holsizlik orqali sezilishi mumkin."
        ),
        "signs": [
            "Tana og‘irligi yoki holsizlik",
            "Tez charchash",
            "Dam olgandan keyin ham tiklanmaslik",
        ],
        "advice": [
            "Har kuni 10–15 daqiqa yengil yurish qiling",
            "Suv ichishni va ovqatlanish vaqtini tartiblang",
            "Kunning oxirida tanani bo‘shashtirish mashqlarini qiling",
        ],
    },
}

STRESS_FALLBACK_PROFILE: StressAreaProfile = {
    "title": "Aralash stress signallari",
    "explanation": "Stress bir nechta yo‘nalishda aralash ko‘rinmoqda.",
    "signs": [
        "Charchoq, diqqat pasayishi yoki kayfiyat tebranishlari",
        "Uyqu, ish yoki munosabatlarda bir vaqtda bosim",
        "Dam olganda ham ichki xotirjamlik kamayishi",
    ],
    "advice": [
        "Kun davomida 10 daqiqalik sokin tanaffusni odatga aylantiring",
        "Eng muhim 3 ta vazifani belgilab, qolganini keyinga qoldiring",
        "Bosim ko‘payganda yaqin inson bilan qisqa, ochiq suhbat qiling",
    ],
}

DIMENSION_LABELS: dict[str, str] = {
    "emotional_pressure": "Tana va charchoq",
    "sleep_energy": "Uyqu va energiya",
    "work_pressure": "Ish/o‘qish bosimi",
    "relationship_pressure": "Munosabatlar",
    "overthinking": "Ortiqcha o‘ylash",
}


def resolve_strongest_dimension(dimension_scores: dict[str, int]) -> str | None:
    if not dimension_scores:
        return None
    max_value = max(dimension_scores.values())
    if max_value <= 0:
        return None
    leaders = [key for key, value in dimension_scores.items() if value == max_value]
    if len(leaders) != 1:
        return None
    return leaders[0]


def get_level_profile(level: str) -> StressLevelProfile:
    return STRESS_LEVEL_PROFILES.get(level, STRESS_LEVEL_PROFILES["medium"])


def get_area_profile(dimension: str | None) -> tuple[StressAreaProfile, bool]:
    if dimension and dimension in STRESS_AREA_PROFILES:
        return STRESS_AREA_PROFILES[dimension], True
    return STRESS_FALLBACK_PROFILE, False


def build_stress_result_view(result) -> dict[str, Any]:
    level_profile = get_level_profile(result.level)
    dimension_scores = result.dimension_scores_dict
    strongest_dimension = resolve_strongest_dimension(dimension_scores)
    if strongest_dimension is None and result.strongest_dimension in STRESS_AREA_PROFILES:
        scores = dimension_scores or {}
        stored_score = scores.get(result.strongest_dimension)
        if stored_score and stored_score > 0:
            leaders = [key for key, value in scores.items() if value == stored_score]
            if len(leaders) == 1:
                strongest_dimension = result.strongest_dimension

    area_profile, area_found = get_area_profile(strongest_dimension)
    total_score = int(result.total_score)
    max_score = STRESS_MAX_SCORE

    if area_found:
        overview_summary = (
            f"{total_score}/{max_score} ball. Eng kuchli signal «{area_profile['title']}» "
            f"yo‘nalishida. {level_profile['summary_line']}"
        )
    else:
        overview_summary = (
            f"{total_score}/{max_score} ball. {STRESS_FALLBACK_PROFILE['explanation']} "
            f"{level_profile['summary_line']}"
        )

    return {
        "level_profile": level_profile,
        "area_profile": area_profile,
        "area_found": area_found,
        "strongest_dimension": strongest_dimension or result.strongest_dimension,
        "strongest_area_title": area_profile["title"],
        "max_score": max_score,
        "overview_summary": overview_summary,
        "hero_paragraphs": [level_profile["description"], *level_profile["hero_notes"]],
    }
