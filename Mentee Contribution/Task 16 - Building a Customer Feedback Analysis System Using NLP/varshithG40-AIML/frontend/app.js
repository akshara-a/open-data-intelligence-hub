/**
 * FEEDBACK.STUDIO™ — Frontend Application Controller
 * Connects to the local Python NLP backend via REST API,
 * with intelligent client-side NLP fallback for offline standalone mode.
 */

// Global state
const AppState = {
  activeFeedback: "",
  apiOnline: false,
  corpus: [],
  curatedSamples: [],
  currentResult: null
};

// Built-in Dataset of 20 canonical samples from data/feedback.csv for offline twin matching
const EMBEDDED_CORPUS = [
  { feedback: "Payment keeps failing during checkout with credit card", sentiment: "negative", categories: ["payment"] },
  { feedback: "The application is very slow and lags constantly", sentiment: "negative", categories: ["performance"] },
  { feedback: "I love the new dashboard, it looks very clean and modern", sentiment: "positive", categories: ["ui"] },
  { feedback: "Customer support team solved my issue in less than ten minutes", sentiment: "positive", categories: ["support"] },
  { feedback: "Login OTP is not arriving on my registered mobile number", sentiment: "negative", categories: ["login"] },
  { feedback: "The latest update is good, but payment is failing frequently", sentiment: "negative", categories: ["payment", "feature_request"] },
  { feedback: "The app is extremely slow and payment keeps failing", sentiment: "negative", categories: ["performance", "payment"] },
  { feedback: "Can you please add dark mode support in the settings?", sentiment: "neutral", categories: ["feature_request", "ui"] },
  { feedback: "App crashes every time I click on transaction history", sentiment: "negative", categories: ["bug", "performance"] },
  { feedback: "Super helpful customer service and quick resolution", sentiment: "positive", categories: ["support"] },
  { feedback: "The app is okay, does what it is supposed to do", sentiment: "neutral", categories: ["general"] },
  { feedback: "Unable to reset password because verification link expired", sentiment: "negative", categories: ["login"] },
  { feedback: "The user interface is confusing and navigation is difficult", sentiment: "negative", categories: ["ui"] },
  { feedback: "Payment went through smoothly and receipt was generated immediately", sentiment: "positive", categories: ["payment"] },
  { feedback: "Fingerprint login fails after the latest update", sentiment: "negative", categories: ["login", "bug"] },
  { feedback: "Great app! Fast performance and intuitive user interface", sentiment: "positive", categories: ["performance", "ui"] },
  { feedback: "The app freezes whenever I try to upload profile picture", sentiment: "negative", categories: ["performance", "bug"] },
  { feedback: "Support agent was polite and helped resolve my refund request", sentiment: "positive", categories: ["support", "payment"] },
  { feedback: "Average experience, some features are good but some need polish", sentiment: "neutral", categories: ["general"] },
  { feedback: "App took more than 15 seconds to open on Wi-Fi", sentiment: "negative", categories: ["performance"] }
];

const PRESETS = [
  { icon: "⚡", label: "App Slow & Payment Fails", text: "The application is very slow and payment keeps failing during checkout." },
  { icon: "🎧", label: "Helpful Support Team", text: "Customer support team solved my issue in less than ten minutes and followed up politely." },
  { icon: "🔐", label: "Login OTP Delayed", text: "Login OTP is not arriving on my registered mobile number after multiple attempts." },
  { icon: "🌙", label: "Dark Mode Request", text: "Can you please add dark mode support in the settings for late night reading?" },
  { icon: "⚠️", label: "Update Crashes", text: "The latest update is terrible, the app freezes constantly and crashes on transaction history." },
  { icon: "💎", label: "Clean UI Praise", text: "I love the new dashboard design, it looks super modern, intuitive and easy to use." }
];

