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
