#!/usr/bin/env python3
"""Initialize and maintain a small local, append-only health journal."""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
import uuid
from datetime import UTC, date, datetime
from pathlib import Path
from typing import cast

SCHEMA_VERSION = 1
EVENT_TYPES = {
    "weight",
    "meal",
    "workout",
    "sleep",
    "measurement",
    "symptom",
    "lab",
    "medicine",
    "supplement",
    "note",
    "correction",
}
UNCERTAINTY_LEVELS = {"low", "medium", "high"}


def default_data_dir() -> Path:
    return Path.cwd() / ".health-coach"


def resolve_data_dir(value: str | None) -> Path:
    return Path(value).expanduser().resolve() if value else default_data_dir().resolve()


def initial_profile() -> dict[str, object]:
    return {
        "schema_version": SCHEMA_VERSION,
        "country": "FR",
        "language": "en",
        "units": "metric",
        "goals": {},
        "preferences": {
            "tracking_depth": "standard",
            "response_tone": "neutral",
        },
        "health_context": {},
    }


def write_json_atomic(path: Path, value: object) -> None:
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False
    ) as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
        temporary_path = Path(handle.name)
    temporary_path.chmod(0o600)
    temporary_path.replace(path)


def initialize(data_dir: Path) -> dict[str, object]:
    data_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    data_dir.chmod(0o700)
    created: list[str] = []

    profile_path = data_dir / "profile.json"
    if not profile_path.exists():
        write_json_atomic(profile_path, initial_profile())
        created.append(profile_path.name)

    events_path = data_dir / "events.jsonl"
    if not events_path.exists():
        events_path.touch(mode=0o600)
        created.append(events_path.name)

    ignore_path = data_dir / ".gitignore"
    if not ignore_path.exists():
        ignore_path.write_text("*\n!.gitignore\n", encoding="utf-8")
        created.append(ignore_path.name)

    return {"data_dir": str(data_dir), "created": created, "existing": not created}


def load_profile(data_dir: Path) -> dict[str, object]:
    path = data_dir / "profile.json"
    if not path.exists():
        raise ValueError(f"profile not found; initialize storage first: {path}")
    value = cast(object, json.loads(path.read_text(encoding="utf-8")))
    if not isinstance(value, dict):
        raise ValueError("unsupported or invalid profile schema")
    profile = cast(dict[str, object], value)
    if profile.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("unsupported or invalid profile schema")
    return profile


def deep_merge(
    current: dict[str, object], patch: dict[str, object]
) -> dict[str, object]:
    result = current.copy()
    for key, value in patch.items():
        if key == "schema_version":
            continue
        existing = result.get(key)
        if isinstance(existing, dict) and isinstance(value, dict):
            result[key] = deep_merge(
                cast(dict[str, object], existing), cast(dict[str, object], value)
            )
        else:
            result[key] = value
    return result


def read_json_object() -> dict[str, object]:
    value = cast(object, json.load(sys.stdin))
    if not isinstance(value, dict):
        raise TypeError("input must be a JSON object")
    return cast(dict[str, object], value)


def update_profile(data_dir: Path, patch: dict[str, object]) -> dict[str, object]:
    profile = deep_merge(load_profile(data_dir), patch)
    profile["schema_version"] = SCHEMA_VERSION
    write_json_atomic(data_dir / "profile.json", profile)
    return profile


def parse_iso_date(value: str) -> date:
    normalized = value.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(normalized).date()
    except ValueError:
        return date.fromisoformat(value)


def load_events(data_dir: Path) -> list[dict[str, object]]:
    path = data_dir / "events.jsonl"
    if not path.exists():
        raise ValueError(f"event log not found; initialize storage first: {path}")
    events: list[dict[str, object]] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            event = cast(object, json.loads(line))
            if not isinstance(event, dict):
                raise TypeError(f"invalid event at line {line_number}")
            events.append(cast(dict[str, object], event))
    return events


