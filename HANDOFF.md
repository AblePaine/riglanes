# RigLanes handoff

Written 2026-10-16. Whoever picks this up next: read this file and then [CONTRIBUTING-AGENTS.md](CONTRIBUTING-AGENTS.md).

## 1. What RigLanes is and why it exists

RigLanes is a parts compatibility database for **2–8 GPU local AI inference rigs**, with a newsletter on top. It answers the questions people building multi-GPU boxes keep asking in forum threads:
- How many CPU PCIe lanes does each slot actually get?
- Which slots can be bifurcated?
- Will this PSU feed N GPUs?
- Will the rig trip a 15A/120V household circuit?

**Revenue plan (none of it is set up yet):**
1. Affiliate links on parts. The `affiliate_url` field exists but every entry is empty.
2. Sponsors in the newsletter and on the site (risers, PSU, frame and board makers).
3. Paid "verified listings", where a vendor pays to have a part tested or verified. These must be clearly labelled and must never change the specs.

### Demand evidence (public threads)
- r/LocalLLaMA: HUANANZHI H12D-8D + 4x RTX 3090 for LLM inference. The owner is asking for real per-slot and bifurcation info because "documentation and real-world reports are a bit scattered". https://www.reddit.com/r/LocalLLaMA/comments/1t2hejy/anyone_running_huananzhi_h12d8d_bmc_with_4x_rtx/
- r/LocalLLM: "Optimal AM5 mobo for 4x3090?" Confusion about chipset x1 slots vs CPU lanes, bifurcation and PCIe switches. https://www.reddit.com/r/LocalLLM/comments/1wife7u/optimal_am5_mobo_for_4x3090/
- r/LocalLLaMA: "4 GPU on AM5 platform". Bifurcation and M.2-riser questions, PCIe errors, and slot power worries. https://www.reddit.com/r/LocalLLaMA/comments/1hipolr/4_gpu_on_am5_platform/
- r/LocalLLaMA: EPYC 9575F + 4x RTX 3090 build (Supermicro H13SSL-N, 2050W PSU, Corsair 9000D, 250W power limits). 380+ points, and the comments are asking about slot power and risers. https://www.reddit.com/r/LocalLLaMA/comments/1tx9tf2/finally_finished_my_llm_server_epyc_9575f_4_rtx/
- cpompa.com: 4x RTX 3090 inference server guide (EPYC + ROMED8-2T, NVLink, power limiting). It shows people want written build guides. https://cpompa.com/docs/ai-inference-3090.html
- More along the same lines: https://www.reddit.com/r/LocalLLaMA/comments/1rozgei/best_way_to_build_a_4_rtx_3090_ai_server_with/ and https://www.reddit.com/r/LocalLLaMA/comments/1f7vpnw/need_advice_on_4x3090_inference_build/

### Competitor gaps
Re-verify these before quoting them publicly; they reflect the original research and general knowledge.
- **PCPartPicker** checks socket, size and wattage fit. It does not model per-slot CPU vs chipset lanes, bifurcation, risers or PCIe switches, multi-PSU setups, or circuit load. It is also consumer-focused, with thin coverage of EPYC and server boards.
- **Forum threads and single-build guides** (Reddit, ServeTheHome, cpompa.com, club-3090 on GitHub) hold the real knowledge, but it is scattered, tied to one build, and not searchable by spec.
- **Maker spec pages** often skip lane sharing, physical slot order and bifurcation modes. RigLanes collects those details and links the source for each one.

### Future add-ons (ideas, not built)
- **TokPerDollar**: a page ranking GPUs and rigs by tokens per second per dollar (and per watt), using community-submitted benchmarks.
- **DealRig**: tracks used and new prices for the parts in the database (for example used 3090s and EPYC boards) and alerts subscribers to deals. It pairs naturally with affiliate revenue.

## 2. Current state

