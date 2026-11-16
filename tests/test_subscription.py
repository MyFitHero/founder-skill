import json
import unittest

from _load import load, example

ae = load("founder-subscription", "app_economics")


def spec():
    with open(example("founder-subscription", "example.json"), encoding="utf-8") as fh:
        return json.load(fh)


class Subscription(unittest.TestCase):
    def test_lifetime_blends_monthly_and_annual(self):
        d = spec()
        # 0.35 x 1/0.19 + 0.65 x 12/0.72
        self.assertAlmostEqual(ae.lifetime_months(d, ae.SCENARIOS["base"]), 12.68, places=2)

    def test_refunds_lower_net_price(self):
        d = spec()
        with_refunds = ae.net_price(d, 79.99)
        d.pop("refund_rate")
        self.assertAlmostEqual(with_refunds, ae.net_price(d, 79.99) * 0.96, places=2)  # web fixed fee is not refunded

    def test_missing_refunds_are_said_not_guessed(self):
        d = spec()
        d.pop("refund_rate")
        self.assertIn("Refunds: not modelled", ae.report(d, 12))

    def test_hold_and_budget_are_inverse(self):
        d = spec()
        text = ae.hold_report(d, [1000])
        self.assertIn("| 1,000 | 5,260 |", text)
        # 2,300 a month at CPI 4.5 settles near 97 payers in the base case
        self.assertIn("| 2,300 | 97 |", ae.budget_report(d, [2300]))

    def test_base_ltv_counts_refunds(self):
        r = ae.analyse(spec(), "base", 24)
        self.assertAlmostEqual(r["ltv"], 71.32, places=1)

    def test_bad_refund_rate_is_refused(self):
        import os, tempfile
        d = spec()
        d["refund_rate"] = 1.5
        fd, path = tempfile.mkstemp(suffix=".json")
        with os.fdopen(fd, "w") as fh:
            json.dump(d, fh)
        try:
            with self.assertRaises(SystemExit):
                ae.load(path)
        finally:
            os.remove(path)


if __name__ == "__main__":
    unittest.main()
