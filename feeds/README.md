# Family dashboard feeds

## Co-parenting (custody weeks)

- **Source URL:** https://script.google.com/macros/s/AKfycbxfOcUXPSFwl6NFLjOQp4rSGwoqc6V_zZ8Ra2-oKMVIrobNknJfABtdcnSxfigTeBQ/exec
- **Local ICS:** `coparenting.ics`
- **JSON for the UI:** `coparenting.json` (generated — do not hand-edit)

### Refresh

```bash
# From repo root (school-dashboard/):
python3 feeds/refresh_coparenting.py --fetch
# Or, if ICS is already updated locally:
python3 feeds/refresh_coparenting.py
```

`--fetch` downloads a fresh ICS from the source URL, saves `coparenting.ics`, then rebuilds `coparenting.json`.

Custody blocks are events whose SUMMARY looks like `👨 Alex (7 days)` / `👩 Anna-Karin (7 days)` (emoji + parent name, optional day count). Other calendar notes stay in the ICS but are omitted from the JSON.

## SportAdmin (Ollie football)

- **Source URL:** https://portalweb.sportadmin.se/webcal?id=f619c1f3-826c-4bd7-a8c8-a344b3470d48
- **Calendar:** Sportadmin Huddinge Idrottsförening (P2016 training + matches)
- **Local ICS:** `sportadmin.ics`
- **JSON for the UI:** `sportadmin.json` (generated — do not hand-edit)
- **Club messages (curated):** `sportadmin-messages.json` (hand-maintained bilingual summaries)

### Refresh

```bash
# From repo root (school-dashboard/):
python3 feeds/refresh_sportadmin.py --fetch
# Or, if ICS is already updated locally:
python3 feeds/refresh_sportadmin.py
```

`--fetch` downloads a fresh ICS from SportAdmin, saves `sportadmin.ics`, then rebuilds `sportadmin.json`.

Events are classified by SUMMARY: starts with `Match` → `match`; contains `träning`/`Träning` → `training`; otherwise `other`. Optional `gathering` is extracted from `Samling: HH:MM` in the description. Times use `Europe/Stockholm`.

## Health (logoped / dentist)

- **JSON for the UI:** `health.json` (static snapshot — no public ICS URL)
- **Sources:** Alex’s primary Google Calendar (`alex.mcnab2011@gmail.com`) and the Family calendar (`family03128392050150890041@group.calendar.google.com`)
- **Kinds:** `logoped`, `dentist`, or `other`; `who` is `Ellie` or `Ollie`

### Refresh

There is no public ICS feed. Refresh manually or via Grok Bot from Google Calendar (list/search events for logoped/dentist on primary + Family), then rewrite `health.json`. Do **not** commit OAuth secrets — keep a static JSON snapshot only.

Include upcoming appointments only. Past events are omitted.

Do not add pickup-clash flags: school finish times are FYI only; Ollie can go to fritids/Eftis or home.

## Other important dates (family / travel)

- **JSON for the UI:** `other-dates.json` (manual / Grok snapshot — hand-edit OK)
- **Sources:** Family calendar non-health events (trips, travel, etc.), curated into this file
- **Fields:** `start`, `end`, bilingual `summary` / `summary_sv`, optional `notes` / `notes_sv`, `location`, `who` (array of names), `source`

### Refresh

No public ICS URL yet. Maintain as a static snapshot (Grok Bot or hand-edit). Later this can pull Family calendar events that are not health (logoped/dentist). Include upcoming/current events only; past ones can be dropped. Empty notes are fine — fill in flight details later.

## School finish times (Vklass lectures)

- **ICS sources:** `ellie-lectures.ics`, `ollie-lectures.ics` (Vklass lecture exports)
- **JSON for the UI:** `schedule.json` (generated — do not hand-edit finish times)
- **Builder:** `python3 feeds/build_schedule.py`

Finish time per weekday = modal max `DTEND` of lessons that day. Keys are JS `getDay()` strings (`"1"`=Mon … `"5"`=Fri). Display names in the UI are Ellie / Ollie.

## Drums + orchestra (Ollie)

- **JSON for the UI:** `drums.json` (hand-maintained — edit OK)
- Friday drum lesson fields are at the top level (`day`, `time_start`, …).
- `orchestra` block: Thursday orchestra 18:10–18:50, every other Thursday, alternating with Thursday football. `orchestra.dates` lists the session dates (ISO `YYYY-MM-DD`); `date_notes` holds per-date notes (e.g. höstlov).

### Orchestra-week football skip rule

When `orchestra.skip_football_on_dates` is `true`, `index.html` marks any SportAdmin **training** event on a **Thursday** whose date is in `orchestra.dates` as skipped (greyed, struck through, flag "Orchestra week, no football" / "Orkestervecka, ingen fotboll"). The rule is applied at render time, so `sportadmin.json` stays untouched and `refresh_sportadmin.py` can regenerate it freely without undoing the skip. To change the alternation, edit `orchestra.dates` only.

## Standing weekly items (School tab)

- **JSON for the UI:** `standing.json` (hand-maintained — edit OK)
- Shown under the finish-time bar on the School tab. Bilingual `text` / `text_sv`, `who` array, `weekday` as JS `getDay()` number (4 = Thursday) for the "Today" flag.
- Kept separate from `data.json` / embedded `DASHBOARD_DATA` so the Friday Veckobrev refresh (which rewrites `items`) does not remove it.
