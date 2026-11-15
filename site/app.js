const state = { banks: [], training: null, bank: "ccaf", domain: "all", search: "", mode: "study", questions: [], quiz: null, trainingQuiz: null };
const $ = (selector) => document.querySelector(selector);
const escapeHtml = (value) => String(value).replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;" }[char]));

async function init() {
  const response = await fetch("questions.json");
  if (!response.ok) throw new Error(`Could not load question bank (${response.status})`);
  ({ banks: state.banks } = await response.json());
  const trainingResponse = await fetch("training.json");
  if (trainingResponse.ok && $("#training-chapters")) {
    state.training = await trainingResponse.json();
    renderTraining();
  }
  if (!$("#study-view")) return;
  updateSummary();
  renderDomainFilter();
  render();
  document.querySelectorAll("[data-bank]").forEach((button) => button.addEventListener("click", () => {
    state.bank = button.dataset.bank; state.domain = "all"; state.mode = "study";
    document.querySelectorAll("[data-bank]").forEach((item) => item.classList.toggle("active", item === button));
    setModeButtons(); renderDomainFilter(); render();
  }));
  if ($("#search")) $("#search").addEventListener("input", (event) => { state.search = event.target.value.trim().toLowerCase(); render(); });
  if ($("#domain-filter")) $("#domain-filter").addEventListener("change", (event) => { state.domain = event.target.value; render(); });
  if ($("#study-mode")) $("#study-mode").addEventListener("click", () => setMode("study"));
  if ($("#quiz-mode")) $("#quiz-mode").addEventListener("click", () => setMode("quiz"));
  if ($("#random-quiz")) $("#random-quiz").addEventListener("click", () => startQuiz(true));
  if ($("#hero-quiz")) $("#hero-quiz").addEventListener("click", () => { document.querySelector("#study").scrollIntoView(); startQuiz(); });
  if ($("#nav-quiz")) $("#nav-quiz").addEventListener("click", (event) => { event.preventDefault(); startQuiz(); });
  if (document.body.dataset.page === "quiz") startQuiz();
}

