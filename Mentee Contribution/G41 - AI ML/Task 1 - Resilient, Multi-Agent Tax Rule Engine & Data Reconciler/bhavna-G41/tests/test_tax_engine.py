
import unittest

from reasoning_agent.rule_loader import load_tax_rules
from reasoning_agent.tax_engine import calculate_depreciation


class TestTaxEngine(unittest.TestCase):

    def test_india_tax_calculation(self):
        rules = load_tax_rules("India")

        asset_data = {
            "asset_name": "laptop",
            "quantity": 1,
            "purchase_cost": 100000,
            "purchase_date": "2026-04-05",
            "placed_in_service_date": "2026-04-05",
            "jurisdiction": "India",
            "currency": "INR"
        }

        result = calculate_depreciation(asset_data, rules)

        self.assertEqual(result["status"], "calculated")
        self.assertEqual(result["method"], "WDV")
        self.assertEqual(result["depreciation_amount"], 40000.00)
        self.assertEqual(result["closing_wdv"], 60000.00)

    def test_us_tax_calculation(self):
        rules = load_tax_rules("US")

        asset_data = {
            "asset_name": "laptop",
            "quantity": 1,
            "purchase_cost": 100000,
            "purchase_date": "2026-04-05",
            "placed_in_service_date": "2026-04-05",
            "jurisdiction": "US",
            "region": "California",
            "currency": "USD"
        }

        result = calculate_depreciation(asset_data, rules)

        self.assertEqual(result["status"], "manual_review")
        self.assertIn("rule_id", result)

    def test_invalid_asset_cost(self):
        rules = load_tax_rules("India")

        asset_data = {
            "asset_name": "laptop",
            "purchase_cost": -1000,
            "purchase_date": "2026-04-05",
            "placed_in_service_date": "2026-04-05",
            "jurisdiction": "India",
            "currency": "INR"
        }

        result = calculate_depreciation(asset_data, rules)

        self.assertEqual(result["status"], "error")


if __name__ == "__main__":
    unittest.main()
