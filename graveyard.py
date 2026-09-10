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
                   refresh: bool = False, ranking_type: str | None = None) -> dict:
    # ROS boards are not week-scoped; the API wants week 0 with type=ros.
    ranking_type = ranking_type or ("weekly" if week else "draft")
    if ranking_type == "ros":
        week = 0
    params = {
        "position": position,
        "scoring": scoring,
        "week": str(week),
        "type": ranking_type,
        "experts": "available",
    }
    url = f"{BASE_URL}/nfl/{season}/consensus-rankings?" + urllib.parse.urlencode(params)

    os.makedirs(CACHE_DIR, exist_ok=True)
    cache = os.path.join(CACHE_DIR,
                         f"{season}-wk{week}-{position}-{scoring}-{ranking_type}.json")
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
        sys.exit(f"FantasyPros API error {exc.code} for {position}/{scoring} "
                 f"{ranking_type} week {week}:\n{body}")
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
            # Spelling varies across FantasyPros payloads; take whichever is set.
            "status": (p.get("player_injury_status") or p.get("injury_status")
                       or p.get("player_status") or "").strip(),
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
    ("SFLX", ("QB", "RB", "WR", "TE")),
    ("RB", ("RB",)),
    ("RB", ("RB",)),
    ("WR", ("WR",)),
    ("WR", ("WR",)),
    ("FLEX", ("RB", "WR", "TE")),
    ("TE", ("TE",)),
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


# ---------------------------------------------------------------- strategy mode
# The elimination curve from STRATEGY.md. The cut more than doubles from week 1
# to week 11, which is the whole reason to spend cheap assets early.
ELIMINATION = {
    1: (752, 87, 11.6), 2: (665, 82, 12.3), 3: (583, 76, 13.0),
    4: (507, 70, 13.8), 5: (437, 65, 14.9), 6: (372, 59, 15.9),
    7: (313, 54, 17.3), 8: (259, 49, 18.9), 9: (210, 43, 20.5),
    10: (167, 38, 22.8), 11: (129, 33, 25.6),
}

# Residual-value filter: the rest-of-season positional band to keep in the bank.
# A player whose ROS rank is inside this band is one you will still want later,
# so he is not a burn candidate however good his matchup is this week. Weighted
# by pool tightness -- see the tightness table in STRATEGY.md. DST is absent on
# purpose: matchups regenerate weekly, so there is no future week where you need
# a specific defense. Never filter it.
HOARD_BAND = {"QB": 12, "RB": 12, "TE": 8, "WR": 15}

# Weeks in which prior-year matchup data is least trustworthy, so volume and
# role certainty outrank matchup quality.
STALE_DATA_WEEKS = 4

# From this week on the cut is steep enough that you must beat closer to the
# median: deploy the bank, put a real QB in superflex, and stacking becomes
# defensible because ceiling starts to matter.
ENDGAME_WEEK = 9


def positional_rank(player: dict) -> float | None:
    return pos_rank_number(player)


def delta_board(season: int, week: int, position: str, scoring: str,
                refresh: bool = False) -> list[dict]:
    """Join this week's board against the rest-of-season board.

    delta = ROS rank - weekly rank. Positive means he is ranked better this week
    than for the season as a whole, so this is the week to spend him.
    """
    weekly = extract_players(fetch_rankings(season, week, position, scoring,
                                            refresh=refresh, ranking_type="weekly"))
    ros = extract_players(fetch_rankings(season, week, position, scoring,
                                         refresh=refresh, ranking_type="ros"))
    ros_rank = {}
    for p in ros:
        r = positional_rank(p)
        if r is not None:
            ros_rank[norm(p["name"])] = r

    out = []
    for p in weekly:
        wk = positional_rank(p)
        rs = ros_rank.get(norm(p["name"]))
        if wk is None:
            continue
        row = dict(p)
        row["position"] = p["position"] or position
        row["wk_rank"] = wk
        row["ros_rank"] = rs
        # No ROS ranking at all means the experts do not see him as a season
        # asset -- nothing to hoard, so treat the whole gap as spendable.
        row["delta"] = (rs - wk) if rs is not None else None
        out.append(row)
    return out


