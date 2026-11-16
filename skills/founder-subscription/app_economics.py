#!/usr/bin/env python3
"""Subscription-app unit economics, stress-tested. Standard library only, no network.

Usage: python3 -I app_economics.py inputs.json [--months 24] [--out report.md]
       python3 -I app_economics.py inputs.json --hold 1000 10000
       python3 -I app_economics.py inputs.json --budget 575 2300 5750

A missing field is an error, never a guess. Every input without an entry in
"sources" is listed as UNSOURCED in the report. Optional "refund_rate" (share of
gross refunded); when it is absent the report says refunds are not modelled.

--hold N: installs needed EVERY month to keep N payers at steady state.
--budget B: payers a constant monthly ad budget B (same currency as prices)
            settles at, with no organic installs.
"""
import argparse, json, sys

REQUIRED = ["plans", "channel_mix", "fees", "install_to_trial", "trial_to_paid",
            "monthly_churn", "annual_renewal", "variable_cost_per_payer_month",
            "free_cost_per_active_month", "free_monthly_churn", "fixed_monthly",
            "organic_installs_per_month", "paid_spend_per_month", "cost_per_install",
            "cash_start"]

# Stress multipliers. They are stress tests chosen to hurt, not benchmarks.
SCENARIOS = {
    "base": dict(conv=1.0, churn=1.0, organic=1.0, cpi=1.0, var=1.0),
    "pessimistic": dict(conv=0.6, churn=1.5, organic=0.5, cpi=1.5, var=1.3),
    "brutal": dict(conv=0.4, churn=2.0, organic=0.25, cpi=2.0, var=1.6),
}


def die(msg):
    sys.exit("ERROR: " + msg)


def load(path):
    with open(path, encoding="utf-8") as fh:
        d = json.load(fh)
    missing = [k for k in REQUIRED if k not in d]
    if missing:
        die("missing fields: " + ", ".join(missing))
    mix = sum(p["mix"] for p in d["plans"])
    if abs(mix - 1) > 1e-6:
        die("plans mix must sum to 1 (got %.3f)" % mix)
    if abs(sum(d["channel_mix"].values()) - 1) > 1e-6:
        die("channel_mix must sum to 1")
    for p in d["plans"]:
        if p["period_months"] not in (1, 12):
            die("period_months must be 1 or 12 (%s)" % p["name"])
    if not 0 <= d.get("refund_rate", 0.0) < 1:
        die("refund_rate must be between 0 and 1")
    return d


def lifetime_months(d, s):
    """Expected paid months of one new payer at steady state (no horizon cap),
    blended by plan mix: 1/churn for monthly, 12/(1-renewal) for annual."""
    churn = min(1.0, d["monthly_churn"] * s["churn"])
    renew = max(0.0, 1 - (1 - d["annual_renewal"]) * s["churn"])
    total = 0.0
    for p in d["plans"]:
        if p["period_months"] == 1:
            life = 1 / churn if churn > 0 else float("inf")
        else:
            life = 12 / (1 - renew) if renew < 1 else float("inf")
        total += p["mix"] * life
    return total


def hold_report(d, targets):
    """Installs a month needed to keep each target payer count, per scenario."""
    out = ["# Installs needed to hold a payer count (steady state)", "",
           "Steady state: payers = new payers per month x expected paid months. "
           "No ads, no horizon cap.", "",
           "| payers to hold | " + " | ".join(SCENARIOS) + " |",
           "|---|" + "---|" * len(SCENARIOS)]
    for t in targets:
        cells = []
        for n, s in SCENARIOS.items():
            conv = d["install_to_trial"] * d["trial_to_paid"] * s["conv"]
            life = lifetime_months(d, s)
            cells.append("{:,.0f}".format(t / (conv * life)) if conv > 0 else "inf")
        out.append("| {:,.0f} | ".format(t) + " | ".join(cells) + " |")
    out += ["", "Expected paid months per payer: " + "; ".join(
        "%s %.1f" % (n, lifetime_months(d, s)) for n, s in SCENARIOS.items())]
    return "\n".join(out)


def budget_report(d, budgets):
    """Payers a constant monthly ad budget settles at, with no organic installs."""
    out = ["# Payers a constant ad budget settles at (steady state, ads only)", "",
           "| monthly budget | " + " | ".join(SCENARIOS) + " |",
           "|---|" + "---|" * len(SCENARIOS)]
    for b in budgets:
        cells = []
        for n, s in SCENARIOS.items():
            conv = d["install_to_trial"] * d["trial_to_paid"] * s["conv"]
            cpi = d["cost_per_install"] * s["cpi"]
            cells.append("{:,.0f}".format(b / cpi * conv * lifetime_months(d, s)))
        out.append("| {:,.0f} | ".format(b) + " | ".join(cells) + " |")
    out += ["", "The budget is spent every month forever to stay at that level."]
    return "\n".join(out)