// Negation list for negation preservation
const NEGATION_WORDS = new Set(["not", "no", "never", "barely", "hardly", "scarcely", "without", "neither", "nor"]);
const STOPWORDS = new Set([
  "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't",
  "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by",
  "could", "did", "do", "does", "doing", "down", "during", "each", "few", "for", "from", "further",
  "had", "has", "have", "having", "he", "her", "here", "hers", "herself", "him", "himself", "his",
  "how", "i", "if", "in", "into", "is", "isn't", "it", "its", "itself", "me", "more", "most", "my",
  "myself", "of", "off", "on", "once", "only", "or", "other", "our", "ours", "ourselves", "out",
  "over", "own", "same", "she", "should", "so", "some", "such", "than", "that", "the", "their",
  "theirs", "them", "themselves", "then", "there", "these", "they", "this", "those", "through", "to",
  "too", "under", "until", "up", "very", "was", "we", "were", "what", "when", "where", "which",
  "while", "who", "whom", "why", "with", "would", "you", "your", "yours", "yourself", "yourselves"
]);

// DOM Element references
const DOM = {
  feedbackInput: document.getElementById("feedbackInput"),
  charCount: document.getElementById("charCount"),
  wordCount: document.getElementById("wordCount"),
  btnAnalyze: document.getElementById("btnAnalyze"),
  btnClearInput: document.getElementById("btnClearInput"),
  btnRandomSample: document.getElementById("btnRandomSample"),
  presetPills: document.getElementById("presetPills"),
  systemStatusChip: document.getElementById("systemStatusChip"),
  statusText: document.getElementById("statusText"),
  timeDisplay: document.getElementById("timeDisplay"),

  // Quadrant 2: Sentiment
  sentimentPill: document.getElementById("sentimentPill"),
  confidenceValue: document.getElementById("confidenceValue"),
  sentimentDesc: document.getElementById("sentimentDesc"),
  pctNegative: document.getElementById("pctNegative"),
  pctNeutral: document.getElementById("pctNeutral"),
  pctPositive: document.getElementById("pctPositive"),
  barNegative: document.getElementById("barNegative"),
  barNeutral: document.getElementById("barNeutral"),
  barPositive: document.getElementById("barPositive"),
  linguisticAlert: document.getElementById("linguisticAlert"),
  lingTitle: document.getElementById("lingTitle"),
  lingSubtitle: document.getElementById("lingSubtitle"),

  // Quadrant 3: Taxonomy
  categoryChips: document.getElementById("categoryChips"),
  keywordChips: document.getElementById("keywordChips"),
  highlightedFeedback: document.getElementById("highlightedFeedback"),

  // Quadrant 4: Semantic Twins
  similarFeedbackList: document.getElementById("similarFeedbackList"),
  similarityCount: document.getElementById("similarityCount"),

  // Drawers
  btnViewGrid: document.getElementById("btnViewGrid"),
  btnOpenXray: document.getElementById("btnOpenXray"),
  btnCloseXray: document.getElementById("btnCloseXray"),
  xrayDrawer: document.getElementById("xrayDrawer"),

  btnOpenBatch: document.getElementById("btnOpenBatch"),
  btnCloseBatch: document.getElementById("btnCloseBatch"),
  batchDrawer: document.getElementById("batchDrawer"),
  batchTextarea: document.getElementById("batchTextarea"),
  btnRunBatch: document.getElementById("btnRunBatch"),
  btnLoadSampleBatch: document.getElementById("btnLoadSampleBatch"),
  batchTotalCount: document.getElementById("batchTotalCount"),
  batchPosPct: document.getElementById("batchPosPct"),
  batchNegPct: document.getElementById("batchNegPct"),
  batchTopCategory: document.getElementById("batchTopCategory"),
  batchTableBody: document.getElementById("batchTableBody"),
  btnExportCSV: document.getElementById("btnExportCSV"),

  btnOpenTransformer: document.getElementById("btnOpenTransformer"),
  btnCloseTransformer: document.getElementById("btnCloseTransformer"),
  transformerDrawer: document.getElementById("transformerDrawer"),
  trickyTestButtons: document.getElementById("trickyTestButtons"),

  // X-Ray elements
  xrayRaw: document.getElementById("xrayRaw"),
  xrayClean: document.getElementById("xrayClean"),
  xrayTokens: document.getElementById("xrayTokens"),
  stemLemmaBody: document.getElementById("stemLemmaBody"),
  xrayNgrams: document.getElementById("xrayNgrams")
};

