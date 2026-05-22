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
    return;
  }
  getTelegramUserId();
}

function dimensionLabel(key) {
  const map = {
    communication: "Muloqot",
    trust: "Ishonch",
    attention: "E'tibor",
    emotional_closeness: "Hissiy yaqinlik",
  };
  return map[key] || key;
}

const DIMENSION_TEASER_ORDER = [
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

function dimensionTeaserLine(dimensionKey, score) {
  const n = Number(score);
  const s = Number.isNaN(n) ? 0 : n;
  const tier = s >= 70 ? "high" : s >= 45 ? "mid" : "low";
  const lines = {
    communication: {
      high: "Muloqotingiz yaxshi yo‘lga qo‘yilgan, bir-biringizni eshitish oson.",
      mid: "Muloqot o‘rtacha: ba’zi vaziyatlarda tushunmovchilik seziladi.",
      low: "Muloqotda muammo bor: hislarni ochiq aytish va tinglash ustida ishlash kerak.",
    },
    trust: {
      high: "Ishonch darajasi yaxshi, munosabatda tayanch hissi bor.",
      mid: "Ishonch o‘rtacha: barqarorlik va aniq kelishuvlar foyda beradi.",
      low: "Ishonch bo‘yicha muammo bor, kichik va izchil qadamlar bilan tiklash kerak.",
    },
    attention: {
      high: "E’tibor darajasi yaxshi: bir-biringizga vaqt va diqqat ajratyapsiz.",
      mid: "E’tibor o‘rtacha: kundalik shoshilishda bu jihat ba’zan pasayadi.",
      low: "E’tibor bo‘yicha muammo bor: sifatli vaqt va g‘amxo‘rlikni ko‘paytirish zarur.",
    },
    emotional_closeness: {
      high: "Hissiy yaqinlik yaxshi: samimiylik va iliqlik seziladi.",
      mid: "Hissiy yaqinlik o‘rtacha: chuqur mavzularni ko‘proq ochish kerak bo‘lishi mumkin.",
      low: "Hissiy yaqinlikda muammo bor: xavfsiz va samimiy suhbatlarni ko‘paytirish muhim.",
    },
  };
  const dimLines = lines[dimensionKey] || lines.communication;
  return dimLines[tier];
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

async function startTest() {
  setMessage("");
  const button = document.getElementById("start-test-btn");
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
    const relEl = form?.querySelector(
      'input[name="relationship_type"]:checked',
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
        initiator_zodiac: zodiacEl ? zodiacEl.value : "",
        relationship_type: relEl ? relEl.value : "married",
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

    setToken(session.token);
    const tok = session.token;
    window.location.href = `/quiz/init/${encodeURIComponent(tok)}`;
  } catch (error) {
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

  if (requested === "initiator") {
    if (st.initiator_answered) {
      window.location.replace(`/share/${encodeURIComponent(token)}?host=1`);
      return null;
    }
    return "initiator";
  }

  if (!st.partner_registered) {
    window.location.replace(`/start/${encodeURIComponent(token)}`);
    return null;
  }
  if (st.partner_answered) {
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
  if (!token) {
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
            const submitResponse = await fetch(`/api/sessions/${token}/answers`, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                role,
                answers,
              }),
            });
            if (!submitResponse.ok) {
              throw new Error(await parseError(submitResponse));
            }
            const data = await submitResponse.json();
            if (data.status === "completed") {
              if (role === "initiator") {
                window.location.href = `/share/${encodeURIComponent(token)}?host=1`;
                return;
              }
              window.location.href = `/partner/complete/${encodeURIComponent(token)}`;
              return;
            } else {
              if (role === "initiator") {
                window.location.href = `/share/${encodeURIComponent(token)}?host=1`;
                return;
              }
              setMessage("Rahmat! Javoblaringiz saqlandi.");
              if (submitButton) {
                submitButton.disabled = false;
              }
            }
          } catch (error) {
            setMessage(error.message || "Javoblarni yuborib bo‘lmadi");
            if (submitButton) {
              submitButton.disabled = false;
            }
          }
        });
    }
  } catch (error) {
    setMessage(error.message || "Savollarni yuklab bo‘lmadi");
  }
}

async function loadResultPage() {
  const token = hydrateTokenFromUrl();
  if (!token) {
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
    const differencesBlock = document.getElementById("differences-block");
    const differencesText = document.getElementById("differences-text");
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
    if (dimensionTeasersEl) {
      dimensionTeasersEl.innerHTML = "";
      const scores = normalizeDimensionScores(result.dimension_scores || {});
      DIMENSION_TEASER_ORDER.forEach((dimension) => {
        const raw = scores[dimension];
        const scoreNum = typeof raw === "number" ? raw : 0;
        const card = document.createElement("article");
        card.className = "teaser-card";
        const title = document.createElement("h3");
        title.className = "teaser-title";
        title.textContent = dimensionLabel(dimension);
        const pct = document.createElement("p");
        pct.className = "teaser-pct";
        pct.textContent = `${Number.isFinite(scoreNum) ? scoreNum : 0}%`;
        const body = document.createElement("p");
        body.className = "teaser-body";
        body.textContent = dimensionTeaserLine(
          dimension,
          Number.isFinite(scoreNum) ? scoreNum : 0,
        );
        card.appendChild(title);
        card.appendChild(pct);
        card.appendChild(body);
        dimensionTeasersEl.appendChild(card);
      });
    }
    renderFullAnalysis(result);
    if (differencesText && differencesBlock) {
      const diff = (result.differences || "").trim();
      if (diff) {
        differencesText.textContent = diff;
        differencesBlock.classList.remove("hidden");
      } else {
        differencesBlock.classList.add("hidden");
      }
    }
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
    setMessage(error.message || "Natijani yuklab bo‘lmadi");
  }
}

function init() {
  const page = document.body.dataset.page;
  if (page === "index") {
    initIndexTelegramId();
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
    const partnerForm = document.getElementById("partner-form");
    partnerForm?.addEventListener("submit", async (event) => {
      event.preventDefault();
      const msg = document.getElementById("message");
      if (msg) {
        msg.textContent = "";
      }
      const tokenEl = document.getElementById("session-token");
      const token = tokenEl ? tokenEl.value : "";
      const form = document.getElementById("partner-form");
      if (!form || !form.reportValidity()) {
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
      try {
        const res = await fetch(`/api/sessions/${token}/partner`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            partner_name: nameInput ? nameInput.value.trim() : "",
            partner_age: ageInput ? Number(ageInput.value) : 0,
            partner_gender: genderEl ? genderEl.value : "",
            partner_zodiac: zodiacEl ? zodiacEl.value : "",
            partner_telegram_id: getTelegramUserId(),
          }),
        });
        if (!res.ok) {
          throw new Error(await parseError(res));
        }
        setToken(token);
        window.location.href = `/questions.html?token=${encodeURIComponent(token)}&role=partner`;
      } catch (error) {
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

  if (page === "result") {
    loadResultPage();
  }
}

document.addEventListener("DOMContentLoaded", init);
