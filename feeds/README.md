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
