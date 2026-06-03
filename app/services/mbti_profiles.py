"""MBTI type profiles and helpers for result page and premium PDF."""

from __future__ import annotations

from typing import Any

MBTI_LETTER_META: dict[str, dict[str, str]] = {
    "I": {
        "pair": "I / E",
        "chosen_label": "I — Ichkariga moyil",
        "chosen_text": (
            "Energingiz ko‘pincha ichki fikr, chuqur suhbat va yolg‘iz vaqtdan to‘ladi. "
            "Katta shovqinli muhitdan keyin tinchlik va qayta tiklanish vaqti kerak."
        ),
        "other_label": "E — Tashqariga moyil",
        "other_text": "Odamlar, harakat va jonli muhit orqali tez quvvatlanadi.",
    },
    "E": {
        "pair": "I / E",
        "chosen_label": "E — Tashqariga moyil",
        "chosen_text": (
            "Suhbat, yangi tajriba va jamoa muhiti sizni ruhlantiradi. "
            "Fikrlarni gapirish orqali ularni aniqlashtirish osonroq keladi."
        ),
        "other_label": "I — Ichkariga moyil",
        "other_text": "Ichki dunyo va yolg‘iz vaqt orqali energiya to‘planadi.",
    },
    "N": {
        "pair": "N / S",
        "chosen_label": "N — Intuitiv (imkoniyat)",
        "chosen_text": (
            "Siz tafsilotdan oldin umumiy rasm, ma'no va kelajakdagi imkoniyatni ko‘rasiz. "
            "G‘oya, tizim va «nima bo‘lishi mumkin» savollari sizga yaqin."
        ),
        "other_label": "S — Sensorik (fakt)",
        "other_text": "Hozirgi fakt, tajriba va aniq detallarga tayangan holda qaraydi.",
    },
    "S": {
        "pair": "N / S",
        "chosen_label": "S — Sensorik (fakt)",
        "chosen_text": (
            "Siz amaliy tajriba, aniq ma'lumot va hozirgi vaziyatga tayanasiz. "
            "Ishonchli faktlar va tekshirilgan qadamlar siz uchun muhim."
        ),
        "other_label": "N — Intuitiv (imkoniyat)",
        "other_text": "Kelajakdagi imkoniyat va umumiy rasmga ko‘proq e'tibor beradi.",
    },
    "T": {
        "pair": "T / F",
        "chosen_label": "T — Mantiqiy",
        "chosen_text": (
            "Qarorlarda adolat, mantiq va obyektiv mezonlar ustun keladi. "
            "Muammoni tahlil qilib, eng samarali yechimni izlash odatiy."
        ),
        "other_label": "F — Hissiy",
        "other_text": "Insonlar hissi, munosabat va qadriyatlarni ko‘proq hisobga oladi.",
    },
    "F": {
        "pair": "T / F",
        "chosen_label": "F — Hissiy",
        "chosen_text": (
            "Siz odamlarning his-tuyg‘ulari, munosabat ohangi va qadriyatlarini sezasiz. "
            "Qarorda hamma uchun adolatli va insonparvar yechim muhim."
        ),
        "other_label": "T — Mantiqiy",
        "other_text": "Mantiq, qoida va samaradorlikka ko‘proq tayangan holda qaror qiladi.",
    },
    "J": {
        "pair": "J / P",
        "chosen_label": "J — Rejali",
        "chosen_text": (
            "Reja, tartib va aniq muddat sizga xotirjamlik beradi. "
            "Ishni yakunlash va ro‘yxat bo‘yicha borish tabiiy keladi."
        ),
        "other_label": "P — Moslashuvchan",
        "other_text": "Variantlarni ochiq qoldirish va vaziyatga moslashishni afzal ko‘radi.",
    },
    "P": {
        "pair": "J / P",
        "chosen_label": "P — Moslashuvchan",
        "chosen_text": (
            "Siz yangi ma'lumot kelganda rejani moslashtira olasiz. "
            "Erkinlik, tanlov va ochiq variantlar sizni charchatmaydi, balki rag‘batlantiradi."
        ),
        "other_label": "J — Rejali",
        "other_text": "Oldindan reja tuzish va ishni vaqtida yakunlashni qadrlaydi.",
    },
}

