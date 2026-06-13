function setMessage(text) {
  const messageEl = document.getElementById("message");
  if (messageEl) {
    messageEl.textContent = text || "";
  }
}

function setToken(token) {
  return token || "";
}

const INITIATOR_TG_ID_KEY = "initiator_tg_id";
const PARTNER_TG_ID_KEY = "partner_tg_id";
const FLOW_LOG_PREFIX = "[love-flow]";

function flowLog(step, detail) {
  const suffix =
    detail === undefined
      ? ""
      : ` ${typeof detail === "string" ? detail : JSON.stringify(detail)}`;
  console.log(`${FLOW_LOG_PREFIX} ${step}${suffix}`);
}

function normalizeTelegramId(raw) {
  if (raw === undefined || raw === null) {
    return null;
  }
  const trimmed = String(raw).trim();
  return /^\d+$/.test(trimmed) ? trimmed : null;
}

function readTgIdFromUrl() {
  const params = new URLSearchParams(window.location.search);
  return normalizeTelegramId(params.get("tg_id"));
}

function persistPartnerTelegramId(id) {
  const normalized = normalizeTelegramId(id);
  if (!normalized) {
    return null;
  }
  try {
    sessionStorage.setItem(PARTNER_TG_ID_KEY, normalized);
  } catch (_error) {
    // ignore private mode / quota errors
  }
  return normalized;
}

function getPartnerTelegramUserId() {
  const user = window.Telegram?.WebApp?.initDataUnsafe?.user;
  const fromSdk = normalizeTelegramId(user?.id);
  if (fromSdk) {
    return persistPartnerTelegramId(fromSdk);
  }

  try {
    const fromStorage = normalizeTelegramId(
      sessionStorage.getItem(PARTNER_TG_ID_KEY),
    );
    if (fromStorage) {
      return fromStorage;
    }
  } catch (_error) {
    // ignore
  }

  const params = new URLSearchParams(window.location.search);
  const fromUrl = normalizeTelegramId(params.get("partner_tg_id"));
  if (fromUrl) {
    return persistPartnerTelegramId(fromUrl);
  }

  return null;
}

function initTelegramWebApp() {
  const webApp = window.Telegram?.WebApp;
  if (!webApp) {
    flowLog("telegram_webapp_unavailable");
    return;
  }
  try {
    webApp.ready();
    webApp.expand?.();
    flowLog("telegram_webapp_ready", {
      platform: webApp.platform || "unknown",
      version: webApp.version || "unknown",
    });
  } catch (error) {
    flowLog("telegram_webapp_init_failed", error?.message || String(error));
  }
}

function persistInitiatorTelegramId(id) {
  const normalized = normalizeTelegramId(id);
  if (!normalized) {
    return null;
  }
  try {
    sessionStorage.setItem(INITIATOR_TG_ID_KEY, normalized);
  } catch (_error) {
    // ignore private mode / quota errors
  }
  const hidden = document.getElementById("initiator-tg-id");
  if (hidden) {
    hidden.value = normalized;
  }
  return normalized;
}

function getTelegramUserId() {
  const user = window.Telegram?.WebApp?.initDataUnsafe?.user;
  const fromSdk = normalizeTelegramId(user?.id);
  if (fromSdk) {
    return persistInitiatorTelegramId(fromSdk);
  }

  const fromHidden = normalizeTelegramId(
    document.getElementById("initiator-tg-id")?.value,
  );
  if (fromHidden) {
    return persistInitiatorTelegramId(fromHidden);
  }

  try {
    const fromStorage = normalizeTelegramId(
      sessionStorage.getItem(INITIATOR_TG_ID_KEY),
    );
    if (fromStorage) {
      return fromStorage;
    }
  } catch (_error) {
    // ignore
  }

  const fromUrl = readTgIdFromUrl();
  if (fromUrl) {
    return persistInitiatorTelegramId(fromUrl);
  }

  return null;
}

function initIndexTelegramId() {
  const fromUrl = readTgIdFromUrl();
  if (fromUrl) {
    persistInitiatorTelegramId(fromUrl);
    flowLog("initiator_tg_id_from_url", { tgId: fromUrl });
    return;
  }
  const tgId = getTelegramUserId();
  flowLog("initiator_tg_id_resolved", { tgId: tgId || "(missing)" });
}

function dimensionLabel(key) {
  if (window.LoveDimensionInsights) {
    return LoveDimensionInsights.dimensionLabel(key);
  }
  const map = {
    communication: "Muloqot",
    trust: "Ishonch",
    attention: "E’tibor",
    emotional_closeness: "Hissiy yaqinlik",
  };
  return map[key] || key;
}

const DIMENSION_TEASER_ORDER = window.LoveDimensionInsights?.order || [
  "communication",
  "trust",
  "attention",
  "emotional_closeness",
];

let activeQuestionIndex = 0;

