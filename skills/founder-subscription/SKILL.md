---
name: founder-subscription
description: >-
  The subscription-app CFO (MyFitHero fork). Builds the economics of a mobile or
  web subscription before money is spent: net price after Apple, Google and web
  fees and refunds, LTV of one payer, CAC and payback, 24 months of cash under
  three stress scenarios (base, pessimistic, brutal), the installs needed EVERY
  month to hold 1,000 / 10,000 / 100,000 payers, and the payers a monthly ad
  budget settles at. Every market input carries a dated public source or is
  flagged UNSOURCED. Use instead of founder-cfo for any subscription or freemium
  app: "unit economics", "LTV", "CAC", "is the app profitable", "how many
  installs", "what does 2,000 euros of ads buy", "business plan by tier".
argument-hint: "[path to economics.json] [--hold N ...] [--budget B ...]"
---

# founder-subscription

`founder-cfo` is shaped like a cafe: one price, units a day, rent. A subscription
app has none of that. What decides it is conversion, renewal and the volume of
installs you must find every month just to stand still. This skill computes
those, and stresses them until they hurt.

Tool in this folder (standard library only, no network):

```bash
python3 -I "${CLAUDE_SKILL_DIR}/app_economics.py" founder/economics.json --out founder/economics.md
python3 -I "${CLAUDE_SKILL_DIR}/app_economics.py" founder/economics.json --hold 1000 10000 100000
python3 -I "${CLAUDE_SKILL_DIR}/app_economics.py" founder/economics.json --budget 575 2300 5750
```

## Step 1: the inputs, each with a dated source

Write `founder/economics.json` (shape: `example.json` in this folder, the
MyFitHero median scenario of 15/11/2026). A missing field is an error; the tool
never guesses.

| field | what goes in it |
| --- | --- |
| `plans` | each plan: `name`, `price`, `period_months` (1 or 12), `mix` (shares sum to 1) |
| `channel_mix` | share of payers per channel: `apple`, `google`, `web` |
| `fees` | store commission per channel, `web_pct` and `web_fixed` for the card processor |
| `refund_rate` | share of gross refunded (optional, but the report says when it is missing) |
| `install_to_trial`, `trial_to_paid` | the funnel; their product is install to payer |
| `monthly_churn`, `annual_renewal` | monthly churn of monthly payers, first renewal rate of annual payers |
| `variable_cost_per_payer_month` | AI, infra and per-user tools for one payer |
| `free_cost_per_active_month`, `free_monthly_churn` | what a free user costs and how fast they leave |
| `fixed_monthly` | what you pay every month regardless |
| `organic_installs_per_month`, `paid_spend_per_month`, `cost_per_install` | volume and ads (a number or a list of monthly values) |
| `cash_start` | cash on day one (0 makes "lowest cash" the money to advance) |
| `sources` | one entry per field: where the number comes from, with its date |

**Where numbers come from (rule of the MyFitHero fork, Christophe 15/11/2026):**

1. Decisions the founder made (prices, quotas, trial length): cite the decision
   and its date.
2. Market benchmarks: a public source read for this run, named and dated
   (RevenueCat State of Subscription Apps, AppTweak, Apple and Google fee pages,
   provider price pages). Search the web for the latest edition; do not reuse a
   number from an older `founder/` file, an earlier run or the app's repo. Those
   are obsolete by default.
3. Anything else is `HYPOTHESE` / `ASSUMPTION` in `sources`, or left out of
   `sources` so the report lists it as UNSOURCED.

Before the run, open every URL cited in `sources` and check it says what the
entry claims. An unreachable or mismatched source makes that input UNSOURCED
(idea taken from alinaqi/ideavalidator, MIT).

Adjust the benchmark to the product and say why in `sources` (example: a trial
without card converts below the category median). Then check the adjustment
against a second number (revenue per install at day 60, for example).

## Step 2: run it, three ways

1. The full report: verdict, per-plan net price, LTV over 36 months, CAC,
   payback, 24 months of cash, under three stress scenarios.
2. `--hold`: installs needed every month to keep each payer count at steady
   state. This is usually the number that kills the plan.
3. `--budget`: payers a constant ad budget settles at with no organic installs.
   Convert the founder's currency first (write the rate in `sources`).

The stress multipliers are chosen to hurt, not to be likely. Lead with the
pessimistic scenario. The verdict is computed by the tool; never soften it in
your note.

## Step 3: the note, in the founder's language

At the top of `founder/economics.md`, in plain words:

- **The verdict and why**, in one line, with the check that failed.
- **Margin once a tier is reached** versus **the volume needed to hold it**
  (`--hold`). Say which of the two is the real problem.
- **Ads**: CAC against LTV, and what each budget the founder named buys
  (`--budget`). If ads lose money, say it plainly and say what ads are still
  good for (buying a measurement of real conversion).
- **The UNSOURCED inputs**, listed, and the real measurement that replaces each
  (for example: ~500 real installs replace the conversion benchmark).
- **Confidence**: high, medium or low, and what would change it.

Things the tool does not model, to add by hand when they matter: Apple moving
from 15% to 30% on first-year subscriptions above 1 M$ of proceeds, the
subscription-platform fee (RevenueCat 1% above 2,500 $/month), Stripe Billing
0.7%, taxes, salaries, resale value.

## Rules

- Every number in the note comes from the tool's output or a sourced input.
- A simulated buyer panel never feeds `trial_to_paid`. Panels give objections,
  not conversion.
- Not financial, tax or legal advice; say once that an accountant should check
  structure and tax before money moves.

## Output

`founder/economics.json`, `founder/economics.md` (plus one json/md pair per
scenario if the founder asked for low / median / high). Next: `/founder-launch`
turns the kill numbers into a real test; `/founder-pricing` if the margin is thin.