MBTI_PROFILES: dict[str, dict[str, Any]] = {
    "INTJ": {
        "code": "INTJ",
        "title_uz": "Strategik fikrlovchi",
        "short_description": (
            "Siz uzoq muddatli maqsadni ko‘ra oladigan, tizimli fikrlaydigan va mustaqil "
            "qaror qabul qiladigan odamsiz. Murakkab muammolarni tahlil qilib, samarali yo‘l topish sizga tabiiy."
        ),
        "strengths": [
            "Strategik va uzoqni ko‘ra olish",
            "Mustaqil va mantiqiy qarorlar",
            "Murakkab tizimlarni tez tushunish",
            "Maqsadga qat'iy intilish",
        ],
        "weaknesses": [
            "His-tuyg‘ularni ba'zan e'tiborsiz qoldirish",
            "Natija sekin bo‘lsa sabrni yo‘qotish",
            "Hamma narsani o‘zingiz nazorat qilishga urinish",
        ],
        "work_style": (
            "Ishda sizga aniq maqsad, mustaqil fikr va murakkab vazifalar mos keladi. "
            "Samarasiz yig‘ilishlar va noaniq vazifalar energiyangizni tez tugatadi. "
            "Strategiya, IT, analitika yoki mahsulot yo‘nalishlarida kuchli ochilasiz."
        ),
        "relationship_style": (
            "Munosabatda sizga ishonch, hurmat va aqliy moslik muhim. "
            "Yuzaki e'tibordan ko‘ra sherigingizning qadriyatlari va fikrlashi siz uchun asosiy. "
            "Hislaringizni ba'zan so‘z bilan ham ifodalash munosabatni iliqroq qiladi."
        ),
        "mini_advice": [
            "G‘oyani boshqalarga sodda va iliq tushuntiring — bu qabul qilinishni osonlashtiradi.",
            "Har bir vazifani o‘zingiz ko‘tarish o‘rniga ishonchli odamlarga bo‘ling.",
            "Dam olishni ham rejangizning bir qismi deb qabul qiling.",
        ],
    },
    "INTP": {
        "code": "INTP",
        "title_uz": "Mantiqiy tadqiqotchi",
        "short_description": (
            "Siz g‘oyalar, sabablar va tizimlar qanday ishlashini tushunishni yoqtirasiz. "
            "Mustaqil o‘rganish, savol berish va chuqur tahlil sizga kuch beradi."
        ),
        "strengths": [
            "Kuchli analitik tafakkur",
            "Yangi va noodatiy yechimlar topish",
            "Mustaqil o‘rganish va tahlil",
            "Murakkab g‘oyalarni tushunish",
        ],
        "weaknesses": [
            "Fikrni amalga olib chiqishni kechiktirish",
            "Rutina va takroriy vazifalarda zerikish",
            "His-tuyg‘ularni ifodalashda qiyinchilik",
        ],
        "work_style": (
            "Sizga intellektual erkinlik, vaqt va chuqur tahlil imkoniyati kerak. "
            "Tadqiqot, dasturlash, arxitektura yoki ilmiy yo‘nalishlar sizga mos. "
            "Yakun muddatini aniq belgilash g‘oyani real natijaga aylantiradi."
        ),
        "relationship_style": (
            "Sizga aqliy uyg‘unlik va shaxsiy erkinlik muhim. "
            "Sherigingiz sizni tushunishga va bosim qilmasdan suhbat qurishga tayyor bo‘lishi kerak. "
            "Muhim hislaringizni vaqtida, hatto qisqa ham bo‘lsa, ayting."
        ),
        "mini_advice": [
            "Katta g‘oyani 3 ta kichik, aniq vazifaga bo‘ling.",
            "Muhim qarorni qabul qilishdan oldin bitta odam bilan muhokama qiling.",
            "Kun oxirida bitta amaliy qadam yozib qo‘ying.",
        ],
    },
    "ENTJ": {
        "code": "ENTJ",
        "title_uz": "Maqsadli strateg",
        "short_description": (
            "Siz katta maqsad qo‘yish, tizim qurish va odamlarni natijaga yo‘naltirishga moyilsiz. "
            "Tez qaror, reja va o‘sish sizga tabiiy kuch beradi."
        ),
        "strengths": [
            "Kuchli strategiya va yetakchilik",
            "Tez va aniq qaror qabul qilish",
            "Samaradorlikni oshirish",
            "Qiyin vaziyatlarda mas'uliyat olish",
        ],
        "weaknesses": [
            "Odamlarning hissiy holatini chetda qoldirish",
            "Juda tez temp tufayli charchoq",
            "Boshqalarga juda yuqori talab qo‘yish",
        ],
        "work_style": (
            "Siz loyiha rahbari, strateg yoki biznes rivojlantirish kabi rollarda yaxshi ishlay olasiz. "
            "Aniq maqsad, mas'uliyat zonalari va o‘sish imkoniyati bo‘lgan muhit sizga mos. "
            "Natija bilan birga jamoa kayfiyatiga ham vaqt ajrating."
        ),
        "relationship_style": (
            "Munosabatda sizga hurmat, halollik va birga o‘sish muhim. "
            "Mustaqil, kuchli va maqsadli sherik sizga yaqinroq. "
            "Ba'zan yumshoqroq ohang va tinglash ishonchni mustahkamlaydi."
        ),
        "mini_advice": [
            "Muhim suhbatdan oldin 30 soniya pauza qiling.",
            "Vazifani topshirganda niyat va kutishlarni aniq yozing.",
            "Haftada bir marta jamoa yoki yaqin odam bilan his-tuyg‘ularni muhokama qiling.",
        ],
    },
    "ENTP": {
        "code": "ENTP",
        "title_uz": "Yangilik izlovchi",
        "short_description": (
            "Siz fikr almashish, yangi yechim topish va mavjud qoidalarni savol ostiga qo‘yishni yoqtirasiz. "
            "Murakkab vaziyatlarda tez va ijodiy fikrlaysiz."
        ),
        "strengths": [
            "Innovatsion va tez fikrlash",
            "Muammoga turli tomondan qarash",
            "Kuchli muloqot va bahslashish",
            "Yangi imkoniyatlarni ko‘rish",
        ],
        "weaknesses": [
            "Bahsda boshqalarning chegarasini unutish",
            "Bitta yo‘nalishni oxirigacha olib borishda qiyinchilik",
            "Rutina va batafsil hujjatlar zeriktiradi",
        ],
        "work_style": (
            "Sizga yangi g‘oya, tez o‘zgarish va intellektual chaqirish bor ish mos. "
            "Startap, mahsulot, kreativ strategiya yoki muzokara talab qiladigan rollar sizga yaqin. "
            "Eng yaxshi 1-2 loyihani tanlab, energiyangizni shu yoqqa qaratish foydali."
        ),
        "relationship_style": (
            "Sizga jonli suhbat, intellektual qiziqish va erkinlik kerak. "
            "Sherigingiz sizni bahslashdan qo‘rqmasligi, lekin hurmat chegarasini saqlashi muhim. "
            "Muhim mavzularda tinglash vaqtini ham ataylab ajrating."
        ),
        "mini_advice": [
            "G‘oyani himoya qilishdan oldin raqib emas, hamkor sifatida tinglang.",
            "Har hafta bitta g‘oyani real prototip yoki test qadamiga aylantiring.",
            "Zerikarli, lekin muhim vazifalarni kichik bloklarga bo‘ling.",
        ],
    },
    "INFJ": {
        "code": "INFJ",
        "title_uz": "Tinch idealist",
        "short_description": (
            "Siz chuqur ma'no, qadriyat va insonlarning ichki holatini tushunishga intilasiz. "
            "Ko‘pincha uzoq muddatli maqsad va boshqalarga foyda keltirish haqida o‘ylaysiz."
        ),
        "strengths": [
            "Kuchli sezgi va empatiya",
            "Uzoq muddatli maqsadga sodiq qolish",
            "Yaxshi tinglovchi va maslahatchi",
            "Strategik va mazmunli fikrlash",
        ],
        "weaknesses": [
            "Ideal natijani kutib o‘zingizga bosim berish",
            "Boshqalarning muammosini haddan tashqari o‘zlashtirish",
            "Tushunmagan muhitda tez yopilish",
        ],
        "work_style": (
            "Sizga ma'noli ish, odamlarga yordam va uzoq muddatli maqsad muhim. "
            "Psixologiya, ta'lim, kontent strategiyasi yoki ijtimoiy loyihalar sizning kuchingizni ochadi. "
            "Ish joyida qadriyatlar va hurmat bo‘lmasa, tez charchaysiz."
        ),
        "relationship_style": (
            "Munosabatda ruhiy yaqinlik, ishonch va birga o‘sish siz uchun asosiy. "
            "Siz sherigingiz bilan faqat vaqt o‘tkazishni emas, birga ma'no yaratishni xohlaysiz. "
            "Hammasini taxmin qilish o‘rniga ochiq va sokin suhbat qiling."
        ),
        "mini_advice": [
            "Har doim ham hammani qutqarish sizning vazifangiz emas — chegarani eslang.",
            "Ichingizdagi fikrni kech qoldirmasdan, yumshoq ifodalang.",
            "Dam olishni ham haftalik rejangizga kiriting.",
        ],
    },
    "INFP": {
        "code": "INFP",
        "title_uz": "Samimiy orzuchi",
        "short_description": (
            "Siz qadriyat, his va ma'noga katta ahamiyat berasiz. "
            "O‘zingizga yaqin g‘oya topilganda unga chin dildan berilib ketishingiz mumkin."
        ),
        "strengths": [
            "Kuchli tasavvur va ijodkorlik",
            "Chuqur empatiya va samimiyat",
            "Qadriyatlarga sodiq qolish",
            "Odamlarni nozik tushunish",
        ],
        "weaknesses": [
            "Real qadamni boshlashdan oldin juda ko‘p o‘ylash",
            "Tanqidni yurakka yaqin olish",
            "O‘z ehtiyojini aytmasdan ichida saqlash",
        ],
        "work_style": (
            "Sizga ma'noli, ijodiy va insonlarga foyda beradigan muhit mos. "
            "Qattiq nazorat va faqat raqamga qaratilgan ish sizni tez charchatadi. "
            "Yozish, dizayn, psixologiya yoki ijtimoiy loyihalar kuchli tomonlaringizni ochadi."
        ),
        "relationship_style": (
            "Sizga samimiyat, chuqur suhbat va ruhiy yaqinlik kerak. "
            "Sizni shoshirmaydigan, hislaringizni hurmat qiladigan sherik mos keladi. "
            "Munosabatda o‘zingizni ham unutmaslik — bu barqarorlik uchun muhim."
        ),
        "mini_advice": [
            "Katta orzularni kichik, aniq vazifalarga bo‘ling.",
            "Tanqidni shaxsiy rad etish emas, o‘sish signali deb ko‘ring.",
            "Hislaringizni ishonchli odamga ochiq ayting.",
        ],
    },
    "ENFJ": {
        "code": "ENFJ",
        "title_uz": "Ilhomlantiruvchi yetakchi",
        "short_description": (
            "Siz odamlarni tushunish, ularga yo‘l ko‘rsatish va umumiy maqsad atrofida birlashtirishga moyilsiz. "
            "Muloqot va qadriyatlar siz uchun juda muhim."
        ),
        "strengths": [
            "Empatik yetakchilik",
            "Kuchli muloqot va ilhomlantirish",
            "Jamoani birlashtirish",
            "Odamlarning salohiyatini ko‘rish",
        ],
        "weaknesses": [
            "Boshqalarning muammosini haddan tashqari o‘zlashtirish",
            "Rad etilishdan xavotirlanish",
            "O‘z ehtiyojini ikkinchi reja qilish",
        ],
        "work_style": (
            "Siz murabbiy, HR, ta'lim yoki kommunikatsiya loyihalarida kuchli ishlay olasiz. "
            "Jamoa ruhiyati va umumiy maqsad siz uchun muhim. "
            "Ko‘p odam bilan ishlaganda o‘zingiz uchun ham tiklanish vaqti qoldiring."
        ),
        "relationship_style": (
            "Siz munosabatda g‘amxo‘rlik, ochiq muloqot va bir-birini o‘stirishni qadrlaysiz. "
            "Sherigingiz sizning mehnatingizni ko‘rishi va sizga ham qo‘llab-quvvatlash berishi muhim. "
            "Yordam berish bilan shaxsiy chegarani muvozanatlang."
        ),
        "mini_advice": [
            "«Yo‘q» deyish ham mehribonlikning bir shakli — o‘rganing.",
            "Kun oxirida o‘zingiz uchun 15 daqiqa ajrating.",
            "Kutilmalarni boshqalar o‘ylamasin, aniq ayting.",
        ],
    },
    "ENFP": {
        "code": "ENFP",
        "title_uz": "Ilhomlantiruvchi",
        "short_description": (
            "Siz yangi g‘oyalar, odamlar va imkoniyatlardan ilhom olasiz. "
            "Boshqalarga motivatsiya berish va noodatiy yo‘l topish sizga tabiiy."
        ),
        "strengths": [
            "Kreativ va qiziquvchan fikrlash",
            "Odamlarni tez ruhlantirish",
            "Yangi imkoniyatlarni ko‘rish",
            "Samimiy va ochiq muloqot",
        ],
        "weaknesses": [
            "Ko‘p g‘oya ichida bitta yo‘nalishni tugatish qiyinligi",
            "Zerikarli tartib va takroriy ishlar",
            "Hamma narsaga ulgurishga urinish",
        ],
        "work_style": (
            "Sizga ijodiy erkinlik, odamlar bilan aloqa va yangi g‘oyalar bor muhit mos. "
            "Marketing, media, trening yoki startap kabi yo‘nalishlarda yorqin ochilasiz. "
            "Har oy 1-2 ta asosiy maqsadni tanlash energiyangizni saqlaydi."
        ),
        "relationship_style": (
            "Munosabatda jonli suhbat, kulgi va hissiy ochiqlik sizni baxtli qiladi. "
            "Siz sherigingiz bilan birga o‘sishni va hayotni qiziqroq qilishni xohlaysiz. "
            "Muhim va'dalarni aniqroq qilish ishonchni mustahkamlaydi."
        ),
        "mini_advice": [
            "Eng muhim 1-2 maqsadni tanlab, qolganini ro‘yxatga qo‘ying.",
            "G‘oyani boshlashdan oldin kichik yakun muddatini belgilang.",
            "Sizni charchatadigan muhitdan vaqtincha uzoqlashing.",
        ],
    },
    "ISTJ": {
        "code": "ISTJ",
        "title_uz": "Mas'uliyatli tartibkor",
        "short_description": (
            "Siz tartib, aniqlik va ishonchlilikni qadrlaysiz. "
            "Ishni reja bilan bajarish, va'daga sodiq qolish va natijani oxirigacha yetkazish sizga tabiiy."
        ),
        "strengths": [
            "Mas'uliyatli va intizomli",
            "Detallarga e'tiborli",
            "Ishonchli va barqaror",
            "Qoidalarga hurmat bilan qarash",
        ],
        "weaknesses": [
            "Tez o‘zgarishlarga moslashish qiyinligi",
            "Yangi g‘oyalarga ehtiyotkor yondashish",
            "His-tuyg‘ularni ifodalashda kamchilik",
        ],
        "work_style": (
            "Sizga aniq vazifa, qoidalar va barqaror jarayon mos. "
            "Hisob, loyiha koordinatsiyasi, sifat nazorati kabi rollarda ishonch uyg‘otasiz. "
            "Kutilmagan o‘zgarishlarda qisqa moslashish rejasini oldindan o‘ylab qo‘ying."
        ),
        "relationship_style": (
            "Munosabatda sizga ishonch, sodiq qolish va aniq xatti-harakat muhim. "
            "Siz sevgan insoningizga amal bilan ham, so‘z bilan ham ishonch berasiz. "
            "Ba'zan his-tuyg‘ularni ham ochiq aytish yaqinlikni kuchaytiradi."
        ),
        "mini_advice": [
            "Katta o‘zgarishni kichik qadamlarga bo‘ling.",
            "Muhim hisslaringizni «men xohlayman» deb aniq ayting.",
            "Dam olish ham mas'uliyat — uni rejalashtiring.",
        ],
    },
    "ISFJ": {
        "code": "ISFJ",
        "title_uz": "G'amxo'r himoyachi",
        "short_description": (
            "Siz odamlarga yordam berish, muhitni tinch saqlash va mas'uliyatni jimgina bajarishga moyilsiz. "
            "Ishonch, hurmat va amaliy yordam siz uchun muhim."
        ),
        "strengths": [
            "Mehribon va e'tiborli",
            "Sabrli va yordamga tayyor",
            "Ishni puxta bajarish",
            "Jamoada iliq muhit yaratish",
        ],
        "weaknesses": [
            "O‘zingizni ko‘p berib charchash",
            "Rad etishdan qo‘rqish",
            "O‘z ehtiyojini kech sezish",
        ],
        "work_style": (
            "Siz o‘qituvchilik, tibbiyot, mijozlar bilan ishlash yoki HR kabi sohalarda yaxshi moslashasiz. "
            "Aniq tartib va odamlarga foyda beradigan vazifa sizni ruhlantiradi. "
            "Boshqalarga yordam berish bilan o‘z chegarangizni ham saqlang."
        ),
        "relationship_style": (
            "Siz munosabatda g‘amxo‘rlik, barqarorlik va kundalik e'tiborni ko‘rsatasiz. "
            "Sizga hurmat qiladigan va mehnatingizni qadrlaydigan sherik mos. "
            "O‘z ehtiyojingizni aytsangiz, munosabat yanada sog‘lom bo‘ladi."
        ),
        "mini_advice": [
            "Haftada bir marta «men uchun» vaqt rejalashtiring.",
            "Yordam berishdan oldin «bugun qanchalik qulay?» deb o‘zingizga so‘rang.",
            "Katta yukni bo‘lib, kichik qadamlar bilan bajaring.",
        ],
    },
    "ESTJ": {
        "code": "ESTJ",
        "title_uz": "Qat'iyatli tashkilatchi",
        "short_description": (
            "Siz tartib, natija va mas'uliyatni qadrlaysiz. "
            "Jamoani tashkil qilish, vazifani taqsimlash va ishni yakunlash sizga yaxshi chiqadi."
        ),
        "strengths": [
            "Kuchli tashkilotchilik",
            "Aniq va tez qaror qabul qilish",
            "Mas'uliyat va qat'iyat",
            "Natijaga yo‘naltirilganlik",
        ],
        "weaknesses": [
            "Boshqalarning tempini yetarlicha hisobga olmaslik",
            "Juda qattiq talab qo‘yish",
            "Moslashuvchanlikni kamaytirish",
        ],
        "work_style": (
            "Siz menejer, operatsion rahbar yoki administrator sifatida samarali ishlay olasiz. "
            "Aniq rollar, qoidalar va hisob-kitob sizga mos muhit. "
            "Talabchanlikni tushuntirish va qo‘llab-quvvatlash bilan muvozanatlang."
        ),
        "relationship_style": (
            "Munosabatda sizga halollik, ishonch va aniq kelishuvlar muhim. "
            "Siz sevgan insoningizga barqarorlik va amaliy yordam berasiz. "
            "Ba'zan yumshoqroq ohang va tinglash yaqinlikni oshiradi."
        ),
        "mini_advice": [
            "Muhim suhbatda avval tinglang, keyin xulosa qiling.",
            "Talablaringizni «men xohlayman» emas, «bizga kerak» deb yumshating.",
            "Haftada bir marta faqat dam olish kunini rejalashtiring.",
        ],
    },
    "ESFJ": {
        "code": "ESFJ",
        "title_uz": "Mehribon tashkilotchi",
        "short_description": (
            "Siz odamlar orasida iliqlik, tartib va hamkorlik yaratishga moyilsiz. "
            "Boshqalarning ehtiyojini sezish va amaliy yordam berish sizga xos."
        ),
        "strengths": [
            "Kuchli ijtimoiy sezgirlik",
            "Jamoani birlashtirish",
            "Mas'uliyatli yordam",
            "An'analar va kelishuvlarga hurmat",
        ],
        "weaknesses": [
            "Boshqalarning fikriga ortiqcha bog‘lanish",
            "Rad etilishdan xavotirlanish",
            "O‘z fikrini e'tiborsiz qoldirish",
        ],
        "work_style": (
            "Siz HR, o‘qituvchilik, mijozlar tajribasi yoki tadbir tashkil qilishda kuchli. "
            "Jamoa muhiti va odamlar bilan aloqa sizni rag‘batlantiradi. "
            "O‘z qaroringiz ham muhim — uni vaqtida ifodalang."
        ),
        "relationship_style": (
            "Siz munosabatda g‘amxo‘rlik, e'tibor va kundalik qo‘llab-quvvatlashni ko‘rsatasiz. "
            "Sizga sizni qadrlaydigan va minnatdorchilik bildiradigan sherik mos. "
            "O‘z ehtiyojingizni aytsangiz, munosabat tengroq bo‘ladi."
        ),
        "mini_advice": [
            "Bir marta «bugun o‘zim uchun nima xohlayman?» deb yozing.",
            "Rad etish — munosabatni buzish emas, chegarani saqlash.",
            "Katta yordamni kichik, barqaror qadamlarga bo‘ling.",
        ],
    },
    "ISTP": {
        "code": "ISTP",
        "title_uz": "Amaliy usta",
        "short_description": (
            "Siz vaziyatni tez kuzatib, amaliy yechim topishga moyilsiz. "
            "Nazariyadan ko‘ra tajriba, harakat va real natija sizga yaqinroq."
        ),
        "strengths": [
            "Muammoni tez va amaliy hal qilish",
            "Sokin va kuzatuvchan",
            "Texnik narsalarni tez tushunish",
            "Moslashuvchan va mustaqil",
        ],
        "weaknesses": [
            "Uzoq reja va ko‘p tushuntirishda zerikish",
            "His-tuyg‘ularni kam ifodalash",
            "Qoidaga ortiqcha qarshilik",
        ],
        "work_style": (
            "Siz muhandislik, texnika, operatsion muammolar yoki analitika kabi sohalarda yaxshi ishlay olasiz. "
            "Amaliy vazifa, erkinlik va natijani ko‘rish sizni rag‘batlantiradi. "
            "Muhim qarorlarda niyatingizni qisqa va aniq ayting."
        ),
        "relationship_style": (
            "Munosabatda sizga ishonch, shaxsiy erkinlik va bosimsiz yaqinlik muhim. "
            "Siz sevgan insoningizga amal bilan ham ishonch berasiz. "
            "Ba'zan bir-ikkita samimiy gap munosabatni iliqroq qiladi."
        ),
        "mini_advice": [
            "Muhim hisslaringizni yozib yoki qisqa xabar bilan ayting.",
            "Murakkab vazifani kichik, aniq bosqichlarga bo‘ling.",
            "Zerikarli, lekin kerakli ishlarni vaqt blokiga qo‘ying.",
        ],
    },
    "ISFP": {
        "code": "ISFP",
        "title_uz": "Nozik didli yaratuvchi",
        "short_description": (
            "Siz erkinlik, samimiylik va go‘zallikni qadrlaysiz. "
            "Odamlarga yumshoq munosabatda bo‘lish va o‘z uslubingiz bilan ijod qilish sizga xos."
        ),
        "strengths": [
            "Ijodiy did va estetika",
            "Samimiy va muloyim munosabat",
            "Moslashuvchanlik",
            "Hozirgi lahzani yaxshi his qilish",
        ],
        "weaknesses": [
            "Nizolar va keskin tanqidga sezgirlik",
            "O‘z fikrini himoya qilishda ikkilanish",
            "Uzoq muddatli rejaning kechikishi",
        ],
        "work_style": (
            "Siz dizayn, san'at, fotografiya yoki xizmat ko‘rsatish kabi yo‘nalishlarda yorqin ishlay olasiz. "
            "Erkinlik va shaxsiy uslubga hurmat muhim. "
            "Kichik, aniq muddatlar ijodiy ishni ham yakunlashga yordam beradi."
        ),
        "relationship_style": (
            "Munosabatda sizga yumshoqlik, hurmat va shaxsiy makon muhim. "
            "Sizni bosim qilmasdan, samimiy yaqinlik quradigan sherik mos. "
            "O‘z fikringizni sokin, lekin aniq aytish — bu ham g‘urur."
        ),
        "mini_advice": [
            "Bir kichik loyihani bugun boshlab, yakunlang.",
            "Tanqidni shaxsiy emas, vaziyat haqida deb qabul qiling.",
            "O‘zingiz uchun yoqimli muhit yarating — bu energiyangizni tiklaydi.",
        ],
    },
    "ESTP": {
        "code": "ESTP",
        "title_uz": "Faol harakatkor",
        "short_description": (
            "Siz tez harakat qilish, odamlar bilan aloqa o‘rnatish va imkoniyatni joyida ko‘rishga moyilsiz. "
            "Real vaziyatlarda o‘zingizni yaxshi ko‘rsatasiz."
        ),
        "strengths": [
            "Jasorat va tez harakat",
            "Amaliy qaror qabul qilish",
            "Kuchli muloqot",
            "Vaziyatga tez moslashish",
        ],
        "weaknesses": [
            "Shoshilinch qarorlar",
            "Uzoq reja va batafsil hujjatlar",
            "Qoidaga ortiqcha qarshilik",
        ],
        "work_style": (
            "Siz sotuv, tadbirkorlik, event yoki operatsion rollarda kuchli. "
            "Tez natija, harakat va real vaziyat sizni rag‘batlantiradi. "
            "Katta qarorlardan oldin qisqa pauza va hisob-kitob foydali."
        ),
        "relationship_style": (
            "Munosabatda sizga jonli aloqa, umumiy tajriba va ochiq muloqot kerak. "
            "Siz sherigingiz bilan birga harakat qilganda yaqinlashasiz. "
            "Muhim mavzularda shoshilmasdan gaplashish ishonchni saqlaydi."
        ),
        "mini_advice": [
            "Muhim qarordan oldin «ertaga ham shunday qilamanmi?» deb o‘zingizga so‘rang.",
            "Haftada bir marta tinch, chuqur suhbat vaqti ajrating.",
            "Energiyangizni sport yoki harakat bilan barqarorlashtiring.",
        ],
    },
    "ESFP": {
        "code": "ESFP",
        "title_uz": "Quvnoq ilhom beruvchi",
        "short_description": (
            "Siz odamlar bilan tez yaqinlashadigan, muhitga energiya olib kiradigan va hayotni jonli his qiladigan odamsiz. "
            "Amaliy tajriba va ijobiy aloqa siz uchun muhim."
        ),
        "strengths": [
            "Ochiqko‘ngil va iliq munosabat",
            "Jamoani ruhlantirish",
            "Hozirgi imkoniyatni ko‘rish",
            "Moslashuvchanlik",
        ],
        "weaknesses": [
            "Uzoq muddatli rejani kechiktirish",
            "Zerikarli majburiyatlar",
            "Qiyin tanqidga sezgirlik",
        ],
        "work_style": (
            "Siz boshlovchilik, sotuv, servis yoki media kabi sohalarda yorqin ishlay olasiz. "
            "Odamlar, harakat va ijobiy muhit sizni rag‘batlantiradi. "
            "Kichik tartib (ro‘yxat, muddat) erkinlikni saqlab, natijani yaxshilaydi."
        ),
        "relationship_style": (
            "Munosabatda sizga quvnoqlik, e'tibor va birga yaxshi vaqt o‘tkazish muhim. "
            "Siz sevgan insoningizga iliq va samimiy bo‘lasiz. "
            "Muhim va'dalarni yozib qo‘yish ishonchni mustahkamlaydi."
        ),
        "mini_advice": [
            "Har hafta 3 ta eng muhim vazifani tanlang va ularni birinchi bajaring.",
            "Katta xarajot yoki qarordan oldin bir kech o‘ylab ko‘ring.",
            "Sizni charchatadigan muhitdan qisqa tanaffus oling.",
        ],
    },
}

