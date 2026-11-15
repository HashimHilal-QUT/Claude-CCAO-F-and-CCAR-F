"""Build ccar-f-exam-trainer.html from the template, the question bank and the domain digests.

Refuses to build if any question fails the format checks, so a malformed item never reaches the page.
Usage: python build-exam-trainer.py
"""
import importlib.util
import json
import pathlib
import re
import shutil
import subprocess
import sys
from collections import Counter

HERE = pathlib.Path(__file__).parent
BANK_DIR = HERE / "bank"
TEMPLATE = HERE / "exam-trainer-template.html"
OUT = HERE / "ccar-f-exam-trainer.html"
SITE_DIR = HERE.parent / "docs"          # the only folder the DXC GitHub site serves
PODCAST_DIR = SITE_DIR / "podcast"

EXPECTED = {1: 32, 2: 22, 3: 24, 4: 24, 5: 18}
TASKS = {1: 7, 2: 5, 3: 6, 4: 6, 5: 6}
SCENARIOS = {"customer-support", "code-generation", "multi-agent-research",
             "developer-productivity", "ci-cd", "structured-extraction"}
TEXT_FIELDS = ("stem", "explanation", "plainExample", "technicalExample", "concept")


def check(q, d):
    errs = []
    if q.get("domain") != d:
        errs.append("domain")
    t = str(q.get("task", ""))
    if not (t.startswith(f"{d}.") and t[2:].isdigit() and 1 <= int(t[2:]) <= TASKS[d]):
        errs.append(f"task {t!r}")
    if q.get("scenario") not in SCENARIOS:
        errs.append(f"scenario {q.get('scenario')!r}")
    typ = q.get("type")
    opts = q.get("options") or []
    want_opts, want_correct = (5, 2) if typ == "multi" else (4, 1)
    if typ not in ("single", "multi"):
        errs.append("type")
    if len(opts) != want_opts or not all(isinstance(o, str) and o.strip() for o in opts):
        errs.append(f"options x{len(opts)}")
    corr = q.get("correct") or []
    if len(corr) != want_correct or len(set(corr)) != len(corr) or not all(isinstance(i, int) and 0 <= i < len(opts) for i in corr):
        errs.append(f"correct {corr}")
    if len(q.get("whyWrong") or []) != len(opts):
        errs.append("whyWrong length")
    for f in TEXT_FIELDS:
        if not isinstance(q.get(f), str) or not q[f].strip():
            errs.append(f"missing {f}")
    if typ == "multi" and "select two" not in q.get("stem", "").lower():
        errs.append("multi stem lacks (Select TWO.)")
    return errs


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def probe_seconds(path):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                                capture_output=True, text=True, check=True).stdout.strip())


SENTENCE_END = re.compile(r"(?<=[.!?])\s+(?=[\"“(]?[A-Z0-9])|(?<=[.!?][\"”])\s+(?=[\"“]?[A-Z0-9])")


def build_subtitles(gen, ed, chapter_md, items, durations):
    """Timed read-along text for each recorded part, keyed by part index.

    Every recorded request's text and length are known, so where each request starts in the joined part is exact
    (plus the [beat] silences). Only a sentence's position inside one request is estimated, by its spoken length.
    Text shown is the written script (identifiers as spelled), not the spoken form sent to the voice.
    """
    title, sections = ed.parse(chapter_md)
    queue = [(title, ed.spoken(title), False)]      # the chapter title is the first thing the narrator says
    queue += [(raw, ed.spoken(raw), beat) for raw, beat in
             ((x, i > 0 and s["paras"][i - 1] == ed.BEAT) for s in sections for i, x in enumerate(s["paras"])) if raw != ed.BEAT]
    queue.reverse()
    subs = {}
    for p in items:
        if not p["file"].exists() or not all(c["file"].exists() for c in p["chunks"]):
            continue
        paras, t = [], 0.0
        for c in p["chunks"]:
            key = c["file"].name
            if key not in durations:
                durations[key] = probe_seconds(c["file"])
            spoken_paras = c["text"].split("\n\n")
            weights = []
            for sp in spoken_paras:
                raw, want, beat = queue.pop()
                if want != sp:
                    raise SystemExit(f"subtitles: script and recording disagree near {raw[:60]!r}; rebuild the spoken edition")
                sents = [s for s in SENTENCE_END.split(raw) if s.strip()]
                paras.append({"beat": beat, "s": sents})
                weights.append([max(1, len(ed.spoken(s))) for s in sents])
            total = sum(map(sum, weights))
            span, at = durations[key], t
            for para, w in zip(paras[-len(spoken_paras):], weights):
                starts = []
                for x in w:
                    starts.append(at)
                    at += span * x / total
                para["s"] = [[s0, s] for s0, s in zip(starts, para["s"])]
            t += span + (gen.BEAT_SECONDS if c["beat_after"] else 0)
        scale = probe_seconds(p["file"]) / t        # re-encoding shifts each join by a few milliseconds; spread that evenly
        for para in paras:
            para["s"] = [[round(s0 * scale, 1), s] for s0, s in para["s"]]
        subs[p["index"]] = {"v": 1, "paras": paras}
    return subs


