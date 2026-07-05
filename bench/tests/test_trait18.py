"""Tests for the PACKET-018 trait harness. Stub runner, temp runs dir,
no model calls."""

import importlib
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import runner


class _TraitHarness(unittest.TestCase):

    def setUp(self):
        self._real_runs = runner.RUNS
        self._real_run_once = runner.run_once
        self._tmp = tempfile.TemporaryDirectory()
        runner.RUNS = self._tmp.name
        import trait18
        self.tr = importlib.reload(trait18)

    def tearDown(self):
        runner.RUNS = self._real_runs
        runner.run_once = self._real_run_once
        importlib.reload(self.tr)
        self._tmp.cleanup()

    def _stub_run(self):
        calls = []

        def stub(task, criteria, work_features, **kw):
            calls.append({"landscape": kw.get("landscape"),
                          "model": kw.get("model")})
            return {"run_id": f"stub-{len(calls)}", "verdict": "pass",
                    "evidence": {"passed": True,
                                 "results": [{"ok": True, "call": "f(1)",
                                              "got": "1", "expect": "1"}],
                                 "error": None}}

        runner.run_once = stub
        return calls


class TestTrait18(_TraitHarness):

    def test_byte_check_and_store(self):
        self.assertTrue(self.tr.byte_check())
        lessons = self.tr.load_store()
        self.assertEqual(len(lessons), 2)
        for l in lessons:
            aw = l["applies_when"]
            self.assertEqual(aw["rule_class"], "tie_break")
            self.assertEqual(aw["stated_direction"], "last")

    def test_both_lessons_ride_longest_word(self):
        lessons = self.tr.load_store()
        tools = self.tr.cell_tools("armed", lessons)
        self.assertEqual(len(tools), 2)
        self.assertEqual(self.tr.cell_tools("none", lessons), [])

    def test_touched_store_refused(self):
        bad = os.path.join(self._tmp.name, "touched.jsonl")
        with open(self.tr.STORE, "rb") as f:
            original = f.read()
        with open(bad, "wb") as f:
            f.write(original + b"\n")
        self.tr.STORE = bad
        with self.assertRaises(SystemExit):
            self.tr.byte_check()

    def test_interleave_seat_and_resume(self):
        calls = self._stub_run()
        rows = self.tr.run_cells(repeats=2)
        self.assertEqual([r["cell"] for r in rows],
                         ["none", "armed"] * 2)
        self.assertTrue(all(c["model"] == "mistral:7b" for c in calls))
        self.assertTrue(all(
            r["tools"] == (2 if r["cell"] == "armed" else 0)
            for r in rows))
        calls.clear()
        rows2 = self.tr.run_cells(repeats=2,
                                  prior_rows=self.tr._load_rows())
        self.assertEqual(calls, [])
        self.assertEqual(len(rows2), 4)

    def test_tables_mark_rule_and_watch(self):
        rows = [
            {"cell": "none", "task": "longest_word",
             "checks": {"longest_word('cat door bird')": False,
                        "longest_word('')": True,
                        "longest_word('one')": True}},
            {"cell": "armed", "task": "longest_word",
             "checks": {"longest_word('cat door bird')": True,
                        "longest_word('')": False,
                        "longest_word('one')": True}},
        ]
        table = self.tr.check_table(rows)
        self.assertTrue(
            table["longest_word('cat door bird')"]["rule_check"])
        self.assertTrue(table["longest_word('')"]["watch"])
        self.assertTrue(table["longest_word('one')"]["watch"])
        pooled = self.tr.pooled_rule_checks(rows)
        self.assertEqual(pooled["none"]["passed"], 0)
        self.assertEqual(pooled["armed"]["passed"], 1)


if __name__ == "__main__":
    unittest.main()
