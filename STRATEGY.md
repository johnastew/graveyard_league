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

## The elimination curve — the single most important table

| Week | Teams | Reaped | % cut |
| --- | --- | --- | --- |
| 1 | 752 | 87 | **11.6%** |
| 2 | 665 | 82 | 12.3% |
| 3 | 583 | 76 | 13.0% |
| 4 | 507 | 70 | 13.8% |
| 5 | 437 | 65 | 14.9% |
| 6 | 372 | 59 | 15.9% |
| 7 | 313 | 54 | 17.3% |
| 8 | 259 | 49 | 18.9% |
| 9 | 210 | 43 | 20.5% |
| 10 | 167 | 38 | 22.8% |
| 11 | 129 | 33 | **25.6%** |

The cut line **more than doubles in difficulty** from week 1 to week 11. A point is
worth roughly half as much in week 1 as it is in week 11. Spending a 13-point player
now to bank a 13-point player for later is not break-even — it is profit.

Corollary: teams cut in week 1 are teams that started someone **inactive**, not teams
that were eight points light. Optimize for *zero status risk* first, points second.

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
week. Here it **permanently consumes the asset**. Weight every "questionable", "workload
uncertainty", "wait a week to see" flag far more heavily than the analyst intends.

"I'd like to wait a week and see" is nearly free advice in this format — waiting is exactly
what the format lets you do.

### An inactive starter is burned (confirmed)

**Starting a player who turns out inactive burns him for the season anyway.** Confirmed
with the league, week 1 2026. This was the most load-bearing open question and the answer
is the punishing one.

There is therefore **no free roll**. You cannot start a questionable player hoping to
"find out" — if he sits you pay the full asset price and score zero in that slot. The
expected cost of a game-time decision is not `p(out) x (points forgone)`, it is
`p(out) x (points forgone + the asset, permanently)`, and the asset half is charged
whether or not he plays.

Three consequences:

- **A status flag is disqualifying, not a discount.** There is no delta large enough to
  price it, because the downside is not a bad week — it is a bad week *plus* losing the
  player from every future week.
- **A zero is fatal in a way that being light is not.** Week 1 you might survive a zero at
  one slot; by week 11 at a 25.6% cut you will not. The cost of status risk rises on the
  same curve as everything else.
- **It sharpens the QB banking rule.** The late-week worry was "the QB board is thin, so
  how much status risk do I tolerate?" The answer is none — which means the thin-board
  problem has to be solved *in advance*, by banking enough arms, not absorbed later by
  starting someone doubtful. Bank the top ~12 harder, not less hard.

Never start a player with an unresolved status flag unless you can verify active before
lock. `./gy s` drops them automatically; `--cleared "Name"` re-admits one you have
personally confirmed active.

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
  gets the touches is knowable in week 1; how good the opposing defense is, is not.
  **But check that the "hard fact" is still true.** This principle was illustrated with
  "Alvin Kamara is out, handing Travis Etienne the backfield" — and by Wednesday of week
  1 Kamara was practising in a limited capacity and listed questionable, not out. A
  role premise built on someone else's injury decays exactly as fast as the injury
  report, and unlike a status flag on your own player it never trips the filter. **Re-
  verify the absence that creates the role, not just the health of the player you are
  starting.**
- By roughly week 5 current-season defensive data becomes usable and this caveat relaxes.

## Shelf-life caveat

Decay only matters for players you would *actually start*. A QB31 with benching risk is not
an asset worth "preserving" — you were never going to start him, and if he is benched his
replacement is just as good. Spending a start on him to avoid "wasting" him is sunk-cost
reasoning. The shelf-life principle earns its keep in the genuinely useful band.

## Weekly checklist

1. Pull weekly + ROS ranks for every position.
2. Compute delta for the eligible (unburned) pool.
3. Filter out anyone whose ROS rank still sits inside the band you will need later,
   weighted by pool tightness (skip this filter entirely for DST).
4. Drop anyone with an unresolved status flag.
5. Sanity-check any matchup-based edge against offseason turnover (weeks 1-4 especially).
6. Take the highest remaining deltas that clear the survival bar for the week's cut %.
7. Check team/game overlap — decorrelate early in the season.
8. Verify inactives before lock.
9. For any starter whose role depends on another player's absence, verify that other
   player is still out — the tooling cannot see this dependency.
10. Record the burn in `data/used_players.json` via `./gy u "Name"` **after** lineups lock.

## Season deployment plan

| Weeks | Cut % | Posture |
| --- | --- | --- |
| 1-4 | 11.6-13.8% | Cheapest survivable lineup. Spend every decaying asset. Punt superflex here if needed. |
| 5-8 | 14.9-18.9% | Mid-tier. Ranks ~8-15. |
| 9+ | 20.5-25.6% | Deploy the bank. Never punt. Stacks become acceptable. |

## Week 1 lineup (2026) — final

| Slot | Player | Team | Wk | ROS | Delta | Proj |
| --- | --- | --- | --- | --- | --- | --- |
| QB | Kirk Cousins | LV | QB28 | — | — | ~13.4 |
| SFLX | Tua Tagovailoa | ATL | QB31 | — | — | ~13.5 |
| RB | Travis Etienne Jr. | NO | RB16 | RB18 | +2 | ~13.2 |*
| RB | Tony Pollard | TEN | RB27 | RB33 | +6 | 11.6 |
| WR | Davante Adams | LAR | WR21 | WR29 | +8 | ~10.8 |
| WR | DK Metcalf | PIT | WR31 | WR33 | +2 | 11.8 |
| FLEX | Quentin Johnston | LAC | WR34 | WR38 | +4 | 13.1 |
| TE | Dallas Goedert | PHI | TE8 | TE12 | +4 | 14.3 |
| DST | Jacksonville | JAC | DST1 | — | +11 | ~8 |

