const state = { banks: [], bank: "ccaf", domain: "all", search: "", mode: "study", questions: [], quiz: null };
const $ = (selector) => document.querySelector(selector);
const escapeHtml = (value) => String(value).replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;" }[char]));

async function init() {
  const response = await fetch("questions.json");
  if (!response.ok) throw new Error(`Could not load question bank (${response.status})`);
  ({ banks: state.banks } = await response.json());
  updateSummary();
  renderDomainFilter();
  render();
  document.querySelectorAll("[data-bank]").forEach((button) => button.addEventListener("click", () => {
    state.bank = button.dataset.bank; state.domain = "all"; state.mode = "study";
    document.querySelectorAll("[data-bank]").forEach((item) => item.classList.toggle("active", item === button));
    setModeButtons(); renderDomainFilter(); render();
  }));
  $("#search").addEventListener("input", (event) => { state.search = event.target.value.trim().toLowerCase(); render(); });
  $("#domain-filter").addEventListener("change", (event) => { state.domain = event.target.value; render(); });
  $("#study-mode").addEventListener("click", () => setMode("study"));
  $("#quiz-mode").addEventListener("click", () => setMode("quiz"));
  $("#random-quiz").addEventListener("click", startQuiz);
  $("#hero-quiz").addEventListener("click", () => { document.querySelector("#study").scrollIntoView(); startQuiz(); });
}

function currentBank() { return state.banks.find((bank) => bank.id === state.bank); }
function updateSummary() {
  const total = state.banks.reduce((sum, bank) => sum + bank.questions.length, 0);
  $("#total-count").textContent = total;
  state.banks.forEach((bank) => { $(`#${bank.id}-count`).textContent = bank.questions.length; });
}
function renderDomainFilter() {
  $("#domain-filter").innerHTML = `<option value="all">All domains</option>` +
    currentBank().domains.map((domain) => `<option value="${domain.id}">Domain ${domain.id}: ${escapeHtml(domain.name)}</option>`).join("");
  $("#domain-filter").value = state.domain;
}
function filteredQuestions() {
  return currentBank().questions.filter((question) => {
    const text = `${question.stem} ${question.explanation} ${Object.values(question.options).join(" ")}`.toLowerCase();
    return (state.domain === "all" || String(question.domain_id) === state.domain) && (!state.search || text.includes(state.search));
  });
}
function render() {
  state.questions = filteredQuestions();
  $("#results-count").textContent = `${state.questions.length} question${state.questions.length === 1 ? "" : "s"}`;
  $("#empty-state").classList.toggle("hidden", state.questions.length > 0 || state.mode === "quiz");
  $("#study-view").classList.toggle("hidden", state.mode !== "study");
  $("#quiz-view").classList.toggle("hidden", state.mode !== "quiz");
  if (state.mode === "study") renderStudy();
}
function renderStudy() {
  $("#study-view").innerHTML = state.questions.map((question, index) => {
    const options = Object.entries(question.options).map(([letter, text]) =>
      `<div class="option"><span class="letter">${letter}</span><span>${escapeHtml(text)}</span></div>`).join("");
    return `<article class="question-card"><div class="question-meta"><span>Domain ${question.domain_id} · ${escapeHtml(question.domain_name)}</span><span class="question-number">#${index + 1}</span></div><h3>${escapeHtml(question.stem)}</h3><div class="options">${options}</div><button class="reveal" type="button" data-answer="${question.id}">Show answer & rationale ↓</button><div class="answer-panel hidden" id="answer-${question.id}"><strong>Correct answer: ${question.correct_answer}</strong><br>${escapeHtml(question.explanation)}</div></article>`;
  }).join("");
  document.querySelectorAll("[data-answer]").forEach((button) => button.addEventListener("click", () => {
    const panel = $(`#answer-${button.dataset.answer}`);
    panel.classList.toggle("hidden");
    button.textContent = panel.classList.contains("hidden") ? "Show answer & rationale ↓" : "Hide answer ↑";
  }));
}
function setMode(mode) {
  state.mode = mode; setModeButtons();
  if (mode === "quiz") startQuiz(); else render();
}
function setModeButtons() {
  $("#study-mode").classList.toggle("active", state.mode === "study");
  $("#quiz-mode").classList.toggle("active", state.mode === "quiz");
}
function startQuiz() {
  const pool = [...filteredQuestions()].sort(() => Math.random() - 0.5).slice(0, 10);
  if (!pool.length) return;
  state.mode = "quiz"; state.quiz = { questions: pool, index: 0, score: 0, answered: false };
  setModeButtons(); render(); renderQuiz();
  document.querySelector("#study").scrollIntoView({ behavior: "smooth" });
}
function renderQuiz() {
  const quiz = state.quiz; const question = quiz.questions[quiz.index]; const progress = quiz.index / quiz.questions.length * 100;
  $("#quiz-view").innerHTML = `<div class="quiz-shell"><div class="quiz-progress"><span>QUESTION ${quiz.index + 1} OF ${quiz.questions.length}</span><span>${quiz.score} correct</span></div><div class="quiz-track"><span style="width:${progress}%"></span></div><h3>${escapeHtml(question.stem)}</h3><div class="quiz-options">${Object.entries(question.options).map(([letter, text]) => `<button class="quiz-option" data-choice="${letter}" type="button"><span class="letter">${letter}</span><span>${escapeHtml(text)}</span></button>`).join("")}</div><div id="quiz-feedback"></div></div>`;
  document.querySelectorAll("[data-choice]").forEach((button) => button.addEventListener("click", () => answerQuiz(button.dataset.choice)));
}
function answerQuiz(choice) {
  const quiz = state.quiz; if (quiz.answered) return; quiz.answered = true;
  const question = quiz.questions[quiz.index]; if (choice === question.correct_answer) quiz.score++;
  document.querySelectorAll("[data-choice]").forEach((button) => { button.disabled = true; if (button.dataset.choice === question.correct_answer) button.classList.add("correct"); else if (button.dataset.choice === choice) button.classList.add("incorrect"); });
  $("#quiz-feedback").innerHTML = `<div class="quiz-feedback"><strong>${choice === question.correct_answer ? "Correct." : `Not quite — the answer is ${question.correct_answer}.`}</strong><br>${escapeHtml(question.explanation)}<br><button class="quiz-next" type="button">${quiz.index + 1 === quiz.questions.length ? "See results" : "Next question →"}</button></div>`;
  $(".quiz-next").addEventListener("click", () => { if (quiz.index + 1 === quiz.questions.length) showQuizResult(); else { quiz.index++; quiz.answered = false; renderQuiz(); } });
}
function showQuizResult() {
  const quiz = state.quiz; const percent = Math.round(quiz.score / quiz.questions.length * 100);
  $("#quiz-view").innerHTML = `<div class="quiz-shell quiz-result"><p class="eyebrow">Quiz complete</p><strong>${percent}%</strong><p>You answered ${quiz.score} of ${quiz.questions.length} correctly.</p><button class="quiz-next" type="button" id="try-again">Try another quiz</button></div>`;
  $("#try-again").addEventListener("click", startQuiz);
}
init().catch((error) => { $("#study-view").innerHTML = `<div class="empty-state"><h3>Question bank unavailable</h3><p>${escapeHtml(error.message)}</p></div>`; });
