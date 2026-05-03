MBTI_PROFILES: dict[str, dict[str, object]] = {
    "ISTJ": {
        "title": "Mas'uliyatli Tashkilotchi",
        "short_description": "Siz tartib, aniqlik va ishonchlilikni qadrlaydigan odamsiz. Ishni reja bilan bajarish, va'daga sodiq qolish va natijani oxirigacha yetkazish sizga tabiiy keladi.",
        "strengths": [
            "Mas'uliyatli va intizomli",
            "Detallarga e'tiborli",
            "Ishonchli va barqaror",
            "Qoidalarga hurmat bilan qaraydi",
        ],
        "warning": "Ba'zan o'zgarishlarga moslashish qiyin tuyulishi yoki yangi g'oyalarga ehtiyotkor qarashingiz mumkin. Vaziyat talab qilganda moslashuvchanlik ham kuchli tomon bo'lishi mumkin.",
        "suitable_roles": [
            "Hisobchi",
            "Loyiha koordinatori",
            "Administrator",
            "Sifat nazorati mutaxassisi",
        ],
        "next_test_cta": "Keyingi qadam: stress darajangizni ham tekshirib ko'ring.",
    },
    "ISFJ": {
        "title": "G'amxo'r Himoyachi",
        "short_description": "Siz odamlarga yordam berish, muhitni tinch saqlash va mas'uliyatni jimgina bajarishga moyilsiz. Siz uchun ishonch, hurmat va amaliy yordam muhim.",
        "strengths": [
            "Mehribon va e'tiborli",
            "Sabrli va yordamga tayyor",
            "Ishni puxta bajaradi",
            "Jamoada iliq muhit yaratadi",
        ],
        "warning": "O'zingizni ko'p berib yuborib, charchoqni kech sezishingiz mumkin. Boshqalarga yordam berish bilan birga o'z ehtiyojlaringizni ham ochiq aytish muhim.",
        "suitable_roles": [
            "O'qituvchi",
            "Hamshira",
            "Mijozlar bilan ishlash mutaxassisi",
            "HR assistent",
        ],
        "next_test_cta": "Keyingi qadam: hissiy charchoqni aniqlash uchun stress testini sinab ko'ring.",
    },
    "INFJ": {
        "title": "Ilhomlantiruvchi Maslahatchi",
        "short_description": "Siz chuqur ma'no, qadriyat va insonlarning ichki holatini tushunishga intilasiz. Ko'pincha uzoq muddatli maqsad va boshqalarga foyda keltirish haqida o'ylaysiz.",
        "strengths": [
            "Kuchli sezgi va empatiya",
            "Mazmunli maqsadga sodiq",
            "Yaxshi tinglovchi",
            "Strategik va ijodiy fikrlaydi",
        ],
        "warning": "Ideal natijani kutish ba'zan bosim keltirishi mumkin. Har doim ham hammani tushunish yoki qutqarish shart emasligini eslatib turish foydali.",
        "suitable_roles": [
            "Psixolog",
            "Kontent strateg",
            "Murabbiy",
            "Ijtimoiy loyiha menejeri",
        ],
        "next_test_cta": "Keyingi qadam: ichki bosimni yaxshiroq tushunish uchun stress testini ko'ring.",
    },
    "INTJ": {
        "title": "Strategik Me'mor",
        "short_description": "Siz tizim, reja va uzoq muddatli natijalarni ko'rishga moyilsiz. Murakkab muammolarni tahlil qilish va yaxshiroq yechim topish sizga yoqadi.",
        "strengths": [
            "Strategik fikrlash",
            "Mustaqil qaror qabul qilish",
            "Murakkab tizimlarni tushunish",
            "Maqsadga qat'iy borish",
        ],
        "warning": "Ba'zan his-tuyg'ular yoki jamoaning kayfiyati ikkinchi darajali ko'rinishi mumkin. Yechim bilan birga muloqot ohangiga ham e'tibor berish natijani kuchaytiradi.",
        "suitable_roles": [
            "Biznes analitik",
            "Dasturchi",
            "Mahsulot strateg",
            "Tadqiqotchi",
        ],
        "next_test_cta": "Keyingi qadam: yuqori maqsadlar bosimini stress testi orqali tekshiring.",
    },
    "ISTP": {
        "title": "Amaliy Usta",
        "short_description": "Siz vaziyatni tez kuzatib, amaliy yechim topishga moyilsiz. Nazariyadan ko'ra tajriba, harakat va real natija sizga yaqinroq.",
        "strengths": [
            "Muammoni tez hal qiladi",
            "Sokin va kuzatuvchan",
            "Amaliy fikrlaydi",
            "Texnik narsalarni tez tushunadi",
        ],
        "warning": "Uzoq reja yoki ko'p tushuntirish talab qilinganda zerikishingiz mumkin. Muhim qarorlar oldidan boshqalarga niyatingizni aniqroq aytish foydali.",
        "suitable_roles": [
            "Muhandis",
            "Texnik mutaxassis",
            "Data analyst",
            "Operatsion muammolar bo'yicha mutaxassis",
        ],
        "next_test_cta": "Keyingi qadam: ish bosimi sizga qanday ta'sir qilishini stress testi bilan ko'ring.",
    },
    "ISFP": {
        "title": "Nozik Didli Yaratuvchi",
        "short_description": "Siz erkinlik, samimiylik va go'zallikni qadrlaysiz. Odamlarga yumshoq munosabatda bo'lish va o'z uslubingiz bilan ijod qilish sizga xos.",
        "strengths": [
            "Ijodiy did",
            "Samimiy va muloyim",
            "Moslashuvchan",
            "Hozirgi lahzani yaxshi his qiladi",
        ],
        "warning": "Nizolar yoki keskin tanqid sizga kuchli ta'sir qilishi mumkin. O'z fikringizni sokin, lekin aniq himoya qilishni mashq qilish foydali.",
        "suitable_roles": [
            "Dizayner",
            "Fotograf",
            "SMM ijodkori",
            "Kosmetolog yoki stilist",
        ],
        "next_test_cta": "Keyingi qadam: hissiy bosimingizni stress testi orqali baholang.",
    },
    "INFP": {
        "title": "Samimiy Orzuchi",
        "short_description": "Siz qadriyat, his va ma'noga katta ahamiyat berasiz. O'zingizga yaqin g'oya topilganda unga chin dildan berilib ketishingiz mumkin.",
        "strengths": [
            "Kuchli tasavvur",
            "Empatiya va samimiyat",
            "Qadriyatlarga sodiqlik",
            "Ijodiy yozish va fikrlash",
        ],
        "warning": "Real muddatlar va amaliy qadamlar e'tibordan chetda qolishi mumkin. Katta orzuni kichik, aniq vazifalarga bo'lish sizga yordam beradi.",
        "suitable_roles": [
            "Yozuvchi",
            "Psixologik yordam mutaxassisi",
            "Kontent yaratuvchi",
            "NNT loyiha xodimi",
        ],
        "next_test_cta": "Keyingi qadam: ichki xavotir darajasini stress testi bilan tekshiring.",
    },
    "INTP": {
        "title": "Mantiqiy Tadqiqotchi",
        "short_description": "Siz g'oyalar, sabablar va tizimlar qanday ishlashini tushunishni yoqtirasiz. Mustaqil fikr, savol berish va chuqur tahlil sizga kuch beradi.",
        "strengths": [
            "Analitik tafakkur",
            "Mustaqil o'rganish",
            "Murakkab g'oyalarni tushunish",
            "Yangi yechimlar topish",
        ],
        "warning": "Fikrni amaliy yakunga yetkazish yoki boshqalarga sodda tushuntirish ba'zan ortga surilishi mumkin. Natijani vaqtida chiqarish uchun chegaralangan reja qo'yish foydali.",
        "suitable_roles": [
            "Dasturchi",
            "Tadqiqotchi",
            "Data scientist",
            "Arxitektor yoki tizim dizayneri",
        ],
        "next_test_cta": "Keyingi qadam: aqliy charchoqni stress testi bilan baholang.",
    },
    "ESTP": {
        "title": "Faol Tadbirkor",
        "short_description": "Siz tez harakat qilish, odamlar bilan aloqa o'rnatish va imkoniyatni joyida ko'rishga moyilsiz. Real vaziyatlarda o'zingizni yaxshi ko'rsatasiz.",
        "strengths": [
            "Jasorat va tashabbus",
            "Tez moslashish",
            "Kuchli muloqot",
            "Amaliy qaror qabul qilish",
        ],
        "warning": "Shoshilinch qarorlar ba'zan uzoq muddatli oqibatlarni e'tibordan qoldirishi mumkin. Katta qadamlar oldidan qisqa pauza va hisob-kitob foydali.",
        "suitable_roles": [
            "Sotuv menejeri",
            "Tadbirkor",
            "Event menejer",
            "Biznes rivojlantirish mutaxassisi",
        ],
        "next_test_cta": "Keyingi qadam: tez temp sizni charchatyaptimi, stress testi bilan bilib oling.",
    },
    "ESFP": {
        "title": "Quvnoq Ilhom Beruvchi",
        "short_description": "Siz odamlar bilan tez yaqinlashadigan, muhitga energiya olib kiradigan va hayotni jonli his qiladigan odamsiz. Amaliy tajriba va ijobiy aloqa sizga muhim.",
        "strengths": [
            "Ochiqko'ngil va iliq",
            "Jamoani ruhlantiradi",
            "Moslashuvchan",
            "Hozirgi imkoniyatni ko'ra oladi",
        ],
        "warning": "Uzoq muddatli reja yoki zerikarli majburiyatlarni ortga surish ehtimoli bor. Erkinlikni saqlagan holda kichik tartib yaratish natijani yaxshilaydi.",
        "suitable_roles": [
            "Boshlovchi",
            "Sotuv yoki servis mutaxassisi",
            "SMM mutaxassisi",
            "Turizm bo'yicha maslahatchi",
        ],
        "next_test_cta": "Keyingi qadam: kundalik ritmingiz stressga qanday ta'sir qilishini tekshiring.",
    },
    "ENFP": {
        "title": "G'oyaparast Motivator",
        "short_description": "Siz yangi g'oyalar, odamlar va imkoniyatlardan ilhom olasiz. Boshqalarga motivatsiya berish va noodatiy yo'l topish sizga tabiiy.",
        "strengths": [
            "Kreativ va qiziquvchan",
            "Odamlarni ruhlantiradi",
            "Yangi imkoniyatlarni ko'radi",
            "Tez aloqa o'rnatadi",
        ],
        "warning": "Ko'p g'oya ichida bitta yo'nalishni oxirigacha olib borish qiyin bo'lishi mumkin. Eng muhim 1-2 maqsadni tanlash energiyangizni kuchaytiradi.",
        "suitable_roles": [
            "Marketing mutaxassisi",
            "Kontent kreator",
            "Trener",
            "Startap asoschisi",
        ],
        "next_test_cta": "Keyingi qadam: ko'p g'oya va ish bosimini stress testi bilan baholang.",
    },
    "ENTP": {
        "title": "Topqir Bahschi",
        "short_description": "Siz fikr almashish, yangi yechim topish va mavjud qoidalarni savol ostiga qo'yishni yoqtirasiz. Murakkab vaziyatlarda tez fikrlaysiz.",
        "strengths": [
            "Topqirlik",
            "Innovatsion fikrlash",
            "Kuchli bahslashish qobiliyati",
            "Muammoga turli tomondan qarash",
        ],
        "warning": "Bahs jarayonida boshqalarning hissiy chegaralarini sezmay qolishingiz mumkin. G'oyani himoya qilish bilan birga tinglash ham ishonch yaratadi.",
        "suitable_roles": [
            "Tadbirkor",
            "Mahsulot menejeri",
            "Kreativ strateg",
            "Huquq yoki muzokara mutaxassisi",
        ],
        "next_test_cta": "Keyingi qadam: yuqori dinamika stressga aylanyaptimi, tekshirib ko'ring.",
    },
    "ESTJ": {
        "title": "Qat'iyatli Boshqaruvchi",
        "short_description": "Siz tartib, natija va mas'uliyatni qadrlaysiz. Jamoani tashkil qilish, vazifani taqsimlash va ishni yakunlash sizga yaxshi chiqadi.",
        "strengths": [
            "Tashkilotchilik",
            "Aniq qaror qabul qilish",
            "Mas'uliyat va qat'iyat",
            "Natijaga yo'nalganlik",
        ],
        "warning": "Ba'zan boshqalarning tempini yoki his-tuyg'usini yetarlicha hisobga olmaslik mumkin. Talabchanlikni tushuntirish va qo'llab-quvvatlash bilan muvozanatlash foydali.",
        "suitable_roles": [
            "Menejer",
            "Operatsion direktor",
            "Administrator",
            "Savdo rahbari",
        ],
        "next_test_cta": "Keyingi qadam: mas'uliyat bosimini stress testi bilan o'lchang.",
    },
    "ESFJ": {
        "title": "Mehribon Tashkilotchi",
        "short_description": "Siz odamlar orasida iliqlik, tartib va hamkorlik yaratishga moyilsiz. Boshqalarning ehtiyojini sezish va amaliy yordam berish sizga xos.",
        "strengths": [
            "Kuchli ijtimoiy sezgirlik",
            "Jamoani birlashtirish",
            "Mas'uliyatli yordam",
            "An'analar va kelishuvlarga hurmat",
        ],
        "warning": "Boshqalarning fikriga ortiqcha bog'lanib qolish yoki rad etilishdan xavotirlanish mumkin. O'z qarashingiz ham muhimligini unutmaslik kerak.",
        "suitable_roles": [
            "HR mutaxassisi",
            "O'qituvchi",
            "Mijozlar tajribasi menejeri",
            "Tadbir tashkilotchisi",
        ],
        "next_test_cta": "Keyingi qadam: boshqalarga ko'p e'tibor berish sizni charchatyaptimi, tekshiring.",
    },
    "ENFJ": {
        "title": "Ilhomlantiruvchi Yetakchi",
        "short_description": "Siz odamlarni tushunish, ularga yo'l ko'rsatish va umumiy maqsad atrofida birlashtirishga moyilsiz. Muloqot va qadriyatlar siz uchun juda muhim.",
        "strengths": [
            "Empatik yetakchilik",
            "Kuchli muloqot",
            "Jamoani ruhlantirish",
            "Odamlarning salohiyatini ko'ra olish",
        ],
        "warning": "Boshqalarning muammosini haddan tashqari o'zingizga olishingiz mumkin. Yordam berish bilan chegaralarni saqlash o'rtasida muvozanat kerak.",
        "suitable_roles": [
            "Murabbiy",
            "HR rahbari",
            "Ta'lim loyihasi menejeri",
            "Kommunikatsiya mutaxassisi",
        ],
        "next_test_cta": "Keyingi qadam: hissiy yuklamangizni stress testi bilan baholang.",
    },
    "ENTJ": {
        "title": "Maqsadli Strateg",
        "short_description": "Siz katta maqsad qo'yish, tizim qurish va odamlarni natijaga yo'naltirishga moyilsiz. Tez qaror, reja va o'sish sizga kuch beradi.",
        "strengths": [
            "Kuchli strategiya",
            "Yetakchilik va tashabbus",
            "Samaradorlikka e'tibor",
            "Qiyin qarorlarni qabul qilish",
        ],
        "warning": "Natijaga shunchalik fokuslanib, odamlarning hissiy holatini chetda qoldirish ehtimoli bor. Kuchli liderlik aniq talab bilan birga empatiyani ham talab qiladi.",
        "suitable_roles": [
            "CEO yoki loyiha rahbari",
            "Biznes strateg",
            "Mahsulot rahbari",
            "Konsultant",
        ],
        "next_test_cta": "Keyingi qadam: yuqori ambitsiya stressga aylanyaptimi, tekshirib ko'ring.",
    },
}