/** Qisqa hissiy jumla — umumiy foizga qarab (serverdagi ball hisoblashi o‘zgarmaydi). */
function emotionalSummaryFromOverall(percent) {
  const n = Number(percent);
  if (Number.isNaN(n)) {
    return "Natija hozircha aniqlanmadi, iltimos keyinroq qayta urinib ko‘ring.";
  }
  if (n <= 40) {
    return "Sizlar orasida ayrim muhim tafovutlar bor. Ba’zi savollarda qarashlaringiz sezilarli darajada farq qiladi.";
  }
  if (n <= 60) {
    return "Sizlar orasida yaqinlik bor, lekin ba’zi muhim jihatlarda bir-biringizni to‘liq tushunmaslik seziladi.";
  }
  if (n <= 80) {
    return "Sizlar ko‘p jihatdan bir-biringizga mos kelasiz. Ba’zi kichik tafovutlar bor.";
  }
  return "Sizlar orasida juda yaxshi moslik bor. Bu mustahkam munosabat uchun kuchli asos.";
}

function buildDimensionTeaserCard(dimensionKey, scoreNum) {
  const insight = window.LoveDimensionInsights
    ? LoveDimensionInsights.getDimensionInsight(dimensionKey, scoreNum)
    : {
        label: dimensionLabel(dimensionKey),
        score: scoreNum,
        statusLabel: "—",
        explanation: "",
        recommendation: "",
        tier: "mid",
      };

  const card = document.createElement("article");
  card.className = `teaser-card teaser-card--${insight.tier}`;

  const header = document.createElement("div");
  header.className = "teaser-card__header";

  const title = document.createElement("h3");
  title.className = "teaser-title";
  title.textContent = insight.label;

  const status = document.createElement("span");
  status.className = `teaser-status teaser-status--${insight.tier}`;
  status.textContent = insight.statusLabel;

  header.appendChild(title);
  header.appendChild(status);

  const pct = document.createElement("p");
  pct.className = "teaser-pct";
  pct.textContent = `${Number.isFinite(insight.score) ? insight.score : 0}%`;

  const explanation = document.createElement("p");
  explanation.className = "teaser-explanation";
  explanation.textContent = insight.explanation;

  const recLabel = document.createElement("p");
  recLabel.className = "teaser-rec-label";
  recLabel.textContent = "Tavsiya";

  const recommendation = document.createElement("p");
  recommendation.className = "teaser-recommendation";
  recommendation.textContent = insight.recommendation;

  card.appendChild(header);
  card.appendChild(pct);
  card.appendChild(explanation);
  card.appendChild(recLabel);
  card.appendChild(recommendation);
  return card;
}

function renderDifferencesBlock(dimensionScores) {
  const differencesBlock = document.getElementById("differences-block");
  const differencesText = document.getElementById("differences-text");
  const differencesSubtext = document.getElementById("differences-subtext");
  const differencesRec = document.getElementById("differences-rec");
  if (!differencesBlock || !differencesText) {
    return;
  }

  const content = window.LoveDimensionInsights
    ? LoveDimensionInsights.buildDifferencesContent(dimensionScores)
    : {
        hasGaps: false,
        text: (dimensionScores && "") || "",
        subtext: "",
        recommendation: "",
      };

  if (!content.text) {
    differencesBlock.classList.add("hidden");
    return;
  }

  differencesText.textContent = content.text;
  if (differencesSubtext) {
    if (content.hasGaps && content.subtext) {
      differencesSubtext.textContent = content.subtext;
      differencesSubtext.classList.remove("hidden");
    } else {
      differencesSubtext.textContent = "";
      differencesSubtext.classList.add("hidden");
    }
  }
  if (differencesRec) {
    if (content.hasGaps && content.recommendation) {
      differencesRec.textContent = content.recommendation;
      differencesRec.classList.remove("hidden");
    } else {
      differencesRec.textContent = "";
      differencesRec.classList.add("hidden");
    }
  }
  differencesBlock.classList.remove("hidden");
}

function normalizeDimensionScores(rawScores) {
  const scores = {};
  DIMENSION_TEASER_ORDER.forEach((dimension) => {
    const raw = rawScores ? rawScores[dimension] : 0;
    const value =
      typeof raw === "number" ? raw : Number.parseInt(String(raw), 10);
    scores[dimension] = Number.isFinite(value) ? value : 0;
  });
  return scores;
}

function buildSituationLine(weakDims) {
  if (!weakDims.length) {
    return "Katta ziddiyat ehtimoli past, lekin muntazam suhbatni saqlash muhim.";
  }
  const first = weakDims[0];
  const map = {
    communication:
      "Keskin paytda bir-biringizni to‘liq eshitmaslik yoki gapni ichda olib yurish holatlari yuz berishi mumkin.",
    trust:
      "Noaniq vaziyatlarda shubha va noto‘g‘ri xulosa qilish ehtimoli yuqori bo‘ladi.",
    attention:
      "Band paytlarda e’tibor yetishmasligi sabab mayda ranjishlar yig‘ilib borishi mumkin.",
    emotional_closeness:
      "Hissiy mavzularda yopilish yoki ichki kechinmalarni aytmaslik masofani oshirishi mumkin.",
  };
  return map[first] || map.communication;
}

