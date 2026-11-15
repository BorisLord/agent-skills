from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

from scripts import health_events, health_metrics, health_store

SCRIPTS = Path(health_store.__file__).parent


class JournalSafetyTests(unittest.TestCase):
    def test_existing_ignore_and_tracked_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", directory], check=True)
            ignore = root / ".gitignore"
            ignore.write_text("*.tmp\n!/profile.json\n", encoding="utf-8")
            health_store.initialize(root)
            first = ignore.read_text(encoding="utf-8")
            health_store.initialize(root)
            self.assertEqual(ignore.read_text(encoding="utf-8"), first)
            self.assertTrue(first.startswith("*.tmp\n!/profile.json\n"))
            for name in ("profile.json", "events.jsonl"):
                subprocess.run(
                    ["git", "-C", directory, "check-ignore", "-q", name], check=True
                )
            subprocess.run(
                ["git", "-C", directory, "add", "-f", "profile.json"], check=True
            )
            before = (root / "profile.json").read_bytes()
            for action in (
                lambda: health_store.initialize(root),
                lambda: health_store.update_profile(root, {"goals": {}}),
                lambda: health_store.append_event(
                    root,
                    {
                        "type": "meal",
                        "effective_at": "2026-01-01",
                        "data": {"kcal": 100},
                    },
                ),
            ):
                with self.assertRaisesRegex(ValueError, "tracked or staged"):
                    action()
            self.assertEqual((root / "profile.json").read_bytes(), before)
            self.assertEqual((root / "events.jsonl").read_text(), "")

    def test_numeric_inputs_and_no_partial_write(self) -> None:
        for bad in (True, "80", None, float("nan"), float("inf"), -1, 0):
            with self.subTest(value=bad), self.assertRaises(ValueError):
                health_metrics.parse_weight_observations(
                    [{"date": "2026-01-01", "weight_kg": bad}]
                )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            health_store.initialize(root)
            for bad in (True, "400", None, float("nan"), float("inf"), -1):
                with self.subTest(value=bad), self.assertRaises(ValueError):
                    health_store.append_event(
                        root,
                        {
                            "type": "meal",
                            "effective_at": "2026-01-01",
                            "data": {"kcal": bad},
                        },
                    )
            self.assertEqual((root / "events.jsonl").read_bytes(), b"")
            before = (root / "profile.json").read_bytes()
            with self.assertRaises(ValueError):
                health_store.update_profile(root, {"bad": float("nan")})
            self.assertEqual((root / "profile.json").read_bytes(), before)
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "health_metrics.py"), "trend"],
            input='[{"date":"2026-01-01","weight_kg":"NaN"}]',
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")

    def test_correction_and_daily_confirmation_replay(self) -> None:
        meal: dict[str, object] = {
            "id": "m",
            "type": "meal",
            "effective_at": "2026-01-01",
            "data": {"kcal": 400},
        }
        confirmed: dict[str, object] = {
            "id": "d",
            "type": "intake_day",
            "effective_at": "2026-01-01",
            "data": {"complete": True},
        }
        correction: dict[str, object] = {
            "id": "c",
            "type": "correction",
            "effective_at": "2026-01-02",
            "data": {"corrects_id": "m", "replacement": {"kcal": 500}},
        }
        self.assertEqual(health_events.replay([meal, confirmed])[1], {date(2026, 1, 1)})
        self.assertFalse(health_events.replay([meal, confirmed, correction])[1])
        self.assertTrue(
            health_events.replay(
                [meal, confirmed, correction, {**confirmed, "id": "d2"}]
            )[1]
        )
        revoked: dict[str, object] = {
            **confirmed,
            "id": "d3",
            "data": {"complete": False},
        }
        self.assertFalse(health_events.replay([meal, confirmed, revoked])[1])
        chain: dict[str, object] = {
            **correction,
            "id": "c2",
            "data": {"corrects_id": "c", "replacement": {"kcal": 600}},
        }
        with self.assertRaisesRegex(ValueError, "original event"):
            health_events.replay([meal, correction, chain])
        replacement: dict[str, object] = {
            **chain,
            "data": {"corrects_id": "m", "replacement": {"kcal": 600}},
        }
        self.assertEqual(
            health_events.replay([meal, correction, replacement])[0][0]["data"],
            {"kcal": 600},
        )
        self.assertEqual(meal["data"], {"kcal": 400})
        with self.assertRaises(ValueError):
            health_events.replay([{**confirmed, "data": {"complete": "true"}}])

    def test_calibration_window_and_completeness(self) -> None:
        events: list[dict[str, object]] = []
        for index in range(15):
            day = (date(2026, 1, 1) + timedelta(days=index)).isoformat()
            events.extend(
                [
                    {"type": "weight", "effective_at": day, "data": {"weight_kg": 80}},
                    {
                        "type": "intake_day",
                        "effective_at": day,
                        "data": {"complete": True},
                    },
                ]
            )

        def calculate(
            data: list[dict[str, object]],
        ) -> subprocess.CompletedProcess[str]:
            return subprocess.run(
                [sys.executable, str(SCRIPTS / "health_metrics.py"), "observed-tdee"],
                input=json.dumps(data),
                text=True,
                capture_output=True,
                check=False,
            )

        result = calculate(events)
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["window_start"], "2026-01-02")
        self.assertEqual(payload["intake_confirmed_days"], 14)
        self.assertEqual(payload["intake_logged_days"], 0)
        self.assertEqual(payload["intake_confirmed_coverage_percent"], 100.0)
        self.assertEqual(payload["estimated_observed_tdee_kcal_per_day"], 0)
        missing = calculate(events[:-1])
        self.assertNotEqual(missing.returncode, 0)
        self.assertIn("2026-01-15", missing.stderr)
        late = calculate(
            [
                *events,
                {"type": "meal", "effective_at": "2026-01-05", "data": {"kcal": 400}},
            ]
        )
        self.assertNotEqual(late.returncode, 0)
        self.assertIn("2026-01-05", late.stderr)
        sparse = calculate(
            [
                event
                for event in events
                if event["type"] != "weight" or event["effective_at"] == "2026-01-15"
            ]
        )
        self.assertNotEqual(sparse.returncode, 0)
        self.assertIn("4 weight", sparse.stderr)
