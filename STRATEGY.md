# Graveyard League — Strategy

Working doctrine for League Tycoon "Graveyard". Derived week 1 of the 2026 season
from FantasyPros weekly + rest-of-season data, five published start/sit pieces, and
the league's own elimination table.

## Format

- Full NFL player pool available every week. No draft, no waivers, no roster.
- **Every player you start is locked out for the rest of the season.**
- Weekly elimination. Lowest scorers are cut. No consolation bracket.
- Superflex. Starting slots: QB / SFLX / RB / RB / WR / WR / FLEX / TE / DST. **No kicker.**
- 752 entrants at the start of the 2026 season.

## The rule that applies to every slot: high delta, low residual

**Every position, every week, including DST.** Read this before the elimination curve,
because it is the filter every other decision passes through.

- **Delta** = ROS rank minus weekly rank. **Positive = ranked better this week than for
  the season = spend him now.** Negative = a later asset = bank him.
- **Residual** = what is left over after you burn him, measured against the *usable pool*
  at his position, not against a hoard band.

**The best burn at every slot is high delta AND low residual.** A big positive delta with
nothing left behind is a free slot. Chase that number at QB, RB, WR, TE **and DST** — there
is no position where you should be spending a negative-delta player in a week you can avoid it.

Week 3 2026, what this looks like in practice:

| Slot | Player | Weekly | ROS | Delta | Residual |
| --- | --- | --- | --- | --- | --- |
| WR | Deebo Samuel | WR24 | WR44 | **+20** | nil |
| DST | Carolina | DST9 | DST29 | **+20** | nil |
| RB | Rico Dowdle | RB26 | RB35 | +9 | nil |
| WR | Courtland Sutton | WR33 | WR42 | +9 | nil |
| QB | Tyson Bagent | QB36 | QB38 | +2 | nil |

Nine slots filled that way projected ~101 while burning nothing inside any usable pool.

**Do not spend a negative delta.** Jaylen Waddle at weekly WR21 / ROS WR14 (-7) is a player
the market says is worth *more* later than this week. Burning him is paying a premium to
lose an asset.


## The elimination curve — the single most important table

Final entrant numbers, 2026 season:

| Wk | Teams | Reaped | % cut | Wk | Teams | Reaped | % cut |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1053 | 122 | **11.6%** | 10 | 232 | 53 | 22.8% |
| 2 | 931 | 114 | 12.2% | 11 | 179 | 46 | 25.7% |
| 3 | 817 | 107 | 13.1% | 12 | 133 | 39 | **29.3%** |
| 4 | 710 | 99 | 13.9% | 13 | 94 | 32 | **34.0%** |
| 5 | 611 | 91 | 14.9% | 14 | 62 | 25 | **40.3%** |
| 6 | 520 | 83 | 16.0% | 15 | 37 | 18 | **48.6%** |
| 7 | 437 | 76 | 17.4% | 16 | 19 | 12 | **63.2%** |
| 8 | 361 | 68 | 18.8% | 17 | 7 | — | FINALS |
| 9 | 293 | 61 | 20.8% | | | | |

**17 weeks, 7 teams in the finals. Cumulative odds: 7/1053 = 0.66%.**

The difficulty curve is not linear — it is exponential at the end. Weeks 1-8 cut
11-19%. Weeks 12-16 cut 29%, 34%, 40%, 49%, **63%**. Week 16 requires beating nearly
two-thirds of an already-elite survivor pool in a single week.

A point in week 16 is worth roughly **five times** a point in week 1. Bank accordingly.

## The punt mechanic — the most important tactic in the format

**You can fill a starting slot with a player who is not on any NFL roster.** He scores
zero and costs zero inventory. Discovered in week 1 (Kenny Golladay, Jamal Haynes).

**The principle underneath it: surplus points are worthless.** Weeks are independent and
nothing carries over. Finishing 200th and finishing 600th are identical outcomes — both
are "alive." Every point above the cut line is an asset spent for zero benefit.

This changes the shape of the game. The question is not "which nine players do I start"
— it is **"how few real players can I spend and still clear the cut?"

What it invalidates:

- There is no season-long budget of ~153 forced burns. You spend only what each week
  requires.
- QB scarcity math (34 starts vs ~28-30 usable) collapses. Punt superflex whenever the
  bar allows.
- The pool-tightness and residual-value tables below still describe real scarcity, but
  that scarcity almost never binds, because punting relieves it.

**A real player who scores 2 points is strictly worse than a punt.** He cost inventory
and delivered nothing. Only start a real player when you need his points to clear the bar.

Combined with the exponential curve above, the two facts resolve the central tension of
the format: early survival is nearly free, late survival demands everything, so **punt
maximally early, bank relentlessly, and arrive at weeks 13-17 fully loaded.**

## Game-time sequencing — late games are live options

NFL games stagger across four windows: Thursday, Sunday 1:00, Sunday 4:05/4:25, SNF,
MNF. Players lock individually at kickoff, so **a player in a late game is not a decision
already made — it is a decision still available**, after you know your score and roughly
where the line sits.

Every late-window slot is therefore worth its projection *plus* the option to convert it
into a punt and keep the asset.

**Structure: early core as insurance, late slots as savings.**

- **Early (Thu / Sun 1:00)** — your floor. High-confidence, high-floor players. Their job
  is to establish position, and deferring a decision you are confident about gains nothing.
- **Late (Sun 4:25 / SNF / MNF)** — your lever. Hold and decide live.

**The early core alone should project to roughly 1.4x the expected cut line.** That is the
insurance premium, and the answer to "how far can I take this." Everything above that
multiple can be held late.

Hold the **interchangeable** slots late — DST first (32 options, matchup-driven, you are
indifferent among many), then FLEX and the third receiver.

**Avoid Thursday players.** TNF is negative optionality: you commit before anyone else
does, with no information. Week 1's recommended lineup had Davante Adams in the Thursday
game — the worst possible slot for this.

Do not reserve more than ~4 late slots. Only 10-16 teams play in the late windows, so the
board thins fast, and an early core that busts leaves you betting the week on a short list.

### Two failure modes

1. **The live cut line is not the final cut line**, and with one week of data any
   projection of it is fiction. Do **not** forecast the line. Two substitutes: anchor on
   the *count of real starters* needed (below), and let Monday night — when ~95% of
   scoring is done — carry the decisions that need real information.
2. **The option expires worthless if you are not there.** The swap windows are roughly
   4:20pm and 8:15pm Sunday. A worse player taken for optionality you never exercise is
   strictly a loss.

### Cost of missing this in week 1

Scored 75.76 against a 40.02 line — 35.7 points of surplus across four assets that did not
need spending. Had Rodriguez, Shipley, Otton and Rodgers been late-window players, all four
could have been punted after the 1pm games and banked instead.

### Confirmed: you can swap late

Slots do **not** have to be committed at the start of the week. A player can be swapped
out any time before his game kicks off. This is the strong version of the mechanic, and
it means **you should not build a lineup — you should build a ladder.**

Setting nine players on Saturday throws away the entire advantage.

| When | Do |
| --- | --- |
| Early week | Identify the MNF-eligible pool. Reserve 1-2 slots for it. |
| Sun ~12:55 | Commit the core — 4-5 real players in the 1:00 games. This is the floor. |
| Sun ~4:15 | Score vs. live line. Clear -> punt the 4:25 slots. Short -> add real players. |
| Sun ~8:10 | Same call for the SNF slot. |
| Mon ~8:00 | Near-complete information. Decide the last 1-2 slots. |

