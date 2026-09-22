# Family dashboard

Open **`index.html`** via GitHub Pages or a local static server (`python3 -m http.server` in this folder). The School tab embeds homework data for offline use; the **Key dates** and **Sport & Hobbies** tabs load JSON under `feeds/` (needs HTTP, not `file://`).

## Tabs

1. **School** — Källbrinksskolan homework & tests (`data.json` + embedded copy in `index.html`)
2. **Sport & Hobbies** — Ollie’s football schedule (SportAdmin) + club messages; drums placeholder
3. **Health** — placeholder (logoped / dentist once Family Google Calendar is connected)
4. **Key dates** — co-parenting custody weeks from the ICS feed

Language: EN/SV toggle (saved in `localStorage` as `school-dashboard-lang`). Active tab: `family-dashboard-tab`.

## Refresh feeds

```bash
# Co-parenting custody
python3 feeds/refresh_coparenting.py --fetch   # download ICS + rebuild JSON
python3 feeds/refresh_coparenting.py           # ICS already on disk → JSON only

# SportAdmin football (Ollie)
python3 feeds/refresh_sportadmin.py --fetch    # download ICS + rebuild JSON
python3 feeds/refresh_sportadmin.py            # ICS already on disk → JSON only
```

Source URLs and details: see `feeds/README.md`.

**Grok Bot** refreshes school homework when emails/letters arrive, can re-run the co-parenting script when the custody calendar changes, and can refresh SportAdmin when the football calendar or club emails change.