def get_mbti_profile(result_type: str) -> dict[str, object]:
    return MBTI_PROFILES.get(result_type.upper(), MBTI_PROFILES["INFP"])


RICH_MBTI_RESULTS: dict[str, dict[str, object]] = {
    "INFP": {
        "title": "Ichki dunyosi boy inson",
        "subtitle": "Siz tashqi tomondan sokin ko‘rinsangiz ham, ichingizda juda chuqur hislar, orzular va ma'nolar yashaydi.",
        "about": [
            "Siz hayotga faqat vazifa yoki natija sifatida qaramaysiz. Siz uchun har bir ishning ma'nosi, insonlarga ta'siri va qalbingizga qanchalik yaqinligi muhim.",
            "Siz ko‘pincha boshqalar sezmagan nozik hissiyotlarni payqaysiz. Shu sababli odamlarni tushunish, ularni tinglash va samimiy qo‘llab-quvvatlash sizda tabiiy chiqadi.",
            "Agar biror g‘oya sizning qadriyatlaringizga mos kelsa, unga chin dildan berilasiz. Majburlashdan ko‘ra ilhom, erkinlik va ishonch sizni ko‘proq harakatga keltiradi.",
        ],
        "strengths": [
            "Kuchli tasavvur va ijodiy fikrlash",
            "Odamlarning hislarini nozik sezish",
            "Samimiyat va qadriyatlarga sodiqlik",
            "Chuqur tinglash va tushunish qobiliyati",
            "Ma'noli ishga berilib ketish",
        ],
        "weaknesses": [
            "Ba'zan real qadamni boshlashdan oldin juda ko‘p o‘ylab qolishingiz mumkin.",
            "Tanqidni yurakka yaqin olishingiz ehtimoli bor.",
            "Hamma narsani ideal bo‘lishini kutish charchatishi mumkin.",
            "O‘z ehtiyojingizni aytmasdan, ichingizda saqlab yurishingiz mumkin.",
        ],
        "relationship": [
            "Munosabatda sizga samimiyat, chuqur suhbat va ruhiy yaqinlik juda muhim. Yuzaki e'tibor emas, chin dildan tushunilish sizni baxtli qiladi.",
            "Sizga hislaringizni hurmat qiladigan, sizni shoshirmaydigan va orzularingizni masxara qilmaydigan inson mos keladi.",
            "Siz sevgan insoningizni ilhomlantira olasiz, lekin munosabatda o‘zingizni ham unutmaslik muhim.",
        ],
        "career": [
            "Sizga ma'noli, ijodiy va insonlarga foyda beradigan ish muhiti mos keladi.",
            "Qattiq nazorat, sovuq muhit va faqat raqamga qaratilgan ishlar sizni tez charchatishi mumkin.",
            "Yozish, kontent yaratish, psixologiya, ta'lim, dizayn yoki ijtimoiy loyihalar sizning kuchli tomonlaringizni ochadi.",
        ],
        "advice": [
            "Katta orzularingizni kichik, aniq vazifalarga bo‘ling.",
            "Tanqidni shaxsiy rad etilish deb emas, o‘sish uchun signal deb ko‘rishga harakat qiling.",
            "O‘z hislaringizni ichingizda saqlamay, ishonchli odamga sokin tarzda ayting.",
        ],
    },
    "INFJ": {
        "title": "Insonlarni chuqur tushunadigan yo‘l ko‘rsatuvchi",
        "subtitle": "Siz odamlarning ichki holatini sezadigan, uzoqni ko‘ra oladigan va ma'noli hayot qurishga intiladigan insonsiz.",
        "about": [
            "Siz ko‘pincha vaziyatning yuzasiga emas, uning ortidagi sabab va ma'noga qaraysiz. Odam nima deyayotganidan tashqari, nimani his qilayotganini ham sezishingiz mumkin.",
            "Siz uchun oddiy muvaffaqiyatdan ko‘ra foydali bo‘lish, kimningdir hayotiga yaxshi ta'sir qilish va o‘z yo‘lingizni topish muhim.",
            "Siz sokin ko‘rinsangiz ham, ichingizda kuchli qarashlar va aniq yo‘nalish bor. Ishongan narsangiz uchun uzoq vaqt sabr bilan harakat qila olasiz.",
        ],
        "strengths": [
            "Kuchli sezgi va empatiya",
            "Uzoq muddatli fikrlash",
            "Odamlarni ilhomlantirish",
            "Sabr va ichki qat'iyat",
            "Murakkab hislarni tushuntira olish",
        ],
        "weaknesses": [
            "Hamma narsani mukammal qilishga urinib, o‘zingizga bosim berishingiz mumkin.",
            "Boshqalarning muammosini o‘zingizniki kabi ko‘tarib yurishingiz ehtimoli bor.",
            "Ichingizdagi fikrlarni vaqtida aytmasangiz, charchoq yig‘ilishi mumkin.",
            "Sizni tushunmagan muhitda tez yopilib qolishingiz mumkin.",
        ],
        "relationship": [
            "Munosabatda sizga ishonch, ruhiy yaqinlik va bir-birini o‘stirish muhim. Siz sherigingiz bilan faqat vaqt o‘tkazishni emas, birga ma'no yaratishni xohlaysiz.",
            "Sizga halol, hissiy jihatdan yetuk va ichki dunyoingizga hurmat bilan qaraydigan partner mos keladi.",
            "Siz ko‘p narsani sezganingiz uchun hamma narsani taxmin qilishga urinmasdan, ochiq suhbat qilish munosabatni mustahkamlaydi.",
        ],
        "career": [
            "Sizga odamlar, g‘oyalar va maqsad birlashadigan ishlar mos keladi.",
            "Maslahat berish, ta'lim, psixologiya, strategiya, kontent yoki ijtimoiy loyihalarda o‘zingizni kuchli his qilishingiz mumkin.",
            "Siz uchun ish joyida qadriyatlar, hurmat va uzoq muddatli maqsad bo‘lishi juda muhim.",
        ],
        "advice": [
            "Har doim ham hammani tushunish va qutqarish sizning vazifangiz emasligini eslang.",
            "Ichingizdagi fikrni juda kech aytmasdan, vaqtida va yumshoq ifodalang.",
            "Dam olishni ham rejangizning muhim qismi sifatida qabul qiling.",
        ],
    },
    "ENFP": {
        "title": "G‘oyalar va imkoniyatlardan ilhom oladigan inson",
        "subtitle": "Siz odamlar, yangi fikrlar va kelajakdagi imkoniyatlardan kuch oladigan yorqin energiyali shaxssiz.",
        "about": [
            "Siz bir joyda turib qolishni yoqtirmaysiz. Yangi g‘oya, yangi odam yoki yangi loyiha sizda tezda qiziqish uyg‘otadi.",
            "Siz boshqalarga motivatsiya bera olasiz, chunki odamlardagi yashirin imkoniyatni tez ko‘rasiz. Siz bilan suhbatdan keyin ko‘pchilik o‘ziga ishonchi ortganini sezadi.",
            "Siz uchun erkinlik juda muhim. O‘zingiz ishongan maqsad bo‘lsa, juda katta energiya bilan harakat qilasiz.",
        ],
        "strengths": [
            "Kreativ va noodatiy fikrlash",
            "Odamlarni tez ruhlantirish",
            "Yangi imkoniyatlarni ko‘rish",
            "Samimiy va ochiq muloqot",
            "Moslashuvchanlik va jasorat",
        ],
        "weaknesses": [
            "Ko‘p g‘oya orasida bitta yo‘nalishni oxirigacha olib borish qiyin bo‘lishi mumkin.",
            "Zerikarli tartib yoki takroriy ishlar sizni tez charchatadi.",
            "Ba'zan qarorni his bilan tez qabul qilib, keyin reja yetishmasligi mumkin.",
            "Hamma narsaga ulgurishga urinish energiyangizni bo‘lib yuboradi.",
        ],
        "relationship": [
            "Munosabatda sizga jonli suhbat, kulgi, yangilik va hissiy ochiqlik kerak. Siz sherigingiz bilan birga o‘sishni va hayotni qiziqroq qilishni xohlaysiz.",
            "Sizga sizni cheklamaydigan, lekin kerak paytda yo‘nalish va barqarorlik bera oladigan partner mos keladi.",
            "Hislaringiz tez o‘zgarishi mumkin, shuning uchun muhim mavzularda va'dani aniqroq qilish foydali.",
        ],
        "career": [
            "Sizga ijodiy erkinlik, odamlar bilan aloqa va yangi g‘oyalar bor muhit mos keladi.",
            "Marketing, media, trening, kontent, startap, savdo yoki kreativ strategiya kabi yo‘nalishlarda kuchli ochilasiz.",
            "Siz uchun ish faqat maosh emas, ilhom va o‘sish manbai ham bo‘lishi kerak.",
        ],
        "advice": [
            "Har oy eng muhim 1-2 maqsadni tanlab, energiyangizni shu yoqqa yo‘naltiring.",
            "G‘oyani boshlashdan oldin kichik yakun muddatini belgilang.",
            "Sizni ruhlantiradigan odamlar bilan ko‘proq, kuchingizni so‘radigan muhit bilan kamroq vaqt o‘tkazing.",
        ],
    },
    "INTJ": {
        "title": "Aniq maqsadli strateg",
        "subtitle": "Siz vaziyatga chuqur qaraydigan, reja tuzadigan va kelajakdagi natijani oldindan ko‘ra oladigan insonsiz.",
        "about": [
            "Siz uchun hamma narsa mantiqiy tizimga ega bo‘lishi kerak. Vaqt, energiya va resurs bekorga ketayotganini ko‘rsangiz, uni yaxshilash yo‘lini izlaysiz.",
            "Siz boshqalardan ko‘p maslahat kutmasdan, o‘zingiz tahlil qilib qaror qabul qilishga moyilsiz. Mustaqillik va aqliy erkinlik siz uchun juda muhim.",
            "Sizning kuchingiz shundaki, ko‘pchilik hozirgi muammo bilan band bo‘lganda, siz uning keyingi bosqichini ham ko‘ra olasiz.",
        ],
        "strengths": [
            "Strategik va uzoqni ko‘ra olish",
            "Murakkab muammolarni tahlil qilish",
            "Mustaqil qaror qabul qilish",
            "Maqsadga qat'iy intilish",
            "Samaradorlikni oshirish qobiliyati",
        ],
        "weaknesses": [
            "Ba'zan his-tuyg‘ularni ikkinchi darajali deb ko‘rishingiz mumkin.",
            "Natija sekin bo‘lsa yoki odamlar noaniq gapirsa, sabringiz kamayishi mumkin.",
            "Hamma narsani o‘zingiz nazorat qilishga urinish charchatadi.",
            "Fikringiz juda aniq bo‘lgani uchun uni yumshoqroq tushuntirish kerak bo‘lishi mumkin.",
        ],
        "relationship": [
            "Munosabatda sizga ishonch, hurmat va aqliy moslik muhim. Siz yuzaki e'tibordan ko‘ra, sherigingizning fikrlashi va qadriyatlariga qaraysiz.",
            "Sizga mustaqil, halol, o‘sishga intiladigan va shaxsiy hududingizni hurmat qiladigan partner mos keladi.",
            "Hislaringizni faqat amallar bilan emas, ba'zan so‘z bilan ham ifodalash munosabatni iliqroq qiladi.",
        ],
        "career": [
            "Sizga mustaqil fikr, murakkab vazifa va aniq maqsad bor ish muhiti mos keladi.",
            "Strategiya, IT, mahsulot, analitika, tadqiqot, biznes rivojlantirish kabi yo‘nalishlarda kuchli bo‘lishingiz mumkin.",
            "Siz uchun eng yaxshi muhit: malakali odamlar, kam shovqin, aniq mas'uliyat va o‘sish imkoniyati bor joy.",
        ],
        "advice": [
            "Yaxshi g‘oyani odamlar qabul qilishi uchun uni sodda va iliqroq tushuntiring.",
            "Har bir narsani o‘zingiz ko‘tarishga urinmay, ishonchli odamlarga vazifa bering.",
            "Natija bilan birga jarayondagi insoniy munosabatni ham qadrlashga harakat qiling.",
        ],
    },
}


