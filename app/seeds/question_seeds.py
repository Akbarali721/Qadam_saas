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


COMMUNICATION_QUESTIONS: list[QuestionSeed] = [
    {
        "dimension": "communication",
        "gender_target": "both",
        "text": "Muhim mavzuni ochish kerak bo‘lsa, odatda kim birinchi gap boshlaydi?",
        "options": [
            {"text": "Ko‘pincha hech kim boshlamaydi, mavzu yopilib qoladi", "weight": 1},
            {"text": "Faqat jiddiylashganda gap ochiladi", "weight": 2},
            {"text": "Odatda birimiz boshlaydi, ikkinchimiz qo‘shiladi", "weight": 3},
            {"text": "Ikkalamiz ham ochiq gap boshlay olamiz", "weight": 4},
        ],
    },
    {
        "dimension": "communication",
        "gender_target": "both",
        "text": "Noto‘g‘ri tushunish bo‘lsa, uni qanday aniqlashtirasiz?",
        "options": [
            {"text": "Aniqlashtirmaymiz, ichimizda olib yuramiz", "weight": 1},
            {"text": "Ko‘pincha tortishuvdan keyin aniqlanadi", "weight": 2},
            {"text": "Sokin paytda qayta gaplashib olamiz", "weight": 3},
            {"text": "Darhol hurmat bilan aniqlashtirib olamiz", "weight": 4},
        ],
    },
    {
        "dimension": "communication",
        "gender_target": "both",
        "text": "Band kunlarda ham aloqani saqlash darajangiz qanday?",
        "options": [
            {"text": "Kun bo‘yi deyarli aloqa bo‘lmaydi", "weight": 1},
            {"text": "Faqat zarur paytda qisqa yozamiz", "weight": 2},
            {"text": "Qisqa bo‘lsa ham muntazam xabar beramiz", "weight": 3},
            {"text": "Bandlikda ham bir-birimizni e’tiborsiz qoldirmaymiz", "weight": 4},
        ],
    },
    {
        "dimension": "communication",
        "gender_target": "both",
        "text": "Hissiyotlarni ifoda qilish sizlarda qanchalik oson?",
        "options": [
            {"text": "Hissiyotlar deyarli aytilmaydi", "weight": 1},
            {"text": "Faqat kuchli holatda aytiladi", "weight": 2},
            {"text": "Ko‘p vaziyatlarda ochiq aytishga harakat qilamiz", "weight": 3},
            {"text": "Hissiyotlarni ochiq va tushunarli ifoda qilamiz", "weight": 4},
        ],
    },
    {
        "dimension": "communication",
        "gender_target": "both",
        "text": "Reja o‘zgarsa bir-biringizni qanchalik oldindan ogohlantirasiz?",
        "options": [
            {"text": "Ko‘pincha aytilmaydi, keyin ma’lum bo‘ladi", "weight": 1},
            {"text": "Ba’zan kechikib aytiladi", "weight": 2},
            {"text": "Aksar holatda oldindan xabar beriladi", "weight": 3},
            {"text": "Har doim o‘z vaqtida va aniq ogohlantiramiz", "weight": 4},
        ],
    },
    {
        "dimension": "communication",
        "gender_target": "both",
        "text": "Qiyin mavzularda ohangni nazorat qilish qanday?",
        "options": [
            {"text": "Tezda keskinlashib ketadi", "weight": 1},
            {"text": "Ba’zan ovoz ko‘tariladi", "weight": 2},
            {"text": "Ko‘pincha tinch ohangni saqlaymiz", "weight": 3},
            {"text": "Har doim hurmatli ohangda gaplashamiz", "weight": 4},
        ],
    },
    {
        "dimension": "communication",
        "gender_target": "both",
        "text": "Bir-biringizni tinglash sifati qanday?",
        "options": [
            {"text": "Ko‘proq javob berishga tayyorlanamiz, tinglash kam", "weight": 1},
            {"text": "Tinglaymiz, lekin ko‘p bo‘lib bo‘lib ketamiz", "weight": 2},
            {"text": "Asosan oxirigacha tinglaymiz", "weight": 3},
            {"text": "Faol tinglaymiz va to‘g‘ri tushunganimizni tekshiramiz", "weight": 4},
        ],
    },
    {
        "dimension": "communication",
        "gender_target": "both",
        "text": "Yozma muloqotda (chatda) noaniqliklar qanchalik tez hal bo‘ladi?",
        "options": [
            {"text": "Ko‘pincha hal bo‘lmay, xafa bo‘lib qolamiz", "weight": 1},
            {"text": "Kechikib hal bo‘ladi, orasida sovuqlik bo‘ladi", "weight": 2},
            {"text": "Odatda keyin qo‘ng‘iroq qilib tushuntiramiz", "weight": 3},
            {"text": "Darhol aniqlik kiritib, noto‘g‘ri tushunishni yopamiz", "weight": 4},
        ],
    },
    {
        "dimension": "communication",
        "gender_target": "both",
        "text": "Bir-biringizdan nimani kutishingizni qanchalik aniq aytasiz?",
        "options": [
            {"text": "Kutishlar ko‘pincha aytilmaydi", "weight": 1},
            {"text": "Faqat muammo chiqqanda aytamiz", "weight": 2},
            {"text": "Aksar payt ochiq aytishga harakat qilamiz", "weight": 3},
            {"text": "Kutishlarimizni oldindan aniq va muloyim aytamiz", "weight": 4},
        ],
    },
    {
        "dimension": "communication",
        "gender_target": "both",
        "text": "Kelishmovchilikdan keyin yarashib olish suhbati sizlarda qanday o‘tadi?",
        "options": [
            {"text": "Ko‘pincha umuman bo‘lmaydi", "weight": 1},
            {"text": "Faqat vaqt o‘tib, yuzaki yopiladi", "weight": 2},
            {"text": "Odatda nimalar bo‘lganini muhokama qilamiz", "weight": 3},
            {"text": "Tahlil qilib, keyingi safar uchun kelishuv qilamiz", "weight": 4},
        ],
    },
]