The asymmetry that makes holding safe: **you can always punt a slot, but you can never
un-punt one.** Holding risks needing points with only weak options left. Committing risks
burning an asset you did not need. Week 1 says the second risk is much larger — four
assets spent for 35 points of surplus.

### Punt selection — punts are cheap, not free

**Any player placed in a slot is burned, whether he plays or not.** Confirmed week 1.

Punts therefore consume inventory. The pool of irrelevant players is large enough that
~75 punts a season is never a binding constraint, but selection is not arbitrary:

- **Choose players with no plausible path back.** Retired veterans, long-term unsigned
  players, season-ending IR. Kenny Golladay costs nothing in any scenario.
- **Avoid young unsigned players.** Undrafted rookies get signed. Jamal Haynes was used
  as a week 1 punt; if he lands somewhere in October and becomes usable, that was a real
  asset burned to score zero.
- Keep a vetted punt list rather than improvising at 4:15 on a Sunday.

Two consequences elsewhere:

1. **A real player who is a surprise scratch costs the asset *and* the zero.** This is the
   confirmed basis for never starting an unresolved status flag — it is a double loss, not
   a single one.
2. **The same applies to lottery tickets.** Confirm a ticket is active before locking, or
   it is a guaranteed loss rather than a free roll.

### Lottery tickets early, real players only if needed

The strongest version of the ladder: fill the 1:00 window mostly with **cheap high-variance
players** rather than reliable ones. If two hit, you are clear and can punt every later
slot. If they miss, reinforce from the late windows with real players — which you would
have spent anyway.

**Why this is cheaper than it looks.** The cost of burning a player is proportional to his
*future* value, and for a true scrub that is ~zero — you were never going to start the RB45
in week 12. A lottery ticket is not a gamble with inventory; it is close to a free roll.
So the binding constraint is not "how many scrubs can I afford to burn" (unlimited) but
**"how much reliable reinforcement capacity remains in the late windows"** (thin).

Week 1 validated it accidentally: Carson Wentz (19.22) and Devaughn Vele (19.9) were both
cheap tickets and produced 39 of the 75.76.

**Calibrate the hit rate to ~40%, not 55%.** Of week 1's five genuine tickets (Wentz,
Rodriguez, Shipley, Vele, Otton) two cleared 12 points. The difference compounds:

| Hit rate | P(0-1 hits from 5 tickets) |
| --- | --- |
| 55% | 13% |
| **40%** | **34%** |

At 40%, roughly a third of weeks produce almost nothing early. The fallback must be
genuinely robust.

**So keep 1-2 real floor players in the 1:00 window.** They are the difference between
"tickets missed, sitting on 28, need 15 more" and "tickets missed, sitting on 12, need 35
from a thin board."

| Window | Slots | Contents |
| --- | --- | --- |
| Sun 1:00 | 5-6 | 1-2 floor players + 3-4 lottery tickets |
| Sun 4:25 | 1-2 | held |
| SNF | 1 | held |
| MNF | 1 | held |

**Decorrelate the tickets by bet shape, not just by team.** Five touchdown-dependent
goal-line backs all miss together on a low-scoring slate. Mix a TD-dependent back, a
volume slot receiver, a deep threat, a TE streamer in a plus matchup, a DST.

Ticket profile: cheap inventory, real snap share (a 15-snap player cannot hit), and
touchdown or big-play equity — preferably in a high-total game.

### The 4:25 information gap

1:00 games end ~4:05-4:20; the 4:25 games lock at 4:25. **Final scores from every early
game will not be in before that decision.** Expect 6-8 of 9 final and the rest nearly
done — actionable, but the weakest of the three decision points, not the strongest.

The windows with complete information are **SNF (~8:20pm)** and **MNF (~8:15pm Mon)** —
1-2 games each, so 4-6 teams. That is the reliable reinforcement pool and it is thin.

**Check the SNF and MNF rosters at the start of the week.** If there are not 2-3 players
there you would actually be willing to burn, run fewer tickets that week.

### Monday night is the free-information window

By MNF kickoff roughly 95% of league-wide scoring is complete, so the cut line visible at
that moment is close to final. **No projection is required — you are reading it, not
forecasting it.** Option value concentrates almost entirely in MNF slots; the 4:25 and SNF
windows still involve guesswork.

The constraint is pool size: MNF is 1-2 games, 2-4 teams. Identify who is eligible at the
*start* of the week, not on Monday afternoon. (Week 1's DEN/KC gave Nix, Mahomes, K.
Walker, Kelce, Rice, Sutton, Harvey, Dobbins and two defenses — usually enough.)

## Cut-line log

Track this every week. It is the only way to calibrate how many slots can be punted.

| Week | post-1pm | post-4pm | post-SNF | Final | Our score | Margin |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | - | - | 40.02 | - | 75.76 | +35.74 (survived) |
| 2 | 22.16 | 50.24 | 62.60 | **72.20** | 101.32 | +29.12 (survived) |

**Anchor on the count of real starters, not a point target.** With n=1 a score target is
guesswork; "how many real players do I need" is stabler and is the thing you control.
Week 1: five real starters produced 71.26 against a 40.02 line, and three of them
(Wentz + Vele + Jacksonville = 53.12) cleared it alone.

| Weeks | Cut % | Real starters | Punts |
| --- | --- | --- | --- |
| 1-5 | 11.6-14.9% | 4-5 | 4-5 |
| 6-9 | 16-20.8% | 5-6 | 3-4 |
| 10-13 | 22.8-34.0% | 7-8 | 1-2 |
| 14-16 | 40.3-63.2% | 9 | 0 |

**Week 2 broke this table.** It ran **nine real starters and zero punts** against a
12.2% cut and still only finished +38.72. The week-1 read ("punt 4-5 in weeks 1-5")
was calibrated on a single 40.02 line. Week 2's line was **62.60 before Monday even
started** — higher than week 1's final. One week does not set the punt budget. Treat
the table as a floor on real starters, not a target, until the log has 4-5 rows.

Log **cut line, your score, your rank, and teams remaining** at every checkpoint. The
number actually needed is the ratio *final line / 4pm line*. Two or three weeks of it and
the Sunday-afternoon windows become as safe to act on as Monday already is. Until then,
treat pre-Monday readings as directional only.

Corollary that still holds: teams cut early are teams that started someone **inactive**,
not teams that were eight points light. Optimize for *zero status risk* first.