def net_price(d, price):
    """What reaches the bank from one charge, blended across store channels,
    after refunds when refund_rate is given."""
    f, cm = d["fees"], d["channel_mix"]
    price = price * (1 - d.get("refund_rate", 0.0))
    net = 0.0
    for ch, share in cm.items():
        if ch == "web":
            net += share * (price * (1 - f["web_pct"]) - f["web_fixed"])
        else:
            net += share * price * (1 - f[ch])
    return net


def series(v, months):
    if isinstance(v, list):
        if len(v) < months:
            die("monthly lists need at least %d values" % months)
        return v[:months]
    return [v] * months


def ltv_one_payer(d, s, horizon=36):
    """Contribution of one new payer over `horizon` months, blended by plan mix."""
    var = d["variable_cost_per_payer_month"] * s["var"]
    churn = min(1.0, d["monthly_churn"] * s["churn"])
    renew = max(0.0, 1 - (1 - d["annual_renewal"]) * s["churn"])
    total = 0.0
    for p in d["plans"]:
        alive, val = 1.0, 0.0
        for m in range(horizon):
            if p["period_months"] == 1:
                val += alive * (net_price(d, p["price"]) - var)
                alive *= 1 - churn
            else:
                if m % 12 == 0:
                    val += alive * net_price(d, p["price"])
                val -= alive * var
                if m % 12 == 11:
                    alive *= renew
        total += p["mix"] * val
    return total


def simulate(d, s, months):
    var = d["variable_cost_per_payer_month"] * s["var"]
    churn = min(1.0, d["monthly_churn"] * s["churn"])
    renew = max(0.0, 1 - (1 - d["annual_renewal"]) * s["churn"])
    conv = d["install_to_trial"] * d["trial_to_paid"] * s["conv"]
    organic = series(d["organic_installs_per_month"], months)
    spend = series(d["paid_spend_per_month"], months)
    cpi = d["cost_per_install"] * s["cpi"]
    monthly = {p["name"]: 0.0 for p in d["plans"] if p["period_months"] == 1}
    annual = {p["name"]: [] for p in d["plans"] if p["period_months"] == 12}  # [start, size]
    free, cash, pending = 0.0, float(d["cash_start"]), 0.0
    rows, first_neg, breakeven = [], None, None
    for m in range(months):
        installs = organic[m] * s["organic"] + (spend[m] / cpi if cpi > 0 else 0)
        new_payers = pending          # 14-day trial: payers bill the month after install
        pending = installs * conv
        rev = 0.0
        payers = 0.0
        for p in d["plans"]:
            n = new_payers * p["mix"]
            if p["period_months"] == 1:
                monthly[p["name"]] = monthly[p["name"]] * (1 - churn) + n
                rev += monthly[p["name"]] * net_price(d, p["price"])
                payers += monthly[p["name"]]
            else:
                cohorts = annual[p["name"]]
                for c in cohorts:
                    if m > c[0] and (m - c[0]) % 12 == 0:
                        c[1] *= renew
                        rev += c[1] * net_price(d, p["price"])
                if n:
                    cohorts.append([m, n])
                    rev += n * net_price(d, p["price"])
                payers += sum(c[1] for c in cohorts)
        free = free * (1 - d["free_monthly_churn"]) + installs * (1 - conv)
        cost = payers * var + free * d["free_cost_per_active_month"] * s["var"] \
            + d["fixed_monthly"] + spend[m]
        net = rev - cost
        cash += net
        if cash < 0 and first_neg is None:
            first_neg = m + 1
        if net >= 0 and breakeven is None and m > 0:
            breakeven = m + 1
        rows.append((m + 1, installs, payers, rev, cost, net, cash))
    return rows, first_neg, breakeven, conv


def analyse(d, name, months):
    s = SCENARIOS[name]
    conv = d["install_to_trial"] * d["trial_to_paid"] * s["conv"]
    var = d["variable_cost_per_payer_month"] * s["var"]
    per_plan = []
    for p in d["plans"]:
        per_month = net_price(d, p["price"]) / p["period_months"]
        per_plan.append((p["name"], p["price"], per_month, per_month - var))
    ltv = ltv_one_payer(d, s)
    cpi = d["cost_per_install"] * s["cpi"]
    cac = cpi / conv if conv > 0 else float("inf")
    blended_c = sum(p["mix"] * c for p, (_, _, _, c) in zip(d["plans"], per_plan))
    payback = cac / blended_c if blended_c > 0 else float("inf")
    rows, first_neg, breakeven, _ = simulate(d, s, months)
    min_cash = min(r[6] for r in rows)
    paid = any(x > 0 for x in series(d["paid_spend_per_month"], months))
    checks = [
        ("Every plan earns money after store fees and per-user cost",
         all(c > 0 for *_, c in per_plan)),
        ("LTV(36 mo) / CAC >= 3" + ("" if paid else " (no paid spend: not tested)"),
         (ltv / cac >= 3) if paid else None),
        ("CAC payback <= 12 months" + ("" if paid else " (no paid spend: not tested)"),
         (payback <= 12) if paid else None),
        ("Cash never goes below zero in %d months" % months, first_neg is None),
        ("Monthly net cash turns positive within %d months" % months, breakeven is not None),
    ]
    return dict(name=name, per_plan=per_plan, ltv=ltv, cac=cac, payback=payback,
                rows=rows, first_neg=first_neg, breakeven=breakeven, min_cash=min_cash,
                checks=checks, conv=conv)


