#!/usr/bin/env python3
"""Deterministic health, nutrition, weight, and training calculations."""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from collections.abc import Callable
from datetime import date, datetime, timedelta
from pathlib import Path
from statistics import fmean
from typing import cast

KCAL_PER_KG_WEIGHT_CHANGE = 7700


def energy(args: argparse.Namespace) -> dict[str, object]:
    constant = 5 if args.formula_sex == "male" else -161
    ree = 10 * args.weight_kg + 6.25 * args.height_cm - 5 * args.age + constant
    tdee = ree * args.activity_multiplier
    return {
        "method": "Mifflin-St Jeor resting energy expenditure",
        "method_source": "https://pubmed.ncbi.nlm.nih.gov/2305711/",
        "inputs": vars_for(
            args, "age", "height_cm", "weight_kg", "formula_sex", "activity_multiplier"
        ),
        "resting_energy_expenditure_kcal_per_day": round(ree),
        "estimated_tdee_kcal_per_day": round(tdee),
        "moderate_target_percent_range_kcal_per_day": [
            round(tdee * 0.85),
            round(tdee * 0.90),
        ],
        "moderate_target_absolute_range_kcal_per_day": [
            round(tdee - 500),
            round(tdee - 250),
        ],
        "limitations": [
            "The activity multiplier is a heuristic, not a measurement.",
            "Candidate deficit ranges are not a user-specific prescription.",
            "Calibrate against at least 14 days of reasonably complete observations.",
        ],
    }


def body(args: argparse.Namespace) -> dict[str, object]:
    height_m = args.height_cm / 100
    result: dict[str, object] = {
        "inputs": vars_for(
            args, "height_cm", "weight_kg", "waist_cm", "baseline_weight_kg"
        ),
        "bmi": round(args.weight_kg / height_m**2, 2),
    }
    if args.waist_cm is not None:
        result["waist_to_height_ratio"] = round(args.waist_cm / args.height_cm, 3)
    if args.baseline_weight_kg is not None:
        change = args.weight_kg - args.baseline_weight_kg
        result["weight_change_kg"] = round(change, 3)
        result["weight_change_percent"] = round(
            change / args.baseline_weight_kg * 100, 2
        )
    result["limitations"] = [
        "Measurements are reported without diagnostic classification."
    ]
    return result


def macros(args: argparse.Namespace) -> dict[str, object]:
    protein_g = args.weight_kg * args.protein_g_per_kg
    fat_g = args.weight_kg * args.fat_g_per_kg
    remaining_kcal = args.calories - protein_g * 4 - fat_g * 9
    if remaining_kcal < 0:
        raise ValueError("protein and fat targets exceed the calorie budget")
    carbs_g = remaining_kcal / 4
    return {
        "inputs": vars_for(
            args, "calories", "weight_kg", "protein_g_per_kg", "fat_g_per_kg"
        ),
        "protein_g": round(protein_g, 1),
        "fat_g": round(fat_g, 1),
        "carbohydrate_g": round(carbs_g, 1),
        "energy_check_kcal": round(protein_g * 4 + fat_g * 9 + carbs_g * 4),
        "limitations": [
            "The gram-per-kilogram inputs must come from a current guideline or an agreed user target."
        ],
    }


def parse_weight_observations(raw: object) -> list[tuple[date, float]]:
    if not isinstance(raw, list) or not raw:
        raise ValueError("trend input must be a non-empty JSON array")
    by_day: dict[date, list[float]] = defaultdict(list)
    for item in cast(list[object], raw):
        if not isinstance(item, dict):
            raise ValueError("each observation needs date and weight_kg")
        observation = cast(dict[str, object], item)
        if "date" not in observation or "weight_kg" not in observation:
            raise ValueError("each observation needs date and weight_kg")
        day = date.fromisoformat(str(observation["date"]))
        weight = float(cast(int | float | str, observation["weight_kg"]))
        if weight <= 0:
            raise ValueError("weight_kg must be positive")
        by_day[day].append(weight)
    return sorted((day, fmean(values)) for day, values in by_day.items())