def normalize_event(
    raw: dict[str, object], existing_ids: set[str]
) -> dict[str, object]:
    event_type = raw.get("type")
    if event_type not in EVENT_TYPES:
        raise ValueError(f"type must be one of: {', '.join(sorted(EVENT_TYPES))}")
    effective_at = str(raw.get("effective_at", ""))
    if not effective_at:
        raise ValueError("effective_at is required")
    parse_iso_date(effective_at)
    data = raw.get("data")
    if not isinstance(data, dict):
        raise TypeError("data must be a JSON object")
    event_data = cast(dict[str, object], data)

    uncertainty = str(raw.get("uncertainty", "low"))
    if uncertainty not in UNCERTAINTY_LEVELS:
        raise ValueError("uncertainty must be low, medium, or high")

    if event_type == "correction":
        corrects_id = event_data.get("corrects_id")
        if corrects_id not in existing_ids:
            raise ValueError(
                "correction data.corrects_id must reference an existing event"
            )
        if not isinstance(event_data.get("replacement"), dict):
            raise ValueError("correction data.replacement must be a JSON object")

    return {
        "schema_version": SCHEMA_VERSION,
        "id": str(uuid.uuid4()),
        "recorded_at": datetime.now(UTC).isoformat(),
        "effective_at": effective_at,
        "type": event_type,
        "source": str(raw.get("source", "user")),
        "uncertainty": uncertainty,
        "data": event_data,
    }


def append_event(data_dir: Path, raw: dict[str, object]) -> dict[str, object]:
    events = load_events(data_dir)
    event = normalize_event(raw, {str(item.get("id")) for item in events})
    with (data_dir / "events.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False, separators=(",", ":")))
        handle.write("\n")
    return event


def filter_events(
    events: list[dict[str, object]],
    event_type: str | None,
    since: date | None,
    until: date | None,
) -> list[dict[str, object]]:
    selected: list[dict[str, object]] = []
    for event in events:
        if event_type and event.get("type") != event_type:
            continue
        day = parse_iso_date(str(event.get("effective_at")))
        if since and day < since:
            continue
        if until and day > until:
            continue
        selected.append(event)
    return selected


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", help="local data directory")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("init", help="initialize local storage without overwriting")

    profile_parser = subparsers.add_parser("profile", help="show or update the profile")
    profile_subparsers = profile_parser.add_subparsers(
        dest="profile_command", required=True
    )
    profile_subparsers.add_parser("show")
    profile_subparsers.add_parser("update", help="read a JSON merge patch from stdin")

    event_parser = subparsers.add_parser("event", help="append or list events")
    event_subparsers = event_parser.add_subparsers(dest="event_command", required=True)
    event_subparsers.add_parser("add", help="read one event JSON object from stdin")
    list_parser = event_subparsers.add_parser("list")
    list_parser.add_argument("--type", choices=sorted(EVENT_TYPES))
    list_parser.add_argument("--since", type=date.fromisoformat)
    list_parser.add_argument("--until", type=date.fromisoformat)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    try:
        if args.command == "init" and args.data_dir is None and sys.stdin.isatty():
            default = default_data_dir()
            entered = input(f"Data directory [{default}]: ").strip()
            data_dir = resolve_data_dir(entered or None)
        else:
            data_dir = resolve_data_dir(args.data_dir)

        if args.command == "init":
            result = initialize(data_dir)
        elif args.command == "profile" and args.profile_command == "show":
            result = load_profile(data_dir)
        elif args.command == "profile":
            result = update_profile(data_dir, read_json_object())
        elif args.event_command == "add":
            result = append_event(data_dir, read_json_object())
        else:
            result = filter_events(
                load_events(data_dir), args.type, args.since, args.until
            )
    except (TypeError, ValueError, OSError, json.JSONDecodeError) as error:
        raise SystemExit(f"error: {error}") from error

    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