function buildRecommendations(totalScore, weakDims, strongDims) {
  const recs = [];
  if (weakDims.includes("communication")) {
    recs.push("Har kuni kamida 15 daqiqa telefonlarsiz ochiq suhbat qiling.");
  }
  if (weakDims.includes("trust")) {
    recs.push("Kelishuvlarni oldindan aniq qilib oling va mayda va’dalarni ham bajaring.");
  }
  if (weakDims.includes("attention")) {
    recs.push("Haftasiga bir marta faqat ikkingiz uchun sifatli vaqt ajrating.");
  }
  if (weakDims.includes("emotional_closeness")) {
    recs.push("Hissiyotlarni tanqid qilmasdan tinglash odatini shakllantiring.");
  }
  if (!recs.length) {
    recs.push("Mavjud iliq muhitni saqlash uchun muntazam samimiy suhbatni davom ettiring.");
  }
  if (strongDims.length) {
    recs.push(`Kuchli jihatingiz (${dimensionLabel(strongDims[0])})ni boshqa yo‘nalishlarni yaxshilashda tayanch qiling.`);
  }
  if (totalScore < 50) {
    recs.push("Kichik qadamlar bilan boshlang: bitta odatni 21 kun davomida birga bajaring.");
  }
  return recs.slice(0, 5);
}

function renderFullAnalysis(result) {
  const fullBlock = document.getElementById("full-analysis");
  if (!fullBlock) {
    return;
  }
  if (fullBlock.dataset.staticPremium === "true") {
    return;
  }
  const scores = normalizeDimensionScores(result.dimension_scores || {});
  const weakDims = Object.keys(scores).filter((key) => scores[key] < 40);
  const strongDims = Object.keys(scores).filter((key) => scores[key] > 60);
  const totalScore = Number(result.total_score) || 0;

  const problemEl = document.getElementById("analysis-problem");
  const situationsEl = document.getElementById("analysis-situations");
  const strengthsEl = document.getElementById("analysis-strengths");
  const tipsEl = document.getElementById("analysis-tips");
  const insightEl = document.getElementById("analysis-insight");
  const forecastEl = document.getElementById("analysis-forecast");

  if (problemEl) {
    problemEl.textContent = weakDims.length
      ? `Asosiy bosim ${weakDims.map((d) => dimensionLabel(d)).join(" va ")} yo‘nalishida sezilyapti. Shu nuqtalarda bir-biringizni tushunish qiyinlashadi.`
      : "Keskin muammo ko‘rinmaydi, asosiy vazifa — hozirgi uyg‘unlikni barqaror saqlab qolish.";
  }
  if (situationsEl) {
    situationsEl.textContent = buildSituationLine(weakDims);
  }
  if (strengthsEl) {
    strengthsEl.textContent = strongDims.length
      ? `Sizlarda ${strongDims.map((d) => dimensionLabel(d)).join(", ")} kuchli. Bu munosabatni tiklash va mustahkamlash uchun katta resurs.`
      : "Kuchli tomonlar hali barqaror shakllanmagan, lekin to‘g‘ri yondashuv bilan tez o‘sish mumkin.";
  }
  if (tipsEl) {
    tipsEl.innerHTML = "";
    buildRecommendations(totalScore, weakDims, strongDims).forEach((tip) => {
      const li = document.createElement("li");
      li.textContent = tip;
      tipsEl.appendChild(li);
    });
  }
  if (insightEl) {
    if (weakDims.length >= 2) {
      insightEl.textContent =
        "Sizlar bir-biringizni qadrlaysiz, lekin stress paytida himoya reaksiyasi kuchayadi. Shu paytda ohangni yumshatish munosabatni saqlaydi.";
    } else if (strongDims.length >= 2) {
      insightEl.textContent =
        "Sizlarda hissiy moslashuv yaxshi: kelishmovchilik bo‘lsa ham tezroq tiklanish imkoniyati bor.";
    } else {
      insightEl.textContent =
        "Munosabatda yaqinlik bor, uni ongli ravishda qo‘llab-quvvatlasangiz ishonch yanada chuqurlashadi.";
    }
  }
  if (forecastEl) {
    if (totalScore >= 80) {
      forecastEl.textContent = "Shu tempda davom etsangiz, munosabat yanada mustahkam va sokin bosqichga o‘tadi.";
    } else if (totalScore >= 60) {
      forecastEl.textContent = "To‘g‘ri odatlar bilan yaqin oylar ichida sezilarli ijobiy o‘sish ko‘rish mumkin.";
    } else if (totalScore >= 40) {
      forecastEl.textContent = "Agar hozirdan muloqot va e’tiborni kuchaytirsangiz, vaziyatni ijobiy tomonga burish mumkin.";
    } else {
      forecastEl.textContent = "Hozir murakkab davr, lekin bosqichma-bosqich ish bilan munosabatni tiklash imkoniyati bor.";
    }
  }

  const unlockBtn = document.getElementById("unlock-cta");
  unlockBtn?.addEventListener("click", () => {
    fullBlock.classList.remove("hidden");
    fullBlock.scrollIntoView({ behavior: "smooth", block: "start" });
  });
}