## The core metric: weekly rank minus rest-of-season rank

    delta = (ROS positional rank) - (this week's positional rank)

- **Positive delta** = ranked better this week than for the season = a *now* asset. Spend.
- **Negative delta** = ranked worse this week than for the season = a *later* asset. Bank.

This single number encodes matchup quality, shelf-life/decay risk, and hoarding value
at once. A backup QB about to lose his job, an aging receiver, a committee back — all
surface as large positive deltas without needing to reason about them individually.

Pull both boards from the CLI:

    python3 graveyard.py rankings --week N --position WR            # weekly
    # (ROS via FantasyPros ranking_type=ROS)

## The residual-value filter

Delta tells you *when* to spend a player. It does not tell you what is left over
afterward. The best burn is **high delta AND low residual value**.

Derrick Henry in week 1 was +6 (RB7 weekly, RB13 ROS) — a big gap, but RB13 rest-of-season
is exactly what you will want in week 10 at the position where the pool barely covers the
need. Held. Davante Adams was +8 with WR29 residual — nothing left to bank. Burned.

**Weight residual value by how tight the pool is.**

## Pool tightness by position

| Pos | Starts needed | Usable pool | Consumption | Hoard? |
| --- | --- | --- | --- | --- |
| **QB** | 34 (2 slots x 17) | ~28-30 | **~115%** | **Hardest** |
| RB | ~34 | ~30-35 | ~100% | Hard |
| TE | 17 | ~18-20 | ~90% | Hard |
| WR | ~43 | ~60-70 | ~65% | Above WR15 only |
| DST | 17 | 32 | 53% | **Never** |

### QB is the tightest position (and this took three tries to get right)

Not because only 32 quarterbacks exist — 45+ players start a game at QB in a season, and
backups take over throughout. **The pool replenishes in count but not in quality.** A
backup taking over is almost always worse than the man he replaced; replacements enter at
the bottom of the board, not the middle.

The week-1 quality cliff:

    QB1  Hurts    20.10
    QB10 Lawrence 17.43     QB1 -> QB25 = 4.4 pts across 25 spots
    QB20 Shough   16.14
    QB25 Stroud   15.66     QB25 -> QB32 = 4.0 pts across 7 spots
    QB28 Cousins  14.28
    QB32 Watson   11.68

Startable set is roughly the top 25-28, and it ends abruptly. You need 34 startable
starts. **You cannot fill every superflex with a real QB.**

- Bank the top ~12 QBs hard. They are what separates you in weeks 9-11.
- Spend from the flat QB13-QB28 band early.
- Budget **4-7 punt weeks** where superflex gets a WR/RB instead of a QB.
- **Schedule those punts in weeks 1-5** (11.6-14.9% cut), never in weeks 9-11 (20.5-25.6%).
  Left to drift you would punt late, when you are out of arms and the cut is brutal.

### Backup QBs getting starts are the best superflex fill in the game

The QB pool is the tightest on the board (~115% consumption) and the quality cliff lands
around QB28. **A backup who has just inherited a starting job sits below that cliff on ROS
while carrying a real weekly projection.** That combination — startable now, worthless
later — is the ideal burn, and it is the cheapest way to cover two QB slots without
touching the bank.

Week 3 2026:

| Player | Weekly | ROS | Delta | Proj |
| --- | --- | --- | --- | --- |
| Marcus Mariota (Jayden Daniels, elbow) | QB33 | QB33 | 0 | 14.31 |
| Tyson Bagent (Caleb Williams, hamstring) | QB36 | QB38 | +2 | 12.91 |

Both project like a low-end starter and both are below the cliff, so the residual is nil.
Compare the alternatives at the same points: Kirk Cousins (12.68, ROS QB29) and Aaron
Rodgers (14.57, ROS QB28) sit right at the edge of the usable pool. Same output, worse
asset.

**This is strictly better than the punt-the-superflex plan.** The doctrine budgets 4-7
weeks where SFLX takes a WR/RB because a real QB cannot be spared. A backup on a starting
run fills that slot with ~13 points instead, at the same zero cost. Scan for these first,
every week, before planning a superflex punt.

**The catch is role risk, and it is the specific thing that kills you.** These players are
starting only because someone else is hurt, so the status question is not "is my guy
healthy" but "is the starter still out" — the role-by-absence rule. Grade the reporting:

- *Dislocated elbow, imaging done, consulting specialists, no timetable* (Daniels) — safe.
- *"Week-to-week," optimism "gave way to reality"* (Williams) — **not** safe. Week-to-week
  is not ruled out.

### Check the kickoff window before you worry about role risk

A cheap starter **in a late window resolves his own role risk for free.** Bagent's
week-3 job depended on a week-to-week hamstring — but Chicago played Monday night, so the
slot did not need committing until 8:15pm Monday, by which point the question was settled.

**So the order of operations is: window first, then status.** A provisional starter in the
1:00 window is a real risk that needs a Friday practice report and a fallback name. The
same player on SNF or MNF is simply a free look. Do not discount a name for role risk
until you have checked when he kicks off.


### DST — never hoard

17 starts from 32 teams, and DST scoring is driven by **matchup, not talent**. Matchups
regenerate every week; roughly half the league draws a bad offense any given week. There
is no future week where you need a *specific* defense.

**Rule: take the best matchup available, every week, ignore the team name, never preserve.**
Do not apply the residual-value filter here — that mistake nearly cost us Jacksonville
(week 1's best play at 8.06 projected) in order to protect a DST12 residual that was never
going to be scarce.

The delta metric still helps at DST, but as a **matchup detector**: a big positive gap means
"ranked well above its talent because of who it plays." Tennessee week 1 was +14 (DST12
weekly, DST26 ROS) — pure one-week rental.

**Chase the delta at DST exactly as hard as anywhere else.** Week 3 2026: Carolina
projected 7.70 at DST9 weekly / DST29 ROS (**+20**) while Kansas City projected 7.72 at
DST3 / DST13 (+10). Identical points, but Carolina is ranked ninth purely for its
opponent and has nothing behind it. Take the big delta when the projections tie.

### The one DST exception: a delta-0 elite unit

"Never hoard" is right in spirit but slightly too absolute. Week 3 2026 has **Seattle at
DST1 weekly AND DST1 ROS — delta 0.** That is not a matchup, that is a unit that will be
the best available option in many future weeks, so it does carry residual even at 53% pool
consumption.

Refined rule:

> Take the best matchup available and never preserve a defense for its *talent* —
> **except** at the very top, where a delta-0 DST1 is the best option most weeks and is
> worth leaving on the shelf.

And never buy a **negative** delta at DST: Denver week 3 was DST12 weekly against DST3 ROS
(-9), which is paying for a good defense in its bad matchup.

## Positional point spreads (week 1, for calibration)

| Pos | Best | ~20th | Spread |
| --- | --- | --- | --- |
| RB | 18.92 | 11.36 | 7.6 |
| WR | 16.65 | 10.19 | 6.5 |
| TE | 11.71 | 6.06 | 5.7 |
| QB | 20.10 | 16.14 | 4.0 |
| DST | 8.06 | 4.65 | 3.4 |
| K | 8.45 | 7.11 | 1.3 |

Attention should follow spread. RB and WR decisions matter most; DST is the lowest-leverage
slot on the board.

Note the shape: every position is **flat through the middle and steep at the edges**. That
flatness is what makes the whole strategy cheap — dropping from rank 8 to rank 18 usually
costs 1-3 points while saving an asset worth 12-14 later.

## Correlation: decorrelate early, correlate late

Stacking a QB with his own receiver is **DFS tournament logic** — there you need to win, so
you want the fat right tail. Here you need to *not be in the bottom 11.6%*, which is a floor
problem. Positive correlation raises variance in both directions; the upside is worthless
(finishing 40th and 400th both just mean "alive") and the downside is fatal.

- **Weeks 1-6:** decorrelate. Nine players, nine teams where possible.
- **Weeks 9+:** as the cut approaches 25%, you need to beat closer to the median. Ceiling
  starts to matter and stacks become defensible.
- **Opposite-side pairs are fine at any time** — they are a hedge, and reduce variance.

## Uncertainty is a cost, not just a risk

In redraft, starting a boom/bust player who busts costs you one week; you bench him next
week. Here it **permanently consumes the asset** — confirmed: any player placed in a slot
is burned whether he plays or not, so a surprise scratch is a double loss. Weight every "questionable", "workload
uncertainty", "wait a week to see" flag far more heavily than the analyst intends.

"I'd like to wait a week and see" is nearly free advice in this format — waiting is exactly
what the format lets you do.

Never start a player with an unresolved status flag unless you can verify active before lock.

## Prior-year data has a shelf life too

Every matchup input in this method — projections, strength-of-schedule stars, and the
defensive splits analysts cite — is built on **last season's** data. Offseason personnel
turnover can invalidate it outright, and week 1 is when that risk peaks, because there is
no current-season data yet to correct it.

Week 1 2026 example: Bucky Irving was chosen largely because Cincinnati had been 32nd in
rushing yards allowed, 31st in yards per carry, and 2nd-most fantasy points allowed to
backs in 2025. Derek Brown's Primer: *"we need to throw every Cincy defensive statistic in
the trash from 2025."* The Bengals had added Dexter Lawrence, Jonathan Allen, Boye Mafe,
Cashius Howell, Kyle Dugger and Bryan Cook. A projected elite matchup was actually neutral.

- Before leaning on any defensive split, check whether that unit turned over. A new
  coordinator, a rebuilt front seven, or a new secondary invalidates the number.
- **Weeks 1-4, discount matchup edges and weight volume and role certainty higher.** Who
  gets the touches is knowable in week 1; how good the opposing defense is, is not. Alvin
  Kamara being out — handing Travis Etienne the backfield — is a harder fact than any
  2025 defensive ranking.
- By roughly week 5 current-season defensive data becomes usable and this caveat relaxes.

## Shelf-life caveat

Decay only matters for players you would *actually start*. A QB31 with benching risk is not
an asset worth "preserving" — you were never going to start him, and if he is benched his
replacement is just as good. Spending a start on him to avoid "wasting" him is sunk-cost
reasoning. The shelf-life principle earns its keep in the genuinely useful band.

## Weekly checklist

1. **Estimate this week's cut line** from the log above, then set a target of roughly
   1.5x it for margin.
2. **Decide how many slots to punt.** Fill the rest with the cheapest real players that
   reach the target. Punting is the default; starting a real player is the exception
   that has to earn itself.
3. Pull weekly + ROS ranks for the eligible (unburned) pool and compute delta.
4. Drop anyone with an unresolved status flag.
5. Sanity-check any matchup edge against offseason turnover (weeks 1-4 especially).
6. Take the highest remaining deltas that reach the target, cheapest inventory first.
7. Check team/game overlap — decorrelate early in the season.
7b. **Sort the slate by kickoff window.** Put high-floor players in early games;
    hold interchangeable slots (DST, FLEX, WR3) for the late windows. Avoid TNF.
    Early core should project ~1.4x the expected cut line on its own.
7c. **Do not set a full lineup up front — run the ladder.** Commit the 1:00 core,
    then decide each later window live. Be present ~4:15pm, ~8:10pm, ~8:00pm Mon.
7d. **Log the cut line, your score, your rank and teams remaining at every
    checkpoint.** This is how the guesswork gets retired.
8. Verify inactives before lock. **For any starter whose case rests on another player
   being absent, check that other player's injury line too** — your man's own status
   stays clean even as the role evaporates. **Confirm your punt players are genuinely rostered
   nowhere** — a punt who unexpectedly plays is a wasted burn, not a disaster, but a
   punt who is quietly on a roster and scores is a burned asset you did not intend.
9. Record the burn in `data/used_players.json` via `./gy u "Name"` **after** lineups lock.
10. **Log the actual cut line** in the table above once results are final.

## Season deployment plan

| Weeks | Cut % | Posture |
| --- | --- | --- |
| 1-4 | 11.6-13.9% | Punt 4-5 slots. Cheapest real players only. Spend decaying assets. |
| 5-9 | 14.9-20.8% | Punt 2-4. Mid-tier real starters. |
| 10-13 | 22.8-34.0% | Punt 0-2. Start deploying the bank. |
| 14-16 | 40.3-63.2% | **No punts. Max lineup every week.** Stacks become correct — you need ceiling, not floor. |
| 17 | FINALS | Whatever is left. |

The whole point of punting weeks 1-9 is to still own Gibbs, Chase, Lamar and Bowers when
week 16 asks you to beat 63% of the field.

## Week 1 lineup (2026)

| Slot | Player | Team | Rank | Delta |
| --- | --- | --- | --- | --- |
| QB | Kirk Cousins | LV | QB28 | +3 |
| SFLX | Bryce Young | CAR | QB24 | +2 |
| RB | Travis Etienne Jr. | NO | RB17 | +1 |
| RB | Bucky Irving | TB | RB18 | +2 |
| WR | Davante Adams | LAR | ~WR21 | +8 |
| WR | DK Metcalf | PIT | ~WR23 | +8 |
| FLEX | Ladd McConkey | LAC | WR16 | +6 |
| TE | Kyle Pitts Sr. | ATL | TE5 | +3 |
| DST | Jacksonville | JAC | DST1 | +11 |

Nine players, nine teams, no same-team pairs. Only shared game is Metcalf (PIT) vs
Pitts (ATL) — opposite sides, a hedge.

Nothing burned above QB24 / RB17 / WR16 / TE5. Banked: Gibbs, Bijan, McCaffrey, Chase,
Nacua, St. Brown, Smith-Njigba, Bowers, McBride, Lamar, Allen, Hurts, Burrow, Maye,
Lawrence, Nix, Cook, K. Walker, Jeanty, Chase Brown, Hampton, Flowers, Nabers, A.J. Brown,
Seattle and Houston DST — every negative-delta asset.

Late revisions from Derek Brown's Primer: Etienne upgraded (Alvin Kamara out, full
backfield); Adams confirmed (1st among 109 receivers in separation score and route win
rate — his +8 delta prices hamstring risk, not decline); Irving held but his matchup
downgraded from elite to neutral per the turnover caveat above.

Deliberate exception: Pitts at TE5 is the most expensive piece, taken on a specific read
about Tua's target volume. Validated independently — he rose TE6 -> TE5 during the week and
carries a +3 delta.

## Week 1 result (2026)

**Survived.** Scored 75.76 against a 40.02 cut line.

The lineup actually played diverged sharply from the one recommended below, and was
better: Carson Wentz 19.22, Chris Rodriguez Jr. 2.3, Will Shipley 2.2, Devaughn Vele
19.9, **Kenny Golladay (punt) 0**, Cade Otton 5.6, **Jamal Haynes (punt) 0**, Aaron
Rodgers 12.54, Jaguars DST 14.

Three players cleared the bar on their own — Wentz + Vele + Jacksonville = 53.12. The
other four real starters were 22.6 points of surplus spent on assets that did not need
spending. Rodriguez (2.3) and Shipley (2.2) were worse than punts.

**Nine players burned** (punts count): Wentz, Rodriguez, Shipley, Vele, Golladay,
Otton, Haynes, Rodgers, Jaguars. Recorded in `data/used_players.json`.

**Monday night decision:** held at 75.76 against a live line of 40.02 with only DEN/KC
left. Left both punts (Golladay, Haynes) in place rather than starting real MNF players.
For the line to reach 75.76 all 122 bottom teams would have needed +35.74 from a single
game — and bottom teams are bottom because their lineups already failed, so they have
*less* left to play, not more. Surplus points buy nothing, so any real player started
there would have been a pure waste.

Two picks from the recommended lineup survived into the played one: Jacksonville DST
(14, the most-confirmed call we made) and Aaron Rodgers (12.54). Devaughn Vele, the
19.9-point hit, was a deep flier flagged by the Athletic and Derek Brown's Primer that
the recommendation passed over as too thin.

**The recommendation over-spent by roughly 2.5x.** It projected 104-115 against a bar
of 40. The error was treating the cut line as unknowable and defaulting to caution,
rather than assuming it was low and testing it cheaply.

## Week 2 result (2026)

**Survived.** Scored 101.32 against a final cut line of **72.20**. 114 reaped, 817
standing — the elimination table called both numbers exactly.

| Slot | Player | Pts | Proj |
| --- | --- | --- | --- |
| QB | Cooper Rush (ATL) | -0.56 | 11.3 |
| RB | Chuba Hubbard (CAR) | 14.40 | 12.8 |
| RB | Chris Brooks (GB) | 3.60 | 7.2 |
| WR | Mack Hollins (NE) | 3.80 | 8.5 |
| WR | Rashod Bateman (BAL) | 21.80 | 8.9 |
| TE | Colby Parkinson (LAR) | 3.50 | 7.1 |
| FLEX | Kenneth Walker III (KC) | 23.80 | 17.3 |
| SFLX | Matthew Stafford (LAR) | 26.98 | 16.8 |
| DST | Tampa Bay | 4.00 | 9.6 |

Nine burned, **zero punts**. Recorded in `data/used_players.json` (18 season total).

### The line moved far more than week 1 suggested

| Checkpoint | Line | Move |
| --- | --- | --- |
| Mid-afternoon | 22.16 | - |
| Post-4:25, pre-SNF | 50.24 | **+28.08 (2.27x)** |
| Post-SNF, pre-MNF | 62.60 | +12.36 |
| **Final** | **72.20** | **+9.60** |

**The ratios — the numbers this log exists to produce:**

| Checkpoint | Final / checkpoint |
| --- | --- |
| post-1pm | **3.26x** |
| post-4pm | **1.44x** |
| post-SNF | **1.15x** |

One week of data, so treat these as a first anchor rather than a rule. But the shape is
clear: **a 1pm reading must be roughly tripled, a 4pm reading multiplied by ~1.45, and
even a post-SNF reading is still 15% light.**

Two lessons, and they pull in opposite directions:

1. **A pre-SNF reading carries almost no signal.** The afternoon jump is the mass of the
   field finishing at once. Anchoring on a 1pm or early-4pm number is worthless — at
   22.16 we looked 2x clear and were in fact *behind* four hours later.
2. **But SNF and MNF still move it meaningfully.** +12.36 across SNF alone. The reasoning
   that "most teams are done by SNF so the line barely moves" was wrong, because the
   teams still live at that hour are disproportionately the ones *holding late slots on
   purpose* — the same ladder we run. Survivors cluster at the back of the slate.

**Do not punt a late slot on a pre-SNF line.** The honest read only arrives at MNF
kickoff, exactly as the doctrine already said — week 2 is the proof.

### The ladder paid, twice

Both held slots beat their projections and both were cheap:

- **Stafford 26.98** against a 16.8 projection, taken at 38 years old with no residual.
  The single best points-per-asset burn of the season so far.
- **Parkinson 3.5** — weekly TE32 / ROS TE36, delta +4, residual nil. He underperformed
  and it did not matter. That is what a correct cheap burn looks like: the *asset* was
  right even though the *outcome* was poor.

Holding those two slots to Monday, rather than filling them Sunday at 1pm, was worth
roughly 20 points over the placeholders (Theo Johnson + OBJ, ~4.5 combined).

### What nearly went wrong — the punt that would have ended the season

At 12:55 the live line read 20 against our 43.14 and the instinct was to punt everything
remaining.

**Punting the two Monday slots would have finished 70.84 against a 72.20 final line.
Cut by 1.36 points, in week 2, with the entire bank still on the shelf.**

The whole season turned on two slots held past Sunday afternoon. Every margin in this
document that looked comfortable at the time — 2x the line at 1pm, +8.24 over the
pre-MNF reading — was an artefact of reading an unfinished line.

**The rule this buys: never punt a late slot against anything but a post-MNF-kickoff
line.** Not a 1pm line, not a 4pm line, not a pre-SNF line. There is no cheaper
version of this lesson available.

Correlation note: Stafford and Parkinson are QB and TE on the same team, the worst kind
of pairing (same drives, same script). We took it knowingly because the alternative cost
Isaiah Likely, a TE12-ROS asset. Stafford's 4 TDs meant it never got tested. **Do not
read this as a licence to stack — it was a priced risk that happened to win.**

## Field dynamics: the line drifts, and you still cannot predict it

The field you play in week N is not the field from week N-1. Two forces act on it, and
they point in opposite directions.

**Forces pushing the line up:**

- **Selection.** Managers who punt badly get cut. Every week the survivor pool is
  enriched in people who understand the ladder. You are always playing a better field
  than you played last week, and the filtering is relentless — 122, 114, 107, 99...
- **Learning.** Anyone who nearly died to a bad Monday punt learns the same lesson we
  learned in week 2. Assume the tactics in this document are being independently
  rediscovered across the surviving field.
- **The cut rate itself.** 11.6% -> 63.2%. Independent of scoring, the *percentile* you
  must beat rises every single week.

**Forces pushing the line down:**

- **Inventory depletion.** Every survivor burns 5-9 real players a week and never gets
  them back. By week 14 the field has spent 100+ names each against a startable pool of
  roughly 180. League-wide, late-season lineups are *worse* than early-season ones.
- **Depletion compounds with the line.** A high line forces fewer punts, which burns
  inventory faster, which degrades everyone's week-14 roster, which lowers scores. The
  two effects feed each other.

**Net shape:** early, the quality effect dominates — inventory is deep, so better play
converts straight into points. Late, depletion dominates. The absolute line likely climbs
then flattens or falls, and the turning point is not forecastable. Week 2 is the evidence:
our own best projection was 55-65 and the answer was 72.20.

### The reframe: optimise percentile, not points

The line **in points** is unpredictable. The line **in percentile** is known exactly, for
all 17 weeks, and was known before the season started. It is the `% cut` column of the
elimination table.

Week 3 does not ask for 72 points. It asks you to beat **13.1% of 817 teams.**

So the weekly question is not "what score do I need" — it is **"what percentile am I
buying, and what is the cheapest inventory that buys it?"** The percentile is knowable
and fixed. The points are a translation that only resolves at MNF kickoff.

This also explains why the checkpoint ratios are worth logging but will never be a
formula: they translate percentile into points for *one particular week's* field and
scoring environment. Log them, use them as a sanity check, never as a target.

### The uncomfortable corollary

If survivors are selected for discipline, then the field in week 14 is disproportionately
made of managers who **also banked well**. The relative edge from banking erodes exactly
when the cut is most brutal.

The response is not to bank less. It is to bank *harder* early, because:

1. The absolute requirement for late inventory is unchanged — you still need nine real
   starters in weeks 14-16.
2. The field you will face has been filtered for the same discipline, so the bar for
   "good enough inventory" in week 15 is set by people who also hoarded.
3. Early weeks remain the cheapest place to buy survival. That fact is structural and
   does not erode.

Banking early is not an edge over the field any more. **It is the entry fee for being in
the week-14 conversation at all.**

## The league app's projection is not the consensus rank

The app attaches a point projection to every player it suggests. Those numbers are
**not** the FantasyPros consensus this doctrine is built on, and in week 3 they
disagreed on three of nine slots:

| Player | App proj | Consensus weekly rank |
| --- | --- | --- |
| Courtland Sutton | 9.3 | WR45 |
| Kenyon Sadiq | 7.7 | TE24 |
| Tyson Bagent | 8.3 | QB34 (behind his own backup, Keenum at QB32) |

A projection sorts players by expected points. That is the wrong objective here —
it cannot see burn cost, residual value, or the delta. **Re-rank anything the app
suggests against the weekly and ROS boards before accepting it.** The app is a
lineup optimizer for a format we are not playing.

Corollary: an app projection that sits well above a player's consensus rank is
usually pricing in a role the consensus does not believe in. Check why.

## Status flags hide behind the app's own icons

The app showed Tyson Bagent with a plain "Q". The actual reporting was **concussion
protocol, may miss the game, Case Keenum expected to start.** Those are not the same
fact, and the format punishes the difference twice — the asset *and* the zero.

**Run `injury_status` on every starter, every week.** The app's badge is a summary of
a summary. It does not distinguish "ankle, good to go" from "in protocol, likely out",
and both render as one orange letter.

## Week 3 plan (2026)

Cut 13.1%. **Week 2 is now logged: final line 72.20, and the 18 burns are in
`data/used_players.json`.** The n=1 caveat below is superseded — use the checkpoint
ratios (final is 3.26x the 1pm line, 1.44x the 4pm line, 1.15x the post-SNF line) and
remember that punting the Monday slots in week 2 would have missed the cut by 1.36.

The app's suggested nine, with deltas:

| Slot | Player | Wk | ROS | Delta | Proj | Window | Call |
| --- | --- | --- | --- | --- | --- | --- | --- |
| QB | Drew Lock (SEA) | QB24 | >QB40 | **+16** | 11.3 | Sun 12:00 | Keep, conditional |
| RB | Brian Robinson (ATL) | >RB45 | >RB48 | ~0 | 4.1 | **Thu** | **Cut** |
| RB | Emanuel Wilson (SEA) | RB44 | >RB48 | +5 | 6.2 | Sun 12:00 | Keep |
| WR | Adonai Mitchell (NYJ) | WR30 | >WR50 | **+21** | 9.1 | Sun 12:00 | Keep |
| WR | Deebo Samuel (SF) | WR26 | WR38 | +12 | 12.1 | Sun 3:05 | Keep |
| TE | Kenyon Sadiq (NYJ) | TE24 | TE22 | **-2** | 7.7 | Sun 12:00 | Punt |
| FLEX | Courtland Sutton (DEN) | WR45 | WR40 | **-5** | 9.3 | SNF | Swap -> Adams |
| SFLX | Tyson Bagent (CHI) | QB34 | QB38 | +4 | 8.3 | MNF | Hold, flagged |
| DST | Carolina | DST9 | DST28 | **+19** | 8.8 | Sun 12:00 | **Keep** |
| SFLX | **Michael Penix Jr. (ATL)** | QB28 | QB31 | +3 | **13.49** | **Thu** | **Start** |

Four faults, in order of deadline:

1. **Brian Robinson is a Thursday lock projecting 4.1** — the lowest in the lineup,
   outside both boards, ATL's RB2 behind Bijan. Barely distinguishable from a punt
   while paying the full TNF optionality cost. His ankle cleared, which is beside
   the point.
2. **Drew Lock's role is Sam Darnold's** — Darnold questionable, limited Wednesday,
   **53.7% to play**. The Etienne/Kamara trap again: Lock's own line stays clean
   while the role evaporates. Biggest delta on the board and still a coin flip.
3. **Bagent is in concussion protocol** (see above).
4. **Sutton carries a negative delta** — a bank, not a burn. Davante Adams is in the
   same SNF game and the same FLEX slot at WR16/WR22 (+6), ~30 spots better this week
   and outside the hoard band.

Plus: five of the nine sit in two games (SEA@WAS, NYJ@DET), against the decorrelate rule.

**Correction, made the same day:** an earlier pass in this session called Carolina an
upgrade candidate "because it is only DST9," and floated Seattle instead. Both wrong,
and wrong in the way the top-level rule exists to prevent — it read the raw rank
instead of the delta. Carolina is DST9 weekly against **DST28 ROS (+19, nil residual)**
and is one of the best buys on the board. Seattle is DST1 weekly *and* DST1 ROS: delta
zero, and the single defense that does carry residual. **Keep Carolina.**

Revised ladder — **8-9 real, 0-1 punts** (see the sizing note below):

| When | Do |
| --- | --- |
| Thu, before 7:15 | **SFLX: Michael Penix Jr.** Drop Brian Robinson. |
| Sun ~11:55 | Lock (iff Darnold ruled out) · E. Wilson · Mitchell · Carolina DST. |
| Sun ~3:00 | Deebo. |
| Sun ~7:10 | FLEX: re-pull Sutton's delta first (see below), else Adams. |
| Mon ~7:00 | Last slot. Do not punt it on a pre-SNF line. |

### Final week 3 lineup

Nine real starters, no punts. Projected **85.55** (half-PPR).

| Slot | Player | Wk | ROS | Delta | Proj | Kickoff |
| --- | --- | --- | --- | --- | --- | --- |
| SFLX | Michael Penix Jr. (ATL) | QB28 | QB31 | +3 | 13.49 | **Thu 7:15** |
| QB | Deshaun Watson (CLE) | QB25 | QB32 | +7 | 15.42 | Sun 12:00 |
| WR | Adonai Mitchell (NYJ) | WR30 | WR52 | **+22** | 7.75 | Sun 12:00 |
| RB | Emanuel Wilson (SEA) | RB44 | >RB48 | +4 | 6.41 | Sun 12:00 |
| DST | Carolina | DST9 | DST28 | **+19** | 7.64 | Sun 12:00 |
| WR | Deebo Samuel (SF) | WR26 | WR38 | +12 | 10.05 | Sun 3:05 |
| FLEX | Davante Adams (LAR) | WR16 | WR22 | +6 | 10.84 | SNF |
| RB | Woody Marks (HOU) | RB34 | RB46 | **+12** | 6.92 | unconfirmed |
| TE | Oronde Gadsden II (LAC) | TE15 | TE21 | +6 | 6.99 | Sun 12:00 @ BUF |

**The ladder is thinner than planned.** Gadsden turned out to be an early game, and
taking Penix on Thursday removed the Monday slot, so five players lock at noon and only
**two** live levers remain: Deebo (3:05) and Adams (7:20). There is no MNF look this week
— the free-information window the doctrine leans on hardest is simply absent.

Consequence: **the 3:00 checkpoint carries the weight Monday usually carries**, on a
reading week 2 showed still needs multiplying by ~1.45. Taking a Thursday player costs
more than the Thursday slot; it can cost the Monday option too, if the superflex was the
only late slot left. Check what a Thursday pick does to the *back* of the ladder before
taking it, not just the front.

Nine teams, no same-team pairs. Only shared game is Watson (CLE) against the Carolina
DST — opposite sides, a hedge, which the correlation rule permits at any time.

Three late changes from the first pass, all forced by status checks:

- **Lock -> Watson.** Darnold came back 53.7% to play, making Lock a coin flip on 11.11.
  Watson carries no role dependency, projects 15.46, and is QB32 ROS — below the cliff,
  nil residual. Better on points *and* risk.
- **Sadiq -> Gadsden.** Sadiq was the last negative delta in the lineup (-2). Gadsden is
  +6 with a higher projection and TE21 ROS, outside the usable band.
- **Brian Robinson -> Woody Marks.** Pollard was the first replacement chosen, then came
  back questionable with an ankle and DNP Wednesday; Dowdle was in a boot. Marks was the
  clean +12.

### Delta-chasing caps the ceiling, and that matters once the line is high

85.55 against a line that was 72.20 last week, in a week cutting 13.1% from a field that
has already shed its worst teams. A ~1.18x cushion, where week 2 ran 1.40x on actuals.

**The mechanism: every high-delta player is by definition one the market ranks low.**
Nine of them sum to less than a lineup carrying two real studs. Week 2 cleared partly on
Kenneth Walker (23.80) and Stafford (26.98) — both negative-delta spends from the bank.

So the delta rule optimises *cost per point*, not *points*. That is the right objective
while the line leaves slack, and the wrong one when it does not. The resolution is not to
abandon delta up front but to **let the ladder decide**: lock the cheap core early, read
the 4pm line, and spend into the bank at SNF/MNF only if the reading demands it. Deciding
to overspend on Thursday is guessing; deciding at 8pm Sunday is reading.

Week 3 locks ~51 by Sunday afternoon (Penix, Watson, Mitchell, Wilson, Carolina) and
holds ~35 live.

### The 5-6 starter sizing in this section's first draft was wrong

It was built on week 1's 40.02 line before week 2 was logged, and recommended 5-6 real
players projecting ~50. **Week 2's line was 72.20 and week 3 cuts harder than week 2.**
Fifty points would have been a comfortable elimination. The error was reaching for the
"weeks 1-5: 4-5 real starters" row of the deployment table, which week 2 had already
demoted to a floor rather than a target. When the log and the table disagree, the log
wins — that is what it is for.

Emanuel Wilson improved during the week rather than decaying: he out-touched Jadarian
Price 21-13 in week 2, and Price is questionable with a chest injury. Positive
role-by-absence, which is the rare direction that check points.

### A returning franchise starter is the backup-QB tactic without the catch

Week 3's superflex was taken for a non-fantasy reason — attending ATL @ GB — so the
question was which Falcon costs least. The answer turned out to beat the planned play
outright.

**Michael Penix Jr.: QB28 weekly, QB31 ROS, 13.49 projected.** Below the quality cliff,
so nil residual; a real starter's projection, so a real slot filled. That is exactly the
backup-QB profile recorded above — but **without the role risk that the rule warns
about.** Mariota and Bagent start only until someone heals. Penix *is* the franchise
starter, returning from last season's knee injury and named by Rapoport. Nobody takes
the job back.

**Grade the direction of the role, not just its certainty.** The archetype splits in two:

| | Role comes from | Risk |
| --- | --- | --- |
| Fill-in backup | Starter's absence | Evaporates when he returns |
| **Returning starter** | **His own job** | **None — it only consolidates** |

The second is strictly the better buy at the same price, and the doctrine had collapsed
both into one category.

It also beat the slot it replaced: Bagent projected 7.58 in concussion protocol with
Case Keenum (11.04) ranked ahead of him. Penix is ~6 points better and already confirmed.
**Taking the Thursday game cost nothing here** — the usual TNF objection is committing
without information, and Penix's status was settled before kickoff while Bagent's was not.

Placed in **SFLX rather than QB**, to leave the QB slot open for Sunday while Lock's job
still depends on Darnold (Lock 11.11 projected, Darnold 12.85 — consensus is hedging).

### "Cheapest" stops being the question once the line is known

Jahan Dotson (ATL) was considered as the Falcon instead of Penix. He is **unranked
weekly and unranked ROS** — off both boards past WR85 — with 3 receptions on 8 targets
for 30 yards in two games, 4.5 half-PPR points on the season. That makes him genuinely
cheaper inventory than Penix (QB31 ROS).

He is still wrong, and the reason generalises:

**Divide the cut line by nine.** Week 2: 72.20 / 9 = **8.0 points per slot to survive**;
we cleared at 11.3 per slot. A slot projecting 2-3 is a five-point hole that has to be
refilled from somewhere, and by the time the line is this high there is nowhere cheap
left to refill from.

Weeks 1-2 made inventory the binding constraint, because a 40-point line left slack
everywhere. At 72 the binding constraint is **points per slot**, and the cheapest
available player stops being the right answer. Run the division before reaching for the
cheapest body.

He is also a worse *punt* than a punt: the punt-selection rule wants no plausible path
back (retired, unsigned, season-ending IR), and Dotson is a rostered receiver in his
mid-twenties. Burning him for 2.5 points is the Jamal Haynes error.

**Name-resolution note:** `injury_status` returned nothing for Dotson and he was absent
from an 80-deep weekly board. Neither fact means anything on its own — the tool says so
explicitly. `get_player_stats` resolved him to ATL with a real stat line. **Never infer
a player's team or status from absence in a ranked board.** (The same lapse put Darnell
Mooney on Atlanta in an earlier draft of this session; he is a Giant.)

