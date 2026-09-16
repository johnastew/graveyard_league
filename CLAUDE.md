# Graveyard League

Fantasy football helper for League Tycoon "Graveyard" — weekly elimination, full NFL
pool every week, **every player started is locked out for the rest of the season.**

## Read this before giving any lineup advice

**[`STRATEGY.md`](STRATEGY.md) is the working doctrine. Read it in full before
suggesting a single player.** It is not background — it is the result of a long
iteration that overturned most of the obvious advice, and several of its conclusions
are the opposite of standard fantasy reasoning.

If you skip it you will re-suggest approaches that were already tested and rejected.

The five things most likely to be re-derived wrongly:

1. **Punting is free.** A slot can be filled with a player on no NFL roster. He scores
   zero and costs nothing worth keeping. The question is never "which nine players do I
   start" — it is "how few real players clear the cut?"
2. **Surplus points are worthless.** Weeks are independent. 200th and 600th are the same
   outcome. Every point above the cut line is an asset spent for nothing.
3. **Don't build a lineup, build a ladder.** Players lock individually at kickoff, so
   late-window players are live options. Commit a core at 1:00, decide the rest as
   information arrives. Monday night is near-perfect information.
4. **Early weeks are nearly free, late weeks are brutal.** The cut runs 11.6% in week 1
   and 63.2% in week 16. Bank relentlessly early.
5. **Never start an unresolved status flag.** Any player placed in a slot is burned
   whether he plays or not, so a scratch costs the asset *and* the zero.

## Tooling

- `./gy` / `graveyard.py` — pulls FantasyPros rankings, subtracts burned players
- `data/used_players.json` — the burned list. Commit it.
- `./gy u "Name"` marks a player used; `./gy x "Name"` undoes it

## Working notes

- Record burns **after** lineups lock, not before.
- `cbssports.com` and `rotostreetjournal.com` are blocked by the egress proxy — the
  user has to paste article text.
- Keep `STRATEGY.md` current. When something is learned, commit it there rather than
  leaving it in a conversation that a future session cannot see.