function hasBothZodiacs(result) {
  const a = (result.initiator_zodiac || "").trim();
  const b = (
    result.partner_zodiac ||
    result.respondent_zodiac ||
    ""
  ).trim();
  return Boolean(a && b);
}

async function parseError(response) {
  try {
    const body = await response.json();
    if (body && typeof body.detail === "string") {
      return body.detail;
    }
    if (body && Array.isArray(body.detail)) {
      const parts = body.detail
        .map((item) => {
          if (item && typeof item.msg === "string") {
            return item.msg;
          }
          return null;
        })
        .filter(Boolean);
      if (parts.length) {
        return parts.join(" ");
      }
    }
  } catch (_error) {
    // ignore JSON parse errors
  }
  return `So‘rov bajarilmadi (status: ${response.status})`;
}

function revealLoveProfileForm() {
  flowLog("profile_form_reveal");
  const profileSection =
    document.getElementById("profile-section") ||
    document.getElementById("love-step-form");
  if (!profileSection) {
    flowLog("profile_form_missing");
    return;
  }

  const heroSection = document.getElementById("love-step-hero");
  if (heroSection) {
    heroSection.hidden = true;
  }

  if (profileSection.classList.contains("hidden")) {
    profileSection.classList.remove("hidden");
  }
  if (profileSection.hidden) {
    profileSection.hidden = false;
  }
  profileSection.classList.add("love-step--visible");

  requestAnimationFrame(() => {
    profileSection.scrollIntoView({ behavior: "smooth", block: "start" });
    document.getElementById("initiator-name")?.focus({ preventScroll: true });
  });
}

async function startTest() {
  flowLog("session_create_start");
  setMessage("");
  const button = document.getElementById("profile-submit-btn");
  const form = document.getElementById("initiator-form");
  if (form && !form.reportValidity()) {
    return;
  }
  if (button) {
    button.disabled = true;
  }

  try {
    const nameInput = document.getElementById("initiator-name");
    const ageInput = document.getElementById("initiator-age");
    const genderEl = form?.querySelector(
      'input[name="initiator_gender"]:checked',
    );
    const zodiacEl = form?.querySelector(
      'input[name="initiator_zodiac"]:checked',
    );
    const zodiacValue = zodiacEl ? zodiacEl.value.trim() : "";
    const relEl = form?.querySelector(
      'input[name="relationship_type"]:checked',
    );
    const relHidden = form?.querySelector(
      'input[name="relationship_type"][type="hidden"]',
    );
    const telegramUserId = getTelegramUserId();
    const createSessionUrl = telegramUserId
      ? `/api/sessions?tg_id=${encodeURIComponent(telegramUserId)}`
      : "/api/sessions";
    const response = await fetch(createSessionUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        initiator_name: nameInput ? nameInput.value.trim() : "",
        initiator_age: ageInput ? Number(ageInput.value) : 0,
        initiator_gender: genderEl ? genderEl.value : "",
        initiator_zodiac: zodiacValue || null,
        relationship_type: relEl
          ? relEl.value
          : relHidden
            ? relHidden.value
            : "married",
        initiator_telegram_id: telegramUserId || null,
        creator_telegram_id: telegramUserId || null,
      }),
    });

    if (!response.ok) {
      throw new Error(await parseError(response));
    }

    const session = await response.json();
    if (!session.token) {
      throw new Error("Javobda sessiya tokeni topilmadi");
    }

    flowLog("session_created", { token: session.token });
    setToken(session.token);
    const tok = session.token;
    window.location.href = `/quiz/init/${encodeURIComponent(tok)}`;
  } catch (error) {
    flowLog("session_create_failed", error.message || String(error));
    setMessage(error.message || "Sessiya yaratilmadi");
    if (button) {
      button.disabled = false;
    }
  }
}

function hydrateTokenFromUrl() {
  const bodyToken = document.body?.dataset?.token;
  if (bodyToken) {
    setToken(bodyToken);
    return bodyToken;
  }

  const hiddenToken = document.getElementById("session-token")?.value;
  if (hiddenToken) {
    setToken(hiddenToken);
    return hiddenToken;
  }

  const resultPathMatch = window.location.pathname.match(/^\/result\/([A-Za-z0-9_-]+)$/);
  if (resultPathMatch && resultPathMatch[1]) {
    setToken(resultPathMatch[1]);
    return resultPathMatch[1];
  }

  const params = new URLSearchParams(window.location.search);
  const tokenFromUrl = params.get("token");
  if (tokenFromUrl) {
    setToken(tokenFromUrl);
    return tokenFromUrl;
  }
  return "";
}

function getBootstrappedQuestions() {
  const script = document.getElementById("bootstrap-questions");
  if (!script || !script.textContent) {
    return [];
  }
  try {
    const parsed = JSON.parse(script.textContent);
    return Array.isArray(parsed) ? parsed : [];
  } catch (_error) {
    return [];
  }
}

