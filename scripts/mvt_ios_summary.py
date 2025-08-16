#!/usr/bin/env python3
"""Summarize MVT iOS JSON outputs."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime, timedelta
from pathlib import Path


def parse_ts(value: str) -> datetime | None:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).replace(tzinfo=None)
    except Exception:  # pragma: no cover - best effort parsing
        return None


def main(out_dir: str) -> None:
    path = Path(out_dir)
    total = 0
    modules: set[str] = set()
    recent: list[str] = []
    now = datetime.now(UTC).replace(tzinfo=None)
    cutoff = now - timedelta(days=7)

    for json_file in path.glob("*.json"):
        try:
            data = json.loads(json_file.read_text())
        except Exception:
            continue
        if isinstance(data, list) and data:
            total += len(data)
            modules.add(json_file.stem)
            for item in data:
                ts = None
                for key in ("timestamp", "date", "time"):
                    val = item.get(key)
                    if isinstance(val, str):
                        ts = parse_ts(val)
                        if ts:
                            break
                if ts and ts >= cutoff:
                    recent.append(f"{json_file.name}: {item}")

    print(f"Total matches: {total}")
    if modules:
        print("Modules: " + ", ".join(sorted(modules)))
    else:
        print("Modules: none")
    if recent:
        print("Matches in last 7 days:")
        for line in recent:
            print(f"- {line}")
    else:
        print("No matches in last 7 days.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Summarize MVT iOS scan results")
    parser.add_argument("--out", default="./mvt_out", help="Directory with JSON outputs")
    args = parser.parse_args()
    main(args.out)
