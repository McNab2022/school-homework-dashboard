# Family dashboard

Open **`index.html`** via GitHub Pages or a local static server (`python3 -m http.server` in this folder). The School tab embeds homework data for offline use; the **Key dates** tab loads `feeds/coparenting.json` (needs HTTP, not `file://`).

## Tabs

1. **School** — Källbrinksskolan homework & tests (`data.json` + embedded copy in `index.html`)
2. **Sport & Hobbies** — placeholder (Ollie’s football / drums)
3. **Health** — placeholder (logoped / dentist)
4. **Key dates** — co-parenting custody weeks from the ICS feed

Language: EN/SV toggle (saved in `localStorage` as `school-dashboard-lang`). Active tab: `family-dashboard-tab`.

## Refresh co-parenting feed

```bash
python3 feeds/refresh_coparenting.py --fetch   # download ICS + rebuild JSON
python3 feeds/refresh_coparenting.py           # ICS already on disk → JSON only
```

Source URL and details: see `feeds/README.md`.

**Grok Bot** refreshes school homework when emails/letters arrive, and can re-run the co-parenting script when the custody calendar changes.