function renderQuestions(questions) {
  const mount = document.getElementById("questions-mount");
  if (!mount) {
    return;
  }

  mount.innerHTML = "";
  const total = questions.length;
  questions.forEach((question, index) => {
    const wrapper = document.createElement("section");
    wrapper.className = index === 0 ? "question-block question-block--active" : "question-block";
    wrapper.dataset.questionId = String(question.id);
    wrapper.dataset.questionIndex = String(index);

    const title = document.createElement("p");
    title.className = "question-block__title";
    title.textContent = `💬 Savol ${index + 1}`;
    wrapper.appendChild(title);

    const text = document.createElement("p");
    text.className = "question-block__text";
    text.textContent = question.text;
    wrapper.appendChild(text);

    const stack = document.createElement("div");
    stack.className = "radio-stack";
    question.options.forEach((option) => {
      const row = document.createElement("label");
      row.className = "radio-pill";

      const input = document.createElement("input");
      input.type = "radio";
      input.name = `question-${question.id}`;
      input.value = String(option.id);
      input.required = true;

      const span = document.createElement("span");
      span.className = "radio-pill__text";
      span.textContent = option.text;

      row.appendChild(input);
      row.appendChild(span);
      stack.appendChild(row);
    });
    wrapper.appendChild(stack);
    mount.appendChild(wrapper);
  });
}

function showQuestion(index, total) {
  const nextIndex = Math.min(Math.max(index, 0), Math.max(total - 1, 0));
  activeQuestionIndex = nextIndex;
  document.querySelectorAll(".question-block").forEach((block, blockIndex) => {
    block.classList.toggle("question-block--active", blockIndex === nextIndex);
  });
  const pill = document.getElementById("quiz-progress-pill");
  if (pill && total) {
    pill.textContent = `${nextIndex + 1}/${total}`;
  }
  reportQuizProgress(nextIndex);
}

async function reportQuizProgress(questionIndex) {
  const token = hydrateTokenFromUrl();
  if (!token) {
    return;
  }
  try {
    await fetch(`/api/sessions/${encodeURIComponent(token)}/progress`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question_index: questionIndex }),
    });
  } catch (_error) {
    // Progress tracking should not block the quiz flow.
  }
}

function firstUnansweredQuestionIndex(form, questions) {
  const index = questions.findIndex((question) => {
    return !form.querySelector(`input[name="question-${question.id}"]:checked`);
  });
  return index === -1 ? questions.length - 1 : index;
}

function flashSavedBubble() {
  const bubble = document.getElementById("answer-saved-bubble");
  if (!bubble) {
    return;
  }
  bubble.classList.add("is-visible");
  window.setTimeout(() => {
    bubble.classList.remove("is-visible");
  }, 1200);
}

async function resolveQuizRole(token, preferredRole) {
  const st = await getSessionState(token);
  const requested = (preferredRole || "").trim().toLowerCase();
  flowLog("quiz_role_resolve", { token, requested, state: st });

  if (requested === "initiator") {
    if (st.initiator_answered) {
      flowLog("quiz_redirect_share", { token });
      window.location.replace(`/share/${encodeURIComponent(token)}?host=1`);
      return null;
    }
    return "initiator";
  }

  if (!st.partner_registered) {
    flowLog("quiz_redirect_partner_register", { token });
    window.location.replace(`/start/${encodeURIComponent(token)}`);
    return null;
  }
  if (st.partner_answered) {
    flowLog("quiz_redirect_partner_complete", { token });
    window.location.replace(`/partner/complete/${encodeURIComponent(token)}`);
    return null;
  }
  return "partner";
}

function updateQuizProgress(form, questions) {
  const total = questions.length;
  if (!total) {
    return;
  }
  let answered = 0;
  for (const q of questions) {
    if (form.querySelector(`input[name="question-${q.id}"]:checked`)) {
      answered += 1;
    }
  }
  const fill = document.getElementById("quiz-progress-fill");
  const label = document.getElementById("quiz-progress-label");
  const countEl = document.getElementById("quiz-progress-count");
  const bar = document.getElementById("quiz-progress-bar");
  const pct = Math.round((answered / total) * 100);
  const activeNumber = Math.min(activeQuestionIndex + 1, total);
  const pill = document.getElementById("quiz-progress-pill");
  if (fill) {
    fill.style.width = `${pct}%`;
  }
  if (label) {
    label.textContent =
      answered >= total
        ? "Barcha savollar tanlandi"
        : `Savol ${answered + 1} / ${total}`;
  }
  if (countEl) {
    countEl.textContent = `${answered} / ${total}`;
  }
  if (pill) {
    pill.textContent = `${activeNumber}/${total}`;
  }
  if (bar) {
    bar.setAttribute("aria-valuenow", String(Math.min(Math.max(answered, 1), total)));
    bar.setAttribute("aria-valuemax", String(total));
  }
}

async function getSessionState(token) {
  const res = await fetch(`/api/sessions/${token}/state`);
  if (!res.ok) {
    throw new Error(await parseError(res));
  }
  return res.json();
}

