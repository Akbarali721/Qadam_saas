/* Auto-synced from app/services/love_dimension_insights.py */
(function () {
  const DATA = {"order": ["communication", "trust", "attention", "emotional_closeness"], "labels": {"communication": "Muloqot", "trust": "Ishonch", "attention": "E’tibor", "emotional_closeness": "Hissiy yaqinlik"}, "statusLabels": {"high": "Kuchli tomon", "mid": "E’tibor kerak", "low": "Zaif nuqta"}, "insights": {"communication": {"high": {"explanation": "Sizlarda muloqot yaxshi yo‘lga qo‘yilgan. Bir-biringizni eshitish va fikr almashish imkoniyati bor. Bu munosabatdagi tushunmovchiliklarni yumshatadigan kuchli omil.", "recommendation": "Muhim mavzularni bahsga aylantirmasdan, “men shunday his qildim” uslubida gapirishni davom ettiring."}, "mid": {"explanation": "Muloqot bor, lekin ayrim mavzularda fikrlar ichda qolib ketishi mumkin. Bu vaqt o‘tishi bilan kichik tushunmovchiliklarni kattalashtirishi mumkin.", "recommendation": "Haftada bir marta tinch vaqtda bir-biringizga “Menga nima yetishmayapti?” degan savolni muloyim tarzda bering."}, "low": {"explanation": "Muloqotda masofa sezilishi mumkin. Gaplashish o‘rniga sukut, taxmin qilish yoki xafa bo‘lib yurish holatlari ko‘paygan bo‘lishi ehtimol.", "recommendation": "Avval ayblashdan emas, oddiy savoldan boshlang: “Seni yaxshiroq tushunishim uchun nimani bilishim kerak?”"}}, "trust": {"high": {"explanation": "Ishonch darajasi yaxshi. Bu munosabatda xavfsizlik, tayanch va xotirjamlik hissi borligini ko‘rsatadi.", "recommendation": "Ishonchni saqlash uchun va’dalarni mayda bo‘lsa ham bajarishga harakat qiling. Munosabatda ishonch katta gaplardan emas, doimiy kichik harakatlardan kuchayadi."}, "mid": {"explanation": "Ishonch bor, lekin ayrim holatlarda shubha yoki ichki xavotir paydo bo‘lishi mumkin. Bu odatda ochiq gaplashilmagan mavzular bilan bog‘liq bo‘ladi.", "recommendation": "Noaniq vaziyatlarda taxmin qilish o‘rniga muloyim savol bering: “Men buni to‘g‘ri tushundimmi?”"}, "low": {"explanation": "Ishonch yo‘nalishida ehtiyotkorlik kerak. Munosabatda shubha, xafa bo‘lish yoki xavfsizlik hissining kamayishi sezilishi mumkin.", "recommendation": "Avval ishonchni buzayotgan aniq holatlarni aniqlang. Umumiy ayblovlardan ko‘ra, aniq vaziyat haqida gaplashish foydaliroq."}}, "attention": {"high": {"explanation": "Bir-biringizga vaqt va diqqat ajratish yaxshi ko‘rinadi. Bu munosabatda qadrlanish hissini kuchaytiradi.", "recommendation": "Katta sovg‘alardan ko‘ra, kundalik kichik e’tiborlarni saqlang: xabar yozish, hol so‘rash, tinglash, minnatdorchilik bildirish."}, "mid": {"explanation": "E’tibor bor, lekin ba’zan yetarli sezilmasligi mumkin. Bir tomon mehr ko‘rsatyapman deb o‘ylashi, ikkinchi tomon esa buni yetarli his qilmasligi mumkin.", "recommendation": "Bir-biringizdan “Sen e’tiborni qanday his qilasan?” deb so‘rab ko‘ring. Har kim mehrni har xil qabul qiladi."}, "low": {"explanation": "E’tibor yo‘nalishida bo‘shliq sezilishi mumkin. Bu munosabatda yolg‘izlik, qadrlanmayotgandek his qilish yoki sovuqlik paydo qilishi mumkin.", "recommendation": "Har kuni kichik bo‘lsa ham bitta e’tibor belgisi qoldiring: qisqa xabar, samimiy savol yoki oddiy rahmat."}}, "emotional_closeness": {"high": {"explanation": "Hissiy yaqinlik yaxshi. Sizlarda iliqlik, samimiylik va bir-biringizga ichki yaqinlik borligi seziladi.", "recommendation": "Bu yaqinlikni saqlash uchun faqat muammolar haqida emas, orzular, qo‘rquvlar va xursand qilgan narsalar haqida ham gaplashing."}, "mid": {"explanation": "Hissiy yaqinlik bor, lekin ba’zi paytlarda masofa sezilishi mumkin. Bu ko‘pincha charchoq, bandlik yoki ochiq aytilmagan hislar bilan bog‘liq bo‘ladi.", "recommendation": "“Bugun seni nima charchatdi?” yoki “Men senga qanday yordam bera olaman?” kabi savollar yaqinlikni kuchaytiradi."}, "low": {"explanation": "Hissiy yaqinlikda sovuqlik yoki masofa sezilishi mumkin. Bu munosabatda ichki ehtiyojlar aytilmay qolayotganidan darak berishi ehtimol.", "recommendation": "Bir-biringizni tuzatishga shoshilmang. Avval tinglash va tushunishga harakat qiling."}}}, "differencesHasGaps": {"subtext": "Sizlarda umumiy moslik yaxshi, lekin ayrim hislar yoki fikrlar to‘liq aytilmay qolayotgan bo‘lishi mumkin. Agar bu mavzular tinch va ochiq muhokama qilinsa, munosabat yanada mustahkamlanadi.", "recommendation": "Suhbatni “Sen bunday qilding” deb emas, “Men ba’zan shunday his qilaman” deb boshlash yaxshiroq natija beradi."}, "differencesNoGaps": "Natijada keskin tafovutlar ko‘rinmadi. Bu munosabatda umumiy moslik va tushunish yaxshi shakllanganini bildiradi. Shunday bo‘lsa ham, ochiq muloqot va doimiy e’tibor munosabatni yanada mustahkamlaydi."};

  function scoreTier(score) {
    const n = Number(score);
    if (Number.isNaN(n)) return "low";
    if (n >= 80) return "high";
    if (n >= 50) return "mid";
    return "low";
  }

  function dimensionLabel(key) {
    return DATA.labels[key] || key;
  }

  function formatDimensionList(names) {
    if (!names.length) return "";
    if (names.length === 1) return names[0];
    if (names.length === 2) return `${names[0]} va ${names[1]}`;
    return `${names.slice(0, -1).join(", ")} va ${names[names.length - 1]}`;
  }

  function getDimensionInsight(dimensionKey, score) {
    const tier = scoreTier(score);
    const dimCopy = DATA.insights[dimensionKey] || DATA.insights.communication;
    const tierCopy = dimCopy[tier] || dimCopy.low;
    return {
      dimension: dimensionKey,
      label: dimensionLabel(dimensionKey),
      score,
      tier,
      statusLabel: DATA.statusLabels[tier],
      explanation: tierCopy.explanation,
      recommendation: tierCopy.recommendation,
    };
  }

  function buildDifferencesContent(dimensionScores) {
    const weakNames = DATA.order
      .filter((dim) => (dimensionScores[dim] ?? 0) < 80)
      .map((dim) => dimensionLabel(dim));
    if (weakNames.length) {
      const namesText = formatDimensionList(weakNames);
      return {
        hasGaps: true,
        text:
          `Natijada ${namesText} yo‘nalishlarida biroz farq seziladi. Bu yomon belgi emas — aksincha, aynan qaysi mavzularga e’tibor berish kerakligini ko‘rsatadi.`,
        subtext: DATA.differencesHasGaps.subtext,
        recommendation: DATA.differencesHasGaps.recommendation,
      };
    }
    return {
      hasGaps: false,
      text: DATA.differencesNoGaps,
      subtext: "",
      recommendation: "",
    };
  }

  window.LoveDimensionInsights = {
    order: DATA.order,
    scoreTier,
    dimensionLabel,
    getDimensionInsight,
    buildDifferencesContent,
  };
})();