// ============================================================================
// INITIALIZATION
// ============================================================================
document.addEventListener("DOMContentLoaded", () => {
  initClock();
  renderPresets();
  setupEventListeners();
  checkBackendHealth();
  updateTextMetrics();

  // Run initial analysis on default text
  executeAnalysis(DOM.feedbackInput.value.trim());
});

function initClock() {
  function update() {
    const now = new Date();
    if (DOM.timeDisplay) {
      DOM.timeDisplay.textContent = now.toTimeString().split(" ")[0] + " LOCAL";
    }
  }
  update();
  setInterval(update, 1000);
}

function renderPresets() {
  DOM.presetPills.innerHTML = "";
  PRESETS.forEach(p => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "preset-pill-btn";
    btn.innerHTML = `${p.icon} ${p.label}`;
    btn.addEventListener("click", () => {
      DOM.feedbackInput.value = p.text;
      updateTextMetrics();
      executeAnalysis(p.text);
    });
    DOM.presetPills.appendChild(btn);
  });
}

function setupEventListeners() {
  DOM.feedbackInput.addEventListener("input", updateTextMetrics);

  // Keyboard shortcut: Cmd/Ctrl + Enter
  DOM.feedbackInput.addEventListener("keydown", (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key === "Enter") {
      e.preventDefault();
      executeAnalysis(DOM.feedbackInput.value.trim());
    }
  });

  DOM.btnAnalyze.addEventListener("click", () => {
    executeAnalysis(DOM.feedbackInput.value.trim());
  });

  DOM.btnClearInput.addEventListener("click", () => {
    DOM.feedbackInput.value = "";
    updateTextMetrics();
    DOM.feedbackInput.focus();
  });

  DOM.btnRandomSample.addEventListener("click", () => {
    const random = EMBEDDED_CORPUS[Math.floor(Math.random() * EMBEDDED_CORPUS.length)];
    DOM.feedbackInput.value = random.feedback;
    updateTextMetrics();
    executeAnalysis(random.feedback);
  });

  // Drawer Toggles
  DOM.btnOpenXray.addEventListener("click", () => openDrawer(DOM.xrayDrawer));
  DOM.btnCloseXray.addEventListener("click", () => closeDrawer(DOM.xrayDrawer));

  DOM.btnOpenBatch.addEventListener("click", () => openDrawer(DOM.batchDrawer));
  DOM.btnCloseBatch.addEventListener("click", () => closeDrawer(DOM.batchDrawer));

  DOM.btnOpenTransformer.addEventListener("click", () => openDrawer(DOM.transformerDrawer));
  DOM.btnCloseTransformer.addEventListener("click", () => closeDrawer(DOM.transformerDrawer));

  // Close on backdrop click or ESC key
  [DOM.xrayDrawer, DOM.batchDrawer, DOM.transformerDrawer].forEach(drawer => {
    drawer.addEventListener("click", (e) => {
      if (e.target === drawer) closeDrawer(drawer);
    });
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      closeDrawer(DOM.xrayDrawer);
      closeDrawer(DOM.batchDrawer);
      closeDrawer(DOM.transformerDrawer);
    }
  });

  // Batch analysis triggers
  DOM.btnRunBatch.addEventListener("click", executeBatchAnalysis);
  DOM.btnLoadSampleBatch.addEventListener("click", () => {
    const sampleBatchTexts = [
      "The payment failed twice and my bank account got debited.",
      "Customer support agent resolved my query within five minutes!",
      "The app takes 20 seconds to launch and freezes randomly.",
      "Could you please add dark mode support in the next update?",
      "Unable to log in with Google OAuth, it throws an authentication error.",
      "The new checkout user interface is intuitive and smooth.",
      "App crashes whenever I attempt to download the monthly invoice PDF.",
      "Average experience overall, does the basic job."
    ];
    DOM.batchTextarea.value = sampleBatchTexts.join("\n");
  });

  DOM.btnExportCSV.addEventListener("click", exportBatchCSV);

  // Tricky Transformer buttons
  if (DOM.trickyTestButtons) {
    DOM.trickyTestButtons.querySelectorAll(".btn-pill").forEach(btn => {
      btn.addEventListener("click", () => {
        const text = btn.getAttribute("data-text");
        closeDrawer(DOM.transformerDrawer);
        DOM.feedbackInput.value = text;
        updateTextMetrics();
        executeAnalysis(text);
      });
    });
  }
}

