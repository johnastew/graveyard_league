# Graveyard League helper

Weekly picker for [League Tycoon "Graveyard"](https://leaguetycoon.com/formats/graveyard/)
fantasy football: pick from the whole NFL pool each week, but every player you
start is locked out for the rest of the season. This tool pulls FantasyPros
consensus rankings and subtracts everyone you've already burned.

Strategy, the weekly decision method, and the running lineup log live in
[`STRATEGY.md`](STRATEGY.md). Read that before setting a lineup.

## Setup

```bash
cp .env.example .env      # then put your real key in it
```

`.env` holds `FANTASYPROS_API_KEY` (and optionally `GRAVEYARD_SEASON`) and is
gitignored — the key is never in the code or in a commit. No dependencies
beyond the Python 3 standard library.

## Usage

```bash
./gy                      # eligible players for the current week
./gy 5                    # eligible players for week 5
./gy s                    # delta board + recommended slate (the weekly driver)
./gy s 5                  # ...for week 5
./gy c                    # cheapest lineup that still clears the floor target
./gy c 90                 # ...with the floor target set to 90
./gy u "Bijan Robinson"   # mark used after you start them
./gy l                    # list everyone burned so far
./gy x "Bijan Robinson"   # undo a mistaken mark
```

The full CLI, if you want the knobs:

```bash
python3 graveyard.py rankings --week 5 --position FLEX --scoring HALF \
        --limit 0 --csv out/week5.csv --refresh
python3 graveyard.py use "Player Name" --week 5
```

```bash
python3 graveyard.py cheapest --week 5 --target 95 --reuse 2.0 --csv out/wk5.csv
```

- `--position` — `FLEX`, `QB`, `RB`, `WR`, `TE`, `K`, `DST`, `OP`, …
- `--scoring` — `STD`, `HALF`, `PPR`
- `--limit 0` — print everyone instead of the top 50
- `--refresh` — bypass the on-disk response cache in `data/cache/`

## Strategy mode

`./gy s` is the weekly driver. It implements the checklist in
[STRATEGY.md](STRATEGY.md) as one command:

1. Pulls the weekly **and** rest-of-season boards for QB/RB/WR/TE/DST.
2. Joins them into `delta = ROS rank - weekly rank`. Positive means he is ranked
   better this week than for the season, so this is the week to spend him.
3. Drops everyone already burned (`data/used_players.json`).
4. Drops anyone carrying a status flag — a bust here consumes the asset
   permanently, so an unresolved flag is disqualifying, not a discount.
5. Applies the per-position residual filter: a player whose ROS rank sits inside
   `HOARD_BAND` is one you will still want later, so he is held back however good
   his matchup is. **DST is exempt** — matchups regenerate weekly and no future
   week needs a specific defense.
6. Fills the nine slots with the highest remaining deltas, one team each.

It adapts to the week from the elimination table: through week 8 it decorrelates
and will punt superflex to a WR/RB; from week 9 (`ENDGAME_WEEK`) superflex must be
a real QB and same-team pairs are allowed, because the cut is steep enough that
ceiling starts to matter. In weeks 1-4 it warns that every matchup input is last
season's data.

```bash
./gy s                       # this week
python3 graveyard.py strategy --week 5 --explain --show 10
```

`--explain` lists who was held back and why (`bank (RB9 ROS)`, `status: Q`,
`negative delta`) — use it to check the filter is not hiding someone you want.
`--no-decorrelate` allows same-team pairs early.

The slate is a starting point, not a verdict: it cannot see a beat writer's
snap-count note or a Saturday inactive. Verify before lock, then record the burns
with `./gy u "Name"`.

## Cheapest-lineup mode

`cheapest` answers a different question from `rankings`. Graveyard is a survival
format: you do not need to win the week, you need to not finish in the bottom
slice, and every player you start is gone for good. So the right lineup is the
one that clears the cut using the *least valuable* players who still clear it,
banking the studs for later.

It pulls QB/RB/WR/TE/DST rankings, drops everyone burned and everyone on bye,
and fills the nine-slot board (QB, RB, RB, WR, WR, TE, FLEX, SFLX, DST) to
minimize value burned subject to the lineup's floor clearing `--target`.

Three numbers per player:

| column | meaning |
| --- | --- |
| `FLOOR` | points if the most pessimistic expert is right (from the consensus rank spread) |
| `PROJ` | points at consensus rank |
| `BURN` | season-long value given up by starting him |

`BURN` is `PROJ` plus the player's points above replacement times `--reuse`
(default 2.0), because spending a stud costs you every future week you could
have used him, not just this week's points. `--reuse 0` prices a burn at one
week flat.

**Set `--target` from the actual cut line, not from a good score.** If the
bottom 122 of 1052 go home, look at what last week's 930th-place team scored
and add a safety margin — that number is usually far below what a
maximize-the-week lineup produces, and the gap is exactly the value this mode
saves you.

### Caveat on the numbers

FantasyPros' consensus endpoint returns *ranks*, not projected points, so the
floor and projection come from a rank-to-points curve defined in
`POINT_CURVES` — coarse anchor values, linearly interpolated. They are good
enough to compare slots and pick the next upgrade, and they are not real
projections. Override them with `--curves file.json` (same shape) if you have
better ones. The optimizer itself is a greedy heuristic — cheapest legal
lineup, then repeated best floor-gained-per-value-spent upgrades — not a
proven optimum.

## Files

| path | what |
| --- | --- |
| `STRATEGY.md` | format doctrine, the weekly method, and the lineup log |
| `graveyard.py` | the CLI |
| `gy` | short wrapper for typing on a phone |
| `data/used_players.json` | your burned players — commit this to keep it |
| `data/cache/` | cached API responses, safe to delete |

Name matching ignores case, punctuation, accents and Jr./Sr./III, so
`./gy u "jamarr chase"` will filter out `Ja'Marr Chase`.

## API tier limits

**Current status: a premium key is in place and all 306 players are
returned.** The notes below describe the free-tier behaviour, kept because
the failure mode is silent and easy to misread if a key ever changes.

A **free** FantasyPros public API key is capped server-side at **10 players
per request**, regardless of what you ask for. The response says so itself:

```json
{"count": 306, "limit": 10, "public_api_limited": true, "tier": "free"}
```

`count` is how many players were actually ranked; `limit` is how many you get.
No query parameter widens this — it is a property of the key. The tool prints a
warning whenever it detects the truncation, so a short list is never mistaken
for a short week.

This matters for Graveyard: the top 10 are the players you burn first, so
after a few weeks the visible pool would be entirely locked out and the list
would come back empty. Upgrading the key fixes it with no code change.

Note that a newly issued key can return `403 Forbidden` for several minutes
before it is provisioned. If that happens, wait and re-run before assuming
the key is wrong — this was observed and resolved on its own.

Each run prints a truncated SHA-256 fingerprint of the key in use. It cannot
be reversed into the key, but it changes when the secret changes, which
distinguishes "the secret did not update" from "the key is being rejected".

The response also carries no `tier` field per player, so there is no tier
column; `pos_rank` (RB1, WR7) is shown instead, plus the expert rank range
and average roster percentage.

## Running it from your phone (no laptop, no terminal)

The key lives as a GitHub repository secret, so it is never in the code, never
in a commit, and never pasted into a chat.

**One-time setup** (works in a phone browser):

1. Repo → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**
2. Name it `FANTASYPROS_API_KEY`, paste your key, save.
3. Optionally add a *variable* (same page, Variables tab) `GRAVEYARD_SEASON` = `2026`.

**Every week after that:**

- Repo → **Actions** → **Graveyard** → **Run workflow**
- Pick `rankings` and a week → run it → open the run and read the summary.
  The full list is also attached as a CSV artifact.
- To bury a player: same workflow, action `use`, players `Bijan Robinson, Puka Nacua`.
  It commits the updated `data/used_players.json` back to the branch, so every
  device — and next week's pull — sees it immediately.

Because the roster lives in the repo and the runs happen on GitHub's machines,
any week can be pulled at any time from any device, indefinitely. Nothing
depends on a chat session staying alive.
