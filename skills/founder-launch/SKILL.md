---
name: founder-launch
description: >-
  Your launch lead. Builds a dated, step-by-step launch plan: a cheap real-world
  test first (a waitlist, a pre-sale or a pop-up with a real price, so real buyers
  confirm what the simulated panel said), then the countdown to opening day with
  owners and deadlines, the launch-day run sheet, and the first 90 days of what to
  measure and what to change. Use when the user says "how do I launch", "launch
  plan", "when can I open", "launch checklist", "go live", or "soft open".
argument-hint: "[target launch date]"
---

# founder-launch

Launching is a project with a date. This skill turns everything else in the pack
into a dated plan, and starts with the cheapest way to find out if real people
will pay before the big money goes out.

## Step 0: the pre-mortem and the kill criteria (MyFitHero fork)

Before any date, write the first section of `founder/launch.md`:

1. **Pre-mortem**: "It is 12 months from now and this failed. Why?" Five causes,
   most likely first, each with the evidence that already points to it (from
   `founder/board.md`, the panel's objections, `founder/economics.md`).
2. **Kill criteria**: three to five numbers, written BEFORE any money is spent,
   that stop or change the plan. Each has a metric, a threshold, a date and the
   action if it is missed. Example: "revenue per install at day 60 below 0.80 $
   after ~500 paid installs: stop paid ads". Prefer numbers the business can
   measure itself over market benchmarks.
3. Who decides when a criterion is hit, and that it is not renegotiated after
   the fact.

## Step 1: test before you spend

Pick the cheapest real test that fits the business, and run it before signing the
big costs in `founder/numbers.json`:

| business | the test |
| --- | --- |
| physical shop or café | a pop-up, a market stall or a pre-order list with a price and a date |
| online product | a landing page with the price and a "pre-order" or "join the waitlist" button |
| service or agency | three paid pilot clients at the planned price |
| subscription | a founding-member offer, paid up front |

Write the success line before running it (for example: 50 pre-orders in two weeks
at $6.50). Judge the result against that line and the kill criteria, not against
the panel's buy rate, which is simulated. If the line is missed, trust the real
buyers and go back to `/founder-offer` or `/founder-pricing`.

## Step 2: the countdown

From today to launch day, with real dates (ask for the target date; default to the
earliest realistic one given lead times in `founder/ops.md`). Weekly blocks, each
task with an owner and a deadline:

- Legal and money: registration, bank account, permits from `founder/ops.md`.
- Build: fit-out or website, suppliers ordered by their lead times.
- Brand: sign, packaging, profiles from `founder/brand.md`.
- Marketing: the calendar in `founder/marketing.md` from launch minus 14 days.
- Team: hiring and training on the SOPs.
- A soft open or friends-and-family day before the public launch.

Mark the critical path: the tasks that move the launch date if they slip.

## Step 3: launch day

An hour-by-hour run sheet: who is where, what goes out on which channel, the
opening offer, what to do if something breaks (from the risk register).

## Step 4: the first 90 days (MyFitHero fork: 30 days was too short for a subscription)

An app learns its real economics slowly: the trial ends on day 14, revenue per
install is readable around day 60, the first monthly renewals land on days 30 to
60. So the plan runs 90 days, in three blocks, each ending in a decision written
in advance.

| block | job | what to measure each week | decision at the end |
| --- | --- | --- | --- |
| days 1 to 30: measure | get enough installs to read anything (target set from `/founder-subscription`, often ~500) | installs by source, trial starts, day-1 and day-7 retention, crash-free sessions, support tickets | is the funnel broken somewhere fixable (onboarding, paywall, crash)? fix before buying more installs |
| days 31 to 60: convert | read trial to paid and the first monthly renewals | trial to paid, revenue per install at day 30, refunds, top reasons to cancel (ask them) | do the real numbers sit above or below the median scenario? update `founder/economics.json` with real values and rerun |
| days 61 to 90: decide | compare against the kill criteria | revenue per install at day 60, month-2 renewal, organic installs per week, cost per payer by channel | for each kill criterion: keep, change or stop. Spend more only on a channel whose real cost per payer is below its LTV |

Rules for the block:

- Every number comes from the app's own data (store consoles, payments, the
  app's analytics), never from a benchmark once a real value exists.
- One change at a time per block, written down with its date, so a moved number
  can be traced to a cause.
- Each block closes with a one-page review in `founder/launch.md`: the numbers,
  the decision, and what the next block will measure.

## Output

`founder/launch.md` with the test, the countdown, the run sheet and the 90-day
review. Next: `/founder-plan` compiles everything into the business plan.