PREMIUM_TEASER_ITEMS: list[str] = [
    "Chuqur shaxsiy profil",
    "Kasb va o‘qish yo‘nalishi bo‘yicha tahlil",
    "Munosabatdagi moslik va qiyin tomonlar",
    "Sizni charchatadigan muhit va odamlar",
    "7 kunlik rivojlanish rejasi",
    "PDF shaklida shaxsiy hisobot",
]


def get_mbti_profile(result_type: str) -> dict[str, Any] | None:
    return MBTI_PROFILES.get(result_type.upper())


def get_mbti_letter_breakdown(result_type: str) -> list[dict[str, str]]:
    normalized = result_type.upper()
    if len(normalized) != 4:
        return []
    letters: list[dict[str, str]] = []
    for letter in normalized:
        meta = MBTI_LETTER_META.get(letter)
        if meta is None:
            continue
        letters.append(
            {
                "pair": meta["pair"],
                "chosen_label": meta["chosen_label"],
                "chosen_text": meta["chosen_text"],
                "other_label": meta["other_label"],
            },
        )
    return letters


def generate_mbti_result(mbti_type: str) -> dict[str, object]:
    """Build legacy-shaped content dict for PDF and other consumers."""
    profile = get_mbti_profile(mbti_type)
    if profile is None:
        return {
            "title": mbti_type.upper(),
            "subtitle": (
                "Sizning natijangiz tayyor, lekin bu tip uchun batafsil izoh hozircha qo‘shilmagan."
            ),
            "about": [
                "Sizning natijangiz tayyor, lekin bu tip uchun batafsil izoh hozircha qo‘shilmagan.",
            ],
            "strengths": ["O‘zingizga xos fikrlash uslubi"],
            "weaknesses": ["Batafsil tavsif tez orada qo‘shiladi"],
            "relationship": ["Munosabatda hurmat va ochiq muloqot muhim."],
            "career": ["Kuchli tomonlaringizni hisobga olgan holda yo‘nalish tanlang."],
            "advice": ["Natijangizni kuzatib boring — tez orada to‘liq profil qo‘shiladi."],
        }

    return {
        "title": profile["title_uz"],
        "subtitle": profile["short_description"],
        "about": [profile["short_description"]],
        "strengths": list(profile["strengths"]),
        "weaknesses": list(profile["weaknesses"]),
        "relationship": [profile["relationship_style"]],
        "career": [profile["work_style"]],
        "advice": list(profile["mini_advice"]),
    }