TRUST_QUESTIONS: list[QuestionSeed] = [
    {
        "dimension": "trust",
        "gender_target": "both",
        "text": "Berilgan va’dalarga amal qilish darajangiz qanday?",
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
        "text": "Shubhali vaziyatda bir-biringizga qanday yondashasiz?",
        "options": [
            {"text": "Darhol yomon xulosaga boramiz", "weight": 1},
            {"text": "Ichimizda shubha saqlab yuramiz", "weight": 2},
            {"text": "Avval so‘rab aniqlik kiritamiz", "weight": 3},
            {"text": "Faktga asoslanib, xotirjam gaplashamiz", "weight": 4},
        ],
    },
    {
        "dimension": "trust",
        "gender_target": "both",
        "text": "Shaxsiy chegaralarga (telefon, vaqt, makon) hurmat qanchalik bor?",
        "options": [
            {"text": "Chegaralar tez-tez buziladi", "weight": 1},
            {"text": "Ba’zan noqulay holatlar bo‘ladi", "weight": 2},
            {"text": "Ko‘p holatda chegaralar hurmat qilinadi", "weight": 3},
            {"text": "Chegaralar aniq va izchil hurmat qilinadi", "weight": 4},
        ],
    },
    {
        "dimension": "trust",
        "gender_target": "both",
        "text": "Qiyin paytda bir-biringizga tayana olish hissi qanchalik bor?",
        "options": [
            {"text": "Ko‘pincha yolg‘iz qolaman deb his qilamiz", "weight": 1},
            {"text": "Ba’zan tayanch bor, ba’zan yo‘q", "weight": 2},
            {"text": "Aksar holatda bir-birimizga suyanamiz", "weight": 3},
            {"text": "Qiyin paytda ham ishonchli tayanchmiz", "weight": 4},
        ],
    },
    {
        "dimension": "trust",
        "gender_target": "both",
        "text": "Xatoni tan olish va kechirim so‘rash odati sizlarda qanday?",
        "options": [
            {"text": "Xato tan olinmaydi yoki inkor qilinadi", "weight": 1},
            {"text": "Faqat bosimdan keyin tan olinadi", "weight": 2},
            {"text": "Ko‘p holatda xato tan olinadi", "weight": 3},
            {"text": "Mas’uliyat ochiq olinadi va ishonch tiklanadi", "weight": 4},
        ],
    },
    {
        "dimension": "trust",
        "gender_target": "both",
        "text": "Boshqalar oldida bir-biringizni qo‘llab-quvvatlash darajasi qanday?",
        "options": [
            {"text": "Ko‘pincha yolg‘iz qoldirib qo‘yamiz", "weight": 1},
            {"text": "Ba’zan qo‘llab-quvvatlaymiz", "weight": 2},
            {"text": "Aksar vaziyatda bir-birimizni himoya qilamiz", "weight": 3},
            {"text": "Doim hurmat bilan yonma-yon turamiz", "weight": 4},
        ],
    },
    {
        "dimension": "trust",
        "gender_target": "both",
        "text": "Reja, xarajat yoki tashkiliy masalalarda ochiqlik qanday?",
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
        "text": "Sir saqlash borasida bir-biringizga ishonch qanchalik kuchli?",
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
        "text": "Kechikish yoki rejadagi xatoda ishonchni tiklash qanday kechadi?",
        "options": [
            {"text": "Ayblash davom etadi, masala yopilmaydi", "weight": 1},
            {"text": "Vaqt o‘tibgina unutamiz", "weight": 2},
            {"text": "Gaplashib kelishib olamiz", "weight": 3},
            {"text": "Sabab, yechim va kelishuv bilan tez tiklaymiz", "weight": 4},
        ],
    },
    {
        "dimension": "trust",
        "gender_target": "both",
        "text": "Kelajak bo‘yicha bir-biringizga ishonch hissi qanday?",
        "options": [
            {"text": "Kelajak noaniq va beqaror ko‘rinadi", "weight": 1},
            {"text": "Ba’zi yo‘nalishlarda ikkilanish bor", "weight": 2},
            {"text": "Ko‘p jihatda bir yo‘nalishda ketamiz", "weight": 3},
            {"text": "Uzoq muddatli rejada ham bir-birimizga ishonamiz", "weight": 4},
        ],
    },
]