function currentBank() { return state.banks.find((bank) => bank.id === state.bank); }
function updateSummary() {
  const total = state.banks.reduce((sum, bank) => sum + bank.questions.length, 0);
  if ($("#total-count")) $("#total-count").textContent = total;
  state.banks.forEach((bank) => { if ($(`#${bank.id}-count`)) $(`#${bank.id}-count`).textContent = bank.questions.length; });
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
  const duration = state.questions.length * 2;
  $("#timer-note").textContent = `Official-guide pacing: 2 minutes per question · ${duration >= 60 ? `${Math.floor(duration / 60)}h ${duration % 60}m` : `${duration}m`} total`;
  $("#empty-state").classList.toggle("hidden", state.questions.length > 0 || state.mode === "quiz");
  $("#study-view").classList.toggle("hidden", state.mode !== "study");
  $("#quiz-view").classList.toggle("hidden", state.mode !== "quiz");
  renderTimerPanel();
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
  if ($("#study-mode")) $("#study-mode").classList.toggle("active", state.mode === "study");
  if ($("#quiz-mode")) $("#quiz-mode").classList.toggle("active", state.mode === "quiz");
}
function startQuiz(timed = false) {
  const pool = [...filteredQuestions()].sort(() => Math.random() - 0.5);
  if (!pool.length) return;
  if (state.quiz?.timerId) clearInterval(state.quiz.timerId);
  state.mode = "quiz"; state.quiz = { questions: pool, index: 0, score: 0, answered: false, timed, paused: false, secondsLeft: timed ? pool.length * 2 * 60 : null, timerId: null };
  if (timed) state.quiz.timerId = setInterval(tickQuizTimer, 1000);
  setModeButtons(); render(); renderQuiz();
  document.querySelector("#study").scrollIntoView({ behavior: "smooth" });
}
function renderQuiz() {
  const quiz = state.quiz; const question = quiz.questions[quiz.index]; const progress = quiz.index / quiz.questions.length * 100;
  const timer = quiz.timed ? "Timed" : "Untimed";
  $("#quiz-view").innerHTML = `<div class="quiz-shell"><div class="quiz-progress"><span>QUESTION ${quiz.index + 1} OF ${quiz.questions.length}</span><span>${quiz.score} correct</span><span>${timer}</span></div><div class="quiz-track"><span style="width:${progress}%"></span></div><h3>${escapeHtml(question.stem)}</h3><div class="quiz-options">${Object.entries(question.options).map(([letter, text]) => `<button class="quiz-option" data-choice="${letter}" type="button"><span class="letter">${letter}</span><span>${escapeHtml(text)}</span></button>`).join("")}</div><div id="quiz-feedback"></div></div>`;
  document.querySelectorAll("[data-choice]").forEach((button) => button.addEventListener("click", () => answerQuiz(button.dataset.choice)));
  renderTimerPanel();
}
function renderTimerPanel() {
  const panel = $("#timer-panel");
  if (!panel) return;
  const quiz = state.quiz;
  const time = quiz?.timed ? formatTime(quiz.secondsLeft) : "Not started";
  const note = quiz?.timed ? (quiz.paused ? "Timer paused — resume when ready." : "Timed quiz in progress.") : "Start a timed quiz at 2 minutes per question.";
  $("#timer-panel-time").textContent = time;
  $("#timer-panel-note").textContent = note;
  const button = $("#random-quiz");
  if (!button) return;
  button.textContent = quiz?.timed ? (quiz.paused ? "Start timer" : "Stop timer") : "Start Timer";
  button.onclick = quiz?.timed ? toggleQuizTimer : () => startQuiz(true);
}
function formatTime(seconds) { const hours = Math.floor(seconds / 3600); const minutes = Math.floor(seconds % 3600 / 60); const remainder = seconds % 60; return hours ? `${String(hours).padStart(2, "0")}:${String(minutes).padStart(2, "0")}:${String(remainder).padStart(2, "0")}` : `${String(minutes).padStart(2, "0")}:${String(remainder).padStart(2, "0")}`; }
function toggleQuizTimer() {
  if (!state.quiz?.timed) return;
  state.quiz.paused = !state.quiz.paused;
  renderQuiz();
}
function tickQuizTimer() {
  const quiz = state.quiz;
  if (!quiz?.timed || quiz.paused) return;
  quiz.secondsLeft--;
  renderTimerPanel();
  if (quiz.secondsLeft <= 0) { clearInterval(quiz.timerId); quiz.timerId = null; showQuizResult(true); }
}
function answerQuiz(choice) {
  const quiz = state.quiz; if (quiz.answered) return; quiz.answered = true;
  const question = quiz.questions[quiz.index]; if (choice === question.correct_answer) quiz.score++;
  document.querySelectorAll("[data-choice]").forEach((button) => { button.disabled = true; if (button.dataset.choice === question.correct_answer) button.classList.add("correct"); else if (button.dataset.choice === choice) button.classList.add("incorrect"); });
  $("#quiz-feedback").innerHTML = `<div class="quiz-feedback"><strong>${choice === question.correct_answer ? "Correct." : `Incorrect — the correct answer is ${question.correct_answer}.`}</strong><br>${escapeHtml(question.explanation)}<br><button class="quiz-next" type="button">${quiz.index + 1 === quiz.questions.length ? "See results" : "Next question →"}</button></div>`;
  $(".quiz-next").addEventListener("click", () => { if (quiz.index + 1 === quiz.questions.length) showQuizResult(); else { quiz.index++; quiz.answered = false; renderQuiz(); } });
}
function showQuizResult(timeExpired = false) {
  const quiz = state.quiz; if (quiz.timerId) { clearInterval(quiz.timerId); quiz.timerId = null; }
  const percent = Math.round(quiz.score / quiz.questions.length * 100);
  $("#quiz-view").innerHTML = `<div class="quiz-shell quiz-result"><p class="eyebrow">${timeExpired ? "Time is up" : "Quiz complete"}</p><strong>${percent}%</strong><p>You answered ${quiz.score} of ${quiz.questions.length} correctly${timeExpired ? " before the timer ended" : ""}.</p><button class="quiz-next" type="button" id="try-again">${quiz.timed ? "Start Timer again" : "Try another quiz"}</button></div>`;
  $("#try-again").addEventListener("click", () => startQuiz(quiz.timed));
}
init().catch((error) => { $("#study-view").innerHTML = `<div class="empty-state"><h3>Question bank unavailable</h3><p>${escapeHtml(error.message)}</p></div>`; });