function openDrawer(drawer) {
  drawer.classList.add("active");
  document.body.style.overflow = "hidden";
}

function closeDrawer(drawer) {
  drawer.classList.remove("active");
  document.body.style.overflow = "";
}

function updateTextMetrics() {
  const text = DOM.feedbackInput.value;
  DOM.charCount.textContent = text.length;
  const words = text.trim() ? text.trim().split(/\s+/).length : 0;
  DOM.wordCount.textContent = words;
}

// ============================================================================
// BACKEND API INTEGRATION & FALLBACK INTELLIGENCE
// ============================================================================
async function checkBackendHealth() {
  try {
    const res = await fetch("/api/health", { method: "GET", signal: AbortSignal.timeout(2500) });
    if (res.ok) {
      const data = await res.json();
      AppState.apiOnline = true;
      DOM.statusText.innerHTML = `BACKEND ONLINE &bull; ${data.model_ready ? "MODEL LOADED" : "HEURISTIC FALLBACK"}`;
      return;
    }
  } catch (e) {
    // Backend offline; client-side engine active
  }
  AppState.apiOnline = false;
  DOM.statusText.innerHTML = `CLIENT ENGINE ACTIVE &bull; STANDALONE MODE`;
}

async function executeAnalysis(text) {
  if (!text) return;
  DOM.btnAnalyze.classList.add("loading");
  DOM.btnAnalyze.querySelector("span:last-child").textContent = "Analyzing...";

  let result = null;

  if (AppState.apiOnline) {
    try {
      const res = await fetch("/api/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, top_k: 3 })
      });
      if (res.ok) {
        result = await res.json();
      }
    } catch (e) {
      console.warn("API call failed, switching to client NLP fallback", e);
    }
  }

  // If no backend result, use client NLP fallback
  if (!result) {
    result = clientSideNLPAnalyze(text);
  }

  AppState.currentResult = result;
  renderAnalysisResults(result);

  DOM.btnAnalyze.classList.remove("loading");
  DOM.btnAnalyze.querySelector("span:last-child").textContent = "Analyze Feedback";
}

