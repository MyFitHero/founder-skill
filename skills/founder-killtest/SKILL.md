---
name: founder-killtest
description: >-
  Kill test for a spend or launch decision (MyFitHero fork, adapted from
  SensaiXo/kill-it-first, MIT). Before money or weeks leave your hands (an
  influencer programme, an ad test, a hire, a feature bet), four blind reviewer
  sub-agents attack a frozen one-page case, each from one angle, using only
  evidence that happened. Returns KILL, HOLD, VALIDATE or ADVANCE and the up to
  three cheapest real-world tests, each with a cost, a pass threshold and what a
  pass unlocks. Use when the user says "should I spend on X", "kill test",
  "stress-test this decision", "what is the cheapest way to prove demand",
  "before I pay influencers", "is this worth it".
argument-hint: "[decision in one sentence]"
---

# founder-killtest

The other founder skills ask "is the business viable?". This one asks a narrower
question, at the moment it matters: **is the evidence strong enough for THIS
commitment, and what is the cheapest test that would make it stronger?**

Method adapted from [SensaiXo/kill-it-first](https://github.com/SensaiXo/kill-it-first)
(MIT, licence copied next to this file). Rewritten for this pack; any fault is ours.

## Honest limits, say them once

Its own authors measured it: on four past decisions, the four-reviewer run put
4/4 verdicts in the accepted set; one blunt "attack my idea" chat got 3/4. So the
protocol is not proven better at verdicts. What it adds is a convergence signal
(how many blind reviewers block independently), findings tied to distinct angles,
and an audit trail. Verdicts also vary between runs: **run it twice before acting**
and report both.

## Step 1: the case, frozen

Write `founder/killtest/<case-id>.md`, one page:

- **Decision**: the exact commitment with its number ("pay 40% of first-year
  revenue to 10 micro-influencers"), what leaves your hands (money, weeks), what
  undoing it costs and the last cheap exit, the deadline and who set it, who
  decides.
- **Customer, moment, problem**: who, in which concrete moment, suffers what.
- **Why money flows**: who pays, for what, how much, how often.
- **Current alternatives**: what the customer does today, including nothing.
- **Critical unknowns**: the author's own list. A hidden gap cannot be flagged.
- **Evidence pack**: the rules below.

Commit it before the run (`git` hash in the ledger). Any edit after a verdict is
a new version, and the old verdict stays in the ledger.

### Evidence rules

1. **Only things that happened**: someone paid, did, wrote, clicked. Opinions
   and forecasts go in the unknowns.
2. **Provenance on every item**: source, date, who collected it, how many people.
   An item without it is struck before the run.
3. **A `limit` on every item**: what it does NOT show ("50 likes: attention only,
   nobody asked to pay").
4. **Typed on the ladder, honestly**:

   | rung | type | example |
   | --- | --- | --- |
   | 1 | paid | money changed hands for this offer |
   | 2 | costly action | time spent, data shared, a return visit, an unprompted referral |
   | 3 | stated intent | "I would pay" in an interview or survey |
   | 4 | attention | clicks, likes, free waitlist sign-ups |
   | 5 | analogy | competitors exist, a similar thing worked elsewhere |

   Simulated buyers (`/founder-consumer`), market benchmarks and desk research
   are rung 5 at best. They can justify a test, never a commitment at scale.
5. **At least one item against the case**. If none is known, write "no
   disconfirming evidence gathered"; reviewers treat it as the gap it is.
6. **Anonymise**: no real names of testers, clubs or influencers in the pack.
7. **Check every URL** in the pack opens and says what the item claims, before
   the run. An unreachable or mismatched source is struck.

## Step 2: four blind reviewers

Send ONE message with four Agent calls (`general-purpose`), one per lens. Each
gets the case file path and its lens below, and nothing else: no other files, no
web, no other reviewer's report. Never answer for a reviewer.

| lens | the question |
| --- | --- |
| Outcome and premise | Is this a real, valuable problem for this customer, or an interesting feature? |
| Lifecycle and mechanism | What triggers use, what creates value, what brings people back, and what makes them leave? |
| Authority and boundary | Who experiences it, who decides, who pays, who distributes, who can block, who carries the risk? |
| Evidence validity | Does each item prove demand or only attention and politeness? Name the item, its rung, what it shows and what the case makes it carry. |

Each reviewer writes `founder/killtest/<case-id>-<lens>.md` with findings in
this shape: one-line summary, the claim, evidence item ids and rung, what it
supports and fails to support, the smallest useful experiment that would produce
evidence one rung higher, severity (BLOCKING or ADVISORY), confidence. It ends
with exactly `VERDICT: PASS` or `VERDICT: BLOCKING`. Tell each reviewer: do not
be kind, do not invent a flaw you cannot trace to a line of the case, and do not
demand certainty, only enough evidence for the next step the case proposes.

## Step 3: the verdict

You synthesise, without adding findings of your own:

- **KILL**: a blocking flaw no cheap test can fix.
- **HOLD**: something outside the idea must be settled first (legal, platform,
  company not incorporated, an existing commitment).
- **VALIDATE**: the premise is alive but unproven. No spend at scale until the
  listed tests run.
- **ADVANCE**: the pack already justifies the next named step.

Write `founder/killtest/<case-id>-verdict.md`:

1. The verdict and how many of the four reviewers blocked (4/4 is strong, 1/4
   is weak).
2. Findings that two or more reviewers reached independently, first.
3. Residual risks no test can settle: a human accepts them or not.
4. **Up to three cheapest real tests**, de-duplicated: action, cost (money and
   days), pass threshold written now, and what a pass unlocks. Prefer a test
   that produces rung 1 or 2 evidence.
5. Ten lines of reasoning at most, in plain language.

## Step 4: the ledger

Append one line to `founder/killtest/RUNS.md`, never edit an old one:
`date | case-id | version | commit | verdict | blocking n/4 | outcome (filled later)`.
A case that went KILL, then an edit, then ADVANCE must stay visible as exactly
that. When the real outcome is known, fill only the outcome column.

## Output

`founder/killtest/`. Next: the tests go into the kill criteria of
`/founder-launch`; a VALIDATE before a spend means the spend waits for them.