| Item | Value |
|---|---|
| Live site | https://riglanes.vercel.app (alias: https://riglanes-able-paine.vercel.app) |
| Vercel | Project `riglanes` in the team/scope `able-paine`, free Hobby plan, no custom domain. Deployment protection is off (public). |
| GitHub | https://github.com/AblePaine/riglanes (public, branch `main`) |
| Deploy method | **Git auto-deploy.** Vercel project `riglanes` is linked to `AblePaine/riglanes`, production branch `main`, framework Other, no build command, served from repo root. Every push to `main` builds and goes live on riglanes.vercel.app (also riglanes-git-main-able-paine.vercel.app). First git deploy: commit 265fab6 on 2026-10-16. |
| Parts | 47 in total: 19 motherboards, 9 GPUs, 8 PSUs, 6 risers, 2 PCIe switches, 3 cases. |
| Verification | 46 were checked on the maker's own product or spec page on 2026-10-16. 1 (Super Flower Leadex Platinum 2000W) used a third-party review because the maker page was unavailable. |

The site is plain static HTML with no framework and no build step:
- `index.html`: pitch, plus the newsletter form (placeholder)
- `db.html`: the database, with search and filters
- `checker.html`: the build checker
- `submit.html`: the build submission form (placeholder)
- `style.css`, plus the data files in `data/`

## 2b. RigWatts and WorksOn (added 2026-10-16 on branch `power-software`)

- **RigWatts** (`power.html`, `data/power.json`): measured power for real multi-GPU builds, plus a planner.
  - The planner covers circuits of 15A/20A at 120V, 240V, and 16A at 230V, with 80% continuous-load headroom, an optional peak/transient check, and monthly cost.
  - Default rate: the EIA US average residential price for July 2026, 18.31¢/kWh, from Electric Power Monthly Table 5.6.A. Update it when EIA publishes newer data.
  - The build checker links its wall-draw estimate into the planner (`power.html?w=`).
  - 4 entries so far: 2 measured at the wall, 1 GPU-only, 1 author estimate. Each is labelled in the `measurement` field.
- **WorksOn** (`software.html`, `data/software.json`): rows of card × engine version × backend → works yes/partial/no, plus TP/P2P/NVLink notes, flags/patches, a source URL and a date. 15 entries so far.
- `data/build_power_software.py` regenerates both datasets. It keeps any `needs_retest` flags already set.
- `scripts/watch_releases.py` is a **stub**. It checks the latest GitHub releases of vLLM, llama.cpp and SGLang. When a release differs from what's in `data/release_state.json`, it marks rows for that engine `needs_retest`. It isn't scheduled yet: running it on a GitHub Action needs the owner's OK.
- Both submit forms are placeholders marked TODO. They send nothing.
- **Sources that couldn't be opened:** Reddit blocked every fetch (www, old. and .json all returned 403 or a login wall). That covers r/LocalLLaMA 1o528nk (idle power), 1g54h9l (Supermicro 4x3090), 1jsyv56 (Threadripper 8x3090), and r/ROCm 1uaedpw (R9700 on vLLM 0.22.1). None of their numbers are in the data, even where search snippets showed some. Retry them from a logged-in browser, with the owner's OK, or ask the authors.

## 3. Data schema and how to add or verify parts

**The rule:** only specs confirmed on the maker's page or datasheet. If a spec is unverified, leave it **blank** (`""` / `null`). Never guess. Every part has a `source_url`.

Edit `data/build_data.py`, then run `python3 data/build_data.py`. That regenerates both `data/parts.json` and `data/parts.js`. Don't hand-edit the generated files.

Fields in every part:
- `id`: kebab-case
- `category`: `motherboard`, `gpu`, `psu`, `riser`, `switch` or `case`
- `name`, `manufacturer`
- `source_url`
- `verification`: for example "manufacturer page fetched YYYY-MM-DD"
- `notes`
- `affiliate_url`: always "" for now