def generate_mbti_result(mbti_type: str) -> dict[str, object]:
    normalized_type = mbti_type.upper()
    rich_result = RICH_MBTI_RESULTS.get(normalized_type)
    if rich_result is not None:
        return rich_result

    profile = get_mbti_profile(normalized_type)
    title = str(profile.get("title", "O‘ziga xos shaxsiyat"))
    short_description = str(
        profile.get(
            "short_description",
            "Sizda o‘zingizga xos kuchli tomonlar va qaror qabul qilish uslubi bor.",
        ),
    )
    strengths = [str(item) for item in profile.get("strengths", [])][:5]
    suitable_roles = [str(item) for item in profile.get("suitable_roles", [])][:5]

    return {
        "title": title,
        "subtitle": "Sizning natijangiz fikrlash tarzingiz, munosabatdagi uslubingiz va ishdagi tabiiy kuchlaringiz haqida qisqa tasavvur beradi.",
        "about": [
            short_description,
            "Sizning javoblaringiz shuni ko‘rsatadiki, siz muhim qarorlarda o‘zingizga xos ichki mezonlarga tayanasiz.",
            "Bu tavsif sizni to‘liq cheklab qo‘ymaydi, balki o‘zingizni yaxshiroq tushunish uchun boshlang‘ich yo‘l xaritasi bo‘lib xizmat qiladi.",
        ],
        "strengths": strengths
        or [
            "O‘zingizga xos fikrlash uslubi",
            "Vaziyatga moslashish qobiliyati",
            "Muhim narsalarni sezish",
        ],
        "weaknesses": [
            "Ba'zan kuchli tomonlaringiz haddan tashqari ishlatilganda charchoq paydo bo‘lishi mumkin.",
            "Muhim qarorlarda o‘zingizga vaqt berish foydali.",
            "Odamlarga fikringizni aniqroq tushuntirish ba'zi vaziyatlarda yordam beradi.",
        ],
        "relationship": [
            "Munosabatda sizga hurmat, ishonch va tabiiy muloqot muhim.",
            "Sizga sizni qanday bo‘lsangiz shunday qabul qiladigan, lekin o‘sishga ham undaydigan inson mos keladi.",
        ],
        "career": [
            "Sizga kuchli tomonlaringizni ishlata oladigan va shaxsiy uslubingizga joy beradigan muhit mos keladi.",
            "Mos yo‘nalishlar: " + ", ".join(suitable_roles) if suitable_roles else "Mos yo‘nalishlarni tanlashda qiziqishlaringiz va kuchli tomonlaringizni birga hisobga oling.",
        ],
        "advice": [
            "Natijangizdagi kuchli tomonlardan birini bugunoq amalda ishlatib ko‘ring.",
            "Sizni charchatadigan vaziyatlarni yozib boring va ularga chegaralar qo‘ying.",
            "O‘zingizga mos ish va munosabat muhitini tanlashda ichki ehtiyojlaringizni ham hisobga oling.",
        ],
    }