PARTIAL_POOL: list[QuestionSeed] = [
    *COMMUNICATION_QUESTIONS,
    *TRUST_QUESTIONS,
]


EMOTIONAL_CLOSENESS_QUESTIONS: list[QuestionSeed] = [
    {
        "dimension": "emotional_closeness",
        "gender_target": "both",
        "text": "Ichki kechinmalaringizni bo‘lishishda o‘zingizni qanchalik xavfsiz his qilasiz?",
        "options": [
            {"text": "Ko‘pincha ichimda saqlayman, ochilish qiyin", "weight": 1},
            {"text": "Faqat juda zarur bo‘lsa bo‘lishaman", "weight": 2},
            {"text": "Ko‘p holatda hislarimni ayta olaman", "weight": 3},
            {"text": "Bemalol ochilaman, tinglanishimga ishonaman", "weight": 4},
        ],
    },
    {
        "dimension": "emotional_closeness",
        "gender_target": "both",
        "text": "Xafa bo‘lganingizda bir-biringizga yaqinlashish qanday kechadi?",
        "options": [
            {"text": "Uzoqlashib ketamiz va uzoq sovuqlik bo‘ladi", "weight": 1},
            {"text": "Bir muddat masofa bo‘ladi, keyin asta gaplashamiz", "weight": 2},
            {"text": "Ko‘p holatda tezroq yaqinlashib olamiz", "weight": 3},
            {"text": "Xafa bo‘lsak ham bir-birimizga muloyim qaytamiz", "weight": 4},
        ],
    },
    {
        "dimension": "emotional_closeness",
        "gender_target": "both",
        "text": "Qiyin kunlarda hissiy qo‘llab-quvvatlash darajangiz qanday?",
        "options": [
            {"text": "Ko‘pincha o‘zimga tashlab qo‘yilgandek bo‘laman", "weight": 1},
            {"text": "Ba’zan qo‘llab-quvvatlash bor, ba’zan yetmaydi", "weight": 2},
            {"text": "Aksar payt bir-birimizni ruhlantirib turamiz", "weight": 3},
            {"text": "Qiyin paytda ham bir-birimizga iliq tayanchmiz", "weight": 4},
        ],
    },
    {
        "dimension": "emotional_closeness",
        "gender_target": "both",
        "text": "Bir-biringizning hislarini rad etmasdan qabul qilish qanday?",
        "options": [
            {"text": "Hislar ko‘pincha mensilmaydi yoki inkor qilinadi", "weight": 1},
            {"text": "Ba’zan tushunishga urinamiz, lekin tez bahoga o‘tamiz", "weight": 2},
            {"text": "Ko‘pincha hislarni jiddiy qabul qilamiz", "weight": 3},
            {"text": "Hislarni hurmat bilan tinglab, joy beramiz", "weight": 4},
        ],
    },
    {
        "dimension": "emotional_closeness",
        "gender_target": "both",
        "text": "Mehr va iliqlikni kundalikda qanday ko‘rsatasiz?",
        "options": [
            {"text": "Iliq munosabat kam, ko‘proq sovuqlik seziladi", "weight": 1},
            {"text": "Vaqti-vaqti bilan iliqlik bo‘ladi", "weight": 2},
            {"text": "Ko‘p kunlarda mehrni ko‘rsatib turamiz", "weight": 3},
            {"text": "Iliqlik doimiy va tabiiy hissamizga aylangan", "weight": 4},
        ],
    },
    {
        "dimension": "emotional_closeness",
        "gender_target": "both",
        "text": "Nozik mavzuda himoyaviy reaksiyasiz gaplashish qanchalik oson?",
        "options": [
            {"text": "Tezda yopilib qolamiz yoki keskin himoyalanamiz", "weight": 1},
            {"text": "Ba’zan tinch bo‘lamiz, ba’zan keskinlashamiz", "weight": 2},
            {"text": "Aksar holatda sokin gaplashishga harakat qilamiz", "weight": 3},
            {"text": "Nozik mavzularda ham ochiq va ehtiyotkor muloqot qilamiz", "weight": 4},
        ],
    },
    {
        "dimension": "emotional_closeness",
        "gender_target": "both",
        "text": "Bir-biringizning quvonchiga sherik bo‘lish darajasi qanday?",
        "options": [
            {"text": "Quvonchlar ko‘pincha e’tiborsiz qoladi", "weight": 1},
            {"text": "Ba’zan quvonchni bo‘lishamiz", "weight": 2},
            {"text": "Ko‘p holatda birga xursand bo‘lamiz", "weight": 3},
            {"text": "Bir-birimizning yutug‘ini chin dildan nishonlaymiz", "weight": 4},
        ],
    },
    {
        "dimension": "emotional_closeness",
        "gender_target": "both",
        "text": "Ranjishdan keyin yurakdan kechira olish qanday?",
        "options": [
            {"text": "Ranjish uzoq saqlanadi va tez-tez eslatiladi", "weight": 1},
            {"text": "Kechiramiz, lekin ichki og‘riq qoladi", "weight": 2},
            {"text": "Ko‘p holatda kechirishga erishamiz", "weight": 3},
            {"text": "Tushunib, saboq olib, chinakam kechira olamiz", "weight": 4},
        ],
    },
    {
        "dimension": "emotional_closeness",
        "gender_target": "both",
        "text": "Sukut paytida ham bir-biringiz bilan yaqinlikni his qilasizmi?",
        "options": [
            {"text": "Sukut ko‘pincha sovuqlikdek tuyuladi", "weight": 1},
            {"text": "Ba’zan noqulaylik seziladi", "weight": 2},
            {"text": "Odatda sokinlikda ham aloqani his qilamiz", "weight": 3},
            {"text": "Sukutda ham tinch va yaqin his qilamiz", "weight": 4},
        ],
    },
    {
        "dimension": "emotional_closeness",
        "gender_target": "both",
        "text": "Munosabatda o‘zingiz bo‘lib qolish erkinligi qanchalik bor?",
        "options": [
            {"text": "Ko‘pincha o‘zimni yashirishga majburman", "weight": 1},
            {"text": "Ba’zi tomonlarimni yashiraman", "weight": 2},
            {"text": "Ko‘p jihatdan o‘zim bo‘la olaman", "weight": 3},
            {"text": "To‘liq o‘zim bo‘lib, qabul qilinishni his qilaman", "weight": 4},
        ],
    },
]