def window_average(
    observations: list[tuple[date, float]], start: date, end: date
) -> tuple[float | None, int]:
    values = [weight for day, weight in observations if start <= day <= end]
    return (fmean(values), len(values)) if values else (None, 0)


def trend(_: argparse.Namespace) -> dict[str, object]:
    observations = parse_weight_observations(json.load(sys.stdin))
    rolling: list[dict[str, object]] = []
    for day, _weight in observations:
        average, count = window_average(observations, day - timedelta(days=6), day)
        if average is None:
            raise RuntimeError("rolling window unexpectedly contains no observations")
        rolling.append(
            {
                "date": day.isoformat(),
                "average_kg": round(average, 3),
                "observations": count,
            }
        )
    last_day = observations[-1][0]
    recent, recent_count = window_average(
        observations, last_day - timedelta(days=6), last_day
    )
    previous, previous_count = window_average(
        observations, last_day - timedelta(days=13), last_day - timedelta(days=7)
    )
    change = None if recent is None or previous is None else recent - previous
    return {
        "first_date": observations[0][0].isoformat(),
        "last_date": last_day.isoformat(),
        "calendar_span_days": (last_day - observations[0][0]).days + 1,
        "daily_observation_count": len(observations),
        "rolling_7_day": rolling,
        "recent_7_day_average_kg": rounded(recent, 3),
        "recent_7_day_observations": recent_count,
        "previous_7_day_average_kg": rounded(previous, 3),
        "previous_7_day_observations": previous_count,
        "weekly_average_change_kg": rounded(change, 3),
        "weekly_average_change_percent": (
            None
            if change is None or previous is None
            else round(change / previous * 100, 2)
        ),
        "has_14_calendar_days": (last_day - observations[0][0]).days >= 13,
        "limitations": [
            "Averages use available observations; missing days reduce confidence.",
            "The result does not identify water, glycogen, digestive, hormonal, or tissue changes.",
        ],
    }


def parse_effective_date(value: object) -> date:
    text = str(value).replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(text).date()
    except ValueError:
        return date.fromisoformat(str(value))


def read_events(data_dir: str | None) -> list[dict[str, object]]:
    if data_dir:
        path = Path(data_dir).expanduser().resolve() / "events.jsonl"
        if not path.exists():
            raise ValueError(f"event log not found: {path}")
        loaded: object = [
            cast(object, json.loads(line))
            for line in path.read_text(encoding="utf-8").splitlines()
            if line
        ]
    else:
        loaded = cast(object, json.load(sys.stdin))
    if not isinstance(loaded, list):
        raise ValueError("events must be a JSON array or a valid events.jsonl file")
    events: list[dict[str, object]] = []
    for item in cast(list[object], loaded):
        if not isinstance(item, dict):
            raise ValueError("events must contain JSON objects")
        events.append(cast(dict[str, object], item))
    return apply_corrections(events)


def apply_corrections(events: list[dict[str, object]]) -> list[dict[str, object]]:
    effective: list[dict[str, object]] = []
    positions: dict[str, int] = {}
    for event in events:
        if event.get("type") == "correction":
            data = event.get("data")
            if not isinstance(data, dict):
                continue
            correction = cast(dict[str, object], data)
            target_id = str(correction.get("corrects_id", ""))
            replacement = correction.get("replacement")
            if target_id not in positions or not isinstance(replacement, dict):
                continue
            target = effective[positions[target_id]].copy()
            target["data"] = cast(dict[str, object], replacement)
            effective[positions[target_id]] = target
            continue
        effective.append(event)
        event_id = event.get("id")
        if event_id is not None:
            positions[str(event_id)] = len(effective) - 1
    return effective