function renderTraining() {
  const training = state.training;
  const audioCount = training.chapters.reduce((sum, chapter) => sum + chapter.audio.length, 0);
  if ($("#training-count")) $("#training-count").textContent = `${training.chapters.length} chapters · ${audioCount} podcast episodes · ${training.quiz.length} quiz questions`;
  if ($("#training-chapters")) $("#training-chapters").innerHTML = training.chapters.map((chapter) => `
    <article class="chapter-card">
      <div class="chapter-number">0${chapter.number}</div>
      <div class="chapter-body"><p class="chapter-label">Chapter ${chapter.number}</p><h3>${escapeHtml(chapter.title)}</h3>
      <details><summary>Listen to chapter podcast <span>(${chapter.audio.length} episodes)</span></summary>
      <div class="audio-list">${chapter.audio.map((episode) => `<div class="audio-row"><span>${escapeHtml(episode.title)}</span><audio controls preload="none" src="${encodeURI(episode.file)}"></audio></div>`).join("")}</div></details></div>
    </article>`).join("");
  if ($("#material-links")) {
    const samePage = $("#notes-viewer");
    $("#material-links").innerHTML = training.chapters.map((chapter) => `<a href="${encodeURI(chapter.material)}"${samePage ? ` data-note="${encodeURI(chapter.material)}"` : ' target="_blank" rel="noopener"'}><span>Chapter ${chapter.number}</span>${escapeHtml(chapter.title)} <b>↗</b></a>`).join("");
    if (samePage) {
      const links = document.querySelectorAll("[data-note]");
      links.forEach((link) => link.addEventListener("click", (event) => {
        event.preventDefault();
        samePage.src = link.dataset.note;
        links.forEach((item) => item.classList.toggle("selected", item === link));
      }));
      links[0]?.click();
    }
  }
  if ($("#training-quiz-intro")) $("#training-quiz-intro").textContent = `Practice with all ${training.quiz.length} scenario-based questions from the five training domains.`;
  if ($("#training-quiz-start")) $("#training-quiz-start").addEventListener("click", startTrainingQuiz);
}
function startTrainingQuiz() {
  state.trainingQuiz = { questions: [...state.training.quiz].sort(() => Math.random() - 0.5), index: 0, score: 0, answered: false };
  $("#training-quiz-start").classList.add("hidden");
  renderTrainingQuestion();
}
function renderTrainingQuestion() {
  const quiz = state.trainingQuiz; const question = quiz.questions[quiz.index];
  $("#training-quiz-card").classList.remove("hidden");
  $("#training-quiz-card").innerHTML = `<div class="training-quiz-progress">Question ${quiz.index + 1} of ${quiz.questions.length} · ${quiz.score} correct</div><h4>${escapeHtml(question.stem)}</h4><div class="training-options">${question.options.map((option, index) => `<button type="button" class="training-option" data-training-choice="${index}"><span>${String.fromCharCode(65 + index)}</span>${escapeHtml(option)}</button>`).join("")}</div><div id="training-feedback"></div>`;
  document.querySelectorAll("[data-training-choice]").forEach((button) => button.addEventListener("click", () => answerTrainingQuestion(Number(button.dataset.trainingChoice))));
}
function answerTrainingQuestion(choice) {
  const quiz = state.trainingQuiz; if (quiz.answered) return; quiz.answered = true;
  const question = quiz.questions[quiz.index]; const correct = choice === question.correct; if (correct) quiz.score++;
  document.querySelectorAll("[data-training-choice]").forEach((button) => { button.disabled = true; if (Number(button.dataset.trainingChoice) === question.correct) button.classList.add("correct"); else if (Number(button.dataset.trainingChoice) === choice) button.classList.add("incorrect"); });
  $("#training-feedback").innerHTML = `<div class="training-feedback"><strong>${correct ? "Correct." : `The correct answer is ${String.fromCharCode(65 + question.correct)}.`}</strong><br>${escapeHtml(question.explanation)}<br><button class="quiz-next" id="training-next" type="button">${quiz.index + 1 === quiz.questions.length ? "Finish quiz" : "Next question →"}</button></div>`;
  $("#training-next").addEventListener("click", () => { if (quiz.index + 1 === quiz.questions.length) { $("#training-quiz-card").innerHTML = `<div class="training-result"><strong>${quiz.score}/${quiz.questions.length}</strong><p>Keep going — revisit a chapter guide and try again.</p><button class="quiz-next" id="training-retry" type="button">Try another quiz</button></div>`; $("#training-retry").addEventListener("click", startTrainingQuiz); } else { quiz.index++; quiz.answered = false; renderTrainingQuestion(); } });
}
