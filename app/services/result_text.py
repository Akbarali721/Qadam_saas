def build_result_summary(total_score: int) -> str:
    if total_score >= 80:
        return "Moslik darajasi yuqori"
    if total_score >= 50:
        return "Moslik darajasi o‘rtacha"
    return "Moslik darajasi past"


def build_advice(total_score: int) -> str:
    if total_score >= 80:
        return "Hozirgi uyg‘unlikni saqlang: muntazam suhbat va umumiy rejalarni davom ettiring."
    if total_score >= 50:
        return "Shu haftada bitta odatni mustahkamlang: aniqroq muloqot yoki tinchroq kelishuv."
    return "Har kuni kichik samimiy suhbatdan boshlang va tortishuv uchun sokin qoidalar kelishing."


def _dimension_label_uz(key: str) -> str:
    labels = {
        "communication": "Muloqot",
        "trust": "Ishonch",
        "attention": "E'tibor",
        "emotional_closeness": "Hissiy yaqinlik",
    }
    return labels.get(key, key)


def build_differences_text(dimension_scores: dict[str, int]) -> str:
    lowest_dims = sorted(dimension_scores, key=dimension_scores.get)[:2]
    if not lowest_dims:
        return "Asosiy yo‘nalishlar bo‘yicha ma'lumot tayyor."
    dim_names = ", ".join(_dimension_label_uz(dim) for dim in lowest_dims)
    return (
        f"Asosiy e'tibor berish kerak bo‘lgan yo‘nalishlar: {dim_names}. "
        "Shu mavzularda ochiq va tinch muloqot natijani yaxshilaydi."
    )


def build_zodiac_summary(initiator_zodiac: str | None, partner_zodiac: str | None) -> str:
    if not initiator_zodiac or not partner_zodiac:
        return "Burjlar bo‘yicha ma'lumot to‘liq emas."

    pair_map: dict[tuple[str, str], str] = {
        ("Qo‘y", "Baliq"): "Bir taraf faol, bir taraf sezgir. Muvozanat bo‘lsa yaxshi juftlik bo‘ladi.",
        ("Buzoq", "Qisqichbaqa"): "Barqarorlik va g‘amxo‘rlik uyg‘un keladi, ishonch tez shakllanadi.",
        ("Egizaklar", "Tarozi"): "Muloqot kuchli bo‘ladi, birga zerikish qiyin.",
        ("Arslon", "O‘qotar"): "Ikkalasi ham energiyali. Bir-birini qo‘llasa juda yaxshi natija beradi.",
        ("Sunbula", "Tog‘ echkisi"): "Tartib va mas'uliyat yaqin, uzoq muddatli reja qilish oson.",
    }
    return pair_map.get(
        (initiator_zodiac, partner_zodiac),
        "Burjlar uyg‘unligi o‘rtacha: samimiy muloqot va hurmat har doim asosiy omil.",
    )