async function loadQuestionsPage() {
  const token = hydrateTokenFromUrl();
  flowLog("questions_page_load", { token: token || "(missing)" });
  if (!token) {
    flowLog("questions_missing_token_redirect_home");
    window.location.href = "/";
    return;
  }

  try {
    const params = new URLSearchParams(window.location.search);
    const roleFromUrl = (params.get("role") || "").trim().toLowerCase();
    const roleFromBody = (document.body?.dataset?.role || "").trim().toLowerCase();
    const roleFromHidden = (
      document.getElementById("quiz-role")?.value || ""
    ).trim().toLowerCase();
    const preferredRole = roleFromUrl || roleFromBody || roleFromHidden || "partner";
    const role = await resolveQuizRole(token, preferredRole);
    if (!role) {
      return;
    }
    const state = await getSessionState(token);
    if (
      (role === "initiator" && state.initiator_answered) ||
      (role === "partner" && state.partner_answered)
    ) {
      if (role === "partner") {
        window.location.replace(`/partner/complete/${encodeURIComponent(token)}`);
        return;
      }
      setMessage("Sizning javoblaringiz allaqachon yuborilgan. Rahmat!");
      const submitBtn = document.getElementById("submit-answers-btn");
      if (submitBtn) {
        submitBtn.disabled = true;
      }
      return;
    }

    const hintEl = document.getElementById("quiz-role-hint");
    if (hintEl) {
      hintEl.textContent =
        role === "initiator"
          ? "Siz boshlovchi sifatida qatnashyapsiz — savollarga samimiy javob bering."
          : "Siz hamkor sifatida qatnashyapsiz — savollarga samimiy javob bering.";
    }

    const bootstrappedQuestions = getBootstrappedQuestions();
    let questions = bootstrappedQuestions;
    try {
      const response = await fetch(`/api/sessions/${token}/questions`);
      if (!response.ok) {
        throw new Error(await parseError(response));
      }
      const fetchedQuestions = await response.json();
      if (Array.isArray(fetchedQuestions) && fetchedQuestions.length > 0) {
        questions = fetchedQuestions;
      }
    } catch (error) {
      if (!questions.length) {
        throw error;
      }
    }
    if (!Array.isArray(questions) || questions.length === 0) {
      throw new Error("Savollar topilmadi. Iltimos, qaytadan urinib ko‘ring.");
    }
    renderQuestions(questions);
    showQuestion(0, questions.length);

    const form = document.getElementById("questions-form");
    const progressWrap = document.getElementById("quiz-progress");
    if (progressWrap) {
      progressWrap.classList.remove("hidden");
      progressWrap.setAttribute("aria-hidden", "false");
    }
    if (form) {
      const backBtn = document.getElementById("quiz-back-btn");
      backBtn?.addEventListener("click", () => {
        showQuestion(activeQuestionIndex - 1, questions.length);
      });
      updateQuizProgress(form, questions);
      form.addEventListener("change", () => {
        updateQuizProgress(form, questions);
        flashSavedBubble();
        const nextIndex = firstUnansweredQuestionIndex(form, questions);
        window.setTimeout(() => {
          showQuestion(nextIndex, questions.length);
        }, 260);
      });

      form.addEventListener(
        "submit",
        async (event) => {
          event.preventDefault();
          setMessage("");

          const missingIndex = questions.findIndex((question) => {
            return !form.querySelector(`input[name="question-${question.id}"]:checked`);
          });
          if (missingIndex !== -1) {
            showQuestion(missingIndex, questions.length);
            setMessage("Iltimos, barcha savollarga javob bering.");
            return;
          }

          const answers = questions.map((question) => {
            const selected = form.querySelector(
              `input[name="question-${question.id}"]:checked`,
            );
            return {
              question_id: question.id,
              option_id: Number(selected.value),
            };
          });

          const submitButton = document.getElementById("submit-answers-btn");
          if (submitButton) {
            submitButton.disabled = true;
          }

          try {
            const submitBody = { role, answers };
            if (role === "partner") {
              const partnerTgId = getPartnerTelegramUserId();
              if (partnerTgId) {
                submitBody.partner_telegram_id = partnerTgId;
              }
            }
            flowLog("answers_submit", { token, role, answerCount: answers.length });
            const submitResponse = await fetch(`/api/sessions/${token}/answers`, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify(submitBody),
            });
            if (!submitResponse.ok) {
              throw new Error(await parseError(submitResponse));
            }
            const data = await submitResponse.json();
            flowLog("answers_submit_ok", { token, role, status: data.status });
            if (data.status === "completed") {
              if (role === "initiator") {
                flowLog("redirect_share", { token });
                window.location.href = `/share/${encodeURIComponent(token)}?host=1`;
                return;
              }
              flowLog("redirect_partner_complete", { token });
              window.location.href = `/partner/complete/${encodeURIComponent(token)}`;
              return;
            } else {
              if (role === "initiator") {
                flowLog("redirect_share_partial", { token });
                window.location.href = `/share/${encodeURIComponent(token)}?host=1`;
                return;
              }
              setMessage("Rahmat! Javoblaringiz saqlandi.");
              if (submitButton) {
                submitButton.disabled = false;
              }
            }
          } catch (error) {
            flowLog("answers_submit_failed", error.message || String(error));
            setMessage(error.message || "Javoblarni yuborib bo‘lmadi");
            if (submitButton) {
              submitButton.disabled = false;
            }
          }
        });
    }
  } catch (error) {
    flowLog("questions_page_failed", error.message || String(error));
    setMessage(error.message || "Savollarni yuklab bo‘lmadi");
  }
}

