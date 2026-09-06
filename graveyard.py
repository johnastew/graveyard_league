#!/usr/bin/env python3
"""Graveyard fantasy football helper.

Pulls FantasyPros consensus rankings for a week and filters out every player
you have already started this season (they are locked out permanently under
League Tycoon "Graveyard" rules).

Usage:
    ./graveyard.py rankings [--week N] [--position FLEX] [--scoring HALF]
    ./graveyard.py use "Ja'Marr Chase" [more names...]
    ./graveyard.py unuse "Ja'Marr Chase"
    ./graveyard.py used
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import re
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = "https://api.fantasypros.com/public/v2/json"
ROOT = os.path.dirname(os.path.abspath(__file__))
USED_FILE = os.path.join(ROOT, "data", "used_players.json")
CACHE_DIR = os.path.join(ROOT, "data", "cache")

SUFFIXES = {"jr", "sr", "ii", "iii", "iv", "v"}

# FantasyPros' own spellings. "FLEX" and "DEF" are what everyone types, so we
# accept them and translate.
VALID_POSITIONS = {"QB", "RB", "WR", "TE", "K", "OP", "FLX", "DST", "IDP",
                   "DL", "LB", "DB", "TK", "TQB", "TRB", "TWR", "TTE", "TOL",
                   "HC", "P"}
POSITION_ALIASES = {"FLEX": "FLX", "DEF": "DST", "D/ST": "DST", "PK": "K"}


def resolve_position(pos: str) -> str:
    pos = pos.strip().upper()
    pos = POSITION_ALIASES.get(pos, pos)
    if pos not in VALID_POSITIONS:
        sys.exit(f"Unknown position {pos!r}. Valid: {', '.join(sorted(VALID_POSITIONS))}")
    return pos


# --------------------------------------------------------------------------- env
def load_dotenv(path: str | None = None) -> None:
    """Minimal .env loader so the session works after a plain reopen."""
    path = path or os.path.join(ROOT, ".env")
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            key, val = key.strip(), val.strip().strip('"').strip("'")
            os.environ.setdefault(key, val)


def api_key() -> str:
    key = os.environ.get("FANTASYPROS_API_KEY", "").strip()
    if not key:
        sys.exit(
            "FANTASYPROS_API_KEY is not set.\n"
            "Add it to .env (see .env.example) or export it in your shell."
        )
    return key


# ----------------------------------------------------------------- name matching
def norm(name: str) -> str:
    """Normalize a player name for comparison: 'Ja'Marr Chase Jr.' -> 'jamarr chase'."""
    name = unicodedata.normalize("NFKD", name)
    name = "".join(c for c in name if not unicodedata.combining(c))
    name = name.lower()
    name = re.sub(r"[^a-z0-9\s]", "", name)
    parts = [p for p in name.split() if p not in SUFFIXES]
    return " ".join(parts)


# ------------------------------------------------------------------- used roster
def load_used() -> list[dict]:
    if not os.path.exists(USED_FILE):
        return []
    with open(USED_FILE, encoding="utf-8") as fh:
        data = json.load(fh)
    # Tolerate a plain list of names as well as the richer record form.
    out = []
    for entry in data:
        if isinstance(entry, str):
            out.append({"name": entry, "week": None, "added": None})
        else:
            out.append(entry)
    return out


def save_used(entries: list[dict]) -> None:
    os.makedirs(os.path.dirname(USED_FILE), exist_ok=True)
    with open(USED_FILE, "w", encoding="utf-8") as fh:
        json.dump(entries, fh, indent=2)
        fh.write("\n")


# --------------------------------------------------------------------------- api
def fetch_rankings(season: int, week: int, position: str, scoring: str,
                   refresh: bool = False) -> dict:
    params = {
        "position": position,
        "scoring": scoring,
        "week": str(week),
        "type": "weekly" if week else "draft",
        "experts": "available",
    }
    url = f"{BASE_URL}/nfl/{season}/consensus-rankings?" + urllib.parse.urlencode(params)

    os.makedirs(CACHE_DIR, exist_ok=True)
    cache = os.path.join(CACHE_DIR, f"{season}-wk{week}-{position}-{scoring}.json")
    if os.path.exists(cache) and not refresh:
        with open(cache, encoding="utf-8") as fh:
            return json.load(fh)

    req = urllib.request.Request(url, headers={
        "x-api-key": api_key(),
        "Accept": "application/json",
        "User-Agent": "graveyard-league/1.0",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")[:400]
        sys.exit(f"FantasyPros API error {exc.code} for {position}/{scoring} week {week}:\n{body}")
    except urllib.error.URLError as exc:
        sys.exit(f"Could not reach FantasyPros: {exc.reason}")

    with open(cache, "w", encoding="utf-8") as fh:
        json.dump(payload, fh)
    return payload


def extract_players(payload: dict) -> list[dict]:
    rows = payload.get("players") or payload.get("data") or []
    out = []
    for p in rows:
        out.append({
            "rank": p.get("rank_ecr") or p.get("rank") or p.get("rank_ave"),
            "tier": p.get("tier"),
            "name": p.get("player_name") or p.get("name") or "",
            "position": (p.get("player_position_id") or p.get("position_id")
                         or p.get("position") or ""),
            "team": p.get("player_team_id") or p.get("team_id") or p.get("team") or "",
            "opponent": p.get("player_opponent") or p.get("opponent") or "",
            "bye": p.get("player_bye_week") or p.get("bye_week") or "",
            "ecr": p.get("rank_ave"),
            "best": p.get("rank_min"),
            "worst": p.get("rank_max"),
        })
    return [p for p in out if p["name"]]


# ------------------------------------------------------------------------ output
def print_table(players: list[dict], limit: int) -> None:
    shown = players[:limit] if limit else players
    if not shown:
        print("No eligible players returned.")
        return
    hdr = f"{'#':>4}  {'TIER':>4}  {'POS':<4} {'PLAYER':<24} {'TEAM':<4} {'MATCHUP':<8} {'ECR':>6}"
    print(hdr)
    print("-" * len(hdr))
    for p in shown:
        matchup = p["opponent"] or (f"BYE {p['bye']}" if p["bye"] else "")
        ecr = f"{p['ecr']:.1f}" if isinstance(p["ecr"], (int, float)) else ""
        print(f"{str(p['rank'] or ''):>4}  {str(p['tier'] or ''):>4}  "
              f"{str(p['position'])[:4]:<4} {p['name'][:24]:<24} "
              f"{str(p['team'])[:4]:<4} {str(matchup)[:8]:<8} {ecr:>6}")


def write_csv(players: list[dict], path: str) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)) or ".", exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(players[0].keys()) if players else
                           ["rank", "tier", "name", "position", "team", "opponent",
                            "bye", "ecr", "best", "worst"])
        w.writeheader()
        w.writerows(players)
    print(f"\nWrote {len(players)} rows to {path}")