def observed_tdee(args: argparse.Namespace) -> dict[str, object]:
    events = read_events(args.data_dir)
    weights: dict[date, list[float]] = defaultdict(list)
    intake: dict[date, float] = defaultdict(float)
    for event in events:
        event_type = event.get("type")
        data = event.get("data")
        if not isinstance(data, dict) or "effective_at" not in event:
            continue
        event_data = cast(dict[str, object], data)
        day = parse_effective_date(event["effective_at"])
        if event_type == "weight" and "weight_kg" in event_data:
            weights[day].append(float(cast(int | float | str, event_data["weight_kg"])))
        elif event_type == "meal" and "kcal" in event_data:
            intake[day] += float(cast(int | float | str, event_data["kcal"]))
    observations = sorted((day, fmean(values)) for day, values in weights.items())
    if not observations:
        raise ValueError("observed TDEE requires weight events")
    first_day, last_day = observations[0][0], observations[-1][0]
    span = (last_day - first_day).days + 1
    first_values = [
        (day, weight)
        for day, weight in observations
        if day <= first_day + timedelta(days=6)
    ]
    last_values = [
        (day, weight)
        for day, weight in observations
        if day >= last_day - timedelta(days=6)
    ]
    intake_values = [
        value for day, value in intake.items() if first_day <= day <= last_day
    ]
    if (
        span < 14
        or len(intake_values) < 10
        or len(first_values) < 4
        or len(last_values) < 4
    ):
        raise ValueError(
            "observed TDEE requires at least 14 calendar days, 10 intake days, "
            "and 4 weight observations in both the first and last 7-day windows"
        )
    first_weight = fmean(weight for _day, weight in first_values)
    last_weight = fmean(weight for _day, weight in last_values)
    first_ordinal = fmean(day.toordinal() for day, _weight in first_values)
    last_ordinal = fmean(day.toordinal() for day, _weight in last_values)
    elapsed_days = last_ordinal - first_ordinal
    if elapsed_days <= 0:
        raise ValueError("weight windows do not provide a usable elapsed duration")
    daily_weight_change = (last_weight - first_weight) / elapsed_days
    mean_intake = fmean(intake_values)
    estimate = mean_intake - daily_weight_change * KCAL_PER_KG_WEIGHT_CHANGE
    return {
        "method": "energy-balance estimate from logged intake and smoothed weight change",
        "calendar_span_days": span,
        "intake_logged_days": len(intake_values),
        "intake_coverage_percent": round(len(intake_values) / span * 100, 1),
        "first_window_weight_observations": len(first_values),
        "last_window_weight_observations": len(last_values),
        "first_7_day_average_kg": round(first_weight, 3),
        "last_7_day_average_kg": round(last_weight, 3),
        "mean_logged_intake_kcal_per_day": round(mean_intake),
        "estimated_observed_tdee_kcal_per_day": round(estimate),
        "assumption_kcal_per_kg_weight_change": KCAL_PER_KG_WEIGHT_CHANGE,
        "limitations": [
            "The 7700 kcal/kg conversion is an approximation and weight change is not pure body fat.",
            "Missing or inaccurate meal entries can materially bias the estimate.",
            "Do not change a calorie target automatically from this result.",
        ],
    }


def strength(args: argparse.Namespace) -> dict[str, object]:
    estimated_1rm = (
        args.load_kg if args.reps == 1 else args.load_kg * (1 + args.reps / 30)
    )
    return {
        "method": "Epley estimated one-repetition maximum",
        "inputs": vars_for(args, "load_kg", "reps", "sets"),
        "estimated_1rm_kg": round(estimated_1rm, 2),
        "volume_load_kg": round(args.load_kg * args.reps * args.sets, 2),
        "limitations": ["The 1RM estimate is restricted to sets of 1-12 repetitions."],
    }


