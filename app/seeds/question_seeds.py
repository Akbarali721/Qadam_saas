from __future__ import annotations

from typing import TypedDict


class OptionSeed(TypedDict):
    text: str
    weight: int


class QuestionSeed(TypedDict):
    dimension: str
    gender_target: str
    text: str
    options: list[OptionSeed]


RELATIONSHIP_ORDER_BASE: dict[str, int] = {
    "married": 1,
    "friends": 101,
    "dating": 201,
}

SESSION_QUESTION_COUNT = 12

QUESTIONS_MARRIED: list[QuestionSeed] = [
    {
        "dimension": "communication",
        "gender_target": "both",
        "text": "Muhim oilaviy qarorlarni (moliya, uy, tarbiya) qanday qabul qilasiz?",
        "options": [
            {"text": "Reja yoki kelishuv deyarli yo‘q", "weight": 1},
            {"text": "Ba‘zan muhokama qilamiz", "weight": 2},
            {"text": "Ko‘pincha kelishib olamiz", "weight": 3},
            {"text": "Aniq va uyg‘un reja bor", "weight": 4},
        ],
    },
    {
        "dimension": "communication",
        "gender_target": "both",
        "text": "Uy ishlari yoki oila rejasida kelishmovchilik bo‘lsa, uni qanday hal qilasiz?",
        "options": [
            {"text": "Ochilmaymiz yoki yopilib qolamiz", "weight": 1},
            {"text": "Faqat majbur bo‘lsa gaplashamiz", "weight": 2},
            {"text": "Ko‘pincha ochiq gaplashamiz", "weight": 3},
            {"text": "To‘liq ochiq va xavfsiz muloqot qilamiz", "weight": 4},
        ],
    },
    {
        "dimension": "communication",
        "gender_target": "both",
        "text": "Kundalik hayotdagi muhim yangiliklarni bir-biringizga qanchalik vaqtida yetkazasiz?",
        "options": [
            {"text": "Deyarli hech qachon yoki juda kam", "weight": 1},
            {"text": "Ba‘zan, lekin tartibsiz", "weight": 2},
            {"text": "Ko‘pincha va barqaror", "weight": 3},
            {"text": "Doimiy va tabiiy tarzda", "weight": 4},
        ],
    },
    {
        "dimension": "communication",
        "gender_target": "both",
        "text": "Oilaviy tortishuvdan keyin tinch va tushunarli gaplashish qanday kechadi?",
        "options": [
            {"text": "Ochilmaymiz yoki yopilib qolamiz", "weight": 1},
            {"text": "Faqat majbur bo‘lsa gaplashamiz", "weight": 2},
            {"text": "Ko‘pincha ochiq gaplashamiz", "weight": 3},
            {"text": "To‘liq ochiq va xavfsiz muloqot qilamiz", "weight": 4},
        ],
    },
    {
        "dimension": "trust",
        "gender_target": "both",
        "text": "Moliyaviy masalalarda (byudjet, xarajat, qarz) ochiqlik darajangiz qanday?",
        "options": [
            {"text": "Ko‘p narsa yashirin qoladi", "weight": 1},
            {"text": "Faqat muammo chiqqanda gaplashamiz", "weight": 2},
            {"text": "Asosan ochiq ma’lumot berib boramiz", "weight": 3},
            {"text": "Ochiqlik va oldindan kelishuv odatga aylangan", "weight": 4},
        ],
    },
    {
        "dimension": "trust",
        "gender_target": "both",
        "text": "Oilaviy va‘da va majburiyatlarga amal qilish qanday?",
        "options": [
            {"text": "Va’dalar tez-tez bajarilmay qoladi", "weight": 1},
            {"text": "Ba’zi va’dalar bajariladi, ba’zilari unutiladi", "weight": 2},
            {"text": "Aksar va’dalar bajariladi", "weight": 3},
            {"text": "So‘z va amal odatda bir xil bo‘ladi", "weight": 4},
        ],
    },
    {
        "dimension": "trust",
        "gender_target": "both",
        "text": "Qarindoshlar yoki yaqin do‘stlar oldida bir-biringizga ishonish qanday?",
        "options": [
            {"text": "Ishonch juda past yoki yo‘q", "weight": 1},
            {"text": "Ba‘zan ishonamiz, ba‘zan shubha bor", "weight": 2},
            {"text": "Ko‘pincha ishonchli his qilamiz", "weight": 3},
            {"text": "To‘liq va barqaror ishonch bor", "weight": 4},
        ],
    },
    {
        "dimension": "trust",
        "gender_target": "both",
        "text": "Uzoq yillik oilaviy hayotda bir-biringizga ishonch darajasi qanday?",
        "options": [
            {"text": "Ishonch juda past yoki yo‘q", "weight": 1},
            {"text": "Ba‘zan ishonamiz, ba‘zan shubha bor", "weight": 2},
            {"text": "Ko‘pincha ishonchli his qilamiz", "weight": 3},
            {"text": "To‘liq va barqaror ishonch bor", "weight": 4},
        ],
    },
    {
        "dimension": "emotional_closeness",
        "gender_target": "both",
        "text": "Charchagan yoki qiyin kunda bir-biringizni hissiy qo‘llab-quvvatlash qanday?",
        "options": [
            {"text": "Qo‘llab-quvvatlash deyarli yo‘q", "weight": 1},
            {"text": "Ba‘zan yordam bor, ba‘zan yo‘q", "weight": 2},
            {"text": "Ko‘pincha bir-birimizni qo‘llab-quvvatlaymiz", "weight": 3},
            {"text": "Qiyin paytda ham ishonchli tayanchmiz", "weight": 4},
        ],
    },
    {
        "dimension": "emotional_closeness",
        "gender_target": "both",
        "text": "Oilaviy stress paytida bir-biringiz yonida turishni qanday his qilasiz?",
        "options": [
            {"text": "Qo‘llab-quvvatlash deyarli yo‘q", "weight": 1},
            {"text": "Ba‘zan yordam bor, ba‘zan yo‘q", "weight": 2},
            {"text": "Ko‘pincha bir-birimizni qo‘llab-quvvatlaymiz", "weight": 3},
            {"text": "Qiyin paytda ham ishonchli tayanchmiz", "weight": 4},
        ],
    },
    {
        "dimension": "emotional_closeness",
        "gender_target": "both",
        "text": "Ichki kechinmalarni oila ichida ochish xavfsizligi qanday?",
        "options": [
            {"text": "Ochilish xavfsiz emas deb his qilaman", "weight": 1},
            {"text": "Ba‘zan xavfsiz, ba‘zan ehtiyotkorlik kerak", "weight": 2},
            {"text": "Ko‘pincha xavfsiz ochilaman", "weight": 3},
            {"text": "To‘liq xavfsiz va qabul qilingan his qilaman", "weight": 4},
        ],
    },
    {
        "dimension": "emotional_closeness",
        "gender_target": "both",
        "text": "Xafa bo‘lganda oilaviy muhitda bir-biringizga yaqinlashish qanday kechadi?",
        "options": [
            {"text": "Ochilmaymiz yoki yopilib qolamiz", "weight": 1},
            {"text": "Faqat majbur bo‘lsa gaplashamiz", "weight": 2},
            {"text": "Ko‘pincha ochiq gaplashamiz", "weight": 3},
            {"text": "To‘liq ochiq va xavfsiz muloqot qilamiz", "weight": 4},
        ],
    },
    {
        "dimension": "attention",
        "gender_target": "both",
        "text": "Uy ishi va oila ehtiyojlariga birgalikdagi vaqt qanchalik ajratiladi?",
        "options": [
            {"text": "Deyarli hech qachon yoki juda kam", "weight": 1},
            {"text": "Ba‘zan, lekin tartibsiz", "weight": 2},
            {"text": "Ko‘pincha va barqaror", "weight": 3},
            {"text": "Doimiy va tabiiy tarzda", "weight": 4},
        ],
    },
    {
        "dimension": "attention",
        "gender_target": "both",
        "text": "Bir-biringizning charchoq yoki kayfiyat o‘zgarishini sezish qanday?",
        "options": [
            {"text": "Juda yomon yoki deyarli yo‘q", "weight": 1},
            {"text": "O‘rtacha, ko‘p muammo bor", "weight": 2},
            {"text": "Yaxshi, lekin yaxshilash kerak", "weight": 3},
            {"text": "Juda yaxshi va barqaror", "weight": 4},
        ],
    },
    {
        "dimension": "attention",
        "gender_target": "both",
        "text": "Birgalikdagi dam olish va sifatli oilaviy vaqt qanday rejalashtiriladi?",
        "options": [
            {"text": "Reja yoki kelishuv deyarli yo‘q", "weight": 1},
            {"text": "Ba‘zan muhokama qilamiz", "weight": 2},
            {"text": "Ko‘pincha kelishib olamiz", "weight": 3},
            {"text": "Aniq va uyg‘un reja bor", "weight": 4},
        ],
    },
    {
        "dimension": "attention",
        "gender_target": "both",
        "text": "Kundalik mayda g‘amxo‘rlik va e‘tibor ko‘rsatish odati qanday?",
        "options": [
            {"text": "Deyarli hech qachon yoki juda kam", "weight": 1},
            {"text": "Ba‘zan, lekin tartibsiz", "weight": 2},
            {"text": "Ko‘pincha va barqaror", "weight": 3},
            {"text": "Doimiy va tabiiy tarzda", "weight": 4},
        ],
    },
    {
        "dimension": "future_vision",
        "gender_target": "both",
        "text": "Oilaviy kelajak (bolalar, uy, hayot tartibi) bo‘yicha umumiy tasavvuringiz bormi?",
        "options": [
            {"text": "Reja yoki kelishuv deyarli yo‘q", "weight": 1},
            {"text": "Ba‘zan muhokama qilamiz", "weight": 2},
            {"text": "Ko‘pincha kelishib olamiz", "weight": 3},
            {"text": "Aniq va uyg‘un reja bor", "weight": 4},
        ],
    },
    {
        "dimension": "future_vision",
        "gender_target": "both",
        "text": "Uzoq muddatli oilaviy maqsadlar haqida muntazam gaplashasizmi?",
        "options": [
            {"text": "Deyarli hech qachon yoki juda kam", "weight": 1},
            {"text": "Ba‘zan, lekin tartibsiz", "weight": 2},
            {"text": "Ko‘pincha va barqaror", "weight": 3},
            {"text": "Doimiy va tabiiy tarzda", "weight": 4},
        ],
    },
    {
        "dimension": "future_vision",
        "gender_target": "both",
        "text": "5–10 yillik oilaviy rejalaringiz qanchalik uyg‘un?",
        "options": [
            {"text": "Reja yoki kelishuv deyarli yo‘q", "weight": 1},
            {"text": "Ba‘zan muhokama qilamiz", "weight": 2},
            {"text": "Ko‘pincha kelishib olamiz", "weight": 3},
            {"text": "Aniq va uyg‘un reja bor", "weight": 4},
        ],
    },
    {
        "dimension": "future_vision",
        "gender_target": "both",
        "text": "Katta hayotiy o‘zgarishlarga (ko‘chish, ish, oila kengayishi) birgalikda tayyorgarlik qanday?",
        "options": [
            {"text": "Reja yoki kelishuv deyarli yo‘q", "weight": 1},
            {"text": "Ba‘zan muhokama qilamiz", "weight": 2},
            {"text": "Ko‘pincha kelishib olamiz", "weight": 3},
            {"text": "Aniq va uyg‘un reja bor", "weight": 4},
        ],
    },
    {
        "dimension": "boundaries",
        "gender_target": "both",
        "text": "Qarindoshlar va yaqin do‘stlar bilan munosabat chegaralari qanday belgilanadi?",
        "options": [
            {"text": "Hurmat deyarli sezilmaydi", "weight": 1},
            {"text": "Ba‘zan hurmat bor, ba‘zan buziladi", "weight": 2},
            {"text": "Ko‘pincha hurmat saqlanadi", "weight": 3},
            {"text": "Doimiy va chuqur hurmat bor", "weight": 4},
        ],
    },
    {
        "dimension": "boundaries",
        "gender_target": "both",
        "text": "Shaxsiy vaqt, makon va telefon bo‘yicha oila ichida hurmat qanday?",
        "options": [
            {"text": "Hurmat deyarli sezilmaydi", "weight": 1},
            {"text": "Ba‘zan hurmat bor, ba‘zan buziladi", "weight": 2},
            {"text": "Ko‘pincha hurmat saqlanadi", "weight": 3},
            {"text": "Doimiy va chuqur hurmat bor", "weight": 4},
        ],
    },
    {
        "dimension": "boundaries",
        "gender_target": "both",
        "text": "Oiladan tashqari shaxsiy aloqalar va uchrashuvlar bo‘yicha kelishuvlar bormi?",
        "options": [
            {"text": "Reja yoki kelishuv deyarli yo‘q", "weight": 1},
            {"text": "Ba‘zan muhokama qilamiz", "weight": 2},
            {"text": "Ko‘pincha kelishib olamiz", "weight": 3},
            {"text": "Aniq va uyg‘un reja bor", "weight": 4},
        ],
    },
    {
        "dimension": "boundaries",
        "gender_target": "both",
        "text": "Bir-biringizning shaxsiy ehtiyoj va chegaralariga joy berish qanday?",
        "options": [
            {"text": "Hurmat deyarli sezilmaydi", "weight": 1},
            {"text": "Ba‘zan hurmat bor, ba‘zan buziladi", "weight": 2},
            {"text": "Ko‘pincha hurmat saqlanadi", "weight": 3},
            {"text": "Doimiy va chuqur hurmat bor", "weight": 4},
        ],
    },
    {
        "dimension": "responsibility",
        "gender_target": "both",
        "text": "Uy xarajatlari va byudjet mas‘uliyati qanday taqsimlanadi?",
        "options": [
            {"text": "Adolatsiz yoki noteng taqsimlanadi", "weight": 1},
            {"text": "Ba‘zan adolatli, ba‘zan emas", "weight": 2},
            {"text": "Ko‘pincha adolatli kelishamiz", "weight": 3},
            {"text": "Aniq va adolatli taqsimlangan", "weight": 4},
        ],
    },
    {
        "dimension": "responsibility",
        "gender_target": "both",
        "text": "Bolalar tarbiyasi yoki oila vazifalarida ishtirok darajangiz qanday?",
        "options": [
            {"text": "Adolatsiz yoki noteng taqsimlanadi", "weight": 1},
            {"text": "Ba‘zan adolatli, ba‘zan emas", "weight": 2},
            {"text": "Ko‘pincha adolatli kelishamiz", "weight": 3},
            {"text": "Aniq va adolatli taqsimlangan", "weight": 4},
        ],
    },
    {
        "dimension": "responsibility",
        "gender_target": "both",
        "text": "Muammochi vaziyatda mas‘uliyatni olish va xatoni tuzatish qanday?",
        "options": [
            {"text": "Juda yomon yoki deyarli yo‘q", "weight": 1},
            {"text": "O‘rtacha, ko‘p muammo bor", "weight": 2},
            {"text": "Yaxshi, lekin yaxshilash kerak", "weight": 3},
            {"text": "Juda yaxshi va barqaror", "weight": 4},
        ],
    },
    {
        "dimension": "responsibility",
        "gender_target": "both",
        "text": "Oilaviy majburiyatlarni (tadbir, uchrashuv, va‘da) bajarish qanday?",
        "options": [
            {"text": "Ishonch juda past yoki yo‘q", "weight": 1},
            {"text": "Ba‘zan ishonamiz, ba‘zan shubha bor", "weight": 2},
            {"text": "Ko‘pincha ishonchli his qilamiz", "weight": 3},
            {"text": "To‘liq va barqaror ishonch bor", "weight": 4},
        ],
    },
]