### Weekly boards move during the week; re-pull before each checkpoint

Sutton was **WR33/WR42 (+9)** when pulled Tuesday and **WR45/WR40 (-5)** when pulled
Thursday — a swing that flips him from buy to bank. Deebo moved WR24/WR44 to WR26/WR38
over the same two days.

Saturday added the sharpest example yet. **Drew Lock fell QB24 -> QB31 in 48 hours** once
Darnold was back, and Watson rose QB27 -> QB25. The delta that made Lock the pick on
Thursday (+16) was gone by the weekend.

Note what the board did *not* say: Darnold returned at **QB33, below Lock at QB31.**
The market's view was not "Darnold is better" but "this QB room is unusable either way."
A role-by-absence risk landing does not necessarily promote the man who returns — it can
simply delete the slot's value. Do not plan a fallback that assumes the returning starter
inherits the projection.

Early-week weekly boards are thin because most experts have not submitted yet. **A delta
computed on Tuesday is not valid on Sunday.** Re-pull at each ladder checkpoint, and
treat any Tuesday delta as provisional — especially for a slot that is not committed
until SNF or MNF, where there is no reason to be using stale numbers at all.

### The 1.4x core rule and the 4-5 starter rule conflict

Week 3 surfaced a contradiction between two rules in this document. "Early core should
project ~1.4x the cut line" wants ~63 points against a 45-point line. "Weeks 1-5: 4-5
real starters" buys cheap players projecting 6-12, which reaches ~50 at most.