def cardio(args: argparse.Namespace) -> dict[str, object]:
    hours = args.duration_seconds / 3600
    speed = args.distance_km / hours
    pace_seconds = args.duration_seconds / args.distance_km
    pace_minutes, pace_remainder = divmod(round(pace_seconds), 60)
    result: dict[str, object] = {
        "inputs": vars_for(args, "distance_km", "duration_seconds"),
        "speed_km_per_hour": round(speed, 2),
        "pace_seconds_per_km": round(pace_seconds, 1),
        "pace_min_per_km": f"{pace_minutes}:{pace_remainder:02d}",
        "limitations": [
            "A same-pace distance projection is linear and does not predict performance."
        ],
    }
    if args.project_distance_km is not None:
        projected_seconds = pace_seconds * args.project_distance_km
        projected_minutes, projected_remainder = divmod(round(projected_seconds), 60)
        result["projected_distance_km"] = args.project_distance_km
        result["projected_duration_seconds"] = round(projected_seconds)
        result["projected_duration"] = f"{projected_minutes}:{projected_remainder:02d}"
    return result


def heart_rate(args: argparse.Namespace) -> dict[str, object]:
    if args.max_bpm <= args.resting_bpm:
        raise ValueError("max-bpm must be greater than resting-bpm")
    reserve = args.max_bpm - args.resting_bpm
    bands = [(0.50, 0.60), (0.60, 0.70), (0.70, 0.80), (0.80, 0.90), (0.90, 1.00)]
    zones: list[dict[str, object]] = []
    for index, (lower, upper) in enumerate(bands, start=1):
        zones.append(
            {
                "zone": index,
                "intensity_percent_hrr": [round(lower * 100), round(upper * 100)],
                "bpm": [
                    round(args.resting_bpm + reserve * lower),
                    round(args.resting_bpm + reserve * upper),
                ],
            }
        )
    return {
        "method": "Karvonen heart-rate reserve",
        "method_source": "https://pubmed.ncbi.nlm.nih.gov/13470504/",
        "inputs": vars_for(args, "resting_bpm", "max_bpm"),
        "heart_rate_reserve_bpm": reserve,
        "zones": zones,
        "limitations": [
            "These are conventional training bands, not medical thresholds.",
            "Use a supplied or measured maximum; this command does not estimate it from age.",
        ],
    }


def activity_energy(args: argparse.Namespace) -> dict[str, object]:
    estimate = args.met * 3.5 * args.weight_kg / 200 * args.duration_minutes
    return {
        "method": "MET activity energy estimate",
        "inputs": vars_for(args, "met", "weight_kg", "duration_minutes"),
        "estimated_kcal": round(estimate),
        "limitations": [
            "MET values are population averages and can differ materially from individual expenditure."
        ],
    }


def sleep(args: argparse.Namespace) -> dict[str, object]:
    if args.asleep_hours > args.time_in_bed_hours:
        raise ValueError("asleep-hours cannot exceed time-in-bed-hours")
    return {
        "inputs": vars_for(args, "asleep_hours", "time_in_bed_hours"),
        "sleep_efficiency_percent": round(
            args.asleep_hours / args.time_in_bed_hours * 100, 1
        ),
        "limitations": ["Sleep efficiency alone does not diagnose a sleep disorder."],
    }


def rounded(value: float | None, digits: int) -> float | None:
    return None if value is None else round(value, digits)


def vars_for(args: argparse.Namespace, *names: str) -> dict[str, object]:
    return {name: getattr(args, name) for name in names}


def bounded_number(
    name: str, minimum: float, maximum: float, *, integer: bool = False
) -> Callable[[str], int | float]:
    conversion = int if integer else float

    def parse(value: str) -> int | float:
        number = conversion(value)
        if not minimum <= number <= maximum:
            raise argparse.ArgumentTypeError(
                f"{name} must be between {minimum:g} and {maximum:g}"
            )
        return number

    return parse