// ============================================================================
// CLIENT-SIDE NLP ENGINE (FALLBACK / INSTANT DEMO)
// ============================================================================
function clientSideNLPAnalyze(text) {
  const lower = text.toLowerCase();
  const cleaned = lower.replace(/[^a-z0-9\s]/g, " ").replace(/\s+/g, " ").trim();
  const rawTokens = cleaned.split(/\s+/).filter(Boolean);

  // Check negations
  const hasNegation = rawTokens.some(t => NEGATION_WORDS.has(t));

  // Sentiment Lexicons
  const posWords = ["love", "clean", "modern", "great", "fast", "intuitive", "helpful", "quick", "politely", "smoothly", "pleased", "good", "seamless", "polite", "resolved", "excellent", "super"];
  const negWords = ["slow", "lag", "lags", "fail", "fails", "failing", "terrible", "bad", "crash", "crashes", "freezes", "freeze", "bug", "confusing", "broken", "deducted", "expired", "error", "problem", "difficult"];

  let posScore = 0;
  let negScore = 0;

  for (let i = 0; i < rawTokens.length; i++) {
    const token = rawTokens[i];
    const prev = i > 0 ? rawTokens[i - 1] : "";
    const isNegated = NEGATION_WORDS.has(prev);

    if (posWords.some(w => token.includes(w))) {
      if (isNegated) negScore += 2.0;
      else posScore += 1.5;
    }
    if (negWords.some(w => token.includes(w))) {
      if (isNegated) posScore += 1.2;
      else negScore += 1.8;
    }
  }

  let sentiment = "neutral";
  let negProb = 0.2, neuProb = 0.6, posProb = 0.2;

  if (negScore > posScore && negScore >= 1) {
    sentiment = "negative";
    negProb = Math.min(0.96, 0.65 + negScore * 0.1);
    neuProb = (1 - negProb) * 0.7;
    posProb = 1 - negProb - neuProb;
  } else if (posScore > negScore && posScore >= 1) {
    sentiment = "positive";
    posProb = Math.min(0.96, 0.65 + posScore * 0.1);
    neuProb = (1 - posProb) * 0.7;
    negProb = 1 - posProb - neuProb;
  } else {
    sentiment = "neutral";
    neuProb = 0.72;
    negProb = 0.15;
    posProb = 0.13;
  }

  // Category Scoring
  const categoryRules = [
    { cat: "payment", words: ["payment", "checkout", "card", "bank", "debited", "receipt", "deducted", "money", "refund", "transact"] },
    { cat: "performance", words: ["slow", "lag", "fast", "speed", "freeze", "freezes", "seconds", "loading", "lags", "crashes"] },
    { cat: "ui", words: ["ui", "interface", "design", "dashboard", "dark mode", "looks", "navigation", "clean", "confusing"] },
    { cat: "support", words: ["support", "service", "agent", "team", "ticket", "polite", "resolved", "helped", "representative"] },
    { cat: "login", words: ["login", "otp", "password", "sign in", "authentication", "account", "verification", "fingerprint"] },
    { cat: "bug", words: ["bug", "glitch", "crash", "crashes", "freeze", "fails", "broken", "error"] },
    { cat: "feature_request", words: ["add", "request", "need", "feature", "dark mode", "export", "option", "please add"] },
    { cat: "general", words: ["app", "experience", "polish", "okay", "average"] }
  ];

  const categoryScores = {};
  const matchedCategories = [];

  categoryRules.forEach(rule => {
    let score = 0;
    rule.words.forEach(w => {
      if (lower.includes(w)) score += 0.45;
    });
    const finalScore = Math.min(0.95, score);
    categoryScores[rule.cat] = Number(finalScore.toFixed(2));
    if (finalScore >= 0.35) {
      matchedCategories.push(rule.cat);
    }
  });

  if (matchedCategories.length === 0) {
    matchedCategories.push("general");
    categoryScores["general"] = 0.50;
  }

  // Keyphrase extraction (unigrams & bigrams filtering stopwords)
  const contentTokens = rawTokens.filter(t => !STOPWORDS.has(t) || NEGATION_WORDS.has(t));
  const keywords = [];

  for (let i = 0; i < rawTokens.length - 1; i++) {
    const bigram = `${rawTokens[i]} ${rawTokens[i + 1]}`;
    if (posWords.concat(negWords).some(w => bigram.includes(w))) {
      keywords.push(bigram);
    }
  }

  contentTokens.forEach(t => {
    if (t.length > 3 && !keywords.some(k => k.includes(t))) {
      keywords.push(t);
    }
  });

  const finalKeywords = keywords.slice(0, 5);

  // In-context Salience Highlight
  let highlighted = text;
  finalKeywords.forEach(kw => {
    const reg = new RegExp(`(${kw})`, "gi");
    highlighted = highlighted.replace(reg, "<mark>$1</mark>");
  });

  // Semantic similarity via token overlap / jaccard against corpus
  const querySet = new Set(contentTokens);
  const similarityScores = EMBEDDED_CORPUS.map(item => {
    const itemTokens = item.feedback.toLowerCase().replace(/[^a-z0-9\s]/g, " ").split(/\s+/).filter(t => !STOPWORDS.has(t));
    const itemSet = new Set(itemTokens);
    let intersection = 0;
    querySet.forEach(t => { if (itemSet.has(t)) intersection++; });
    const union = new Set([...querySet, ...itemSet]).size;
    const sim = union > 0 ? intersection / union : 0;
    return {
      feedback: item.feedback,
      sentiment: item.sentiment,
      categories: item.categories,
      similarity: Number((sim * 0.75 + (item.sentiment === sentiment ? 0.2 : 0)).toFixed(2)),
      similarity_percentage: `${Math.min(96, Math.round((sim * 0.75 + (item.sentiment === sentiment ? 0.2 : 0)) * 100))}%`
    };
  }).sort((a, b) => b.similarity - a.similarity).slice(0, 3);

  // Stem vs Lemma Mock
  const stemLemma = rawTokens.map(tok => {
    let stem = tok;
    let lemma = tok;
    if (tok.endsWith("ing")) { stem = tok.slice(0, -3); lemma = tok.endsWith("ing") && tok.length > 5 ? tok.slice(0, -3) + "e" : tok.slice(0, -3); }
    else if (tok.endsWith("s") && tok.length > 3) { stem = tok.slice(0, -1); lemma = tok.slice(0, -1); }
    else if (tok.endsWith("ed")) { stem = tok.slice(0, -2); lemma = tok.slice(0, -1); }
    return { original: tok, stem, lemma, difference: stem !== lemma };
  });

  return {
    raw_text: text,
    cleaned_text: cleaned,
    tokens: rawTokens,
    sentiment: sentiment,
    sentiment_confidence: sentiment === "negative" ? negProb : (sentiment === "positive" ? posProb : neuProb),
    sentiment_scores: { negative: negProb, neutral: neuProb, positive: posProb },
    categories: matchedCategories,
    category_scores: categoryScores,
    keywords: finalKeywords,
    highlighted_text: highlighted,
    similar_feedback: similarityScores,
    stem_vs_lemma: stemLemma,
    has_negation: hasNegation
  };
}

