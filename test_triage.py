import subprocess
import unittest
from unittest.mock import patch
from triage import classify


class ClassificationTests(unittest.TestCase):
    @patch("triage.subprocess.run")
    def test_valid_labels(self, run):
        for label in ("paid_unclear", "fraud_unclear", "other"):
            with self.subTest(label=label):
                run.return_value = subprocess.CompletedProcess(
                    args=[], returncode=0, stdout=label + "\n"
                )
                result = classify("Example note")
                self.assertEqual(result["label"], label)
                self.assertEqual(result["status"], "ok")
                self.assertEqual(run.call_args.kwargs["timeout"], 60)
                self.assertTrue(run.call_args.kwargs["check"])

    @patch("triage.subprocess.run")
    def test_invalid_output(self, run):
        for answer in ("", "close the case", "other\nextra text"):
            with self.subTest(answer=answer):
                run.return_value = subprocess.CompletedProcess(
                    args=[], returncode=0, stdout=answer
                )
                result = classify("Example note")
                self.assertEqual(result["label"], "manual_review")
                self.assertEqual(result["status"], "invalid_output")

    @patch("triage.subprocess.run")
    def test_timeout(self, run):
        run.side_effect = subprocess.TimeoutExpired("ollama", 60)
        result = classify("Example note")
        self.assertEqual(result["label"], "manual_review")
        self.assertEqual(result["status"], "timeout")

    @patch("triage.subprocess.run")
    def test_process_failure(self, run):
        run.side_effect = subprocess.CalledProcessError(1, "ollama")
        result = classify("Example note")
        self.assertEqual(result["label"], "manual_review")
        self.assertEqual(result["status"], "error")

    @patch("triage.subprocess.run")
    def test_missing_executable(self, run):
        run.side_effect = FileNotFoundError("ollama")
        result = classify("Example note")
        self.assertEqual(result["label"], "manual_review")
        self.assertEqual(result["status"], "error")


if __name__ == "__main__":
    unittest.main()
