from __future__ import annotations

import argparse
import io
import json
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from datetime import date, timedelta
from typing import cast

from scripts import health_metrics


class HealthMetricsTests(unittest.TestCase):
    def test_energy_body_and_macros(self) -> None:
        energy = health_metrics.energy(
            argparse.Namespace(
                age=35,
                height_cm=175.0,
                weight_kg=80.0,
                formula_sex="male",
                activity_multiplier=1.4,
            )
        )
        self.assertEqual(energy["resting_energy_expenditure_kcal_per_day"], 1724)
        self.assertEqual(energy["estimated_tdee_kcal_per_day"], 2413)

        body = health_metrics.body(
            argparse.Namespace(
                height_cm=175.0,
                weight_kg=80.0,
                waist_cm=87.5,
                baseline_weight_kg=84.0,
            )
        )
        self.assertEqual(body["bmi"], 26.12)
        self.assertEqual(body["waist_to_height_ratio"], 0.5)
        self.assertEqual(body["weight_change_percent"], -4.76)

        macros = health_metrics.macros(
            argparse.Namespace(
                calories=2000.0,
                weight_kg=80.0,
                protein_g_per_kg=2.0,
                fat_g_per_kg=0.8,
            )
        )
        self.assertEqual(macros["protein_g"], 160.0)
        self.assertEqual(macros["fat_g"], 64.0)
        self.assertEqual(macros["carbohydrate_g"], 196.0)

    def test_macros_reject_impossible_budget(self) -> None:
        with self.assertRaisesRegex(ValueError, "exceed"):
            health_metrics.macros(
                argparse.Namespace(
                    calories=1000.0,
                    weight_kg=100.0,
                    protein_g_per_kg=3.0,
                    fat_g_per_kg=2.0,
                )
            )

    def test_weight_trend(self) -> None:
        observations = [
            {
                "date": (date(2026, 1, 1) + timedelta(days=index)).isoformat(),
                "weight_kg": 80 - index * 0.1,
            }
            for index in range(14)
        ]
        previous_stdin = sys.stdin
        try:
            sys.stdin = io.StringIO(json.dumps(observations))
            result = health_metrics.trend(argparse.Namespace())
        finally:
            sys.stdin = previous_stdin
        self.assertEqual(result["weekly_average_change_kg"], -0.7)
        self.assertTrue(result["has_14_calendar_days"])

    def test_observed_tdee(self) -> None:
        events: list[dict[str, object]] = []
        for index in range(14):
            day = (date(2026, 1, 1) + timedelta(days=index)).isoformat()
            events.extend(
                [
                    {
                        "type": "weight",
                        "effective_at": day,
                        "data": {"weight_kg": 80 - index * 0.05},
                    },
                    {"type": "meal", "effective_at": day, "data": {"kcal": 2000}},
                ]
            )
        previous_stdin = sys.stdin
        try:
            sys.stdin = io.StringIO(json.dumps(events))
            result = health_metrics.observed_tdee(argparse.Namespace(data_dir=None))
        finally:
            sys.stdin = previous_stdin
        self.assertEqual(result["estimated_observed_tdee_kcal_per_day"], 2385)
        self.assertEqual(result["intake_logged_days"], 14)

    def test_observed_tdee_rejects_sparse_data(self) -> None:
        previous_stdin = sys.stdin
        try:
            sys.stdin = io.StringIO(
                json.dumps(
                    [
                        {
                            "type": "weight",
                            "effective_at": "2026-01-01",
                            "data": {"weight_kg": 80},
                        }
                    ]
                )
            )
            with self.assertRaisesRegex(ValueError, "at least 14"):
                health_metrics.observed_tdee(argparse.Namespace(data_dir=None))
        finally:
            sys.stdin = previous_stdin

    def test_corrections_create_an_effective_view_without_rewriting_history(
        self,
    ) -> None:
        events: list[dict[str, object]] = [
            {
                "id": "weight-1",
                "type": "weight",
                "effective_at": "2026-01-01",
                "data": {"weight_kg": 80},
            },
            {
                "id": "correction-1",
                "type": "correction",
                "effective_at": "2026-01-02",
                "data": {
                    "corrects_id": "weight-1",
                    "replacement": {"weight_kg": 79.8},
                },
            },
        ]
        effective = health_metrics.apply_corrections(events)
        self.assertEqual(len(events), 2)
        self.assertEqual(len(effective), 1)
        effective_data = cast(dict[str, object], effective[0]["data"])
        self.assertEqual(effective_data["weight_kg"], 79.8)

    def test_training_and_recovery_formulas(self) -> None:
        strength = health_metrics.strength(
            argparse.Namespace(load_kg=100.0, reps=5, sets=3)
        )
        self.assertEqual(strength["estimated_1rm_kg"], 116.67)
        self.assertEqual(strength["volume_load_kg"], 1500.0)

        cardio = health_metrics.cardio(
            argparse.Namespace(
                distance_km=10.0,
                duration_seconds=3000.0,
                project_distance_km=21.1,
            )
        )
        self.assertEqual(cardio["speed_km_per_hour"], 12.0)
        self.assertEqual(cardio["pace_min_per_km"], "5:00")
        self.assertEqual(cardio["projected_duration"], "105:30")

        heart_rate = health_metrics.heart_rate(
            argparse.Namespace(resting_bpm=60, max_bpm=180)
        )
        zones = cast(list[dict[str, object]], heart_rate["zones"])
        self.assertEqual(zones[0]["bpm"], [120, 132])

        activity = health_metrics.activity_energy(
            argparse.Namespace(met=8.0, weight_kg=80.0, duration_minutes=60.0)
        )
        self.assertEqual(activity["estimated_kcal"], 672)

        sleep = health_metrics.sleep(
            argparse.Namespace(asleep_hours=7.0, time_in_bed_hours=8.0)
        )
        self.assertEqual(sleep["sleep_efficiency_percent"], 87.5)

    def test_cli_reports_invalid_sleep(self) -> None:
        previous_argv = sys.argv
        try:
            sys.argv = [
                "health_metrics.py",
                "sleep",
                "--asleep-hours",
                "9",
                "--time-in-bed-hours",
                "8",
            ]
            with (
                redirect_stdout(io.StringIO()),
                redirect_stderr(io.StringIO()),
                self.assertRaises(SystemExit) as context,
            ):
                health_metrics.main()
        finally:
            sys.argv = previous_argv
        self.assertIn("cannot exceed", str(context.exception))


if __name__ == "__main__":
    unittest.main()
