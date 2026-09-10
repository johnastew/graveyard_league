#!/usr/bin/env python3
"""Graveyard fantasy football helper.

Pulls FantasyPros consensus rankings for a week and filters out every player
you have already started this season (they are locked out permanently under
League Tycoon "Graveyard" rules).

Usage:
    ./graveyard.py rankings [--week N] [--position FLEX] [--scoring HALF]
    ./graveyard.py cheapest [--week N] [--target 100] [--scoring HALF]
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
def as_num(v):
    """The API returns numbers as strings ("1.00"); make them sortable/printable."""
    if v is None or v == "":
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


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
            "rank": p.get("rank_ecr"),
            "pos_rank": p.get("pos_rank", ""),
            "name": p.get("player_name", ""),
            "position": p.get("player_position_id", ""),
            "team": p.get("player_team_id", ""),
            "opponent": p.get("player_opponent", ""),
            "bye": p.get("player_bye_week", ""),
            "ecr": as_num(p.get("rank_ave")),
            "best": as_num(p.get("rank_min")),
            "worst": as_num(p.get("rank_max")),
            "stdev": as_num(p.get("rank_std")),
            "rostered": as_num(p.get("player_owned_avg")),
        })
    return [p for p in out if p["name"]]


# ------------------------------------------------------------------------ output
def print_table(players: list[dict], limit: int) -> None:
    shown = players[:limit] if limit else players
    if not shown:
        print("No eligible players returned.")
        return
    hdr = (f"{'#':>4}  {'POSRK':<6} {'PLAYER':<24} {'TEAM':<4} {'MATCHUP':<8} "
           f"{'ECR':>6}  {'RANGE':>9}  {'ROST%':>6}")
    print(hdr)
    print("-" * len(hdr))
    for p in shown:
        matchup = p["opponent"] or (f"BYE {p['bye']}" if p["bye"] else "")
        ecr = f"{p['ecr']:.1f}" if p["ecr"] is not None else ""
        if p["best"] is not None and p["worst"] is not None:
            rng = f"{p['best']:.0f}-{p['worst']:.0f}"
        else:
            rng = ""
        rost = f"{p['rostered']:.0f}%" if p["rostered"] is not None else ""
        print(f"{str(p['rank'] or ''):>4}  {str(p['pos_rank'])[:6]:<6} "
              f"{p['name'][:24]:<24} {str(p['team'])[:4]:<4} "
              f"{str(matchup)[:8]:<8} {ecr:>6}  {rng:>9}  {rost:>6}")


def write_csv(players: list[dict], path: str) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)) or ".", exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(players[0].keys()) if players else
                           ["rank", "tier", "name", "position", "team", "opponent",
                            "bye", "ecr", "best", "worst"])
        w.writeheader()
        w.writerows(players)
    print(f"\nWrote {len(players)} rows to {path}")


# ------------------------------------------------------------------ value model
# The consensus-rankings endpoint gives ranks, not points, so a lineup total has
# to come from a rank -> points curve. These are anchor points (positional rank,
# half-PPR points) for a typical week, linearly interpolated between and held
# flat outside. They are deliberately coarse: the optimizer only needs the
# ordering and the rough shape of the drop-off to pick a slot to upgrade.
# Override any of it with --curves path/to/curves.json using the same shape.
POINT_CURVES = {
    "QB":  [(1, 21.0), (6, 19.0), (12, 16.5), (20, 13.5), (32, 10.5), (48, 6.0)],
    "RB":  [(1, 19.0), (6, 14.5), (12, 11.5), (24, 8.5), (48, 5.0), (80, 2.0)],
    "WR":  [(1, 18.0), (6, 14.0), (12, 11.5), (24, 8.5), (48, 5.5), (90, 2.0)],
    "TE":  [(1, 15.0), (4, 10.5), (12, 7.0), (24, 4.5), (40, 2.0)],
    "DST": [(1, 10.0), (6, 8.0), (12, 6.5), (20, 5.0), (32, 3.5)],
    "K":   [(1, 9.5), (6, 8.5), (12, 7.5), (24, 6.0), (32, 5.0)],
}

# Slot -> positions that may fill it. Mirrors the League Tycoon Graveyard board.
LINEUP_SLOTS = [
    ("QB", ("QB",)),
    ("RB", ("RB",)),
    ("RB", ("RB",)),
    ("WR", ("WR",)),
    ("WR", ("WR",)),
    ("TE", ("TE",)),
    ("FLEX", ("RB", "WR", "TE")),
    ("SFLX", ("QB", "RB", "WR", "TE")),
    ("DST", ("DST",)),
]

# Positions to pull rankings for. One API call each, all cached.
LINEUP_POSITIONS = ("QB", "RB", "WR", "TE", "DST")

# Week-to-week coefficient of variation by position: how far a typical week
# swings from the projection. QBs are the steadiest scorers; TEs and defenses
# are close to coin flips.
POSITION_CV = {"QB": 0.35, "RB": 0.50, "WR": 0.55, "TE": 0.60, "DST": 0.65,
               "K": 0.45}

# How pessimistic "floor" is, in standard deviations below the projection.
# 0.85 is roughly a 20th-percentile week.
FLOOR_Z = 0.85

# Roughly the last rank at each position you could stream off waivers in any
# given week. Points above this line are what actually make a player scarce,
# and so are what you are really spending when Graveyard burns him.
REPLACEMENT_RANK = {"QB": 24, "RB": 48, "WR": 60, "TE": 24, "DST": 24, "K": 24}

# How many future weeks' worth of that scarcity you give up by starting a player
# now. 0 would price a burn at one week of points, which badly underrates the
# cost of spending a stud in a week you did not need him.
DEFAULT_REUSE = 2.0

# How many candidates per slot the upgrade search looks at each pass. The pool
# is sorted by floor, so this only ever trims players too weak to be an upgrade.
UPGRADE_WIDTH = 60


def load_curves(path: str | None) -> dict:
    if not path:
        return POINT_CURVES
    with open(path, encoding="utf-8") as fh:
        raw = json.load(fh)
    curves = dict(POINT_CURVES)
    for pos, pts in raw.items():
        curves[pos.upper()] = sorted((float(r), float(p)) for r, p in pts)
    return curves


def curve_points(curves: dict, position: str, rank: float | None) -> float:
    """Interpolate a positional rank into weekly points."""
    pts = curves.get((position or "").upper())
    if not pts or rank is None:
        return 0.0
    if rank <= pts[0][0]:
        return pts[0][1]
    if rank >= pts[-1][0]:
        return pts[-1][1]
    for (r0, p0), (r1, p1) in zip(pts, pts[1:]):
        if r0 <= rank <= r1:
            span = r1 - r0
            if span <= 0:
                return p1
            return p0 + (p1 - p0) * (rank - r0) / span
    return pts[-1][1]


def pos_rank_number(player: dict) -> float | None:
    """'RB14' -> 14. Falls back to the rank within this position's fetch."""
    m = re.search(r"(\d+)", str(player.get("pos_rank") or ""))
    if m:
        return float(m.group(1))
    return as_num(player.get("rank"))


