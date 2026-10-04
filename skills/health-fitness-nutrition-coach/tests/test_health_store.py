from __future__ import annotations

import json
import tempfile
import unittest
from datetime import date
from pathlib import Path
from typing import cast

from scripts import health_store


class HealthStoreTests(unittest.TestCase):
    def test_default_storage_name_and_profile_language_are_english(self) -> None:
        self.assertEqual(health_store.default_data_dir().name, ".health-coach")
        self.assertEqual(health_store.initial_profile()["language"], "en")

    def test_initialization_is_non_destructive(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            data_dir = Path(temporary_directory) / "health"
            first = health_store.initialize(data_dir)
            profile_path = data_dir / "profile.json"
            profile_path.write_text(
                '{"schema_version":1,"custom":true}\n', encoding="utf-8"
            )
            second = health_store.initialize(data_dir)

            self.assertIn("profile.json", cast(list[str], first["created"]))
            self.assertEqual(
                json.loads(profile_path.read_text(encoding="utf-8"))["custom"], True
            )
            self.assertTrue(second["existing"])
            self.assertEqual(
                (data_dir / ".gitignore").read_text(encoding="utf-8"),
                "*\n!.gitignore\n",
            )

    def test_profile_update_deep_merges(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            data_dir = Path(temporary_directory) / "health"
            health_store.initialize(data_dir)
            updated = health_store.update_profile(
                data_dir,
                {
                    "preferences": {"response_tone": "supportive"},
                    "goals": {"primary": "maintenance"},
                },
            )
            preferences = cast(dict[str, object], updated["preferences"])
            goals = cast(dict[str, object], updated["goals"])
            self.assertEqual(preferences["tracking_depth"], "standard")
            self.assertEqual(preferences["response_tone"], "supportive")
            self.assertEqual(goals["primary"], "maintenance")

    def test_events_are_append_only_and_corrections_reference_existing_ids(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            data_dir = Path(temporary_directory) / "health"
            health_store.initialize(data_dir)
            original = health_store.append_event(
                data_dir,
                {
                    "type": "weight",
                    "effective_at": "2026-09-01",
                    "source": "user",
                    "uncertainty": "low",
                    "data": {"weight_kg": 80.0},
                },
            )
            correction = health_store.append_event(
                data_dir,
                {
                    "type": "correction",
                    "effective_at": "2026-09-01",
                    "data": {
                        "corrects_id": original["id"],
                        "replacement": {"weight_kg": 79.8},
                    },
                },
            )
            events = health_store.load_events(data_dir)
            self.assertEqual(len(events), 2)
            original_data = cast(dict[str, object], events[0]["data"])
            correction_data = cast(dict[str, object], correction["data"])
            replacement = cast(dict[str, object], correction_data["replacement"])
            self.assertEqual(original_data["weight_kg"], 80.0)
            self.assertEqual(replacement["weight_kg"], 79.8)

    def test_event_filters(self) -> None:
        events: list[dict[str, object]] = [
            {"type": "weight", "effective_at": "2026-09-01"},
            {"type": "meal", "effective_at": "2026-09-02"},
            {"type": "weight", "effective_at": "2026-09-03"},
        ]
        filtered = health_store.filter_events(events, "weight", date(2026, 9, 2), None)
        self.assertEqual(filtered, [{"type": "weight", "effective_at": "2026-09-03"}])

    def test_invalid_correction_fails(self) -> None:
        with self.assertRaisesRegex(ValueError, "existing event"):
            health_store.normalize_event(
                {
                    "type": "correction",
                    "effective_at": "2026-09-01",
                    "data": {"corrects_id": "missing", "replacement": {}},
                },
                set(),
            )


if __name__ == "__main__":
    unittest.main()