def classify(row: dict, week: int,
             cleared: set[str] | None = None) -> tuple[bool, str]:
    """Is this player a burn candidate this week, and if not, why not?

    A status flag is a hard drop, not a ranking penalty: starting a player who
    turns out inactive burns him for the season anyway, so the downside is a
    zero *plus* the permanent loss of the asset. No delta prices that. Only a
    name passed to --cleared (verified active before lock) gets back in.
    """
    pos = (row["position"] or "").upper()
    if row.get("status") and norm(row["name"]) not in (cleared or set()):
        return False, f"status: {row['status']}"
    band = HOARD_BAND.get(pos)
    if band is not None and row["ros_rank"] is not None and row["ros_rank"] <= band:
        return False, f"bank ({pos}{row['ros_rank']:.0f} ROS)"
    if row["delta"] is None:
        return True, "no ROS rank"
    if row["delta"] < 0:
        return False, "negative delta"
    return True, ""


def pick_slate(candidates: list[dict], decorrelate: bool,
               punt_superflex: bool = True) -> list[dict | None]:
    """Highest delta per slot, scarcest slot first, optionally one team each."""
    by_slot = []
    for slot, allowed in LINEUP_SLOTS:
        # Punting superflex is a weeks-1-5 move. Late, it has to be a real QB.
        if slot == "SFLX" and not punt_superflex:
            allowed = ("QB",)
        pool = [p for p in candidates if (p["position"] or "").upper() in allowed]
        pool.sort(key=lambda p: (-(p["delta"] if p["delta"] is not None else 0),
                                 p["wk_rank"]))
        by_slot.append(pool)

    slate: list[dict | None] = [None] * len(LINEUP_SLOTS)
    used_names: set[str] = set()
    used_teams: set[str] = set()
    for idx in sorted(range(len(LINEUP_SLOTS)), key=lambda i: len(by_slot[i])):
        for cand in by_slot[idx]:
            if norm(cand["name"]) in used_names:
                continue
            team = str(cand.get("team") or "")
            if decorrelate and team and team in used_teams:
                continue
            slate[idx] = cand
            used_names.add(norm(cand["name"]))
            if team:
                used_teams.add(team)
            break
    return slate


def print_slate(slate: list[dict | None], week: int) -> None:
    hdr = (f"{'SLOT':<6} {'PLAYER':<24} {'POS':<4} {'TEAM':<4} {'MATCHUP':<8} "
           f"{'WK':>5} {'ROS':>5} {'DELTA':>6}")
    print(hdr)
    print("-" * len(hdr))
    for (slot, _), p in zip(LINEUP_SLOTS, slate):
        if not p:
            print(f"{slot:<6} {'-- no candidate --':<24}")
            continue
        matchup = p["opponent"] or (f"BYE {p['bye']}" if p["bye"] else "")
        ros = f"{p['ros_rank']:.0f}" if p["ros_rank"] is not None else "-"
        delta = f"{p['delta']:+.0f}" if p["delta"] is not None else "-"
        print(f"{slot:<6} {p['name'][:24]:<24} "
              f"{str(p['position'])[:4]:<4} {str(p['team'])[:4]:<4} "
              f"{str(matchup)[:8]:<8} {p['wk_rank']:>5.0f} {ros:>5} {delta:>6}")
    teams = [str(p.get("team")) for p in slate if p and p.get("team")]
    dupes = {t for t in teams if teams.count(t) > 1}
    print("-" * len(hdr))
    print(f"{len(teams)} players, {len(set(teams))} teams"
          + (f" -- SAME-TEAM PAIR: {', '.join(sorted(dupes))}" if dupes else ""))


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


