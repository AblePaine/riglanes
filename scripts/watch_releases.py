#!/usr/bin/env python3
"""STUB: watch vLLM / llama.cpp / SGLang GitHub releases and flag WorksOn entries as 'needs retest'.

Usage:  python3 scripts/watch_releases.py          (then: python3 data/build_power_software.py is NOT needed;
        this script rewrites data/software.json and data/software.js directly)
Uses the public GitHub REST API without auth (60 requests/hour). Set GITHUB_TOKEN in your shell env to raise
the limit; never commit a token. State lives in data/release_state.json (kept out of the deployed site).

TODO: run on a schedule (e.g. a GitHub Action, after asking the owner), and open a PR instead of committing.
"""
import json, os, urllib.request
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPOS = {"vLLM": "vllm-project/vllm", "llama.cpp": "ggml-org/llama.cpp", "SGLang": "sgl-project/sglang"}
STATE = os.path.join(ROOT, "data", "release_state.json")
SOFT = os.path.join(ROOT, "data", "software.json")

def latest(repo):
    req = urllib.request.Request(f"https://api.github.com/repos/{repo}/releases/latest",
                                 headers={"Accept": "application/vnd.github+json", "User-Agent": "riglanes-watch"})
    if os.environ.get("GITHUB_TOKEN"):
        req.add_header("Authorization", "Bearer " + os.environ["GITHUB_TOKEN"])
    with urllib.request.urlopen(req, timeout=20) as r:
        d = json.load(r)
    return d["tag_name"], d.get("published_at")

def main():
    state = json.load(open(STATE)) if os.path.exists(STATE) else {}
    soft = json.load(open(SOFT))
    changed = False
    for engine, repo in REPOS.items():
        try:
            tag, when = latest(repo)
        except Exception as e:
            print(f"{engine}: could not fetch ({e})"); continue
        prev = state.get(engine, {}).get("tag")
        print(f"{engine}: latest {tag} ({when}); last seen {prev}")
        if prev and prev != tag:
            for e in soft:
                if e["engine"] == engine and not e.get("needs_retest"):
                    e["needs_retest"] = True
                    e["retest_reason"] = f"{engine} {tag} released {when}; entry tested on {e['version']}"
                    changed = True
        state[engine] = {"tag": tag, "published_at": when}
    json.dump(state, open(STATE, "w"), indent=1)
    if changed:
        json.dump(soft, open(SOFT, "w"), indent=1)
        open(os.path.join(ROOT, "data", "software.js"), "w").write("window.SOFTWARE=" + json.dumps(soft) + ";\n")
        print("Flagged entries as needs_retest. Review, retest, then clear the flag in software.json.")

if __name__ == "__main__":
    main()