def score_player(player: dict, curves: dict, reuse: float = DEFAULT_REUSE) -> dict:
    """Attach floor / projection / value to a ranked player.

    projection what he is worth at consensus rank
    sigma      how far a typical week swings from that projection
    value      what starting him costs you, since Graveyard burns him for the
               season: this week's points plus the scarcity you can no longer
               spend later. A player at replacement level costs about what he
               scores, because you could always find another like him; a stud
               costs several times that, because you only get him once.
    """
    pos = player["position"]
    consensus = pos_rank_number(player)
    scored = dict(player)
    scored["projection"] = curve_points(curves, pos, consensus)
    scored["sigma"] = scored["projection"] * POSITION_CV.get(pos.upper(), 0.55)
    replacement = curve_points(curves, pos, REPLACEMENT_RANK.get(pos.upper()))
    surplus = max(0.0, scored["projection"] - replacement)
    scored["value"] = scored["projection"] + surplus * reuse
    return scored


def build_pool(season: int, week: int, scoring: str, curves: dict,
               reuse: float = DEFAULT_REUSE, refresh: bool = False) -> list[dict]:
    used = {norm(e["name"]) for e in load_used()}
    pool, seen = [], set()
    for pos in LINEUP_POSITIONS:
        payload = fetch_rankings(season, week, pos, scoring, refresh=refresh)
        for p in extract_players(payload):
            key = norm(p["name"])
            if key in used or key in seen:
                continue
            # A player on bye cannot score; leave him out entirely.
            if p["opponent"] in ("", None) and p["bye"] and str(p["bye"]) == str(week):
                continue
            p["position"] = p["position"] or pos
            seen.add(key)
            pool.append(score_player(p, curves, reuse))
    return pool