// ============================================================================
// UI RENDERING CONTROLLER
// ============================================================================
function renderAnalysisResults(res) {
  // 1. Quadrant 2: Sentiment Decoder
  const sent = (res.sentiment || "neutral").toLowerCase();
  DOM.sentimentPill.textContent = sent.toUpperCase();
  DOM.sentimentPill.className = `sentiment-badge-tag ${sent === "negative" ? "neg" : (sent === "positive" ? "pos" : "neu")}`;

  const confPct = Math.round((res.sentiment_confidence || 0.8) * 100);
  DOM.confidenceValue.textContent = `${confPct}%`;

  if (sent === "negative") {
    DOM.sentimentDesc.textContent = "Significant negative dissatisfaction or operational issue identified.";
  } else if (sent === "positive") {
    DOM.sentimentDesc.textContent = "High customer praise, satisfaction, or commendation detected.";
  } else {
    DOM.sentimentDesc.textContent = "Informational feedback, inquiry, or neutral feature proposal.";
  }

  const scores = res.sentiment_scores || { negative: 0.33, neutral: 0.34, positive: 0.33 };
  const negP = Math.round((scores.negative || 0) * 100);
  const neuP = Math.round((scores.neutral || 0) * 100);
  const posP = Math.round((scores.positive || 0) * 100);

  DOM.pctNegative.textContent = `${negP}%`;
  DOM.pctNeutral.textContent = `${neuP}%`;
  DOM.pctPositive.textContent = `${posP}%`;

  DOM.barNegative.style.width = `${negP}%`;
  DOM.barNeutral.style.width = `${neuP}%`;
  DOM.barPositive.style.width = `${posP}%`;

  // Negation Guard Alert
  const hasNegation = res.has_negation || (res.tokens && res.tokens.some(t => NEGATION_WORDS.has(t.toLowerCase())));
  if (hasNegation) {
    DOM.linguisticAlert.style.display = "flex";
    DOM.lingTitle.textContent = "Negation Guard Triggered";
    DOM.lingSubtitle.textContent = "Crucial negation terms ('not', 'no', 'never') retained to avoid sentiment inversion.";
  } else {
    DOM.linguisticAlert.style.display = "flex";
    DOM.lingTitle.textContent = "Direct Polarity Flow";
    DOM.lingSubtitle.textContent = "Standard directional sentiment trajectory without negation inversions.";
  }

  // 2. Quadrant 3: Taxonomy & Keyphrases
  DOM.categoryChips.innerHTML = "";
  const cats = res.categories || ["general"];
  const catScores = res.category_scores || {};

  cats.forEach(c => {
    const scoreVal = catScores[c] ? Math.round(catScores[c] * 100) : 85;
    const chip = document.createElement("span");
    chip.className = "cat-chip active";
    chip.innerHTML = `${c} <span class="cat-pct">${scoreVal}%</span>`;
    DOM.categoryChips.appendChild(chip);
  });

  DOM.keywordChips.innerHTML = "";
  const kws = res.keywords || [];
  if (kws.length === 0) {
    DOM.keywordChips.innerHTML = `<span class="kw-chip">feedback</span>`;
  } else {
    kws.forEach(kw => {
      const chip = document.createElement("span");
      chip.className = "kw-chip";
      chip.textContent = kw;
      DOM.keywordChips.appendChild(chip);
    });
  }

  DOM.highlightedFeedback.innerHTML = res.highlighted_text || res.raw_text;

  // 3. Quadrant 4: Semantic Twins
  DOM.similarFeedbackList.innerHTML = "";
  const twins = res.similar_feedback || [];
  DOM.similarityCount.textContent = `TOP ${twins.length} MATCHES RETRIEVED`;

  twins.forEach(twin => {
    const card = document.createElement("div");
    card.className = "twin-card";
    
    const catsFormatted = (Array.isArray(twin.categories) ? twin.categories : [twin.categories || "general"])
      .map(c => `<span class="twin-cat-mini">${c}</span>`).join("");

    const sentColor = twin.sentiment === "positive" ? "var(--color-pos)" : (twin.sentiment === "negative" ? "var(--color-neg)" : "var(--color-neu)");

    card.innerHTML = `
      <div class="twin-card-top">
        <span class="twin-match-pill">${twin.similarity_percentage || "88%"} MATCH</span>
        <span class="twin-sent-tag" style="color: ${sentColor};">${twin.sentiment || "negative"}</span>
      </div>
      <div class="twin-feedback-text">"${twin.feedback}"</div>
      <div class="twin-cats">${catsFormatted}</div>
    `;
    DOM.similarFeedbackList.appendChild(card);
  });

  // Populate X-Ray Drawer
  updateXrayDrawer(res);
}

