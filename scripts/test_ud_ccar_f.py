#!/usr/bin/env python3
"""Focused regression checks for the UD-CCAR-F DOCX import."""

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class UdCcArFImportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dataset = json.loads((ROOT / "site" / "ud-ccar-f.json").read_text())
        cls.report = json.loads((ROOT / "site" / "ud-ccar-f-import-report.json").read_text())

    def test_complete_practice_test_and_scenario_counts(self):
        self.assertEqual(len(self.dataset["questions"]), 360)
        self.assertEqual([test["questionCount"] for test in self.dataset["practiceTests"]], [60] * 6)
        self.assertEqual(len(self.dataset["scenarios"]), 6)

    def test_word_answer_keys_support_single_and_multiple_select(self):
        self.assertEqual(self.report["singleSelectQuestions"], 283)
        self.assertEqual(self.report["multiSelectQuestions"], 77)
        self.assertTrue(any(len(q["correctAnswers"]) > 1 for q in self.dataset["questions"]))
        self.assertTrue(all(q["correctAnswers"] for q in self.dataset["questions"]))

    def test_unusual_choice_counts_are_review_only(self):
        review_ids = set(self.report["questionsRequiringManualReview"])
        self.assertEqual(
            review_ids,
            {
                "UD-CCAR-F-PT06-Q030",
                "UD-CCAR-F-PT06-Q059",
                "UD-CCAR-F-PT06-Q060",
            },
        )
        self.assertTrue(all(not q["scorable"] for q in self.dataset["questions"] if q["id"] in review_ids))
        self.assertTrue(all(q["scorable"] for q in self.dataset["questions"] if q["id"] not in review_ids))

    def test_ids_and_answer_order_are_unique_and_stable(self):
        questions = self.dataset["questions"]
        self.assertEqual(len({q["id"] for q in questions}), len(questions))
        self.assertEqual(sum(len(q["options"]) for q in questions), self.report["totalAnswerChoices"])
        self.assertEqual(questions[0]["options"][0]["id"], "A")
        self.assertEqual(questions[0]["options"][1]["id"], "B")
        self.assertGreater(self.report["nativeAlphabeticalNumberedOptions"], 0)

    def test_navigation_opens_the_selected_quiz_bank_directly(self):
        destination = 'href="ud-ccar-f-quiz.html"'
        for page in ("index.html", "study.html", "quiz.html", "ud-ccar-f-quiz.html"):
            html = (ROOT / "site" / page).read_text()
            self.assertIn(destination, html, page)
            self.assertIn("UD-CCAR-F 360-Question Quiz", html, page)
        quiz_hub = (ROOT / "site" / "quiz.html").read_text()
        self.assertNotIn('data-bank="ud-ccar-f"', quiz_hub)
        self.assertIn('data-page="ud-ccar-f-quiz"', (ROOT / "site" / "ud-ccar-f-quiz.html").read_text())


if __name__ == "__main__":
    unittest.main()