Both cannot hold. **The starter count is the rule that survives** — week 1 reached
75.76 not because the projections were high but because two ~10-point projections
returned 19.22 and 19.9. The core clears 1.4x on *hits*, not on projections.

So do not treat a core projecting 36 as failing. Treat the projected total as close to
meaningless and **read the live line at the 4:00 checkpoint instead**. The 1.4x figure
is a description of a good outcome, not a construction target.

## Source notes

- **Start/sit columns are worth more than sleeper columns here.** Start/sit pieces
  carry projections, opponent context and role notes — the inputs the residual filter
  and the role-certainty rule actually need. Sleeper columns explicitly hunt ceiling
  ("some of these guys are going to absolutely faceplant"), which is the wrong tail
  for a survival format. Week 1's sleeper column produced zero usable names: most of
  its picks collided with a slot already filled, sat on a team whose game had already
  kicked off, or were openly conditional on a role nobody had confirmed.
- Prefer sources that state *why* a player is ranked where he is. A rank alone cannot
  be cross-checked against the turnover caveat or the role-certainty rule.

## Role-by-absence: a second-order status risk

The status filter asks whether *your* player is healthy. It cannot ask whether the
player whose absence created your player's role is still absent. Those are different
questions and the second one is not on your player's injury line at all.

Week 1 2026 produced one of each:

