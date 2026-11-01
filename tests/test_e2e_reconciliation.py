import unittest

class ReconciliationE2ETest(unittest.TestCase):
    def setUp(self):
        # Mock data representing system state
        self.system_invoices = [
            {"id": "inv_001", "amount": 100.0, "currency": "USD", "items": [{"id": "item_1", "price": 50.0}, {"id": "item_2", "price": 50.0}]},
            {"id": "inv_002", "amount": 250.0, "currency": "USD", "items": [{"id": "item_3", "price": 250.0}]}
        ]
        self.merchant_statement = {
            "statement_id": "stmt_0823",
            "total_payout": 339.5,
            "fee_rate": 0.03, # 3% fee
            "transactions": [
                {"id": "tx_001", "ref": "inv_001", "amount": 100.0, "fee": 3.0, "net": 97.0},
                {"id": "tx_002", "ref": "inv_002", "amount": 250.0, "fee": 7.5, "net": 242.5}
            ]
        }

    def test_invoice_line_item_matching(self):
        """Test that line items sum up correctly to the invoice total."""
        for invoice in self.system_invoices:
            calculated_total = sum(item["price"] for item in invoice["items"])
            self.assertEqual(calculated_total, invoice["amount"])

    def test_fee_calculation_reconciliation(self):
        """Test that statement fees are calculated correctly based on rates and match net payouts."""
        fee_rate = self.merchant_statement["fee_rate"]
        calculated_total_net = 0.0

        for tx in self.merchant_statement["transactions"]:
            expected_fee = tx["amount"] * fee_rate
            self.assertAlmostEqual(tx["fee"], expected_fee, places=2)

            expected_net = tx["amount"] - expected_fee
            self.assertAlmostEqual(tx["net"], expected_net, places=2)

            calculated_total_net += expected_net

        self.assertAlmostEqual(self.merchant_statement["total_payout"], calculated_total_net, places=2)

    def test_discrepancy_detection(self):
        """Test detection of mismatched or missing line items in reconciliation."""
        # Introduce a discrepancy
        discrepant_statement = {
            "transactions": [
                {"id": "tx_001", "ref": "inv_001", "amount": 100.0, "fee": 3.0, "net": 97.0},
                {"id": "tx_003", "ref": "inv_003", "amount": 500.0, "fee": 15.0, "net": 485.0} # inv_003 missing from system
            ]
        }

        system_invoice_ids = {inv["id"] for inv in self.system_invoices}
        statement_refs = {tx["ref"] for tx in discrepant_statement["transactions"]}

        missing_in_system = statement_refs - system_invoice_ids
        missing_in_statement = system_invoice_ids - statement_refs

        self.assertIn("inv_003", missing_in_system)
        self.assertIn("inv_002", missing_in_statement)

if __name__ == '__main__':
    unittest.main()
