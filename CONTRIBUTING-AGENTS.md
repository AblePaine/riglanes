# Instructions for AI agents working on RigLanes

Read [HANDOFF.md](HANDOFF.md) first.

## Setup
```bash
git clone https://github.com/AblePaine/riglanes && cd riglanes
python3 -m http.server 8765   # open http://localhost:8765
```
No npm, no framework, no build step. The pages load `style.css` and `data/parts.js` (`window.PARTS`).

## Adding or fixing a part
1. Find the **maker's** product page, spec sheet or manual PDF. Fetch it for real; don't rely on memory, retailers, or AI summaries.
2. Add or edit the entry in `data/build_data.py` using the helper for its category (`mb`, `psu`, `gpu`, `acc`).
3. Fill only the fields the source states. Leave everything else blank. Put caveats in `notes`.
4. Set `source_url` to the page you used. Set `verification` to `manufacturer page fetched YYYY-MM-DD`, or name the non-maker source.
5. Run `python3 data/build_data.py`, then check that the count in `db.html` matches.
6. Commit with a message like `parts: add <name> (verified <source domain>)`.

## RigWatts (power) and WorksOn (software) data
- Edit `data/build_power_software.py`, then run it. It writes `data/power.{json,js}` and `data/software.{json,js}`.
- **Power rows:** only numbers the source states.
  - Always fill `measurement` with how the number was taken: `wall`, `GPU only`, or `author estimate`. Set `measured=False` for estimates.
  - Never convert a GPU-only reading into a wall figure.
- **Software rows:** one card × engine version × backend per row.
  - `works` is `yes`, `partial` or `no`.
  - Copy flags and patches exactly as written in the source, and give the source's date.
  - Never write "works" for a version the source didn't test.
- A source you couldn't open (e.g. Reddit returning 403) means **skip it**. Don't use search-snippet numbers.
- Run `python3 scripts/watch_releases.py` to flag rows `needs_retest` when vLLM, llama.cpp or SGLang releases. After retesting with a source, clear `needs_retest` and `retest_reason` in `software.json` (or in the build script output).
- The default $/kWh in `power.html` is EIA data. When you update it, update the month and the link with it.

## Changing the site
- Keep it static. A dependency or build step needs a real reason, written down in HANDOFF.md.
- Test `db.html` filters and `checker.html` in a browser (headless Playwright is fine) and check the console for errors.
- If you change the checker logic, describe the new assumptions in HANDOFF.md section 4.

## Deploying
- The repo is linked to Vercel (project `riglanes`, scope `able-paine`): pushing to `main` deploys it. After each push, confirm https://riglanes.vercel.app returns 200 on every page and shows the right part count.
- Never buy domains, upgrade plans, or turn on paid features without the owner saying yes.

- **Not served:** `.vercelignore` keeps HANDOFF.md, CONTRIBUTING-AGENTS.md, README.md, data/build_data.py, data/parts.json, data/build_power_software.py, data/power.json, data/software.json, data/release_state.json, scripts/ and .gitignore out of the Vercel deployment, so they 404 on the live site but stay in the repo. Add any new repo-only file there. Never list the pages, `style.css`, or `data/parts.js`, `data/power.js` and `data/software.js`.

## Hard rules
- Ask the owner (a yes/no with a recommendation) before you spend money, email or message anyone new, delete anything, or create or connect an account.
- Never commit secrets, tokens, API keys or private IDs.
- Never invent specs. A blank field is correct when the specs are unverified.
- Leave `affiliate_url` empty until the owner sets up affiliate accounts.
- Update HANDOFF.md (state, gaps, roadmap) at the end of every work session.