ATTENTION_QUESTIONS: list[QuestionSeed] = [
    {
        "dimension": "attention",
        "gender_target": "both",
        "text": "Bir-biringizning kayfiyatidagi o‘zgarishni qanchalik tez sezasiz?",
        "options": [
            {"text": "Ko‘pincha umuman sezmaymiz", "weight": 1},
            {"text": "Faqat ancha kuchli bo‘lsa sezamiz", "weight": 2},
            {"text": "Aksar payt sezib, hol so‘raymiz", "weight": 3},
            {"text": "Mayda signallarnigacha payqab, e’tibor beramiz", "weight": 4},
        ],
    },
    {
        "dimension": "attention",
        "gender_target": "both",
        "text": "Muloqot paytida telefon va chalg‘ituvchilarni chetga qo‘yish odatingiz qanday?",
        "options": [
            {"text": "Ko‘pincha gap paytida ham chalg‘ib ketamiz", "weight": 1},
            {"text": "Ba’zan diqqat bo‘linadi", "weight": 2},
            {"text": "Ko‘p holatda suhbatga diqqat qaratamiz", "weight": 3},
            {"text": "Suhbat paytida to‘liq e’tibor beramiz", "weight": 4},
        ],
    },
    {
        "dimension": "attention",
        "gender_target": "both",
        "text": "Bir-biringiz uchun vaqt ajratishni qanchalik rejalaysiz?",
        "options": [
            {"text": "Maxsus vaqt deyarli ajratilmaydi", "weight": 1},
            {"text": "Faqat bo‘sh qolsa uchrashamiz", "weight": 2},
            {"text": "Odatda oldindan vaqt belgilab qo‘yamiz", "weight": 3},
            {"text": "Vaqt ajratish barqaror ustuvorlikka aylangan", "weight": 4},
        ],
    },
    {
        "dimension": "attention",
        "gender_target": "both",
        "text": "Muhim sana yoki voqealarni eslab qolish darajangiz qanday?",
        "options": [
            {"text": "Ko‘pincha unutilib ketadi", "weight": 1},
            {"text": "Ba’zi muhim sanalar esdan chiqadi", "weight": 2},
            {"text": "Aksar muhim sanalarni eslab qolamiz", "weight": 3},
            {"text": "Muhim sanalarni e’tibor bilan eslab, nishonlaymiz", "weight": 4},
        ],
    },
    {
        "dimension": "attention",
        "gender_target": "both",
        "text": "Bir-biringizning ehtiyojini aytmasdan turib payqash qanchalik bo‘ladi?",
        "options": [
            {"text": "Ko‘pincha ehtiyojlar ko‘rinmay qoladi", "weight": 1},
            {"text": "Ba’zan sezamiz, ko‘pincha aytilgach bilamiz", "weight": 2},
            {"text": "Ko‘p holatda ishoralarni payqab qolamiz", "weight": 3},
            {"text": "Mayda ehtiyojlargacha sezib, vaqtida javob beramiz", "weight": 4},
        ],
    },
    {
        "dimension": "attention",
        "gender_target": "both",
        "text": "Kichik iltimoslarga javob berish tezligi qanday?",
        "options": [
            {"text": "Ko‘pincha e’tiborsiz qolib ketadi", "weight": 1},
            {"text": "Kechikib bajariladi", "weight": 2},
            {"text": "Odatda vaqtida bajariladi", "weight": 3},
            {"text": "Darhol yoki oldindan g‘amxo‘rlik bilan bajariladi", "weight": 4},
        ],
    },
    {
        "dimension": "attention",
        "gender_target": "both",
        "text": "Charchagan paytda bir-biringizga ko‘rsatiladigan mehr qanday?",
        "options": [
            {"text": "Charchoq payti ko‘pincha sovuqlashamiz", "weight": 1},
            {"text": "Ba’zan holatni tushunmay qolamiz", "weight": 2},
            {"text": "Odatda holatni inobatga olib muomala qilamiz", "weight": 3},
            {"text": "Charchoqda ham bir-birimizni asraymiz", "weight": 4},
        ],
    },
    {
        "dimension": "attention",
        "gender_target": "both",
        "text": "Bir-biringiz gapirayotganda savol berib aniqlik kiritish odati bormi?",
        "options": [
            {"text": "Ko‘pincha yuzaki eshitib qo‘yamiz", "weight": 1},
            {"text": "Ba’zan savol beramiz", "weight": 2},
            {"text": "Aksar payt yaxshiroq tushunish uchun so‘raymiz", "weight": 3},
            {"text": "Diqqat bilan tinglab, nozik joylarini ham aniqlashtiramiz", "weight": 4},
        ],
    },
    {
        "dimension": "attention",
        "gender_target": "both",
        "text": "Birga bo‘lganingizda suhbatdoshingiz o‘zini qadrli his qiladimi?",
        "options": [
            {"text": "Ko‘pincha e’tiborsizdek his qilinadi", "weight": 1},
            {"text": "Ba’zan qadrli, ba’zan chetda qolgan his bo‘ladi", "weight": 2},
            {"text": "Odatda qadrlanish hissi bor", "weight": 3},
            {"text": "Doimiy ravishda qadrli va ko‘rilganini his qiladi", "weight": 4},
        ],
    },
    {
        "dimension": "attention",
        "gender_target": "both",
        "text": "Mayda quvonchlarni payqab, e’tibor ko‘rsatish odati qanday?",
        "options": [
            {"text": "Mayda quvonchlar ko‘pincha sezilmay qoladi", "weight": 1},
            {"text": "Ba’zan sezamiz, lekin doim emas", "weight": 2},
            {"text": "Aksar holatda payqab quvontiramiz", "weight": 3},
            {"text": "Mayda detallarni ham qadrlab, iliq reaksiya beramiz", "weight": 4},
        ],
    },
]


BASE_QUESTION_POOL: list[QuestionSeed] = [
    *COMMUNICATION_QUESTIONS,
    *TRUST_QUESTIONS,
    *EMOTIONAL_CLOSENESS_QUESTIONS,
    *ATTENTION_QUESTIONS,
]


QUESTIONS_MARRIED: list[QuestionSeed] = [*BASE_QUESTION_POOL]
QUESTIONS_FRIENDS: list[QuestionSeed] = [*BASE_QUESTION_POOL]
QUESTIONS_DATING: list[QuestionSeed] = [*BASE_QUESTION_POOL]