def add_body_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--height-cm", type=bounded_number("height-cm", 100, 250), required=True
    )
    parser.add_argument(
        "--weight-kg", type=bounded_number("weight-kg", 20, 500), required=True
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    energy_parser = subparsers.add_parser("energy")
    energy_parser.add_argument(
        "--age", type=bounded_number("age", 18, 120, integer=True), required=True
    )
    add_body_arguments(energy_parser)
    energy_parser.add_argument(
        "--formula-sex", choices=("female", "male"), required=True
    )
    energy_parser.add_argument(
        "--activity-multiplier",
        type=bounded_number("activity-multiplier", 1, 3),
        required=True,
    )
    energy_parser.set_defaults(handler=energy)

    body_parser = subparsers.add_parser("body")
    add_body_arguments(body_parser)
    body_parser.add_argument("--waist-cm", type=bounded_number("waist-cm", 30, 300))
    body_parser.add_argument(
        "--baseline-weight-kg", type=bounded_number("baseline-weight-kg", 20, 500)
    )
    body_parser.set_defaults(handler=body)

    macros_parser = subparsers.add_parser("macros")
    macros_parser.add_argument(
        "--calories", type=bounded_number("calories", 1, 10000), required=True
    )
    macros_parser.add_argument(
        "--weight-kg", type=bounded_number("weight-kg", 20, 500), required=True
    )
    macros_parser.add_argument(
        "--protein-g-per-kg",
        type=bounded_number("protein-g-per-kg", 0, 5),
        required=True,
    )
    macros_parser.add_argument(
        "--fat-g-per-kg", type=bounded_number("fat-g-per-kg", 0, 5), required=True
    )
    macros_parser.set_defaults(handler=macros)

    trend_parser = subparsers.add_parser(
        "trend", help="read dated weights as JSON from stdin"
    )
    trend_parser.set_defaults(handler=trend)

    observed_parser = subparsers.add_parser("observed-tdee")
    observed_parser.add_argument(
        "--data-dir", help="read events.jsonl; otherwise read a JSON array from stdin"
    )
    observed_parser.set_defaults(handler=observed_tdee)

    strength_parser = subparsers.add_parser("strength")
    strength_parser.add_argument(
        "--load-kg", type=bounded_number("load-kg", 0.1, 1000), required=True
    )
    strength_parser.add_argument(
        "--reps", type=bounded_number("reps", 1, 12, integer=True), required=True
    )
    strength_parser.add_argument(
        "--sets", type=bounded_number("sets", 1, 100, integer=True), default=1
    )
    strength_parser.set_defaults(handler=strength)

    cardio_parser = subparsers.add_parser("cardio")
    cardio_parser.add_argument(
        "--distance-km", type=bounded_number("distance-km", 0.001, 1000), required=True
    )
    cardio_parser.add_argument(
        "--duration-seconds",
        type=bounded_number("duration-seconds", 1, 604800),
        required=True,
    )
    cardio_parser.add_argument(
        "--project-distance-km",
        type=bounded_number("project-distance-km", 0.001, 1000),
    )
    cardio_parser.set_defaults(handler=cardio)

    heart_parser = subparsers.add_parser("heart-rate")
    heart_parser.add_argument(
        "--resting-bpm",
        type=bounded_number("resting-bpm", 20, 220, integer=True),
        required=True,
    )
    heart_parser.add_argument(
        "--max-bpm",
        type=bounded_number("max-bpm", 40, 260, integer=True),
        required=True,
    )
    heart_parser.set_defaults(handler=heart_rate)

    activity_parser = subparsers.add_parser("activity-energy")
    activity_parser.add_argument(
        "--met", type=bounded_number("met", 0.1, 30), required=True
    )
    activity_parser.add_argument(
        "--weight-kg", type=bounded_number("weight-kg", 20, 500), required=True
    )
    activity_parser.add_argument(
        "--duration-minutes",
        type=bounded_number("duration-minutes", 0.1, 10080),
        required=True,
    )
    activity_parser.set_defaults(handler=activity_energy)

    sleep_parser = subparsers.add_parser("sleep")
    sleep_parser.add_argument(
        "--asleep-hours", type=bounded_number("asleep-hours", 0.1, 24), required=True
    )
    sleep_parser.add_argument(
        "--time-in-bed-hours",
        type=bounded_number("time-in-bed-hours", 0.1, 24),
        required=True,
    )
    sleep_parser.set_defaults(handler=sleep)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    try:
        result = args.handler(args)
    except (ValueError, OSError, KeyError, json.JSONDecodeError) as error:
        raise SystemExit(f"error: {error}") from error
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
