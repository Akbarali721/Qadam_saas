from typing import TypedDict


class MbtiOptionSeed(TypedDict):
    text: str
    pole: str
    score: int


class MbtiQuestionSeed(TypedDict):
    text: str
    dimension: str
    options: list[MbtiOptionSeed]


def _options(
    strong_a: str,
    soft_a: str,
    soft_b: str,
    strong_b: str,
    pole_a: str,
    pole_b: str,
) -> list[MbtiOptionSeed]:
    return [
        {"text": strong_a, "pole": pole_a, "score": 2},
        {"text": soft_a, "pole": pole_a, "score": 1},
        {"text": soft_b, "pole": pole_b, "score": 1},
        {"text": strong_b, "pole": pole_b, "score": 2},
    ]


MBTI_QUESTIONS: list[MbtiQuestionSeed] = [
    {
        "text": "Dam olish kunida qanday vaqt o‘tkazasiz?",
        "dimension": "IE",
        "options": _options(
            "Ko‘proq odamlar bilan uchrashib, faol vaqt o‘tkazaman",
            "Yaqinlarim bilan qisqa uchrashuv menga yoqadi",
            "Tinchroq joyda, kam odam bilan dam olganim ma’qul",
            "Yolg‘iz qolib, kuchimni qayta tiklashni xohlayman",
            "E",
            "I",
        ),
    },
    {
        "text": "Uzoq suhbatdan keyin o‘zingizni qanday his qilasiz?",
        "dimension": "IE",
        "options": _options(
            "Yanada ochilib, energiyam oshgandek bo‘ladi",
            "Suhbat yaxshi bo‘lsa, kayfiyatim ko‘tariladi",
            "Biroz tinchlik kerak bo‘lishi mumkin",
            "Odatda charchayman va yolg‘iz qolishni xohlayman",
            "E",
            "I",
        ),
    },
    {
        "text": "Yangi jamoaga tushsangiz qanday tutasiz?",
        "dimension": "IE",
        "options": _options(
            "Tez tanishib, suhbatni o‘zim boshlayman",
            "Bir-ikki odam bilan gaplashib kirishib ketaman",
            "Avval muhitni kuzatib, keyin asta ochilaman",
            "Ko‘proq kuzataman va o‘zimni darrov ko‘rsatmayman",
            "E",
            "I",
        ),
    },
    {
        "text": "Bo‘sh vaqtingizni qanday o‘tkazasiz?",
        "dimension": "IE",
        "options": _options(
            "Tashqariga chiqib, odamlar orasida bo‘lishni yoqtiraman",
            "Reja bo‘lsa, uchrashuvlarga bajonidil boraman",
            "Uyda sokin mashg‘ulotlar ham menga yoqadi",
            "Ko‘pincha yolg‘iz, tinch muhitni tanlayman",
            "E",
            "I",
        ),
    },
    {
        "text": "Qiziqarli idea bo‘lsa nima qilasiz?",
        "dimension": "IE",
        "options": _options(
            "Darhol boshqalar bilan bo‘lishib, fikr olaman",
            "Avval yaqin odamga aytib ko‘raman",
            "Oldin o‘zim ichimda pishitib olaman",
            "Ancha o‘ylab, tayyor bo‘lganda aytaman",
            "E",
            "I",
        ),
    },
    {
        "text": "Ko‘p odamli joyda holatingiz qanday bo‘ladi?",
        "dimension": "IE",
        "options": _options(
            "O‘zimni erkin va jonli his qilaman",
            "Muhit yoqsa, tez moslashaman",
            "Biroz vaqt o‘tib tinchroq joy izlayman",
            "Tez charchayman va ortiqcha shovqindan qochaman",
            "E",
            "I",
        ),
    },
    {
        "text": "Muammo bo‘lsa qanday hal qilasiz?",
        "dimension": "IE",
        "options": _options(
            "Kimdir bilan gaplashib, fikrlarni ovoz chiqarib tartiblayman",
            "Maslahat so‘rash muammoni tezroq ochadi",
            "Avval o‘zim o‘ylab ko‘rishni afzal bilaman",
            "Yolg‘iz tahlil qilib, keyin qaror qilaman",
            "E",
            "I",
        ),
    },
    {
        "text": "Ishlash uslubingiz qanday?",
        "dimension": "IE",
        "options": _options(
            "Jamoa bilan fikr almashib ishlaganda samaraliroqman",
            "Hamkorlik bo‘lsa, motivatsiyam oshadi",
            "Mustaqil ishlashga ham ehtiyoj sezaman",
            "Yolg‘iz va chuqur ishlaganda eng yaxshi natija qilaman",
            "E",
            "I",
        ),
    },
    {
        "text": "Siz ko‘proq nimaga e’tibor berasiz?",
        "dimension": "NS",
        "options": _options(
            "Yangi imkoniyatlar va umumiy ma’noga",
            "G‘oya ortidagi yo‘nalish va ehtimollarga",
            "Aniq faktlar va hozirgi vaziyatga",
            "Ko‘rish, tekshirish va amalda isbotlangan narsalarga",
            "N",
            "S",
        ),
    },
    {
        "text": "O‘rganishda qaysi uslub sizga mos?",
        "dimension": "NS",
        "options": _options(
            "Avval katta rasmni tushunib olish",
            "Mavzuning ma’nosi va bog‘lanishini ko‘rish",
            "Misollar orqali bosqichma-bosqich o‘rganish",
            "Aniq ko‘rsatma va amaliy mashq bilan o‘rganish",
            "N",
            "S",
        ),
    },
    {
        "text": "Kelajak haqida qanday o‘ylaysiz?",
        "dimension": "NS",
        "options": _options(
            "Uzoq imkoniyatlar va katta o‘zgarishlar haqida ko‘p o‘ylayman",
            "Kelajakdagi yo‘nalishlarni tasavvur qilishni yoqtiraman",
            "Avval hozirgi real vaziyatni hisobga olaman",
            "Reja aniq fakt va imkoniyatlarga tayanishi kerak",
            "N",
            "S",
        ),
    },
    {
        "text": "Muammoni qanday yechasiz?",
        "dimension": "NS",
        "options": _options(
            "Noan’anaviy yechim izlayman",
            "Bir nechta ehtimoliy yo‘lni ko‘rib chiqaman",
            "Sinovdan o‘tgan usulni qo‘llayman",
            "Aniq qadamlar bilan amaliy hal qilaman",
            "N",
            "S",
        ),
    },
    {
        "text": "Sizni nimalar ko‘proq qiziqtiradi?",
        "dimension": "NS",
        "options": _options(
            "G‘oyalar, nazariyalar va kelajak imkoniyatlari",
            "Narsalar nima uchun shundayligini tushunish",
            "Real tajriba va foydali amaliy bilimlar",
            "Hozir ishlaydigan, qo‘l bilan ushlab ko‘radigan yechimlar",
            "N",
            "S",
        ),
    },
    {
        "text": "Savol berishda nimaga moyilsiz?",
        "dimension": "NS",
        "options": _options(
            "“Bu nimaga olib boradi?” deb so‘rayman",
            "Yashirin ma’no va bog‘liqlikni izlayman",
            "“Bu qanday ishlaydi?” deb so‘rayman",
            "Aniq tafsilot, fakt va misol so‘rayman",
            "N",
            "S",
        ),
    },
    {
        "text": "Qanday filmlar sizga yoqadi?",
        "dimension": "NS",
        "options": _options(
            "Ma’nosi chuqur, ramz va g‘oyalarga boy filmlar",
            "Kutilmagan konsept yoki noodatiy voqealar",
            "Hayotiy, real va tushunarli voqealar",
            "Aniq syujetli, detallari ishonarli filmlar",
            "N",
            "S",
        ),
    },
    {
        "text": "Siz uchun nima muhimroq?",
        "dimension": "NS",
        "options": _options(
            "Yangi yo‘l ochish va imkoniyatni ko‘rish",
            "Tasavvur va ma’no topish",
            "Barqarorlik va amaliy natija",
            "Aniqlik, tajriba va real foyda",
            "N",
            "S",
        ),
    },
    {
        "text": "Qaror qabul qilishda nimaga tayanasiz?",
        "dimension": "TF",
        "options": _options(
            "Mantiq, adolat va dalillarga",
            "Vaziyatni xolis tahlil qilishga",
            "Odamlarga qanday ta’sir qilishini ham hisobga olaman",
            "His-tuyg‘u, qadriyat va munosabatni birinchi o‘ringa qo‘yaman",
            "T",
            "F",
        ),
    },
    {
        "text": "Bahsda siz uchun nima muhim?",
        "dimension": "TF",
        "options": _options(
            "Haqiqatni aniq topish",
            "Fikrlarni mantiqan tartiblash",
            "Ohangni yumshoq saqlash",
            "Munosabat buzilmasligi va odamlar ranjimasligi",
            "T",
            "F",
        ),
    },
    {
        "text": "Do‘stingiz xato qilsa nima qilasiz?",
        "dimension": "TF",
        "options": _options(
            "Xatosini ochiq va aniq aytaman",
            "Avval muammoni tahlil qilib tushuntiraman",
            "Ehtiyotkorlik bilan aytishga harakat qilaman",
            "Avval uning holatini tushunib, keyin muloyim gapiraman",
            "T",
            "F",
        ),
    },
    {
        "text": "O‘zingizni qanday tasvirlaysiz?",
        "dimension": "TF",
        "options": _options(
            "Xolis, mantiqli va prinsipial",
            "Tahlilga moyil va adolatni qadrlaydigan",
            "Mehribon va odamlarning holatini sezadigan",
            "Hissiy noziklik va qadriyatlarga e’tiborli",
            "T",
            "F",
        ),
    },
    {
        "text": "Tanlashda nimani ustun qo‘yasiz?",
        "dimension": "TF",
        "options": _options(
            "Eng oqilona va samarali variantni",
            "Qoidalarga mos, adolatli qarorni",
            "Odamlarga eng kam og‘ir botadigan yo‘lni",
            "Hamma uchun iliq va qadriyatga mos qarorni",
            "T",
            "F",
        ),
    },
    {
        "text": "Tanqidni qanday qabul qilasiz?",
        "dimension": "TF",
        "options": _options(
            "Asosli bo‘lsa, uni foydali ma’lumot deb ko‘raman",
            "Mazmuni to‘g‘ri bo‘lsa, ohangiga uncha berilmayman",
            "Ohang ham men uchun muhim",
            "Qattiq tanqid menga kuchli ta’sir qilishi mumkin",
            "T",
            "F",
        ),
    },
    {
        "text": "Yordam berishda qanday yondashasiz?",
        "dimension": "TF",
        "options": _options(
            "Muammoning aniq yechimini topishga harakat qilaman",
            "Vaziyatni tartiblab, amaliy maslahat beraman",
            "Avval odamni tinglab, holatini tushunaman",
            "U o‘zini yolg‘iz his qilmasligi uchun yonida bo‘laman",
            "T",
            "F",
        ),
    },
    {
        "text": "Rejaga munosabatingiz qanday?",
        "dimension": "PJ",
        "options": _options(
            "Reja aniq bo‘lsa, o‘zimni xotirjam his qilaman",
            "Asosiy qadamlar oldindan belgilanganini yoqtiraman",
            "Reja bo‘lsa ham, erkinlik qolishi kerak",
            "Vaziyatga qarab harakat qilish menga qulayroq",
            "J",
            "P",
        ),
    },
    {
        "text": "Deadline yaqinlashsa nima qilasiz?",
        "dimension": "PJ",
        "options": _options(
            "Oldindan tugatib qo‘yishga harakat qilaman",
            "Ishni vaqtida bo‘lib chiqaman",
            "Oxirgi kunlarda yaxshiroq tezlashaman",
            "Bosim yaqinlashganda eng faol ishlayman",
            "J",
            "P",
        ),
    },
    {
        "text": "O‘zingizni qanday ko‘rasiz?",
        "dimension": "PJ",
        "options": _options(
            "Tartibli, aniq va yakunlovchi odam sifatida",
            "Reja bilan ishlasam, yaxshi natija qilaman",
            "Moslashuvchan va ochiq variantli odam sifatida",
            "Erkin, vaziyatga qarab tez o‘zgaradigan odam sifatida",
            "J",
            "P",
        ),
    },
    {
        "text": "Ish jarayonida nimani yoqtirasiz?",
        "dimension": "PJ",
        "options": _options(
            "Aniq vazifa, muddat va yakuniy natijani",
            "Nima qilish kerakligi oldindan ravshan bo‘lishini",
            "Jarayonda yangi variantlar paydo bo‘lishini",
            "Erkin sinab ko‘rish va yo‘l-yo‘lakay moslashishni",
            "J",
            "P",
        ),
    },
    {
        "text": "Qaror qabul qilish tezligingiz qanday?",
        "dimension": "PJ",
        "options": _options(
            "Tezroq qaror qilib, mavzuni yopishni yoqtiraman",
            "Yetarli ma’lumot bo‘lsa, qarorni cho‘zmayman",
            "Yana variant qolganini tekshirib ko‘raman",
            "Imkon qadar ochiq qoldirib, keyinroq tanlayman",
            "J",
            "P",
        ),
    },
    {
        "text": "Reja o‘zgarsa qanday bo‘ladi?",
        "dimension": "PJ",
        "options": _options(
            "Jiddiy noqulaylik his qilaman",
            "Yangi reja tez aniq bo‘lsa, moslashaman",
            "O‘zgarish qiziq imkoniyat bo‘lishi mumkin",
            "Reja o‘zgarishi meni uncha bezovta qilmaydi",
            "J",
            "P",
        ),
    },
    {
        "text": "Sizga nima ko‘proq yoqadi?",
        "dimension": "PJ",
        "options": _options(
            "Boshlangan ishni yakunlab, xotirjam bo‘lish",
            "Ishlar tartib bilan ketayotganini ko‘rish",
            "Bir nechta imkoniyat ochiq turgani",
            "Spontanlik va yangi yo‘nalishga burilish imkoniyati",
            "J",
            "P",
        ),
    },
]
