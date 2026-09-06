# Graveyard League helper

Weekly picker for [League Tycoon "Graveyard"](https://leaguetycoon.com/formats/graveyard/)
fantasy football: pick from the whole NFL pool each week, but every player you
start is locked out for the rest of the season. This tool pulls FantasyPros
consensus rankings and subtracts everyone you've already burned.

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

- `--position` — `FLEX`, `QB`, `RB`, `WR`, `TE`, `K`, `DST`, `OP`, …
- `--scoring` — `STD`, `HALF`, `PPR`
- `--limit 0` — print everyone instead of the top 50
- `--refresh` — bypass the on-disk response cache in `data/cache/`

## Files

| path | what |
| --- | --- |
| `graveyard.py` | the CLI |
| `gy` | short wrapper for typing on a phone |
| `data/used_players.json` | your burned players — commit this to keep it |
| `data/cache/` | cached API responses, safe to delete |

Name matching ignores case, punctuation, accents and Jr./Sr./III, so
`./gy u "jamarr chase"` will filter out `Ja'Marr Chase`.

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
