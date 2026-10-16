# RigLanes

**Taking over this project? Read [HANDOFF.md](HANDOFF.md) and [CONTRIBUTING-AGENTS.md](CONTRIBUTING-AGENTS.md).**

Parts compatibility database for 2–8 GPU local AI inference rigs. Plain static site (no build step).

- `index.html` – pitch + newsletter form (TODO placeholder, posts nowhere)
- `db.html` – searchable/filterable parts database
- `checker.html` – build checker (lanes, PSU headroom, 15A/120V circuit load)
- `submit.html` – submit-your-build form (TODO placeholder)
- `data/parts.json` – parts with per-part `source_url` and `verification`; unverified specs are blank
- `data/parts.js` – same data as `window.PARTS` for the pages
- `data/build_data.py` – regenerates both data files: `python3 data/build_data.py`

Run locally: `python3 -m http.server 8765` then open http://localhost:8765

Affiliate link fields (`affiliate_url`) are intentionally empty.

Deploy: pushes to `main` auto-deploy to https://riglanes.vercel.app (Vercel project `riglanes`, Git-linked). See HANDOFF.md section 2.
