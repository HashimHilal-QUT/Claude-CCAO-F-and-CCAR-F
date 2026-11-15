#!/usr/bin/env python3
"""Build the compact training catalog from the local CCAR-F_Training materials."""

from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRAINING = ROOT / "CCAR-F_Training"
OUTPUT = ROOT / "site" / "training.json"
MATERIAL_OUTPUT = ROOT / "site" / "training" / "material"
CHAPTERS = {
    1: ("Agentic Architecture & Orchestration", "chapter-1-agentic-architecture-and-orchestration"),
    2: ("Tool Design & MCP Integration", "chapter-2-tool-design-and-mcp-integration"),
    3: ("Claude Code Configuration & Workflows", "chapter-3-claude-code-configuration-and-workflows"),
    4: ("Prompt Engineering & Structured Output", "chapter-4-prompt-engineering-and-structured-output"),
    5: ("Context Management & Reliability", "chapter-5-context-management-and-reliability"),
}


def title_from_filename(path: Path) -> str:
    value = path.stem.replace("-", " ")
    value = re.sub(r"^part \d+ ", "", value)
    return value.title()


def inline_markup(text: str) -> str:
    text = escape(text)
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", text)


def render_markdown(source: str, title: str) -> str:
    body = []
    paragraph = []
    for line in source.splitlines():
        if line.startswith("# "):
            continue
        if line.startswith("## "):
            if paragraph:
                body.append(f"<p>{' '.join(paragraph)}</p>")
                paragraph = []
            body.append(f"<h2>{inline_markup(line[3:])}</h2>")
        elif line.strip() == "[beat]":
            if paragraph:
                body.append(f"<p>{' '.join(paragraph)}</p>")
                paragraph = []
            body.append('<div class="beat" aria-hidden="true"><span></span><span></span><span></span></div>')
        elif line.strip():
            paragraph.append(inline_markup(line.strip()))
        elif paragraph:
            body.append(f"<p>{' '.join(paragraph)}</p>")
            paragraph = []
    if paragraph:
        body.append(f"<p>{' '.join(paragraph)}</p>")
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)} | Claude Foundations</title><style>
:root{{--ink:#17201f;--muted:#66716f;--paper:#f6f7f3;--green:#1d6b58;--mint:#dcefe5;--line:#dfe4df}}
*{{box-sizing:border-box}}body{{margin:0;background:linear-gradient(135deg,#f6f7f3,#e8f1eb);color:var(--ink);font:17px/1.8 "Georgia",serif}}
.shell{{max-width:820px;margin:auto;padding:50px 28px 90px}}header{{padding:22px 0 42px;border-bottom:1px solid var(--line);margin-bottom:38px}}
.back{{font:11px ui-monospace,monospace;text-transform:uppercase;letter-spacing:.1em;color:var(--green);text-decoration:none}}
.eyebrow{{font:11px ui-monospace,monospace;text-transform:uppercase;letter-spacing:.15em;color:var(--green);margin:38px 0 12px}}
h1{{font:600 clamp(38px,6vw,64px)/1.08 Georgia,serif;letter-spacing:-.04em;margin:0;max-width:720px}}
h2{{font:600 27px/1.2 Georgia,serif;letter-spacing:-.025em;margin:48px 0 14px;color:var(--green-dark,#134b3f)}}
p{{max-width:70ch;margin:0 0 20px}}code{{background:var(--mint);border-radius:4px;padding:2px 5px;font:14px ui-monospace,monospace}}
.beat{{display:flex;gap:6px;margin:27px 0;align-items:center}}.beat span{{display:block;width:5px;height:5px;border-radius:50%;background:#a6bcb0}}
footer{{border-top:1px solid var(--line);margin-top:60px;padding-top:20px;color:var(--muted);font:11px ui-monospace,monospace}}
@media(max-width:600px){{.shell{{padding:25px 20px 60px}}body{{font-size:16px}}h2{{font-size:24px}}}}
</style></head><body><main class="shell"><header><a class="back" href="../../../#training">← Back to training hub</a>
<p class="eyebrow">CCAR-F chapter guide</p><h1>{escape(title)}</h1></header>{''.join(body)}
<footer>Claude Foundations · Exam preparation companion material</footer></main></body></html>"""


def build() -> dict:
    chapters = []
    for number, (title, slug) in CHAPTERS.items():
        podcast_dir = TRAINING / "docs" / "podcast" / slug
        audio = []
        for path in sorted(podcast_dir.glob("*.mp3")):
            audio.append({"title": title_from_filename(path), "file": f"training/podcast/{slug}/{path.name}"})
        script = TRAINING / "podcast-scripts" / f"{slug}.md"
        rendered = MATERIAL_OUTPUT / f"{script.stem}.html"
        rendered.parent.mkdir(parents=True, exist_ok=True)
        rendered.write_text(render_markdown(script.read_text(), title))
        chapters.append({
            "number": number,
            "title": title,
            "slug": slug,
            "audio": audio,
            "material": f"training/material/{rendered.name}",
        })

    quizzes = []
    for path in sorted((TRAINING / "exam-trainer" / "bank").glob("d[1-5].json")):
        for question in json.loads(path.read_text()):
            quizzes.append({
                "id": question["id"],
                "domain": question["domain"],
                "stem": question["stem"],
                "options": question["options"],
                "correct": question["correct"][0],
                "explanation": question["explanation"],
            })
    return {"chapters": chapters, "quiz": quizzes}


if __name__ == "__main__":
    payload = build()
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
    print(f"Wrote {OUTPUT} ({len(payload['chapters'])} chapters, {len(payload['quiz'])} quiz questions)")
