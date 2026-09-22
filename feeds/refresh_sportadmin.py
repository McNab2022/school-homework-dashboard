#!/usr/bin/env python3
"""Convert SportAdmin ICS → JSON for the Family dashboard Sport tab.

Usage:
  python3 feeds/refresh_sportadmin.py           # ICS → JSON only
  python3 feeds/refresh_sportadmin.py --fetch   # download ICS, then convert

Source URL is documented in feeds/README.md.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

FEED_DIR = Path(__file__).resolve().parent
ICS_PATH = FEED_DIR / "sportadmin.ics"
JSON_PATH = FEED_DIR / "sportadmin.json"
SOURCE_URL = (
    "https://portalweb.sportadmin.se/webcal"
    "?id=f619c1f3-826c-4bd7-a8c8-a344b3470d48"
)
TZ = ZoneInfo("Europe/Stockholm")
GATHERING_RE = re.compile(r"Samling:\s*(\d{1,2}[:.]\d{2})", re.IGNORECASE)


def unfold(ics: str) -> str:
    return re.sub(r"\r?\n[ \t]", "", ics)


def unescape(value: str) -> str:
    return (
        value.replace("\\n", "\n")
        .replace("\\,", ",")
        .replace("\\;", ";")
        .replace("\\\\", "\\")
    )


def get_prop(block: str, name: str) -> str | None:
    m = re.search(rf"^{re.escape(name)}[;:](.*)$", block, re.M)
    if not m:
        return None
    return m.group(1).strip()


def parse_ics_dt(raw: str | None) -> str | None:
    """Parse DTSTART/DTEND into ISO date or datetime (Europe/Stockholm)."""
    if not raw:
        return None
    # VALUE=DATE:20260922  or  TZID=Europe/Stockholm:20260922T183000  or  20260922T183000Z
    params, _, value = raw.rpartition(":")
    if not value:
        value = raw
        params = ""
    value = value.strip()
    params_u = params.upper()

    if "VALUE=DATE" in params_u or (len(value) == 8 and value.isdigit()):
        return f"{value[0:4]}-{value[4:6]}-{value[6:8]}"

    if value.endswith("Z") and len(value) >= 15:
        dt = datetime(
            int(value[0:4]),
            int(value[4:6]),
            int(value[6:8]),
            int(value[9:11]),
            int(value[11:13]),
            int(value[13:15]) if len(value) >= 15 and value[13:15].isdigit() else 0,
            tzinfo=ZoneInfo("UTC"),
        )
        return dt.astimezone(TZ).isoformat(timespec="minutes")

    # Local wall time; prefer TZID=Europe/Stockholm (or assume Stockholm)
    if len(value) >= 15 and value[8] == "T":
        dt = datetime(
            int(value[0:4]),
            int(value[4:6]),
            int(value[6:8]),
            int(value[9:11]),
            int(value[11:13]),
            int(value[13:15]) if value[13:15].isdigit() else 0,
            tzinfo=TZ,
        )
        return dt.isoformat(timespec="minutes")

    if len(value) >= 8 and value[:8].isdigit():
        return f"{value[0:4]}-{value[4:6]}-{value[6:8]}"
    return None


def classify_kind(summary: str) -> str:
    s = summary.strip()
    if s.startswith("Match"):
        return "match"
    if re.search(r"tr[äa]ning", s, re.IGNORECASE):
        return "training"
    return "other"


def extract_gathering(description: str) -> str | None:
    m = GATHERING_RE.search(description or "")
    if not m:
        return None
    time = m.group(1).replace(".", ":")
    parts = time.split(":")
    return f"{int(parts[0]):02d}:{parts[1]}"


def parse_events(ics_text: str) -> tuple[str | None, list[dict]]:
    text = unfold(ics_text.replace("\r\n", "\n").replace("\r", "\n"))
    cal_m = re.search(r"^X-WR-CALNAME:(.*)$", text, re.M)
    calendar_name = unescape(cal_m.group(1).strip()) if cal_m else None

    events: list[dict] = []
    for chunk in re.findall(r"BEGIN:VEVENT(.*?)END:VEVENT", text, re.S):
        summary = unescape(get_prop(chunk, "SUMMARY") or "").strip()
        location = unescape(get_prop(chunk, "LOCATION") or "").strip()
        description = unescape(get_prop(chunk, "DESCRIPTION") or "").strip()
        start = parse_ics_dt(get_prop(chunk, "DTSTART"))
        end = parse_ics_dt(get_prop(chunk, "DTEND"))
        if not start:
            continue
        event: dict = {
            "start": start,
            "end": end,
            "summary": summary,
            "location": location,
            "description": description,
            "kind": classify_kind(summary),
        }
        gathering = extract_gathering(description)
        if gathering:
            event["gathering"] = gathering
        events.append(event)

    events.sort(key=lambda e: e["start"])
    return calendar_name, events


def fetch_ics(url: str) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "family-dashboard-refresh/1.0"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--fetch",
        action="store_true",
        help=f"Download fresh ICS from {SOURCE_URL}",
    )
    args = ap.parse_args()

    if args.fetch:
        print(f"Fetching {SOURCE_URL} …", file=sys.stderr)
        data = fetch_ics(SOURCE_URL)
        ICS_PATH.write_bytes(data)
        print(f"Wrote {ICS_PATH} ({len(data)} bytes)", file=sys.stderr)

    if not ICS_PATH.exists():
        print(f"Missing {ICS_PATH}; run with --fetch", file=sys.stderr)
        return 1

    ics_text = ICS_PATH.read_text(encoding="utf-8", errors="replace")
    calendar_name, events = parse_events(ics_text)
    payload = {
        "updated": datetime.now().astimezone().date().isoformat(),
        "timezone": "Europe/Stockholm",
        "source": SOURCE_URL,
        "calendarName": calendar_name or "Sportadmin",
        "events": events,
    }
    JSON_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {JSON_PATH} ({len(events)} events)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
