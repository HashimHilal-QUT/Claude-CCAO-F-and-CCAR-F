#!/usr/bin/env python3
"""Build the compact training catalog from the local CCAR-F_Training materials."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRAINING = ROOT / "CCAR-F_Training"
OUTPUT = ROOT / "site" / "training.json"
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


def build() -> dict:
    chapters = []
    for number, (title, slug) in CHAPTERS.items():
        podcast_dir = TRAINING / "docs" / "podcast" / slug
        audio = []
        for path in sorted(podcast_dir.glob("*.mp3")):
            audio.append({"title": title_from_filename(path), "file": f"training/podcast/{slug}/{path.name}"})
        script = TRAINING / "podcast-scripts" / f"{slug}.md"
        chapters.append({
            "number": number,
            "title": title,
            "slug": slug,
            "audio": audio,
            "material": f"training/material/{script.name}",
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
