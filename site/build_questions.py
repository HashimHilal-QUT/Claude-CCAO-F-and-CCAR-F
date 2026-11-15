#!/usr/bin/env python3
"""Build the browser-ready question dataset from the source JSONL banks."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "site" / "questions.json"
BANKS = {
    "ccaf": {
        "name": "Claude Certified Architect - Foundations",
        "short_name": "CCAR-F",
        "source": ROOT / "ccaf" / "jsonl",
    },
    "ccao": {
        "name": "Claude Certified Associate - Foundations",
        "short_name": "CCAO-F",
        "source": ROOT / "ccao" / "jsonl",
    },
}


def domain_name(path: Path) -> str:
    name = path.stem.split("_", 1)[1].replace("_", " ")
    return name.replace("mcp", "MCP").title()


def load_bank(bank_id: str, config: dict) -> dict:
    questions = []
    domains = []
    for path in sorted(config["source"].glob("domain*.jsonl")):
        domain_id = int(path.stem.split("_", 1)[0].replace("domain", ""))
        domains.append({"id": domain_id, "name": domain_name(path)})
        for line in path.read_text().splitlines():
            question = json.loads(line)
            question["bank"] = bank_id
            question["domain_name"] = domain_name(path)
            questions.append(question)
    return {
        "id": bank_id,
        "name": config["name"],
        "short_name": config["short_name"],
        "domains": domains,
        "questions": questions,
    }


def main() -> None:
    payload = {"banks": [load_bank(bank_id, config) for bank_id, config in BANKS.items()]}
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
    print(f"Wrote {OUTPUT} ({sum(len(bank['questions']) for bank in payload['banks'])} questions)")


if __name__ == "__main__":
    main()