- **Tua Tagovailoa** was taken as a punt carrying benching risk, since Michael Penix Jr.
  sat one ECR spot behind him. The injury report then showed Penix out for the week with
  a torn ACL — the risk priced into the pick had already evaporated.
- **Travis Etienne** was taken because Alvin Kamara was out. By Wednesday Kamara was a
  limited participant and questionable. Etienne's own line stayed clean the whole time,
  so nothing in the tooling flagged it.

**Rule: for every starter whose case rests on someone else being absent, check that
other player on the injury report too.** `./gy s` cannot do this — it reads the ranked
board, which carries no dependency between players. It is a manual step in the
checklist, alongside verifying actives.

## Residual is measured against the usable pool, not the hoard band

The hoard band says *do not spend this player*. It is not the same line as *this player
still has value later*, and conflating them under-counts residual for the tight
positions. A TE12 sits outside the band (8) but well inside a usable pool of ~18-20, so
burning him does cost something. A WR29 sits outside the band (15) and inside a usable
pool of ~60-70 — but WR runs only ~65% consumption, so the surplus refills faster than
you burn it and the residual really is nil.

Before asking "can I go cheaper here?", check the slot against the pool it draws from:

| Pos | Consumption | Going deeper buys you |
| --- | --- | --- |
| QB | ~115% | a lot, until you fall past ~QB28 — below that there is nothing left |
| RB | ~100% | a lot, anywhere inside ~RB30 |
| TE | ~90% | real value inside ~TE18 |
| WR | ~65% | **almost nothing below ~WR15** — the pool outruns the burn |
| DST | 53% | nothing, ever |

