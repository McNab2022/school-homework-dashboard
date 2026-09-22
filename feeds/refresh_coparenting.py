#!/usr/bin/env python3
"""Convert co-parenting ICS → JSON for the Family dashboard Key dates tab.

Usage:
  python3 feeds/refresh_coparenting.py           # ICS → JSON only
  python3 feeds/refresh_coparenting.py --fetch   # download ICS, then convert

Source URL is documented in feeds/README.md.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from datetime import date, datetime, timedelta
from pathlib import Path

FEED_DIR = Path(__file__).resolve().parent
ICS_PATH = FEED_DIR / "coparenting.ics"
JSON_PATH = FEED_DIR / "coparenting.json"
SOURCE_URL = (
    "https://script.google.com/macros/s/"
    "AKfycbxfOcUXPSFwl6NFLjOQp4rSGwoqc6V_zZ8Ra2-oKMVIrobNknJfABtdcnSxfigTeBQ/exec"
)

# 👨 Alex (7 days) / 👩 Anna-Karin / optional day count
CUSTODY_RE = re.compile(
    r"^(?:\U0001F469|\U0001F468)?\s*(Alex|Anna-Karin)(?:\s*\((\d+)\s*days?\))?\s*$",
    re.UNICODE,
)
# Also accept emoji variants that may appear as literal sequences in some files
CUSTODY_RE2 = re.compile(
    r"^(?:👩|👨)?\s*(Alex|Anna-Karin)(?:\s*\((\d+)\s*days?\))?\s*$",
    re.UNICODE,
)


def unfold(ics: str) -> str:
    return re.sub(r"\r?\n[ \t]", "", ics)


def parse_ics_date(raw: str | None) -> date | None:
    if not raw:
        return None
    value = raw.split(":")[-1].strip()
    if len(value) >= 8 and value[:8].isdigit():
        return date(int(value[0:4]), int(value[4:6]), int(value[6:8]))
    return None


def get_prop(block: str, name: str) -> str | None:
    m = re.search(rf"^{re.escape(name)}[;:](.*)$", block, re.M)
    if not m:
        return None
    return m.group(1).strip()


def parent_id(name: str) -> str:
    return "alex" if name == "Alex" else "anna-karin"


def parse_custody_blocks(ics_text: str) -> list[dict]:
    text = unfold(ics_text.replace("\r\n", "\n").replace("\r", "\n"))
    blocks: list[dict] = []
    for chunk in re.findall(r"BEGIN:VEVENT(.*?)END:VEVENT", text, re.S):
        summary = get_prop(chunk, "SUMMARY") or ""
        # Unescape common iCal escapes
        summary = summary.replace("\\,", ",").replace("\\n", " ").replace("\\;", ";")
        m = CUSTODY_RE2.match(summary.strip())
        if not m:
            continue
        parent_name = m.group(1)
        days_in_summary = int(m.group(2)) if m.group(2) else None
        start = parse_ics_date(get_prop(chunk, "DTSTART"))
        end_excl = parse_ics_date(get_prop(chunk, "DTEND"))
        if not start:
            continue
        if not end_excl:
            end_excl = start + timedelta(days=1)
        if end_excl <= start:
            continue
        end_incl = end_excl - timedelta(days=1)
        days = (end_excl - start).days
        blocks.append(
            {
                "start": start.isoformat(),
                "end": end_incl.isoformat(),
                "endExclusive": end_excl.isoformat(),
                "parent": parent_id(parent_name),
                "label": parent_name,
                "days": days_in_summary if days_in_summary is not None else days,
                "summary": summary.strip(),
            }
        )
    blocks.sort(key=lambda b: (b["start"], b["endExclusive"]))
    return blocks


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
    blocks = parse_custody_blocks(ics_text)
    payload = {
        "updated": datetime.now().astimezone().date().isoformat(),
        "timezone": "Europe/Stockholm",
        "source": SOURCE_URL,
        "blocks": blocks,
    }
    JSON_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {JSON_PATH} ({len(blocks)} custody blocks)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
