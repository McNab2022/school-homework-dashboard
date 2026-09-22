#!/usr/bin/env python3
"""Build feeds/schedule.json from Vklass lecture ICS exports.

For each kid, computes Mon–Fri finish time = MAX DTEND of lessons on that
weekday. Prefers the modal daily-max when a weekday has outliers (e.g. half-days).
Weekday keys are JS getDay() strings: "0"=Sun … "6"=Sat (only "1"–"5" filled).
"""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

FEEDS = Path(__file__).resolve().parent
KIDS = [
    ("eleanor", "Ellie", "ellie-lectures.ics"),
    ("oliver", "Ollie", "ollie-lectures.ics"),
]


def parse_events(path: Path):
    text = path.read_text(encoding="utf-8")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\n[ \t]", "", text)
    events = []
    for block in re.findall(r"BEGIN:VEVENT(.*?)END:VEVENT", text, re.S):
        ds = re.search(r"DTSTART(?:;[^:]*)?:(\d{8}T\d{6})", block)
        de = re.search(r"DTEND(?:;[^:]*)?:(\d{8}T\d{6})", block)
        if not ds or not de:
            continue
        start = datetime.strptime(ds.group(1), "%Y%m%dT%H%M%S")
        end = datetime.strptime(de.group(1), "%Y%m%dT%H%M%S")
        events.append((start, end))
    return events


def finish_by_weekday(events):
    """Return dict keyed by JS getDay() string -> HH:MM or None."""
    by_date = defaultdict(list)
    for start, end in events:
        by_date[start.date()].append(end)

    # daily max per weekday (Mon=0..Fri=4 in Python)
    daily_max_by_pywd = defaultdict(list)
    for d, ends in by_date.items():
        if d.weekday() > 4:
            continue
        mx = max(ends)
        daily_max_by_pywd[d.weekday()].append(mx.strftime("%H:%M"))

    out = {str(i): None for i in range(7)}
    for pywd in range(5):
        times = daily_max_by_pywd.get(pywd) or []
        if not times:
            continue
        # modal (most common) daily max; ties → latest time among modes
        counts = Counter(times)
        best_n = max(counts.values())
        candidates = [t for t, n in counts.items() if n == best_n]
        finish = max(candidates)
        js_day = str(pywd + 1)  # Mon=1 … Fri=5
        out[js_day] = finish
    return out


def main():
    kids = {}
    notes_parts = [
        "Finish = end of last lesson that day (max DTEND from Vklass lecture ICS).",
        "Weekday keys are JS getDay() strings: \"0\"=Sun … \"6\"=Sat; school days use \"1\"–\"5\".",
        "Built by feeds/build_schedule.py from ellie-lectures.ics / ollie-lectures.ics.",
    ]
    for kid_id, name, ics_name in KIDS:
        path = FEEDS / ics_name
        if not path.exists() or path.stat().st_size < 50:
            kids[kid_id] = {"name": name, "finishByWeekday": {str(i): None for i in range(7)}}
            notes_parts.append(f"{name}: ICS missing/empty — finish times null.")
            continue
        events = parse_events(path)
        if not events:
            kids[kid_id] = {"name": name, "finishByWeekday": {str(i): None for i in range(7)}}
            notes_parts.append(f"{name}: no VEVENTs — finish times null.")
            continue
        kids[kid_id] = {"name": name, "finishByWeekday": finish_by_weekday(events)}

    payload = {
        "updated": datetime.now().strftime("%Y-%m-%d"),
        "timezone": "Europe/Stockholm",
        "kids": kids,
        "notes": " ".join(notes_parts),
    }
    out = FEEDS / "schedule.json"
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {out}")
    for kid_id, info in kids.items():
        print(kid_id, info["finishByWeekday"])


if __name__ == "__main__":
    main()