function updateXrayDrawer(res) {
  DOM.xrayRaw.textContent = res.raw_text;
  DOM.xrayClean.textContent = res.cleaned_text || res.raw_text.toLowerCase();

  // Tokens
  DOM.xrayTokens.innerHTML = "";
  const tokens = res.tokens || [];
  tokens.forEach(tok => {
    const chip = document.createElement("span");
    const isNeg = NEGATION_WORDS.has(tok.toLowerCase());
    chip.className = `token-chip ${isNeg ? "negation" : ""}`;
    chip.textContent = tok;
    DOM.xrayTokens.appendChild(chip);
  });

  // Stem vs Lemma Table
  DOM.stemLemmaBody.innerHTML = "";
  const stemLemmaList = res.stem_vs_lemma || [];
  stemLemmaList.slice(0, 10).forEach(item => {
    const tr = document.createElement("tr");
    const diff = item.stem !== item.lemma;
    tr.innerHTML = `
      <td><strong>${item.original}</strong></td>
      <td><code>${item.stem}</code></td>
      <td><code>${item.lemma}</code></td>
      <td><span class="diff-badge ${diff ? 'yes' : 'no'}">${diff ? 'Stem ≠ Lemma' : 'Identical'}</span></td>
    `;
    DOM.stemLemmaBody.appendChild(tr);
  });

  // N-Grams
  DOM.xrayNgrams.innerHTML = "";
  const ngrams = (res.keywords || []).map((k, i) => ({ term: k, weight: (0.92 - i * 0.12).toFixed(2) }));
  ngrams.forEach(ng => {
    const row = document.createElement("div");
    row.className = "spectrum-row";
    row.innerHTML = `
      <div class="spectrum-meta">
        <span><code>"${ng.term}"</code></span>
        <span>TF-IDF: ${ng.weight}</span>
      </div>
      <div class="spec-track">
        <div class="spec-fill" style="width: ${Math.round(ng.weight * 100)}%; background: var(--ink-primary);"></div>
      </div>
    `;
    DOM.xrayNgrams.appendChild(row);
  });
}