async function loadResultPage() {
  const token = hydrateTokenFromUrl();
  flowLog("result_page_load", { token: token || "(missing)" });
  if (!token) {
    flowLog("result_missing_token_redirect_home");
    window.location.href = "/";
    return;
  }

  try {
    const response = await fetch(`/api/sessions/${token}/result`);
    if (!response.ok) {
      throw new Error(await parseError(response));
    }

    const result = await response.json();
    const scoreEl = document.getElementById("score");
    const emotionalLineEl = document.getElementById("emotional-line");
    const initiatorZodiacEl = document.getElementById("initiator-zodiac");
    const partnerZodiacEl = document.getElementById("partner-zodiac");
    const zodiacSummaryEl = document.getElementById("zodiac-summary");
    const dimensionTeasersEl = document.getElementById("dimension-teasers");
    const zodiacBlockEl = document.getElementById("zodiac-block");
    const cardEl = document.getElementById("result-card");

    if (scoreEl) {
      scoreEl.textContent = `${result.total_score}%`;
    }
    if (emotionalLineEl) {
      emotionalLineEl.textContent = emotionalSummaryFromOverall(
        result.total_score,
      );
    }
    const scores = normalizeDimensionScores(result.dimension_scores || {});
    if (dimensionTeasersEl) {
      dimensionTeasersEl.innerHTML = "";
      const order = window.LoveDimensionInsights?.order || DIMENSION_TEASER_ORDER;
      order.forEach((dimension) => {
        const raw = scores[dimension];
        const scoreNum = typeof raw === "number" ? raw : 0;
        dimensionTeasersEl.appendChild(
          buildDimensionTeaserCard(
            dimension,
            Number.isFinite(scoreNum) ? scoreNum : 0,
          ),
        );
      });
    }
    renderFullAnalysis(result);
    renderDifferencesBlock(scores);
    if (hasBothZodiacs(result)) {
      if (initiatorZodiacEl) {
        initiatorZodiacEl.textContent = result.initiator_zodiac || "";
      }
      if (partnerZodiacEl) {
        partnerZodiacEl.textContent =
          result.partner_zodiac || result.respondent_zodiac || "";
      }
      if (zodiacSummaryEl) {
        zodiacSummaryEl.textContent = result.zodiac_summary || "";
      }
      if (zodiacBlockEl) {
        zodiacBlockEl.classList.remove("hidden");
      }
    } else if (zodiacBlockEl) {
      zodiacBlockEl.classList.add("hidden");
    }
    if (cardEl) {
      cardEl.classList.remove("hidden");
    }
    flowLog("result_rendered", {
      token,
      score: result.total_score,
      teaserCount: dimensionTeasersEl?.children.length || 0,
    });
    const shareBtn = document.getElementById("result-share-btn");
    shareBtn?.addEventListener("click", async () => {
      const url = `${window.location.origin}/result/${encodeURIComponent(token)}`;
      const text = `Sevgi testi natijamiz: ${result.total_score}% 💜`;
      if (navigator.share) {
        try {
          await navigator.share({
            title: "Sevgi testi natijasi",
            text,
            url,
          });
          return;
        } catch (_error) {
          // Fallback to clipboard below.
        }
      }
      try {
        await navigator.clipboard.writeText(url);
        setMessage("Natija havolasi nusxalandi.");
      } catch (_error) {
        setMessage("Natijani ulashib bo‘lmadi.");
      }
    });

  } catch (error) {
    flowLog("result_page_failed", error.message || String(error));
    setMessage(error.message || "Natijani yuklab bo‘lmadi");
  }
}