QUESTIONS_FRIENDS: list[QuestionSeed] = [
    {
        "dimension": "communication",
        "gender_target": "both",
        "text": "Do‘stlikdagi muhim mavzularda ochiq va to‘g‘ridan-to‘g‘ri gapirish qanday?",
        "options": [
            {"text": "Ochilmaymiz yoki yopilib qolamiz", "weight": 1},
            {"text": "Faqat majbur bo‘lsa gaplashamiz", "weight": 2},
            {"text": "Ko‘pincha ochiq gaplashamiz", "weight": 3},
            {"text": "To‘liq ochiq va xavfsiz muloqot qilamiz", "weight": 4},
        ],
    },
    {
        "dimension": "communication",
        "gender_target": "both",
        "text": "Noto‘g‘ri tushunish yoki xafa bo‘lish bo‘lsa, uni qanday aniqlashtirasiz?",
        "options": [
            {"text": "Ochilmaymiz yoki yopilib qolamiz", "weight": 1},
            {"text": "Faqat majbur bo‘lsa gaplashamiz", "weight": 2},
            {"text": "Ko‘pincha ochiq gaplashamiz", "weight": 3},
            {"text": "To‘liq ochiq va xavfsiz muloqot qilamiz", "weight": 4},
        ],
    },
    {
        "dimension": "communication",
        "gender_target": "both",
        "text": "Band kunlarda do‘stlik aloqasini (xabar, qo‘ng‘iroq) saqlash qanday?",
        "options": [
            {"text": "Deyarli hech qachon yoki juda kam", "weight": 1},
            {"text": "Ba‘zan, lekin tartibsiz", "weight": 2},
            {"text": "Ko‘pincha va barqaror", "weight": 3},
            {"text": "Doimiy va tabiiy tarzda", "weight": 4},
        ],
    },
    {
        "dimension": "communication",
        "gender_target": "both",
        "text": "Kelishmovchilik yoki ranjishdan keyin do‘stlik suhbati qanday kechadi?",
        "options": [
            {"text": "Ochilmaymiz yoki yopilib qolamiz", "weight": 1},
            {"text": "Faqat majbur bo‘lsa gaplashamiz", "weight": 2},
            {"text": "Ko‘pincha ochiq gaplashamiz", "weight": 3},
            {"text": "To‘liq ochiq va xavfsiz muloqot qilamiz", "weight": 4},
        ],
    },
    {
        "dimension": "trust",
        "gender_target": "both",
        "text": "Do‘stlikdagi sir va shaxsiy ma’lumotlarni saqlash qanday?",
        "options": [
            {"text": "Shaxsiy gaplar tashqariga chiqib ketadi", "weight": 1},
            {"text": "Ba’zan ehtiyotsizlik bo‘ladi", "weight": 2},
            {"text": "Odatda sir saqlanadi", "weight": 3},
            {"text": "Maxfiylik bo‘yicha to‘liq ishonch bor", "weight": 4},
        ],
    },
    {
        "dimension": "trust",
        "gender_target": "both",
        "text": "Do‘stlikda va‘da bergan ishlarni bajarish qanday?",
        "options": [
            {"text": "Ishonch juda past yoki yo‘q", "weight": 1},
            {"text": "Ba‘zan ishonamiz, ba‘zan shubha bor", "weight": 2},
            {"text": "Ko‘pincha ishonchli his qilamiz", "weight": 3},
            {"text": "To‘liq va barqaror ishonch bor", "weight": 4},
        ],
    },
    {
        "dimension": "trust",
        "gender_target": "both",
        "text": "Bir-biringizning xatolaringizni tan olish va kechirish qanday?",
        "options": [
            {"text": "Ishonch juda past yoki yo‘q", "weight": 1},
            {"text": "Ba‘zan ishonamiz, ba‘zan shubha bor", "weight": 2},
            {"text": "Ko‘pincha ishonchli his qilamiz", "weight": 3},
            {"text": "To‘liq va barqaror ishonch bor", "weight": 4},
        ],
    },
    {
        "dimension": "trust",
        "gender_target": "both",
        "text": "Do‘stlik munosabatida barqaror ishonch hissi qanday?",
        "options": [
            {"text": "Ishonch juda past yoki yo‘q", "weight": 1},
            {"text": "Ba‘zan ishonamiz, ba‘zan shubha bor", "weight": 2},
            {"text": "Ko‘pincha ishonchli his qilamiz", "weight": 3},
            {"text": "To‘liq va barqaror ishonch bor", "weight": 4},
        ],
    },
    {
        "dimension": "emotional_closeness",
        "gender_target": "both",
        "text": "Do‘st sifatida qiyin paytda yonida turish qanday?",
        "options": [
            {"text": "Qo‘llab-quvvatlash deyarli yo‘q", "weight": 1},
            {"text": "Ba‘zan yordam bor, ba‘zan yo‘q", "weight": 2},
            {"text": "Ko‘pincha bir-birimizni qo‘llab-quvvatlaymiz", "weight": 3},
            {"text": "Qiyin paytda ham ishonchli tayanchmiz", "weight": 4},
        ],
    },
    {
        "dimension": "emotional_closeness",
        "gender_target": "both",
        "text": "Ichki kechinmalarni do‘st bilan bo‘lishish xavfsizligi qanday?",
        "options": [
            {"text": "Ochilish xavfsiz emas deb his qilaman", "weight": 1},
            {"text": "Ba‘zan xavfsiz, ba‘zan ehtiyotkorlik kerak", "weight": 2},
            {"text": "Ko‘pincha xavfsiz ochilaman", "weight": 3},
            {"text": "To‘liq xavfsiz va qabul qilingan his qilaman", "weight": 4},
        ],
    },
    {
        "dimension": "emotional_closeness",
        "gender_target": "both",
        "text": "Xafa bo‘lganda do‘stlik munosabatida yaqinlashish qanday kechadi?",
        "options": [
            {"text": "Ochilmaymiz yoki yopilib qolamiz", "weight": 1},
            {"text": "Faqat majbur bo‘lsa gaplashamiz", "weight": 2},
            {"text": "Ko‘pincha ochiq gaplashamiz", "weight": 3},
            {"text": "To‘liq ochiq va xavfsiz muloqot qilamiz", "weight": 4},
        ],
    },
    {
        "dimension": "emotional_closeness",
        "gender_target": "both",
        "text": "Bir-biringizning hislarini rad etmasdan qabul qilish qanday?",
        "options": [
            {"text": "Hurmat deyarli sezilmaydi", "weight": 1},
            {"text": "Ba‘zan hurmat bor, ba‘zan buziladi", "weight": 2},
            {"text": "Ko‘pincha hurmat saqlanadi", "weight": 3},
            {"text": "Doimiy va chuqur hurmat bor", "weight": 4},
        ],
    },
    {
        "dimension": "attention",
        "gender_target": "both",
        "text": "Do‘stlik uchun vaqt ajratish qanchalik muntazam?",
        "options": [
            {"text": "Deyarli hech qachon yoki juda kam", "weight": 1},
            {"text": "Ba‘zan, lekin tartibsiz", "weight": 2},
            {"text": "Ko‘pincha va barqaror", "weight": 3},
            {"text": "Doimiy va tabiiy tarzda", "weight": 4},
        ],
    },
    {
        "dimension": "attention",
        "gender_target": "both",
        "text": "Do‘stingizning kayfiyatidagi o‘zgarishni sezish qanday?",
        "options": [
            {"text": "Juda yomon yoki deyarli yo‘q", "weight": 1},
            {"text": "O‘rtacha, ko‘p muammo bor", "weight": 2},
            {"text": "Yaxshi, lekin yaxshilash kerak", "weight": 3},
            {"text": "Juda yaxshi va barqaror", "weight": 4},
        ],
    },
    {
        "dimension": "attention",
        "gender_target": "both",
        "text": "Muloqot paytida telefon va chalg‘ituvchilardan uzoqlashish odati qanday?",
        "options": [
            {"text": "Juda yomon yoki deyarli yo‘q", "weight": 1},
            {"text": "O‘rtacha, ko‘p muammo bor", "weight": 2},
            {"text": "Yaxshi, lekin yaxshilash kerak", "weight": 3},
            {"text": "Juda yaxshi va barqaror", "weight": 4},
        ],
    },
    {
        "dimension": "attention",
        "gender_target": "both",
        "text": "Do‘stingiz uchun muhim voqea yoki sanani eslab qolish qanday?",
        "options": [
            {"text": "Deyarli hech qachon yoki juda kam", "weight": 1},
            {"text": "Ba‘zan, lekin tartibsiz", "weight": 2},
            {"text": "Ko‘pincha va barqaror", "weight": 3},
            {"text": "Doimiy va tabiiy tarzda", "weight": 4},
        ],
    },
    {
        "dimension": "future_vision",
        "gender_target": "both",
        "text": "Do‘stlik kelajakda qanday rivojlanishini muhokama qilasizmi?",
        "options": [
            {"text": "Niyatlar noaniq yoki umuman gapirilmaydi", "weight": 1},
            {"text": "Ba‘zi jihatlar aniq, ba‘zilari emas", "weight": 2},
            {"text": "Ko‘pincha niyatlar tushunarli", "weight": 3},
            {"text": "Niyatlar ochiq va bir-birimizga tushunarli", "weight": 4},
        ],
    },
    {
        "dimension": "future_vision",
        "gender_target": "both",
        "text": "Do‘stlik chuqurlashishi yoki soddaroq qolishi haqida fikringiz bormi?",
        "options": [
            {"text": "Niyatlar noaniq yoki umuman gapirilmaydi", "weight": 1},
            {"text": "Ba‘zi jihatlar aniq, ba‘zilari emas", "weight": 2},
            {"text": "Ko‘pincha niyatlar tushunarli", "weight": 3},
            {"text": "Niyatlar ochiq va bir-birimizga tushunarli", "weight": 4},
        ],
    },
    {
        "dimension": "future_vision",
        "gender_target": "both",
        "text": "Uzoq muddatli do‘stlikni saqlash bo‘yicha umumiy rejangiz qanday?",
        "options": [
            {"text": "Reja yoki kelishuv deyarli yo‘q", "weight": 1},
            {"text": "Ba‘zan muhokama qilamiz", "weight": 2},
            {"text": "Ko‘pincha kelishib olamiz", "weight": 3},
            {"text": "Aniq va uyg‘un reja bor", "weight": 4},
        ],
    },
    {
        "dimension": "future_vision",
        "gender_target": "both",
        "text": "Do‘stlik maqsadi (qanday yaqinlik, qanday aloqa) bo‘yicha kelishuv bormi?",
        "options": [
            {"text": "Niyatlar noaniq yoki umuman gapirilmaydi", "weight": 1},
            {"text": "Ba‘zi jihatlar aniq, ba‘zilari emas", "weight": 2},
            {"text": "Ko‘pincha niyatlar tushunarli", "weight": 3},
            {"text": "Niyatlar ochiq va bir-birimizga tushunarli", "weight": 4},
        ],
    },
    {
        "dimension": "boundaries",
        "gender_target": "both",
        "text": "Do‘stlik va boshqa munosabatlar (juftlik, oila) orasidagi chegaralar qanday?",
        "options": [
            {"text": "Hurmat deyarli sezilmaydi", "weight": 1},
            {"text": "Ba‘zan hurmat bor, ba‘zan buziladi", "weight": 2},
            {"text": "Ko‘pincha hurmat saqlanadi", "weight": 3},
            {"text": "Doimiy va chuqur hurmat bor", "weight": 4},
        ],
    },
    {
        "dimension": "boundaries",
        "gender_target": "both",
        "text": "Do‘stlikda shaxsiy vaqt va makon hurmati qanday?",
        "options": [
            {"text": "Hurmat deyarli sezilmaydi", "weight": 1},
            {"text": "Ba‘zan hurmat bor, ba‘zan buziladi", "weight": 2},
            {"text": "Ko‘pincha hurmat saqlanadi", "weight": 3},
            {"text": "Doimiy va chuqur hurmat bor", "weight": 4},
        ],
    },
    {
        "dimension": "boundaries",
        "gender_target": "both",
        "text": "Do‘stlikda noqulay yoki ortiqcha iltimos va bosim qanday hal qilinadi?",
        "options": [
            {"text": "Ochilmaymiz yoki yopilib qolamiz", "weight": 1},
            {"text": "Faqat majbur bo‘lsa gaplashamiz", "weight": 2},
            {"text": "Ko‘pincha ochiq gaplashamiz", "weight": 3},
            {"text": "To‘liq ochiq va xavfsiz muloqot qilamiz", "weight": 4},
        ],
    },
    {
        "dimension": "boundaries",
        "gender_target": "both",
        "text": "Do‘stingizning rad etishiga (yo‘q deyishiga) hurmat qanday?",
        "options": [
            {"text": "Hurmat deyarli sezilmaydi", "weight": 1},
            {"text": "Ba‘zan hurmat bor, ba‘zan buziladi", "weight": 2},
            {"text": "Ko‘pincha hurmat saqlanadi", "weight": 3},
            {"text": "Doimiy va chuqur hurmat bor", "weight": 4},
        ],
    },
    {
        "dimension": "responsibility",
        "gender_target": "both",
        "text": "Do‘stlikda o‘z mas‘uliyatingizni (qo‘llab-quvvatlash, vaqt) qanday olasiz?",
        "options": [
            {"text": "Juda yomon yoki deyarli yo‘q", "weight": 1},
            {"text": "O‘rtacha, ko‘p muammo bor", "weight": 2},
            {"text": "Yaxshi, lekin yaxshilash kerak", "weight": 3},
            {"text": "Juda yaxshi va barqaror", "weight": 4},
        ],
    },
    {
        "dimension": "responsibility",
        "gender_target": "both",
        "text": "Bir-birining ishonchini buzmaslik bo‘yicha mas‘uliyat qanday?",
        "options": [
            {"text": "Ishonch juda past yoki yo‘q", "weight": 1},
            {"text": "Ba‘zan ishonamiz, ba‘zan shubha bor", "weight": 2},
            {"text": "Ko‘pincha ishonchli his qilamiz", "weight": 3},
            {"text": "To‘liq va barqaror ishonch bor", "weight": 4},
        ],
    },
    {
        "dimension": "responsibility",
        "gender_target": "both",
        "text": "Rejalashtirilgan uchrashuvlarga kelish va vaqtga rioya qilish qanday?",
        "options": [
            {"text": "Ishonch juda past yoki yo‘q", "weight": 1},
            {"text": "Ba‘zan ishonamiz, ba‘zan shubha bor", "weight": 2},
            {"text": "Ko‘pincha ishonchli his qilamiz", "weight": 3},
            {"text": "To‘liq va barqaror ishonch bor", "weight": 4},
        ],
    },
    {
        "dimension": "responsibility",
        "gender_target": "both",
        "text": "Do‘stlikdagi xatoni tuzatish uchun qanchalik faol harakat qilasiz?",
        "options": [
            {"text": "Juda yomon yoki deyarli yo‘q", "weight": 1},
            {"text": "O‘rtacha, ko‘p muammo bor", "weight": 2},
            {"text": "Yaxshi, lekin yaxshilash kerak", "weight": 3},
            {"text": "Juda yaxshi va barqaror", "weight": 4},
        ],
    },
]