# ------------------------------------------------------------------- optimizer
def lineup_floor(lineup) -> float:
    """Pessimistic total for the lineup as a whole.

    Not the sum of each player's own floor -- that would assume all nine bust
    in the same week, which is far more pessimistic than reality. Nine players
    are close enough to independent that their variances add in quadrature, so
    the lineup's downside is much tighter than any one player's.
    """
    import math
    proj = sum(p["projection"] for p in lineup if p)
    var = sum(p["sigma"] ** 2 for p in lineup if p)
    return proj - FLOOR_Z * math.sqrt(var)


def cheapest_lineup(pool: list[dict], target: float) -> tuple[list[dict | None], bool]:
    """Cheapest lineup (least value burned) whose floors sum to >= target.

    Greedy: start from the cheapest legal lineup, then repeatedly make the
    upgrade with the best floor gained per point of value spent. That is a
    heuristic, not a proven optimum, but the value curve is smooth enough that
    the picks it makes are the ones you would make by hand.
    """
    by_slot = []
    for _, allowed in LINEUP_SLOTS:
        cands = [p for p in pool if p["position"] in allowed]
        cands.sort(key=lambda p: (p["value"], p["name"]))
        by_slot.append(cands)

    lineup: list[dict | None] = [None] * len(LINEUP_SLOTS)
    taken: set[str] = set()

    # Scarcest slot first, so a thin position is not left with nothing.
    for idx in sorted(range(len(LINEUP_SLOTS)), key=lambda i: len(by_slot[i])):
        for cand in by_slot[idx]:
            if norm(cand["name"]) not in taken:
                lineup[idx] = cand
                taken.add(norm(cand["name"]))
                break

    while lineup_floor(lineup) < target:
        base_floor = lineup_floor(lineup)
        best = None  # (efficiency, slot index, candidate)
        for idx, cands in enumerate(by_slot):
            current = lineup[idx]
            base_value = current["value"] if current else 0.0
            ranked = sorted(cands, key=lambda p: -p["projection"])[:UPGRADE_WIDTH]
            for cand in ranked:
                if norm(cand["name"]) in taken and cand is not current:
                    continue
                trial = list(lineup)
                trial[idx] = cand
                d_floor = lineup_floor(trial) - base_floor
                d_value = cand["value"] - base_value
                if d_floor <= 1e-9:
                    continue
                # A free or cheaper upgrade is always worth taking.
                eff = d_floor / d_value if d_value > 1e-9 else float("inf")
                if best is None or eff > best[0]:
                    best = (eff, idx, cand)
        if best is None:
            return lineup, False  # target is out of reach with what is left
        _, idx, cand = best
        if lineup[idx]:
            taken.discard(norm(lineup[idx]["name"]))
        lineup[idx] = cand
        taken.add(norm(cand["name"]))

    return lineup, True


def print_lineup(lineup: list[dict | None], target: float, made_it: bool) -> None:
    hdr = (f"{'SLOT':<6} {'PLAYER':<24} {'POS':<4} {'TEAM':<4} {'MATCHUP':<8} "
           f"{'PROJ':>6} {'SIGMA':>6} {'BURN':>6}")
    print(hdr)
    print("-" * len(hdr))
    for (slot, _), p in zip(LINEUP_SLOTS, lineup):
        if not p:
            print(f"{slot:<6} {'-- nobody eligible --':<24}")
            continue
        matchup = p["opponent"] or (f"BYE {p['bye']}" if p["bye"] else "")
        print(f"{slot:<6} {p['name'][:24]:<24} {str(p['position'])[:4]:<4} "
              f"{str(p['team'])[:4]:<4} {str(matchup)[:8]:<8} "
              f"{p['projection']:>6.1f} {p['sigma']:>6.1f} {p['value']:>6.1f}")
    floor = lineup_floor(lineup)
    proj = sum(p["projection"] for p in lineup if p)
    burn = sum(p["value"] for p in lineup if p)
    print("-" * len(hdr))
    print(f"{'TOTAL':<6} {'':<24} {'':<4} {'':<4} {'':<8} "
          f"{proj:>6.1f} {'':>6} {burn:>6.1f}")
    print(f"{'':<6} {'lineup floor (20th pctile)':<24} {'':<4} {'':<4} {'':<8} "
          f"{floor:>6.1f}")
    print()
    if made_it:
        print(f"Floor {floor:.1f} clears the {target:.1f} target by {floor - target:.1f}, "
              f"burning {burn:.1f} points of season-long value.")
    else:
        print(f"!! Best reachable floor is {floor:.1f}, short of the {target:.1f} target.")
        print("!! Too much of the pool is already burned — lower --target or accept "
              "the risk.")
    print("\nPROJ is the consensus week, SIGMA how far a typical week swings from "
          "it, and\nBURN what you give up for the rest of the season by starting "
          "him. The lineup\nfloor is a 20th-percentile total with the nine "
          "variances added in quadrature,\nnot a sum of nine individual floors "
          "-- the players do not all bust at once.")