function initSharePage() {
  const inviteInput = document.getElementById("partner-link");
  const inviteLink = inviteInput?.value || "";
  const sessionToken = inviteInput?.dataset.token || "";
  const msg = document.getElementById("message");
  const shareBtn = document.getElementById("telegram-share-btn");
  const copyBtn = document.getElementById("copy-partner-link");
  const shareUrl = shareBtn?.dataset.shareUrl || shareBtn?.getAttribute("href") || "";

  flowLog("share_page_init", {
    token: sessionToken || "(missing)",
    hasInviteLink: Boolean(inviteLink),
    hasShareUrl: Boolean(shareUrl),
  });

  async function copyInviteLink() {
    if (!inviteLink) {
      flowLog("share_copy_missing_link");
      if (msg) msg.textContent = "Taklif havolasi tayyor emas.";
      return;
    }
    try {
      await navigator.clipboard.writeText(inviteLink);
      flowLog("share_copy_ok");
      if (msg) msg.textContent = "Havola nusxalandi.";
    } catch {
      try {
        const helper = document.createElement("textarea");
        helper.value = inviteLink;
        helper.setAttribute("readonly", "");
        helper.style.position = "fixed";
        helper.style.left = "-9999px";
        document.body.appendChild(helper);
        helper.select();
        document.execCommand("copy");
        helper.remove();
        flowLog("share_copy_ok_fallback");
        if (msg) msg.textContent = "Havola nusxalandi.";
      } catch {
        flowLog("share_copy_failed");
        if (msg) msg.textContent = "Nusxalab bo‘lmadi.";
      }
    }
  }

  async function trackInviteShareClick() {
    if (!sessionToken) return;
    try {
      await fetch(`/api/sessions/${encodeURIComponent(sessionToken)}/events/invite-share`, {
        method: "POST",
      });
      flowLog("share_track_ok", { token: sessionToken });
    } catch {
      flowLog("share_track_failed", { token: sessionToken });
    }
  }

  function openTelegramShare(event) {
    event?.preventDefault();
    if (!shareUrl) {
      flowLog("share_open_missing_url");
      if (msg) msg.textContent = "Telegram ulashish havolasi tayyor emas.";
      return;
    }
    trackInviteShareClick();
    const webApp = window.Telegram?.WebApp;
    if (webApp?.openTelegramLink && shareUrl.startsWith("https://t.me/")) {
      flowLog("share_open_telegram_link", { url: shareUrl });
      webApp.openTelegramLink(shareUrl);
      return;
    }
    if (webApp?.openLink) {
      flowLog("share_open_link", { url: shareUrl });
      webApp.openLink(shareUrl);
      return;
    }
    flowLog("share_open_window", { url: shareUrl });
    window.open(shareUrl, "_blank", "noopener,noreferrer");
  }

  copyBtn?.addEventListener("click", copyInviteLink);
  shareBtn?.addEventListener("click", openTelegramShare);
}

function init() {
  const page = document.body.dataset.page;
  flowLog("page_init", { page: page || "(missing)" });
  if (page === "index") {
    initTelegramWebApp();
    initIndexTelegramId();
    const startBtn =
      document.getElementById("start-test-btn") ||
      document.getElementById("hero-start-btn");
    const profileSection =
      document.getElementById("profile-section") ||
      document.getElementById("love-step-form");
    if (startBtn && profileSection) {
      startBtn.addEventListener("click", () => {
        revealLoveProfileForm();
      });
    } else {
      flowLog("index_start_binding_missing", {
        hasStartBtn: Boolean(startBtn),
        hasProfileSection: Boolean(profileSection),
      });
    }
    const initiatorForm = document.getElementById("initiator-form");
    if (initiatorForm) {
      initiatorForm.addEventListener("submit", (event) => {
        event.preventDefault();
        startTest();
      });
    }
    return;
  }

  if (page === "questions") {
    loadQuestionsPage();
    return;
  }

  if (page === "partner") {
    initTelegramWebApp();
    const partnerTgId = getPartnerTelegramUserId();
    flowLog("partner_page_init", { partnerTgId: partnerTgId || "(missing)" });
    const partnerForm = document.getElementById("partner-form");
    partnerForm?.addEventListener("submit", async (event) => {
      event.preventDefault();
      flowLog("partner_register_start");
      const msg = document.getElementById("message");
      if (msg) {
        msg.textContent = "";
      }
      const tokenEl = document.getElementById("session-token");
      const token = tokenEl ? tokenEl.value : "";
      const form = document.getElementById("partner-form");
      if (!form || !form.reportValidity()) {
        flowLog("partner_register_invalid_form");
        return;
      }
      const nameInput = document.getElementById("partner-name");
      const ageInput = document.getElementById("partner-age");
      const genderEl = form.querySelector('input[name="partner_gender"]:checked');
      const zodiacEl = form.querySelector('input[name="partner_zodiac"]:checked');
      const btn = document.getElementById("partner-submit");
      if (btn) {
        btn.disabled = true;
      }
      const partnerTelegramId = getPartnerTelegramUserId();
      try {
        const res = await fetch(`/api/sessions/${token}/partner`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            partner_name: nameInput ? nameInput.value.trim() : "",
            partner_age: ageInput ? Number(ageInput.value) : 0,
            partner_gender: genderEl ? genderEl.value : "",
            partner_zodiac: zodiacEl ? zodiacEl.value : "",
            partner_telegram_id: partnerTelegramId,
          }),
        });
        if (!res.ok) {
          throw new Error(await parseError(res));
        }
        if (partnerTelegramId) {
          persistPartnerTelegramId(partnerTelegramId);
        }
        flowLog("partner_register_ok", { token, partnerTgId: partnerTelegramId || "(missing)" });
        setToken(token);
        window.location.href = `/questions.html?token=${encodeURIComponent(token)}&role=partner`;
      } catch (error) {
        flowLog("partner_register_failed", error.message || String(error));
        if (msg) {
          msg.textContent = error.message || "Saqlab bo‘lmadi";
        }
        if (btn) {
          btn.disabled = false;
        }
      }
    });
    return;
  }

  if (page === "share") {
    initTelegramWebApp();
    initSharePage();
    return;
  }

  if (page === "result") {
    loadResultPage();
  }
}

document.addEventListener("DOMContentLoaded", init);
