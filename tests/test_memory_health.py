#!/usr/bin/env python3
"""Unit tests for scripts/memory_health.py.

Run with: python -m unittest discover -s tests
"""
import json
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

DELIM = "\n§"


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


class TestClassify(unittest.TestCase):
    def test_boundaries(self):
        self.assertEqual(memory_health.classify(84.9), "HEALTHY")
        self.assertEqual(memory_health.classify(85.0), "REVIEW")
        self.assertEqual(memory_health.classify(95.0), "REVIEW")
        self.assertEqual(memory_health.classify(95.1), "URGENT")

    def test_analyze_includes_status(self):
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", suffix=".md", delete=False
        ) as f:
            f.write("x" * 960)  # 96% of 1000 => URGENT
            path = f.name
        try:
            result = memory_health.analyze(path, 1000, DELIM)
            self.assertEqual(result["status"], "URGENT")
        finally:
            os.unlink(path)


class TestAnalyze(unittest.TestCase):
    def test_empty_path_returns_none(self):
        self.assertIsNone(memory_health.analyze("/nonexistent/path.md", 1000, "\n"))

    def test_basic_stats(self):
        content = "entry one\n§entry two\n§entry three"
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", suffix=".md", delete=False
        ) as f:
            f.write(content)
            path = f.name
        try:
            result = memory_health.analyze(path, 1000, DELIM)
            self.assertEqual(result["entries"], 3)
            self.assertEqual(result["chars"], len(content))
            self.assertEqual(result["pct"], round(len(content) / 1000 * 100, 1))
            self.assertEqual(result["status"], "HEALTHY")
        finally:
            os.unlink(path)

    def test_flags_year_and_overlong(self):
        content = "short 2023 note\n§" + "x" * 350
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", suffix=".md", delete=False
        ) as f:
            f.write(content)
            path = f.name
        try:
            result = memory_health.analyze(path, 1000, DELIM)
            self.assertEqual(len(result["flags"]), 2)
            marks = [m for flag in result["flags"] for m in flag["marks"]]
            self.assertTrue(any("2023" in m for m in marks))
            self.assertTrue(any("超长" in m for m in marks))
            # 1-based entry index locates each flagged entry.
            self.assertEqual(result["flags"][0]["index"], 1)
            self.assertEqual(result["flags"][1]["index"], 2)
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

    def write_memory(self, tmpdir, content, name="MEMORY.md"):
        path = os.path.join(tmpdir, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    def default_argv(self, tmpdir):
        return [
            "--mem-dir",
            tmpdir,
            "--files",
            "MEMORY.md:memory_char_limit",
            "--limits",
            "memory_char_limit=1000",
            "--no-config",
        ]

    def test_main_no_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            code, output = self.run_main(["--mem-dir", tmpdir, "--no-config"])
            self.assertEqual(code, 0)
            self.assertIn("NO_MEMORY_FILES", output)

    def test_main_with_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self.write_memory(tmpdir, "entry one\n§entry two 2024\n§" + "x" * 950)
            code, output = self.run_main(self.default_argv(tmpdir))
            self.assertEqual(code, 0)
            self.assertIn("MEMORY.md", output)
            self.assertIn("3 entries", output)
            # Status label and 1-based flag index appear in the output.
            self.assertIn("URGENT", output)
            self.assertIn("FLAG #2: 含日期2024", output)
            self.assertIn("FLAG #3: 超长>300", output)

    def test_main_status_healthy(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self.write_memory(tmpdir, "small entry")
            code, output = self.run_main(self.default_argv(tmpdir))
            self.assertEqual(code, 0)
            self.assertIn("HEALTHY", output)

    def test_main_strict_exit_zero_when_healthy(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self.write_memory(tmpdir, "small entry")
            code, _ = self.run_main(self.default_argv(tmpdir) + ["--strict"])
            self.assertEqual(code, 0)

    def test_main_strict_exit_one_when_urgent(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self.write_memory(tmpdir, "x" * 960)  # 96% => URGENT
            code, _ = self.run_main(self.default_argv(tmpdir) + ["--strict"])
            self.assertEqual(code, 1)

    def test_main_not_strict_exit_zero_when_urgent(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self.write_memory(tmpdir, "x" * 960)
            code, _ = self.run_main(self.default_argv(tmpdir))
            self.assertEqual(code, 0)

    def test_main_json_output(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self.write_memory(tmpdir, "entry 2024\n§" + "x" * 950)
            code, output = self.run_main(self.default_argv(tmpdir) + ["--json"])
            self.assertEqual(code, 0)
            report = json.loads(output)
            self.assertEqual(report["worst_status"], "URGENT")
            self.assertFalse(report["strict"])
            self.assertEqual(len(report["files"]), 1)
            f0 = report["files"][0]
            self.assertEqual(f0["file"], "MEMORY.md")
            self.assertEqual(f0["status"], "URGENT")
            self.assertEqual(f0["flags"][0]["index"], 1)
            self.assertIn("含日期2024", f0["flags"][0]["marks"])

    def test_main_json_no_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            code, output = self.run_main(
                ["--mem-dir", tmpdir, "--no-config", "--json"]
            )
            self.assertEqual(code, 0)
            report = json.loads(output)
            self.assertEqual(report["files"], [])
            self.assertIsNone(report["worst_status"])


if __name__ == "__main__":
    unittest.main()
