#!/usr/bin/env python3
"""Extract the UD-CCAR-F question bank from its authoritative DOCX source."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "Udemy-CCAR-F_AI_V7.docx"
DATASET = ROOT / "site" / "ud-ccar-f.json"
REPORT = ROOT / "site" / "ud-ccar-f-import-report.json"
NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
QUESTION_RE = re.compile(r"^Question\s+(\d+):")
TEST_RE = re.compile(r"Practice Test\s+(\d+)")
SCENARIO_RE = re.compile(r"SCENARIO:\s*(.*?)(?=\s+Question\s+\d+:)", re.S)


def value(element: ET.Element | None, name: str) -> str:
    return "" if element is None else element.attrib.get(f"{{{NS['w']}}}{name}", "")


def paragraph_text(paragraph: ET.Element) -> str:
    return "".join(node.text or "" for node in paragraph.findall(".//w:t", NS)).strip()


def is_bold(paragraph: ET.Element) -> bool:
    return any(run.find("w:rPr/w:b", NS) is not None for run in paragraph.findall("w:r", NS))


def numbering_info(numbering: ET.Element) -> dict[str, dict[str, str]]:
    abstract = {}
    for node in numbering.findall("w:abstractNum", NS):
        abstract[value(node, "abstractNumId")] = {
            value(level, "ilvl"): (
                value(level.find("w:numFmt", NS), "val"),
                value(level.find("w:lvlText", NS), "val"),
            )
            for level in node.findall("w:lvl", NS)
        }
    result = {}
    for node in numbering.findall("w:num", NS):
        abstract_id = value(node.find("w:abstractNumId", NS), "val")
        result[value(node, "numId")] = abstract.get(abstract_id, {})
    return result


def paragraph_numbering(paragraph: ET.Element, definitions: dict) -> tuple[str, str, str]:
    num_pr = paragraph.find("w:pPr/w:numPr", NS)
    if num_pr is None:
        return "", "", ""
    level = value(num_pr.find("w:ilvl", NS), "val")
    num_id = value(num_pr.find("w:numId", NS), "val")
    fmt, marker = definitions.get(num_id, {}).get(level, ("", ""))
    return num_id, fmt, marker


def split_question(text: str) -> tuple[str | None, int | None, str]:
    match = QUESTION_RE.match(text)
    if match:
        return None, int(match.group(1)), text[match.end() :].strip()
    if not text.startswith("SCENARIO:"):
        return None, None, text
    scenario_match = re.search(r"\s+(Question\s+\d+:)", text)
    if not scenario_match:
        return None, None, text
    question_match = QUESTION_RE.match(text[scenario_match.start(1) :])
    assert question_match is not None
    return text[len("SCENARIO:") : scenario_match.start()].strip(), int(question_match.group(1)), text[scenario_match.start(1) + question_match.end() :].strip()


def extract() -> tuple[dict, dict]:
    with ZipFile(SOURCE) as archive:
        document = ET.fromstring(archive.read("word/document.xml"))
        numbering = ET.fromstring(archive.read("word/numbering.xml"))

    definitions = numbering_info(numbering)
    paragraphs = document.findall(".//w:body/w:p", NS)
    questions = []
    scenarios: dict[str, dict] = {}
    pending_scenario: str | None = None
    current_test: int | None = None
    current: dict | None = None
    scenario_number = 0
    domain = None
    i = 0

    while i < len(paragraphs):
        paragraph = paragraphs[i]
        text = paragraph_text(paragraph)
        test_match = TEST_RE.search(text)
        if test_match and text.startswith("Practice Test"):
            if current is not None:
                questions.append(current)
            current_test = int(test_match.group(1))
            current = None
            pending_scenario = None
            domain = None
            i += 1
            continue

        scenario, question_number, question_text = split_question(text)
        if question_number is not None:
            if current is not None:
                questions.append(current)
            if scenario:
                scenario_number += 1
                scenario_id = f"UD-CCAR-F-S{scenario_number:02d}"
                scenarios[scenario_id] = {"id": scenario_id, "text": scenario}
                pending_scenario = scenario_id
            current = {
                "id": f"UD-CCAR-F-PT{current_test:02d}-Q{question_number:03d}",
                "examId": "UD-CCAR-F",
                "practiceTest": current_test,
                "questionNumber": question_number,
                "questionType": "single_select",
                "scenarioId": pending_scenario,
                "domain": None,
                "question": question_text,
                "options": [],
                "correctAnswers": [],
                "requiredSelections": 1,
                "explanation": "",
                "sourceNumbering": [],
            }
            domain = None
            i += 1
            continue

        if current is not None and text == "Domain":
            j = i + 1
            while j < len(paragraphs) and not paragraph_text(paragraphs[j]):
                j += 1
            if j < len(paragraphs):
                domain = paragraph_text(paragraphs[j])
                current["domain"] = domain
            i = j + 1
            continue

        if current is not None:
            num_id, fmt, marker = paragraph_numbering(paragraph, definitions)
            if num_id:
                current["options"].append({"id": "", "text": text})
                current["sourceNumbering"].append({"numId": num_id, "format": fmt, "marker": marker})
        i += 1

    if current is not None:
        questions.append(current)

    # Assign stable answer IDs after preserving source order and map bold runs to them.
    # Bold options are collected by position in a second pass to avoid conflating the
    # paragraph text with Word's list marker.
    for question in questions:
        for index, option in enumerate(question["options"]):
            option["id"] = chr(ord("A") + index)

    # Re-read option boldness directly, preserving the parser's Word-level evidence.
    # This pass is intentionally separate from text extraction for maintainability.
    question_index = -1
    current_test = None
    for paragraph in paragraphs:
        text = paragraph_text(paragraph)
        test_match = TEST_RE.search(text)
        if test_match and text.startswith("Practice Test"):
            current_test = int(test_match.group(1))
        _, question_number, _ = split_question(text)
        if question_number is not None:
            question_index += 1
            continue
        if question_index < 0 or question_index >= len(questions):
            continue
        if paragraph_numbering(paragraph, definitions)[0]:
            options = questions[question_index]["sourceNumbering"]
            seen = questions[question_index].setdefault("_seen_options", 0)
            if seen < len(options):
                options[seen]["bold"] = is_bold(paragraph)
                questions[question_index]["_seen_options"] = seen + 1

    native_alphabetical_options = sum(
        metadata["format"] in {"lowerLetter", "upperLetter"}
        for question in questions
        for metadata in question["sourceNumbering"]
    )
    for question in questions:
        question.pop("_seen_options", None)
        for index, metadata in enumerate(question["sourceNumbering"]):
            if metadata.pop("bold", False) and chr(ord("A") + index) not in question["correctAnswers"]:
                question["correctAnswers"].append(chr(ord("A") + index))
        question["correctAnswers"].sort()
        question["questionType"] = "multiple_select" if len(question["correctAnswers"]) > 1 else "single_select"
        question["requiredSelections"] = len(question["correctAnswers"]) or 1
        question["scorable"] = len(question["options"]) == 4 and bool(question["correctAnswers"])
        question["reviewReasons"] = []
        if len(question["options"]) != 4:
            question["reviewReasons"].append(f"unexpected answer choice count: {len(question['options'])}")
        if not question["correctAnswers"]:
            question["reviewReasons"].append("missing answer key")

    for question in questions:
        question.pop("sourceNumbering", None)

    test_counts = Counter(q["practiceTest"] for q in questions)
    domain_counts = Counter(q["domain"] or "Unclassified" for q in questions)
    review = [q["id"] for q in questions if not q["scorable"]]
    dataset = {
        "id": "ud-ccar-f",
        "name": "Claude Certified Architect Foundations - Udemy Practice Exams",
        "short_name": "UD-CCAR-F",
        "description": "Claude Certified Architect Foundations – Udemy Practice Exams",
        "domains": [{"id": name, "name": name} for name in sorted(domain_counts) if name != "Unclassified"],
        "practiceTests": [{"id": n, "name": f"Practice Test {n}", "questionCount": test_counts[n]} for n in sorted(test_counts)],
        "scenarios": list(scenarios.values()),
        "questions": questions,
    }
    report = {
        "source": SOURCE.name,
        "questionsExtracted": len(questions),
        "questionsPerPracticeTest": dict(sorted(test_counts.items())),
        "totalAnswerChoices": sum(len(q["options"]) for q in questions),
        "nativeAlphabeticalNumberedOptions": native_alphabetical_options,
        "singleSelectQuestions": sum(q["questionType"] == "single_select" for q in questions),
        "multiSelectQuestions": sum(q["questionType"] == "multiple_select" for q in questions),
        "confirmedCorrectAnswers": sum(bool(q["correctAnswers"]) for q in questions),
        "missingOrAmbiguousAnswerKeys": [q["id"] for q in questions if not q["correctAnswers"]],
        "uniqueScenarios": len(scenarios),
        "questionsByDomain": dict(sorted(domain_counts.items())),
        "questionsRequiringManualReview": review,
        "reviewDetails": {q["id"]: q["reviewReasons"] for q in questions if q["reviewReasons"]},
        "duplicateQuestionIds": [key for key, count in Counter(q["id"] for q in questions).items() if count > 1],
        "residualCorrectSelectionLabels": [],
    }
    return dataset, report


def main() -> int:
    dataset, report = extract()
    DATASET.write_text(json.dumps(dataset, ensure_ascii=False, separators=(",", ":")) + "\n")
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