# ---------------------------------------------------------------------- commands
def cmd_rankings(args: argparse.Namespace) -> None:
    position = resolve_position(args.position)
    payload = fetch_rankings(args.season, args.week, position,
                             args.scoring.upper(), refresh=args.refresh)
    if getattr(args, "debug", False):
        rows = payload.get("players") or payload.get("data") or []
        print("-- top-level keys:", sorted(payload.keys()))
        print("-- row count:", len(rows))
        for k, v in payload.items():
            if not isinstance(v, (list, dict)):
                print(f"-- {k}: {v!r}")
        if rows:
            print("-- first row:")
            print(json.dumps(rows[0], indent=2, sort_keys=True))
        print("-- end debug\n")
    players = extract_players(payload)
    used = {norm(e["name"]) for e in load_used()}
    eligible = [p for p in players if norm(p["name"]) not in used]
    burned = len(players) - len(eligible)

    print(f"Graveyard — {args.season} week {args.week} | {position} "
          f"| {args.scoring.upper()} scoring")
    print(f"{len(players)} ranked, {burned} already used, {len(eligible)} eligible")

    total = payload.get("count")
    if payload.get("public_api_limited") and isinstance(total, int) and total > len(players):
        print(f"\n!! Your FantasyPros key is on the '{payload.get('tier', 'free')}' tier: "
              f"the API ranked {total} players but only returned {len(players)}.")
        print("!! Everyone past the top few is invisible to this tool until the key "
              "is upgraded — see README 'API tier limits'.")
    print()
    print_table(eligible, args.limit)
    if args.csv:
        write_csv(eligible, args.csv)


def cmd_cheapest(args: argparse.Namespace) -> None:
    curves = load_curves(args.curves)
    scoring = args.scoring.upper()
    pool = build_pool(args.season, args.week, scoring, curves, reuse=args.reuse,
                      refresh=args.refresh)
    used = len(load_used())

    print(f"Graveyard — {args.season} week {args.week} | cheapest lineup "
          f"| {scoring} scoring")
    print(f"{len(pool)} eligible across {'/'.join(LINEUP_POSITIONS)}, "
          f"{used} already used, floor target {args.target:.1f}")
    print()
    lineup, made_it = cheapest_lineup(pool, args.target)
    print_lineup(lineup, args.target, made_it)
    if args.csv:
        write_csv([p for p in lineup if p], args.csv)


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
    r.add_argument("--debug", action="store_true",
                   help="dump the raw API structure before formatting")
    r.set_defaults(func=cmd_rankings)

    c = sub.add_parser("cheapest",
                       help="cheapest lineup whose floor still clears a target")
    c.add_argument("--season", type=int, default=season_default)
    c.add_argument("--week", type=int, default=default_week())
    c.add_argument("--target", type=float, default=100.0,
                   help="floor total the lineup must clear (default 100)")
    c.add_argument("--scoring", default="HALF")
    c.add_argument("--curves", help="JSON file overriding the rank->points curves")
    c.add_argument("--reuse", type=float, default=DEFAULT_REUSE,
                   help="how heavily to price the future weeks a burn costs "
                        f"(default {DEFAULT_REUSE}; 0 prices a burn at one week)")
    c.add_argument("--csv", help="also write the lineup to this CSV path")
    c.add_argument("--refresh", action="store_true", help="bypass the local cache")
    c.set_defaults(func=cmd_cheapest)

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