def verdict(results):
    def ok(r):
        return all(c is not False for _, c in r["checks"])
    base, pess = results["base"], results["pessimistic"]
    if not ok(base):
        return "NOT VIABLE", "fails even on your own base inputs"
    if not ok(pess):
        return "FRAGILE", "holds on your inputs, breaks under the pessimistic stress"
    if not ok(results["brutal"]):
        return "VIABLE UNDER STRESS", "survives the pessimistic case, not the brutal one"
    return "VIABLE UNDER STRESS", "survives every stress case"


def fmt(x):
    return "inf" if x == float("inf") else "{:,.2f}".format(x)


def report(d, months):
    res = {n: analyse(d, n, months) for n in SCENARIOS}
    v, why = verdict(res)
    out = ["# Subscription unit economics", "",
           "**Verdict: %s** (%s). Computed, not written." % (v, why), ""]
    unsourced = [k for k in REQUIRED if k not in d.get("sources", {})]
    if unsourced:
        out += ["**UNSOURCED inputs (assumptions, not facts):** " + ", ".join(unsourced), ""]
    if "refund_rate" in d:
        out += ["Refunds: %.1f%% of gross%s." % (100 * d["refund_rate"],
                "" if "refund_rate" in d.get("sources", {}) else " (UNSOURCED)"), ""]
    else:
        out += ["Refunds: not modelled (no refund_rate). Results are optimistic by that much.", ""]
    out += ["Stress multipliers (chosen to hurt, not benchmarks): " +
            "; ".join("%s conv x%.1f churn x%.1f organic x%.2f CPI x%.1f cost x%.1f"
                      % (n, s["conv"], s["churn"], s["organic"], s["cpi"], s["var"])
                      for n, s in SCENARIOS.items()), ""]
    for n in ("pessimistic", "base", "brutal"):
        r = res[n]
        out += ["## Scenario: %s" % n, "",
                "| plan | price | net / month after fees | contribution / month |",
                "|---|---|---|---|"]
        out += ["| %s | %s | %s | %s |" % (a, fmt(b), fmt(c), fmt(e)) for a, b, c, e in r["per_plan"]]
        out += ["", "- install -> paying conversion: %.2f%%" % (100 * r["conv"]),
                "- LTV of one payer, 36 months, contribution: %s" % fmt(r["ltv"]),
                "- expected paid months per payer (steady state): %s" % fmt(lifetime_months(d, SCENARIOS[n])),
                "- CAC per payer (paid installs): %s" % fmt(r["cac"]),
                "- CAC payback: %s months" % fmt(r["payback"]),
                "- lowest cash: %s%s" % (fmt(r["min_cash"]),
                    " (runs out in month %d)" % r["first_neg"] if r["first_neg"] else ""),
                "- first month with positive net cash: %s" % (r["breakeven"] or "never in horizon"),
                "", "Checks:"]
        out += ["- [%s] %s" % ({True: "PASS", False: "FAIL", None: "N/A"}[c], t) for t, c in r["checks"]]
        out += ["", "| month | installs | payers | net revenue | costs | net | cash |",
                "|---|---|---|---|---|---|---|"]
        out += ["| %d | %d | %d | %s | %s | %s | %s |" % (m, i, p, fmt(rv), fmt(c), fmt(nt), fmt(cs))
                for m, i, p, rv, c, nt, cs in r["rows"]]
        out.append("")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs")
    ap.add_argument("--months", type=int, default=24)
    ap.add_argument("--out")
    ap.add_argument("--hold", type=float, nargs="+", metavar="PAYERS")
    ap.add_argument("--budget", type=float, nargs="+", metavar="BUDGET")
    a = ap.parse_args()
    d = load(a.inputs)
    if a.hold:
        text = hold_report(d, a.hold)
    elif a.budget:
        text = budget_report(d, a.budget)
    else:
        text = report(d, a.months)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