QUESTIONS_DATING: list[QuestionSeed] = [
    {
        "dimension": "communication",
        "gender_target": "both",
        "text": "Tanishuv bosqichida muloqot chastotasi va uslubi sizlarni qondiradimi?",
        "options": [
            {"text": "Deyarli hech qachon yoki juda kam", "weight": 1},
            {"text": "Ba‘zan, lekin tartibsiz", "weight": 2},
            {"text": "Ko‘pincha va barqaror", "weight": 3},
            {"text": "Doimiy va tabiiy tarzda", "weight": 4},
        ],
    },
    {
        "dimension": "communication",
        "gender_target": "both",
        "text": "Dastlabki bosqichda hislaringizni ochiq aytish qanday?",
        "options": [
            {"text": "Ochilmaymiz yoki yopilib qolamiz", "weight": 1},
            {"text": "Faqat majbur bo‘lsa gaplashamiz", "weight": 2},
            {"text": "Ko‘pincha ochiq gaplashamiz", "weight": 3},
            {"text": "To‘liq ochiq va xavfsiz muloqot qilamiz", "weight": 4},
        ],
    },
    {
        "dimension": "communication",
        "gender_target": "both",
        "text": "Noto‘g‘ri tushunish bo‘lsa, tezda aniqlashtirasizmi?",
        "options": [
            {"text": "Ochilmaymiz yoki yopilib qolamiz", "weight": 1},
            {"text": "Faqat majbur bo‘lsa gaplashamiz", "weight": 2},
            {"text": "Ko‘pincha ochiq gaplashamiz", "weight": 3},
            {"text": "To‘liq ochiq va xavfsiz muloqot qilamiz", "weight": 4},
        ],
    },
    {
        "dimension": "communication",
        "gender_target": "both",
        "text": "Uchrashuvdan keyin aloqani davom ettirish qanday kechadi?",
        "options": [
            {"text": "Deyarli hech qachon yoki juda kam", "weight": 1},
            {"text": "Ba‘zan, lekin tartibsiz", "weight": 2},
            {"text": "Ko‘pincha va barqaror", "weight": 3},
            {"text": "Doimiy va tabiiy tarzda", "weight": 4},
        ],
    },
    {
        "dimension": "trust",
        "gender_target": "both",
        "text": "Yangi munosabatda bir-biringizning niyatlari (munosabat maqsadi) qanchalik aniq?",
        "options": [
            {"text": "Niyatlar noaniq yoki umuman gapirilmaydi", "weight": 1},
            {"text": "Ba‘zi jihatlar aniq, ba‘zilari emas", "weight": 2},
            {"text": "Ko‘pincha niyatlar tushunarli", "weight": 3},
            {"text": "Niyatlar ochiq va bir-birimizga tushunarli", "weight": 4},
        ],
    },
    {
        "dimension": "trust",
        "gender_target": "both",
        "text": "Uchrashuv va vaqtga oid va‘dalarga amal qilish qanday?",
        "options": [
            {"text": "Ishonch juda past yoki yo‘q", "weight": 1},
            {"text": "Ba‘zan ishonamiz, ba‘zan shubha bor", "weight": 2},
            {"text": "Ko‘pincha ishonchli his qilamiz", "weight": 3},
            {"text": "To‘liq va barqaror ishonch bor", "weight": 4},
        ],
    },
    {
        "dimension": "trust",
        "gender_target": "both",
        "text": "Tanishuv bosqichida shaxsiy chegaralar (telefon, xususiy hayot) hurmati qanday?",
        "options": [
            {"text": "Hurmat deyarli sezilmaydi", "weight": 1},
            {"text": "Ba‘zan hurmat bor, ba‘zan buziladi", "weight": 2},
            {"text": "Ko‘pincha hurmat saqlanadi", "weight": 3},
            {"text": "Doimiy va chuqur hurmat bor", "weight": 4},
        ],
    },
    {
        "dimension": "trust",
        "gender_target": "both",
        "text": "Yangi munosabatda ishonch shakllanishi qanday kechmoqda?",
        "options": [
            {"text": "Ishonch juda past yoki yo‘q", "weight": 1},
            {"text": "Ba‘zan ishonamiz, ba‘zan shubha bor", "weight": 2},
            {"text": "Ko‘pincha ishonchli his qilamiz", "weight": 3},
            {"text": "To‘liq va barqaror ishonch bor", "weight": 4},
        ],
    },
    {
        "dimension": "emotional_closeness",
        "gender_target": "both",
        "text": "Bir-biringizga yaqinlik va qiziqish hissi qanday?",
        "options": [
            {"text": "Juda yomon yoki deyarli yo‘q", "weight": 1},
            {"text": "O‘rtacha, ko‘p muammo bor", "weight": 2},
            {"text": "Yaxshi, lekin yaxshilash kerak", "weight": 3},
            {"text": "Juda yaxshi va barqaror", "weight": 4},
        ],
    },
    {
        "dimension": "emotional_closeness",
        "gender_target": "both",
        "text": "Xafa bo‘lganda tinch va xavfsiz gaplashish mumkinmi?",
        "options": [
            {"text": "Ochilish xavfsiz emas deb his qilaman", "weight": 1},
            {"text": "Ba‘zan xavfsiz, ba‘zan ehtiyotkorlik kerak", "weight": 2},
            {"text": "Ko‘pincha xavfsiz ochilaman", "weight": 3},
            {"text": "To‘liq xavfsiz va qabul qilingan his qilaman", "weight": 4},
        ],
    },
    {
        "dimension": "emotional_closeness",
        "gender_target": "both",
        "text": "Hissiy ochilish va qabul qilinish xavfsizligi qanday?",
        "options": [
            {"text": "Ochilish xavfsiz emas deb his qilaman", "weight": 1},
            {"text": "Ba‘zan xavfsiz, ba‘zan ehtiyotkorlik kerak", "weight": 2},
            {"text": "Ko‘pincha xavfsiz ochilaman", "weight": 3},
            {"text": "To‘liq xavfsiz va qabul qilingan his qilaman", "weight": 4},
        ],
    },
    {
        "dimension": "emotional_closeness",
        "gender_target": "both",
        "text": "Qiyin paytda yonida turish va qo‘llab-quvvatlash qanday?",
        "options": [
            {"text": "Qo‘llab-quvvatlash deyarli yo‘q", "weight": 1},
            {"text": "Ba‘zan yordam bor, ba‘zan yo‘q", "weight": 2},
            {"text": "Ko‘pincha bir-birimizni qo‘llab-quvvatlaymiz", "weight": 3},
            {"text": "Qiyin paytda ham ishonchli tayanchmiz", "weight": 4},
        ],
    },
    {
        "dimension": "attention",
        "gender_target": "both",
        "text": "Bir-biriga vaqt va diqqat ajratish qanday?",
        "options": [
            {"text": "Deyarli hech qachon yoki juda kam", "weight": 1},
            {"text": "Ba‘zan, lekin tartibsiz", "weight": 2},
            {"text": "Ko‘pincha va barqaror", "weight": 3},
            {"text": "Doimiy va tabiiy tarzda", "weight": 4},
        ],
    },
    {
        "dimension": "attention",
        "gender_target": "both",
        "text": "Uchrashuvlar va muloqot sifatiga e‘tibor qanday?",
        "options": [
            {"text": "Juda yomon yoki deyarli yo‘q", "weight": 1},
            {"text": "O‘rtacha, ko‘p muammo bor", "weight": 2},
            {"text": "Yaxshi, lekin yaxshilash kerak", "weight": 3},
            {"text": "Juda yaxshi va barqaror", "weight": 4},
        ],
    },
    {
        "dimension": "attention",
        "gender_target": "both",
        "text": "Bir-biringizning ehtiyojlarini payqash va hurmat qilish qanday?",
        "options": [
            {"text": "Juda yomon yoki deyarli yo‘q", "weight": 1},
            {"text": "O‘rtacha, ko‘p muammo bor", "weight": 2},
            {"text": "Yaxshi, lekin yaxshilash kerak", "weight": 3},
            {"text": "Juda yaxshi va barqaror", "weight": 4},
        ],
    },
    {
        "dimension": "attention",
        "gender_target": "both",
        "text": "Muloqot paytida chalg‘itishsiz tinglash qanday?",
        "options": [
            {"text": "Juda yomon yoki deyarli yo‘q", "weight": 1},
            {"text": "O‘rtacha, ko‘p muammo bor", "weight": 2},
            {"text": "Yaxshi, lekin yaxshilash kerak", "weight": 3},
            {"text": "Juda yaxshi va barqaror", "weight": 4},
        ],
    },
    {
        "dimension": "future_vision",
        "gender_target": "both",
        "text": "Munosabatning kelajagi haqida ochiq gaplashilganmi?",
        "options": [
            {"text": "Niyatlar noaniq yoki umuman gapirilmaydi", "weight": 1},
            {"text": "Ba‘zi jihatlar aniq, ba‘zilari emas", "weight": 2},
            {"text": "Ko‘pincha niyatlar tushunarli", "weight": 3},
            {"text": "Niyatlar ochiq va bir-birimizga tushunarli", "weight": 4},
        ],
    },
    {
        "dimension": "future_vision",
        "gender_target": "both",
        "text": "Uzoq muddatli rejalaringiz bir-biringizga mos keladimi?",
        "options": [
            {"text": "Reja yoki kelishuv deyarli yo‘q", "weight": 1},
            {"text": "Ba‘zan muhokama qilamiz", "weight": 2},
            {"text": "Ko‘pincha kelishib olamiz", "weight": 3},
            {"text": "Aniq va uyg‘un reja bor", "weight": 4},
        ],
    },
    {
        "dimension": "future_vision",
        "gender_target": "both",
        "text": "Bu munosabat qayerga borishini muhokama qilish qanday kechadi?",
        "options": [
            {"text": "Niyatlar noaniq yoki umuman gapirilmaydi", "weight": 1},
            {"text": "Ba‘zi jihatlar aniq, ba‘zilari emas", "weight": 2},
            {"text": "Ko‘pincha niyatlar tushunarli", "weight": 3},
            {"text": "Niyatlar ochiq va bir-birimizga tushunarli", "weight": 4},
        ],
    },
    {
        "dimension": "future_vision",
        "gender_target": "both",
        "text": "Kelajakdagi bir-biriga moslik haqida umumiy fikringiz qanday?",
        "options": [
            {"text": "Reja yoki kelishuv deyarli yo‘q", "weight": 1},
            {"text": "Ba‘zan muhokama qilamiz", "weight": 2},
            {"text": "Ko‘pincha kelishib olamiz", "weight": 3},
            {"text": "Aniq va uyg‘un reja bor", "weight": 4},
        ],
    },
    {
        "dimension": "boundaries",
        "gender_target": "both",
        "text": "Erta bosqichda shaxsiy chegaralar qanday belgilanadi?",
        "options": [
            {"text": "Hurmat deyarli sezilmaydi", "weight": 1},
            {"text": "Ba‘zan hurmat bor, ba‘zan buziladi", "weight": 2},
            {"text": "Ko‘pincha hurmat saqlanadi", "weight": 3},
            {"text": "Doimiy va chuqur hurmat bor", "weight": 4},
        ],
    },
    {
        "dimension": "boundaries",
        "gender_target": "both",
        "text": "Yaqinlik tezligi va masofa bo‘yicha kelishuvlar bormi?",
        "options": [
            {"text": "Reja yoki kelishuv deyarli yo‘q", "weight": 1},
            {"text": "Ba‘zan muhokama qilamiz", "weight": 2},
            {"text": "Ko‘pincha kelishib olamiz", "weight": 3},
            {"text": "Aniq va uyg‘un reja bor", "weight": 4},
        ],
    },
    {
        "dimension": "boundaries",
        "gender_target": "both",
        "text": "Rad etishga (yo‘q deyishga) hurmat qanday?",
        "options": [
            {"text": "Hurmat deyarli sezilmaydi", "weight": 1},
            {"text": "Ba‘zan hurmat bor, ba‘zan buziladi", "weight": 2},
            {"text": "Ko‘pincha hurmat saqlanadi", "weight": 3},
            {"text": "Doimiy va chuqur hurmat bor", "weight": 4},
        ],
    },
    {
        "dimension": "boundaries",
        "gender_target": "both",
        "text": "Boshqa odamlar yoki ijtimoiy tarmoqlarda munosabat chegaralari qanday?",
        "options": [
            {"text": "Hurmat deyarli sezilmaydi", "weight": 1},
            {"text": "Ba‘zan hurmat bor, ba‘zan buziladi", "weight": 2},
            {"text": "Ko‘pincha hurmat saqlanadi", "weight": 3},
            {"text": "Doimiy va chuqur hurmat bor", "weight": 4},
        ],
    },
    {
        "dimension": "responsibility",
        "gender_target": "both",
        "text": "Uchrashuv va rejalarga mas‘uliyat bilan yondashish qanday?",
        "options": [
            {"text": "Ishonch juda past yoki yo‘q", "weight": 1},
            {"text": "Ba‘zan ishonamiz, ba‘zan shubha bor", "weight": 2},
            {"text": "Ko‘pincha ishonchli his qilamiz", "weight": 3},
            {"text": "To‘liq va barqaror ishonch bor", "weight": 4},
        ],
    },
    {
        "dimension": "responsibility",
        "gender_target": "both",
        "text": "Bir-birining vaqtini hurmat qilish qanday?",
        "options": [
            {"text": "Hurmat deyarli sezilmaydi", "weight": 1},
            {"text": "Ba‘zan hurmat bor, ba‘zan buziladi", "weight": 2},
            {"text": "Ko‘pincha hurmat saqlanadi", "weight": 3},
            {"text": "Doimiy va chuqur hurmat bor", "weight": 4},
        ],
    },
    {
        "dimension": "responsibility",
        "gender_target": "both",
        "text": "Noto‘g‘ri xulq-atvor uchun mas‘uliyat olish qanday?",
        "options": [
            {"text": "Juda yomon yoki deyarli yo‘q", "weight": 1},
            {"text": "O‘rtacha, ko‘p muammo bor", "weight": 2},
            {"text": "Yaxshi, lekin yaxshilash kerak", "weight": 3},
            {"text": "Juda yaxshi va barqaror", "weight": 4},
        ],
    },
    {
        "dimension": "responsibility",
        "gender_target": "both",
        "text": "Munosabatni rivojlantirish uchun qanchalik faol harakat qilasiz?",
        "options": [
            {"text": "Deyarli hech qachon yoki juda kam", "weight": 1},
            {"text": "Ba‘zan, lekin tartibsiz", "weight": 2},
            {"text": "Ko‘pincha va barqaror", "weight": 3},
            {"text": "Doimiy va tabiiy tarzda", "weight": 4},
        ],
    },
]