# ---------------------------------------------------------------------- commands
def cmd_rankings(args: argparse.Namespace) -> None:
    position = resolve_position(args.position)
    payload = fetch_rankings(args.season, args.week, position,
                             args.scoring.upper(), refresh=args.refresh)
    players = extract_players(payload)
    used = {norm(e["name"]) for e in load_used()}
    eligible = [p for p in players if norm(p["name"]) not in used]
    burned = len(players) - len(eligible)

    print(f"Graveyard — {args.season} week {args.week} | {position} "
          f"| {args.scoring.upper()} scoring")
    print(f"{len(players)} ranked, {burned} already used, {len(eligible)} eligible\n")
    print_table(eligible, args.limit)
    if args.csv:
        write_csv(eligible, args.csv)


def cmd_use(args: argparse.Namespace) -> None:
    entries = load_used()
    have = {norm(e["name"]) for e in entries}
    today = dt.date.today().isoformat()
    for raw in args.names:
        if norm(raw) in have:
            print(f"already used: {raw}")
            continue
        entries.append({"name": raw.strip(), "week": args.week, "added": today})
        have.add(norm(raw))
        print(f"buried: {raw.strip()}" + (f" (week {args.week})" if args.week else ""))
    save_used(entries)
    print(f"{len(entries)} players used this season.")


def cmd_unuse(args: argparse.Namespace) -> None:
    entries = load_used()
    targets = {norm(n) for n in args.names}
    kept = [e for e in entries if norm(e["name"]) not in targets]
    removed = len(entries) - len(kept)
    save_used(kept)
    print(f"Removed {removed}. {len(kept)} players used this season.")


def cmd_used(args: argparse.Namespace) -> None:
    entries = load_used()
    if not entries:
        print("No players used yet — the whole pool is live.")
        return
    print(f"{len(entries)} players used this season:")
    for e in sorted(entries, key=lambda e: (e.get("week") or 0, e["name"])):
        wk = f"wk{e['week']}" if e.get("week") else "  -"
        print(f"  {wk:>4}  {e['name']}")


# ------------------------------------------------------------------------- entry
def default_week() -> int:
    """Rough NFL week from today's date; override with --week."""
    try:
        start = dt.date(int(os.environ.get("GRAVEYARD_SEASON", 0)) or dt.date.today().year, 9, 1)
    except ValueError:
        start = dt.date(dt.date.today().year, 9, 1)
    # first Thursday on/after Sep 1
    start += dt.timedelta(days=(3 - start.weekday()) % 7)
    week = (dt.date.today() - start).days // 7 + 1
    return max(1, min(18, week))


def main(argv: list[str] | None = None) -> None:
    load_dotenv()
    season_default = int(os.environ.get("GRAVEYARD_SEASON") or dt.date.today().year)

    ap = argparse.ArgumentParser(prog="graveyard", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd")

    r = sub.add_parser("rankings", help="show eligible players for a week")
    r.add_argument("--season", type=int, default=season_default)
    r.add_argument("--week", type=int, default=default_week())
    r.add_argument("--position", default="FLEX",
                   help="FLEX/FLX, QB, RB, WR, TE, K, DST, OP, ...")
    r.add_argument("--scoring", default="HALF")
    r.add_argument("--limit", type=int, default=50, help="0 for all")
    r.add_argument("--csv", help="also write results to this CSV path")
    r.add_argument("--refresh", action="store_true", help="bypass the local cache")
    r.set_defaults(func=cmd_rankings)

    u = sub.add_parser("use", help="mark players as started (locks them out)")
    u.add_argument("names", nargs="+")
    u.add_argument("--week", type=int, default=None)
    u.set_defaults(func=cmd_use)

    n = sub.add_parser("unuse", help="undo a mistaken 'use'")
    n.add_argument("names", nargs="+")
    n.set_defaults(func=cmd_unuse)

    l = sub.add_parser("used", help="list players already burned this season")
    l.set_defaults(func=cmd_used)

    args = ap.parse_args(argv)
    if not args.cmd:
        args = ap.parse_args(["rankings"])
    args.func(args)


if __name__ == "__main__":
    main()
