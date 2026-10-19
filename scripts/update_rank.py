#!/usr/bin/env python3
"""Fetch live Valorant rank for avendail#4974 and write rank.json.

Uses the unofficial HenrikDev API (https://docs.henrikdev.xyz). Needs a free
API key in the HENRIK_API_KEY env var (GitHub repo secret).
If the request fails, rank.json is left untouched so the site keeps showing
the last known rank.
"""
import json, os, sys, urllib.request, urllib.error
from datetime import datetime, timezone

NAME, TAG = "avendail", "4974"
REGION, PLATFORM = "na", "pc"
OUT = os.environ.get("RANK_OUT", "rank.json")
URL = f"https://api.henrikdev.xyz/valorant/v3/mmr/{REGION}/{PLATFORM}/{NAME}/{TAG}"


def fetch():
    key = os.environ.get("HENRIK_API_KEY")
    if not key:
        sys.exit("HENRIK_API_KEY is not set")
    req = urllib.request.Request(URL, headers={"Authorization": key, "User-Agent": "portfolio-rank-tracker"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def main():
    try:
        body = fetch()
    except (urllib.error.URLError, TimeoutError) as e:
        sys.exit(f"API request failed, keeping old rank.json: {e}")

    d = body.get("data") or {}
    cur = d.get("current") or {}
    peak = d.get("peak") or {}
    tier = (cur.get("tier") or {}).get("name")
    if not tier:
        sys.exit(f"Unexpected response shape, keeping old rank.json: {str(body)[:300]}")

    out = {
        "tag": f"{NAME}#{TAG}",
        "tier": tier,                      # e.g. "Ascendant 2"
        "rr": cur.get("rr"),               # rank rating 0-99
        "peak": (peak.get("tier") or {}).get("name"),
        "updated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }

    # Skip the write (and therefore the commit) when nothing changed.
    try:
        with open(OUT) as f:
            old = json.load(f)
        if all(old.get(k) == out[k] for k in ("tier", "rr", "peak")):
            print("Rank unchanged:", tier, out["rr"], "RR")
            return
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2)
        f.write("\n")
    print("Wrote", OUT, out)


if __name__ == "__main__":
    main()