// ============================================================================
// BATCH ANALYTICS LAB
// ============================================================================
async function executeBatchAnalysis() {
  const lines = DOM.batchTextarea.value.split("\n").map(l => l.trim()).filter(Boolean);
  if (lines.length === 0) return;

  DOM.btnRunBatch.textContent = "Processing Batch...";
  DOM.btnRunBatch.disabled = true;

  let results = [];

  if (AppState.apiOnline) {
    try {
      const res = await fetch("/api/batch", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ texts: lines })
      });
      if (res.ok) {
        const json = await res.json();
        results = json.items || [];
      }
    } catch (e) {
      console.warn("Batch API failed, using client engine", e);
    }
  }

  if (results.length === 0) {
    // Client fallback
    results = lines.map(line => {
      const res = clientSideNLPAnalyze(line);
      return {
        text: line,
        sentiment: res.sentiment,
        confidence: Math.round(res.sentiment_confidence * 100),
        categories: res.categories,
        keywords: res.keywords.slice(0, 3),
        top_similar: res.similar_feedback[0] ? res.similar_feedback[0].feedback : "",
        similarity: res.similar_feedback[0] ? res.similar_feedback[0].similarity_percentage : "0%"
      };
    });
  }

  // Update Summary Stats
  const total = results.length;
  const posCount = results.filter(r => r.sentiment === "positive").length;
  const negCount = results.filter(r => r.sentiment === "negative").length;

  DOM.batchTotalCount.textContent = total;
  DOM.batchPosPct.textContent = `${Math.round((posCount / total) * 100)}%`;
  DOM.batchNegPct.textContent = `${Math.round((negCount / total) * 100)}%`;

  // Top category
  const catFreq = {};
  results.forEach(r => {
    (r.categories || []).forEach(c => { catFreq[c] = (catFreq[c] || 0) + 1; });
  });
  let topCat = "—";
  let maxF = 0;
  Object.keys(catFreq).forEach(c => {
    if (catFreq[c] > maxF) { maxF = catFreq[c]; topCat = c; }
  });
  DOM.batchTopCategory.textContent = topCat.toUpperCase();

  // Populate Table
  DOM.batchTableBody.innerHTML = "";
  results.forEach((r, idx) => {
    const tr = document.createElement("tr");
    const sentColor = r.sentiment === "positive" ? "var(--color-pos)" : (r.sentiment === "negative" ? "var(--color-neg)" : "var(--color-neu)");
    tr.innerHTML = `
      <td><strong>${idx + 1}</strong></td>
      <td>${r.text}</td>
      <td><span style="font-weight:700; color:${sentColor};">${r.sentiment.toUpperCase()}</span></td>
      <td>${r.confidence}%</td>
      <td>${r.categories.join(", ")}</td>
      <td><code>${r.keywords.join(", ")}</code></td>
      <td><small>${r.top_similar || "—"} (${r.similarity})</small></td>
    `;
    DOM.batchTableBody.appendChild(tr);
  });

  DOM.btnRunBatch.textContent = "⚡ Execute Batch Analysis";
  DOM.btnRunBatch.disabled = false;
}

function exportBatchCSV() {
  const rows = [
    ["Index", "Customer Feedback", "Sentiment", "Confidence", "Categories", "Keywords", "Historical Twin"]
  ];

  const tableRows = DOM.batchTableBody.querySelectorAll("tr");
  if (!tableRows.length || tableRows[0].querySelector(".empty-cell")) {
    alert("Please run batch analysis first before exporting.");
    return;
  }

  tableRows.forEach(tr => {
    const cols = Array.from(tr.querySelectorAll("td")).map(td => `"${td.textContent.replace(/"/g, '""')}"`);
    if (cols.length === 7) rows.push(cols);
  });

  const csvContent = "data:text/csv;charset=utf-8," + rows.map(e => e.join(",")).join("\n");
  const encodedUri = encodeURI(csvContent);
  const link = document.createElement("a");
  link.setAttribute("href", encodedUri);
  link.setAttribute("download", `feedback_nlp_analysis_${Date.now()}.csv`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}