The practical test: **going deeper only pays when the player you drop is someone you
would actually start again.** Week 1 2026 ran into this three times — the lineup had
already been taken down to two QBs, three WRs and a DST with no residual between them,
so further "cheaper" moves at WR were selling points for nothing, while the RB and TE
slots still held assets worth preserving.

## Bank watch

- **Brock Bowers (knee)** is out for week 1 after a meniscus trim. Reporting split on
  severity: Eisenberg said "could miss multiple weeks," Schefter said "a game or two."
  Take the specific report over the vague one — the ROS TE1 is frozen for a week or
  two, not the month. He is still bankable for the endgame; do not panic-spend the
  TE board around his absence. Tre Tucker becomes Las Vegas's lead pass-catcher while
  he is out, which is a burn candidate in any week Kirk Cousins is not started.
- **Isaiah Likely** (NYG) — week 2 board has him weekly **TE7 / ROS TE12**, a +5 delta,
  so the week-1 "negative delta, pure hoard" read is out of date. He is now a *good*
  burn on delta alone, but ROS TE12 sits well inside a usable pool of ~18-20, so the
  residual is real. Hold him for weeks 9-13 unless a week genuinely needs the points;
  spend a TE30+ body first.

## Things we got wrong (so we don't re-derive them)

- **"WR and RB are both ~60 deep."** No. RB is ~30-35 usable against ~34 starts. RB is
  scarce; WR is not, below WR15.