def build_podcast():
    """List every chapter and part, and copy finished part audio next to the page.

    Part titles and file names come from the audio generator's own plan, so the two can never disagree.
    """
    gen = load_module("generate_audio", HERE.parent / "podcast-scripts" / "generate-audio.py")
    ed = load_module("elevenlabs_edition", HERE.parent / "podcast-scripts" / "build-elevenlabs-edition.py")
    dur_cache = gen.OUT_DIR / "chunk-durations.json"      # probing hundreds of clips is slow; lengths never change for a given file
    durations = json.loads(dur_cache.read_text(encoding="utf-8")) if dur_cache.exists() else {}
    chapters = []
    for n in range(1, 6):
        src, out, items = gen.plan(n)
        subs = build_subtitles(gen, ed, next(src.parent.parent.glob(f"chapter-{n}-*.md")).read_text(encoding="utf-8"), items, durations)
        title = src.read_text(encoding="utf-8").splitlines()[0].split(":", 1)[-1].strip()
        parts = []
        # Part i of chapter n narrates task statement n.i; part 0 is the domain introduction.
        tasks_line_up = len(items) == TASKS[n] + 1
        if not tasks_line_up:
            print(f"NOTE: chapter {n} has {len(items) - 1} parts for {TASKS[n]} task statements, so its parts get no 'Test me' task")
        for p in items:
            rel = sub_rel = None
            seconds = 0
            if p["file"].exists():
                rel = f"{src.stem}/{p['file'].name}"
                dest = PODCAST_DIR / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                if not dest.exists() or dest.stat().st_mtime < p["file"].stat().st_mtime:
                    shutil.copy2(p["file"], dest)
                seconds = round(probe_seconds(p["file"]))
                if p["index"] in subs:
                    sub_rel = rel[:-4] + ".json"
                    (PODCAST_DIR / sub_rel).write_text(json.dumps(subs[p["index"]], ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
            task = f"{n}.{p['index']}" if tasks_line_up and p["index"] else None
            parts.append({"title": re.sub(r"^Part [a-z\- ]+:\s*", "", p["title"], flags=re.I), "file": rel, "subs": sub_rel,
                          "seconds": seconds, "task": task})
        chapters.append({"n": n, "title": title, "parts": parts})
    dur_cache.write_text(json.dumps(durations, indent=0, sort_keys=True), encoding="utf-8")
    # Remove site audio and subtitles no part points to any more (a renamed part leaves its old files behind otherwise).
    listed = {PODCAST_DIR / p[k] for c in chapters for p in c["parts"] for k in ("file", "subs") if p[k]}
    for f in [*PODCAST_DIR.rglob("*.mp3"), *PODCAST_DIR.rglob("*.json")] if PODCAST_DIR.exists() else []:
        if f not in listed:
            f.unlink()
            print(f"removed stale site audio: {f.relative_to(PODCAST_DIR)}")
    return {"base": "podcast/", "chapters": chapters}


def main():
    bank, digests, problems = [], {}, []
    ids = Counter()
    for d, n in EXPECTED.items():
        qs = json.loads((BANK_DIR / f"d{d}.json").read_text(encoding="utf-8"))
        if len(qs) != n:
            problems.append(f"d{d}.json has {len(qs)} questions, expected {n}")
        for q in qs:
            ids[q.get("id")] += 1
            for e in check(q, d):
                problems.append(f"{q.get('id')}: {e}")
        bank += qs
        digests[str(d)] = (BANK_DIR / f"d{d}-digest.md").read_text(encoding="utf-8").strip()
    problems += [f"duplicate id {i}" for i, c in ids.items() if c > 1]

    # Glossary: every term and alias must actually occur in question text the page underlines.
    gpath = BANK_DIR / "glossary.json"
    glossary = json.loads(gpath.read_text(encoding="utf-8")) if gpath.exists() else []
    if not glossary:
        print("NOTE: no glossary.json yet, so the page will show no term underlines")
    covered = "\n".join(t for q in bank for t in [q.get("stem", ""), q.get("explanation", ""), *(q.get("options") or []), *(q.get("whyWrong") or [])])
    forms_seen = set()
    for g in glossary:
        if not isinstance(g.get("plain"), str) or not g["plain"].strip() or len(g["plain"].split()) > 40:
            problems.append(f"glossary {g.get('term')!r}: plain definition missing or over 40 words")
        for f in [g.get("term", ""), *(g.get("aliases") or [])]:
            key = str(f).lower()
            if not key or key in forms_seen:
                problems.append(f"glossary form {f!r}: empty or duplicated")
            forms_seen.add(key)
            if not re.search(r"(?<![\w.\-/])" + re.escape(f) + r"(?![\w\-])", covered, re.I):
                problems.append(f"glossary form {f!r}: never appears in question text")

    # Length giveaway: is the correct option the single longest one? Chance is ~25% for singles.
    longest = {}
    for d in EXPECTED:
        singles = [q for q in bank if q.get("domain") == d and q.get("type") == "single" and len(q.get("options") or []) == 4]
        hits = 0
        for q in singles:
            lens = [len(o) for o in q["options"]]
            top = max(lens)
            if lens.count(top) == 1 and lens.index(top) in q["correct"]:
                hits += 1
        rate = hits / len(singles) if singles else 0
        longest[d] = f"{hits}/{len(singles)}"
        if rate > 0.5:
            problems.append(f"domain {d}: correct option is the longest in {hits}/{len(singles)} single-answer items (length gives the answer away)")
    if problems:
        print("BUILD REFUSED:\n  " + "\n  ".join(problems))
        sys.exit(1)

    def embed(obj):
        return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")

    podcast = build_podcast()
    html = TEMPLATE.read_text(encoding="utf-8")
    for token in ("__BANK_JSON__", "__DIGESTS_JSON__", "__GLOSSARY_JSON__", "__PODCAST_JSON__"):
        assert html.count(token) == 1, token
    html = html.replace("__BANK_JSON__", embed(bank)).replace("__DIGESTS_JSON__", embed(digests)).replace("__GLOSSARY_JSON__", embed(glossary))
    html = html.replace("__PODCAST_JSON__", embed(podcast))
    OUT.write_text(html, encoding="utf-8")
    SITE_DIR.mkdir(exist_ok=True)
    (SITE_DIR / "index.html").write_text(html, encoding="utf-8")

    pos = Counter(i for q in bank for i in q["correct"] if q["type"] == "single")
    print(f"built {OUT.name}: {len(bank)} questions, {len(glossary)} glossary terms, {OUT.stat().st_size // 1024} KB")
    print("by domain:", dict(Counter(q["domain"] for q in bank)))
    print("by scenario:", dict(Counter(q["scenario"] for q in bank)))
    print("correct option is the longest (chance ~25%):", longest)
    print("multi:", sum(q["type"] == "multi" for q in bank), "| single-answer positions A-D:", [pos[i] for i in range(4)])


if __name__ == "__main__":
    main()
