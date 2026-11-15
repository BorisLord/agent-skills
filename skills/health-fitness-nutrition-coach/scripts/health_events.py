"""Validate and replay append-only health events."""

from __future__ import annotations

import json
import math
from datetime import date, datetime
from typing import cast


def number(value: object, name: str, *, positive: bool = False) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a finite JSON number")
    try:
        result = float(value)
    except OverflowError as error:
        raise ValueError(f"{name} must be finite") from error
    if not math.isfinite(result) or result < 0 or (positive and result == 0):
        raise ValueError(
            f"{name} must be finite and {'positive' if positive else 'nonnegative'}"
        )
    return result


def event_day(value: object) -> date:
    return datetime.fromisoformat(str(value).replace("Z", "+00:00")).date()


def validate_data(kind: object, data: dict[str, object]) -> None:
    json.dumps(data, allow_nan=False)
    if kind == "weight":
        number(data.get("weight_kg"), "weight_kg", positive=True)
    elif kind == "meal":
        number(data.get("kcal"), "kcal")
    elif kind == "intake_day" and not isinstance(data.get("complete"), bool):
        raise ValueError("intake_day data.complete must be a boolean")


def replay(
    events: list[dict[str, object]],
) -> tuple[list[dict[str, object]], set[date]]:
    effective: list[dict[str, object]] = []
    positions: dict[str, int] = {}
    complete: set[date] = set()
    for event in events:
        data = event.get("data")
        if not isinstance(data, dict):
            raise ValueError("event data must be a JSON object")
        payload = cast(dict[str, object], data)
        kind = event.get("type")
        if kind == "correction":
            target_id = payload.get("corrects_id")
            replacement = payload.get("replacement")
            if not isinstance(target_id, str) or target_id not in positions:
                raise ValueError(
                    "correction must reference an existing original event, not another correction"
                )
            if not isinstance(replacement, dict):
                raise ValueError("correction replacement must be a JSON object")
            target = effective[positions[target_id]].copy()
            payload = cast(dict[str, object], replacement)
            kind = target.get("type")
            validate_data(kind, payload)
            target["data"] = payload
            effective[positions[target_id]] = target
            day = event_day(target.get("effective_at"))
        else:
            validate_data(kind, payload)
            day = event_day(event.get("effective_at"))
            effective.append(event)
            event_id = event.get("id")
            if event_id is not None:
                if str(event_id) in positions:
                    raise ValueError("duplicate event id")
                positions[str(event_id)] = len(effective) - 1
        if kind == "meal":
            complete.discard(day)
        elif kind == "intake_day":
            if payload["complete"]:
                complete.add(day)
            else:
                complete.discard(day)
    return effective, complete
