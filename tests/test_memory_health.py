#!/usr/bin/env python3
"""Unit tests for scripts/memory_health.py.

Run with: python -m unittest discover -s tests
"""
import os
import sys
import tempfile
import unittest
from io import StringIO
from pathlib import Path

# Add repo root to path so we can import the script under test.
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import memory_health  # noqa: E402


class TestParsers(unittest.TestCase):
    def test_parse_files(self):
        self.assertEqual(
            memory_health.parse_files("A.md:limit_a,B.md:limit_b"),
            {"A.md": "limit_a", "B.md": "limit_b"},
        )

    def test_parse_files_invalid(self):
        with self.assertRaises(ValueError):
            memory_health.parse_files("A.md")

    def test_parse_limits(self):
        limits = memory_health.parse_limits("memory_char_limit=1000,user_char_limit=500")
        self.assertEqual(limits["memory_char_limit"], 1000)
        self.assertEqual(limits["user_char_limit"], 500)

    def test_parse_limits_invalid(self):
        with self.assertRaises(ValueError):
            memory_health.parse_limits("memory_char_limit")


class TestAnalyze(unittest.TestCase):
    def test_empty_path_returns_none(self):
        self.assertIsNone(memory_health.analyze("/nonexistent/path.md", 1000, "\n"))

    def test_basic_stats(self):
        content = "entry one\n\u00a7entry two\n\u00a7entry three"
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", suffix=".md", delete=False
        ) as f:
            f.write(content)
            path = f.name
        try:
            result = memory_health.analyze(path, 1000, "\n\u00a7")
            self.assertEqual(result["entries"], 3)
            self.assertEqual(result["chars"], len(content))
            self.assertEqual(result["pct"], round(len(content) / 1000 * 100, 1))
        finally:
            os.unlink(path)

    def test_flags_year_and_overlong(self):
        content = "short 2023 note\n\u00a7" + "x" * 350
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", suffix=".md", delete=False
        ) as f:
            f.write(content)
            path = f.name
        try:
            result = memory_health.analyze(path, 1000, "\n\u00a7")
            self.assertEqual(len(result["flags"]), 2)
            flag_texts = [fl for _, fl in result["flags"]]
            self.assertTrue(any("2023" in fl for fl in flag_texts))
            self.assertTrue(any("超长" in fl for fl in flag_texts))
        finally:
            os.unlink(path)


class TestMain(unittest.TestCase):
    def run_main(self, argv):
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        try:
            code = memory_health.main(argv)
            output = sys.stdout.getvalue()
        finally:
            sys.stdout = old_stdout
        return code, output

    def test_main_no_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            code, output = self.run_main(["--mem-dir", tmpdir, "--no-config"])
            self.assertEqual(code, 0)
            self.assertIn("NO_MEMORY_FILES", output)

    def test_main_with_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "MEMORY.md")
            with open(path, "w", encoding="utf-8") as f:
                f.write("entry one\n\u00a7entry two 2024\n\u00a7" + "x" * 350)
            code, output = self.run_main(
                [
                    "--mem-dir",
                    tmpdir,
                    "--files",
                    "MEMORY.md:memory_char_limit",
                    "--limits",
                    "memory_char_limit=1000",
                    "--no-config",
                ]
            )
            self.assertEqual(code, 0)
            self.assertIn("MEMORY.md", output)
            self.assertIn("3 entries", output)
            self.assertIn("FLAG: 含日期2024", output)
            self.assertIn("FLAG: 超长>300", output)


if __name__ == "__main__":
    unittest.main()