Fields by category:
- **motherboard:**
  - Platform and form: `platform`, `socket`, `form_factor`
  - `slots`: a list of `{gen, lanes, label}`
  - `gpu_slot_count`: counts slots with ≥ x8
  - `cpu_lanes_to_slots`
  - `bifurcation`
- **gpu:** `vram_gb`, `tdp_w` (board power), `power_connector`
- **psu:** `wattage`, `input_voltage` (state the 120V rating if it differs), `pcie_8pin`, `pcie_12v_2x6`
- **riser / switch:**
  - Link: `pcie_gen`, `lanes`, `length`
  - Switch-specific: `upstream`, `downstream`, `bifurcation_modes`
  - Other: `power`, `inputs`, `outputs`
- **case:** `form_factor`/`mb_support`, `expansion_slots`, `max_gpu_length_mm`, `psu_max_length_mm`

**To verify a part:**
1. Open the maker page (or the PDF manual for slot and bifurcation detail).
2. Copy only what it states.
3. Update `verification` with the date.
4. If the source is not the maker, say so in `verification`.

## 4. Known gaps

- **RigWatts/WorksOn:**
  - Small datasets (4 power rows, 15 software rows), and no SGLang entries yet.
  - Reddit sources are unreachable without a login.
  - Only 2 power rows are true wall readings.
  - The planner ignores PSU efficiency curves and other loads on the circuit.
  - The release watcher is an unscheduled stub.

- **ASRock Rack ROMED8-2T:** the maker page doesn't show per-slot lane sharing with OCuLink and M.2. Needs the manual.
- **Supermicro H12SSL-i / H12SSL-NT / H13SSL-N:** physical slot order isn't on the product pages. Needs the manuals.
- **Blank bifurcation fields:** most boards. The ASUS WRX90E and TRX50 pages point to an ASUS FAQ that wasn't fetched.
- **Blank PCIe connector counts:** PSUs Seasonic Prime PX-1600, Super Flower Leadex Platinum 2000W and Corsair HX1500i (2025).
- **Gigabyte MZ32-AR0:** Slot_1 is counted as x8, assuming Slot_2 is populated.
- **No open frames:** Veddha and AAAwave were dropped because there was no reliable maker spec page.
- **The checker doesn't model** risers or switches (lane fan-out, signal-integrity limits), transient power spikes, per-GPU connector counts against PSU connectors, multi-PSU setups, or slot power.
- **The newsletter and submit forms send nothing.** They are TODO placeholders.
- **No affiliate IDs,** no sponsors, **no domain**.

## 5. Prioritized roadmap

1. ~~Connect the repo to Vercel~~ (done 2026-10-16).
2. **Wire up the forms** with a free provider (Buttondown free tier for the newsletter; a Vercel function plus free storage, or a GitHub-issue form, for submissions). **Ask the owner before creating any new account.**
3. **Grow to 100+ parts,** same verification rule. Priorities: open frames, more risers and MCIO/OCuLink adapters, 2000W+ and 240V PSUs, used-market boards (H12SSL, ROMED8-2T, MZ32).
4. **Affiliate sign-ups** (Amazon, Newegg and others). These need the owner, since they involve the owner's identity and tax info.
5. **A weekly newsletter:** new parts, a build of the week, deals.
6. **A build-report pipeline:** submissions → review → published build pages with measured tokens/s and power.
7. **Sponsor outreach.** The owner must approve every new contact and every deal.
8. **A domain purchase** (for example riglanes.com). Needs owner approval, since it costs money.
9. **Grow RigWatts/WorksOn:** wall-meter submissions, SGLang rows, and retesting rows that the watcher flags.
10. **The TokPerDollar page,** using benchmark data from build reports.

## 6. Operating principles

- The owner just taps **yes/no**. Bring one clear recommendation with a reason, not a menu.
- **Always ask first** before spending money, emailing or messaging anyone new, deleting anything, or connecting or creating an account.
- Never invent specs. Blank beats wrong.
- No secrets in the repo.
- Talk like a friend texting: short, plain and direct.