\* Etienne carries the lineup's only open question: Kamara is questionable, not out
(see "Role-by-absence" below). Re-check Saturday; pivot to Chuba Hubbard (CAR,
RB30/ROS40, +10) or Kenny Gainwell (TB, +3) if Kamara practises in full.

Every one of the nine is absent from the league-wide injury report — no designation
on any of them.

Nine players, nine teams, ~110 projected. Only shared game is Tua (ATL) vs Metcalf
(PIT) — opposite sides, a hedge, though that game carries a 42.0 total, the quietest
on the slate.

Banked: Bryce Young (QB24), Bucky Irving (RB20), Ladd McConkey (WR22), Kyle Pitts
(TE8), plus every elite — Gibbs, Bijan, McCaffrey, Chase, Nacua, St. Brown,
Smith-Njigba, Bowers, McBride, Lamar, Allen, Hurts, Burrow, Maye, Lawrence, Nix,
Shough, Cook, K. Walker, Jeanty, Chase Brown, Hampton, Flowers, Nabers, A.J. Brown,
Higgins, Fannin, Seattle and Houston DST.

### How it moved off the first draft

- **Pitts (TE5) -> Goedert.** Pitts was ROS TE8 — inside the TE hoard band, the only
  band violation in the lineup — and his thesis was Tua's target volume while Tua
  ranks QB31. Goedert is ROS TE12 (spendable) *and* projects higher, 14.3 vs 11.2.
  Cheaper asset and more points; the "deliberate exception" did not survive contact
  with the residual filter.
- **Bryce Young (QB24) -> Tua (QB31).** Young sits inside the startable band and is a
  real superflex body at ~115% QB consumption; Tua is below the band, so per the
  shelf-life caveat he is worth nothing later. Costs ~3.3 points to bank a usable arm.
  Confirmed startable: depth chart position 1, no injury designation, and Eisenberg
  writes Atlanta's week as "with Tua Tagovailoa under center." **A weeks-1-5 move
  only.**
- **Irving (RB19) -> Pollard (RB27).** Irving's entire case was the Cincinnati
  matchup, which the turnover check had already voided. Pollard draws the Jets, who
  allowed the most fantasy points to backs in 2025, with Tennessee favoured at home.
  Note Irving was later confirmed 100% and endorsed as "a great RB2 play" — holding
  him would not have been a mistake, just a more expensive one.
- **McConkey (WR17) -> a deep FLEX.** McConkey at ROS WR22 was the only WR in the
  lineup with real residual. Adams (ROS WR29) and Metcalf (ROS WR33) have almost
  nothing left to bank, so burning them is close to free — their high *weekly* rank
  is not a reason to avoid them.

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
- **"Cincinnati is the softest RB matchup on the board."** Built on 2025 splits. They
  rebuilt the defensive line over the offseason. Prior-year data needs a turnover check.
- **"Protect Jacksonville's DST12 residual."** Applied the RB scarcity rule to a loose,
  matchup-driven pool. Residual value must be weighted by pool tightness.
- **"Michael Wilson is the biggest delta on the WR board, so start him."** He was
  WR36 weekly against WR55 ROS, a +19 gap and the largest anywhere. He was also
  Arizona's *third* option behind Marvin Harrison Jr. and Trey McBride, "terrible
  last year when Harrison was healthy," as a 9.5-point underdog against the defence
  that finished 5th in fewest points allowed to receivers. **A large positive delta
  on a deep player usually means an analyst likes him, not that he will see the
  ball.** Delta encodes matchup and shelf-life; it cannot see target share. Cross-
  check role before burning anyone whose delta comes from a low ROS rank rather than
  a high weekly one — the same role-certainty rule that applies to deep RBs.
- **"Read the weekly rank to judge how expensive a player is."** The residual filter
  runs on ROS rank. A player can look costly this week and be nearly free as an
  asset: Adams was WR21 weekly but WR29 ROS with a +8 delta — the textbook burn.

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
- **Isaiah Likely** (NYG) is weekly TE11 against ROS TE10 — a *negative* delta, so he
  is a hoard, not a burn, and one of the few tight ends worth carrying toward weeks
  9-11. SportsLine's model has him TE9 ahead of LaPorta and Kelce, as the clear No. 1
  tight end for Jaxson Dart.

## Open questions

- Confirm exact starting slots against the league page.
- Contest end week (assumed 17 for all pool math above).
- Entrant count: the elimination table above is built on 752, but 1052 has also been
  cited. Every cut percentage and posture threshold moves if it is the latter.

**Answered:** does an inactive starter count as burned? **Yes** — see "An inactive starter
is burned" above.

## Tooling

The weekly checklist above is implemented as `./gy s` (`graveyard.py strategy`). It
joins the weekly and ROS boards into a delta column, drops burned players and status
flags, applies the per-position residual filter (`HOARD_BAND` in `graveyard.py`, DST
exempt), and prints the recommended slate plus the top burn candidates per position.

It reads the week off the elimination table: decorrelates and allows a superflex punt
through week 8, requires a real QB in superflex and permits same-team pairs from week 9
(`ENDGAME_WEEK`), and warns about stale prior-year data through week 4.

Since an inactive start burns the player anyway, the status filter is a hard drop rather
than a ranking penalty. `--cleared "Name"` re-admits a player you have verified active.

Steps it cannot do for you: verifying inactives before lock (step 8), and the
offseason-turnover sanity check on any matchup edge (step 5). `--explain` shows who was
held back and why, so the filter never silently hides a player you wanted.