def cmd_strategy(args: argparse.Namespace) -> None:
    scoring = args.scoring.upper()
    week = args.week
    used = {norm(e["name"]) for e in load_used()}

    print(f"Graveyard — {args.season} week {week} | strategy | {scoring} scoring")
    if week in ELIMINATION:
        field, reaped, pct = ELIMINATION[week]
        print(f"{field} alive, {reaped} cut this week ({pct}%). "
              + ("Cheapest survivable lineup; spend decaying assets."
                 if pct < 15 else
                 "Mid-tier; ranks ~8-15." if pct < 20 else
                 "Deploy the bank. Do not punt."))
    else:
        print(f"No elimination row for week {week} — check the league page.")

    rows, burned = [], 0
    for pos in LINEUP_POSITIONS:
        for row in delta_board(args.season, week, pos, scoring, refresh=args.refresh):
            if norm(row["name"]) in used:
                burned += 1
                continue
            rows.append(row)

    cleared = {norm(n) for n in (args.cleared or [])}
    candidates, held = [], []
    for row in rows:
        ok, why = classify(row, week, cleared)
        (candidates if ok else held).append((row, why))
    candidates = [r for r, _ in candidates]

    print(f"{len(rows)} eligible, {burned} already burned, "
          f"{len(candidates)} spendable, {len(held)} held back")
    if cleared:
        # Clearing a status flag only lifts that one gate -- the hoard band and
        # delta still apply -- so report where each cleared player actually ended
        # up rather than implying he made the slate.
        for row in rows:
            if norm(row["name"]) not in cleared or not row.get("status"):
                continue
            ok, why = classify(row, week, cleared)
            print(f"Cleared {row['name']} ({row['status']}): "
                  + ("now spendable" if ok else f"still held -- {why}"))
        for name in args.cleared:
            if norm(name) not in {norm(r["name"]) for r in rows}:
                print(f"!! --cleared {name!r} matched nobody on this week's board.")
    if week <= STALE_DATA_WEEKS:
        print(f"!! Week {week}: matchup inputs are last season's data. Weight volume "
              f"and role\n!! certainty over matchup quality, and check any defensive "
              f"split for turnover.")
    print()

    # Decorrelate while the cut is shallow; from the endgame on, ceiling matters
    # and same-game exposure is an acceptable price for it.
    decorrelate = week < ENDGAME_WEEK and not args.no_decorrelate
    slate = pick_slate(candidates, decorrelate=decorrelate,
                       punt_superflex=week < ENDGAME_WEEK)
    if week >= ENDGAME_WEEK:
        print(f"Week {week} is endgame: superflex must be a real QB, and "
              f"same-team pairs are allowed.\n")
    print_slate(slate, week)

    print(f"\nTop burn candidates by delta:")
    for pos in LINEUP_POSITIONS:
        best = sorted((c for c in candidates if (c["position"] or "").upper() == pos),
                      key=lambda p: -(p["delta"] if p["delta"] is not None else 0))[:args.show]
        line = ", ".join(
            f"{p['name']} ({pos}{p['wk_rank']:.0f}, "
            f"{('%+d' % p['delta']) if p['delta'] is not None else 'n/a'})"
            for p in best)
        print(f"  {pos:<4} {line}")

    if args.explain:
        print(f"\nHeld back:")
        for row, why in sorted(held, key=lambda rw: rw[0]["wk_rank"])[:args.show * 4]:
            print(f"  {row['name'][:24]:<24} {str(row['position']):<4} "
                  f"wk{row['wk_rank']:.0f}  {why}")

    print("\nDELTA is ROS rank minus this week's rank: positive means he is ranked "
          "better\nnow than for the season, so this is the week to spend him. Players "
          "inside the\nper-position hoard band are held back regardless of delta "
          "(never for DST).")
    print("An inactive start burns the player anyway, so anyone carrying a status "
          "flag is\ndropped outright. Verify actives before lock -- re-admit one with "
          "--cleared\n\"Name\" -- then record the burns with ./gy u \"Name\".")
    if args.csv:
        write_csv([p for p in slate if p], args.csv)


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

    g = sub.add_parser("strategy",
                       help="delta board + recommended slate for the week")
    g.add_argument("--season", type=int, default=season_default)
    g.add_argument("--week", type=int, default=default_week())
    g.add_argument("--scoring", default="HALF")
    g.add_argument("--show", type=int, default=6,
                   help="how many burn candidates to list per position")
    g.add_argument("--cleared", action="append", metavar="NAME",
                   help="re-admit a status-flagged player you have verified "
                        "active before lock; repeatable")
    g.add_argument("--explain", action="store_true",
                   help="also list who was held back and why")
    g.add_argument("--no-decorrelate", action="store_true",
                   help=f"allow same-team pairs (automatic from week {ENDGAME_WEEK})")
    g.add_argument("--csv", help="also write the slate to this CSV path")
    g.add_argument("--refresh", action="store_true", help="bypass the local cache")
    g.set_defaults(func=cmd_strategy)

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