- **"QB is flat, so don't hoard it."** True in 1-QB. False in superflex, where quality
  runs out.
- **"Only 32 QBs exist, so superflex is impossible to fill."** Wrong count — 45+ start a
  game. Right conclusion for the wrong reason; the real constraint is quality, not bodies.
- **"Backups replenish the QB pool."** They replenish *count*, not *quality*. Replacements
  arrive as QB29s.
- **"K and DST are both near-noise."** K yes (1.3 spread). DST no (3.4) — comparable to QB.
- **"QB-WR stacks are the good kind of correlation."** DFS logic. Wrong for a floor format.
- **Ignored kickoff times entirely.** Late-window players are live options; we put
  Davante Adams in the Thursday game, the worst slot for information.
- **Missed the punt mechanic entirely.** Assumed every slot had to be filled with a
  real player, which inflated every scarcity calculation in this document.
- **Treated the week 1 cut line as unknowable** and defaulted to caution. It was 40.02;
  we projected 104-115. Assume the bar is low and test it.
- **Stopped the elimination curve at week 11.** The real peak is 63.2% in week 16.
- **"Cincinnati is the softest RB matchup on the board."** Built on 2025 splits. They
  rebuilt the defensive line over the offseason. Prior-year data needs a turnover check.
- **"The final line will land 55-65."** It landed 72.20. Forecasting the line remains
  fiction even with a checkpoint series in hand — the doctrine's "read it, do not
  project it" rule survives week 2 intact, and the one time we projected anyway we
  were 10+ points light in the direction that gets you eliminated.
- **"Most teams are done by SNF, so the line barely moves after it."** Wrong, week 2:
  +12.36 across SNF, then +9.60 more across MNF. The teams still live late are the ones deliberately holding
  late slots, so the tail of the slate is *enriched* in movement, not drained of it.
- **Asserted TE scarcity without pulling the ROS board.** Argued David Njoku was an
  expensive burn on "TE pool is tight" grounds. He is ROS TE30 — residual near nil.
  Pool tightness is an argument about a *position*; residual is a fact about a *player*.
  Check the ROS rank before claiming an individual is worth protecting.
- **"Protect Jacksonville's DST12 residual."** Applied the RB scarcity rule to a loose,
  matchup-driven pool. Residual value must be weighted by pool tightness.
- **Trusted the league app's point projections.** They are not the FantasyPros
  consensus and they optimize for total points, which is the wrong objective in a
  survival format. Week 3 had them disagreeing with the consensus rank on three of
  nine slots.
- **Read the app's "Q" badge as the injury report.** It collapsed "ankle, cleared to
  play" and "in concussion protocol, backup expected to start" into the same icon.
- **Sized week 3 off week 1's line after week 2 was already logged.** Recommended 5-6
  real starters projecting ~50 against a line that had just come in at 72.20. Always
  re-read the cut-line log before quoting the deployment table.
- **Called Carolina DST an upgrade candidate for being "only DST9."** Raw rank, not
  delta — at DST28 ROS it was a +19 buy. The top-level rule exists precisely to stop
  this, and it still got applied per-position out of habit.
- **Computed deltas once, early in the week, and reused them.** Weekly boards fill in
  as experts submit; Sutton swung +9 to -5 in two days.

## Open questions

- ~~Confirm exact starting slots~~ — **answered: QB/RB/RB/WR/WR/TE/FLEX/SFLX/DST.**
- ~~Does an inactive starter count as burned?~~ — **answered: yes. Any player placed in
  a slot is burned, played or not.** See "Punt selection" below.
- ~~Contest end week~~ — **answered: 17 weeks, finals with 7 teams.**

## Tooling backlog

`graveyard.py` should grow a `--strategy` mode that joins weekly and ROS ranks into a single
delta column, applies the residual filter per position, excludes burned players, and prints
the recommended slate. That turns the weekly checklist above into one command.
