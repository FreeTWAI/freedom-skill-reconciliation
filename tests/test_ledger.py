import unittest
from decimal import Decimal, ROUND_HALF_UP

class TestLedgerCalculations(unittest.TestCase):
    def test_transaction_balance_validation_valid(self):
        # Transaction balance must balance to zero (credits == debits)
        credits = sum([Decimal('100.00')])
        debits = sum([Decimal('50.00'), Decimal('50.00')])
        self.assertEqual(credits, debits, "Credits must equal debits for a valid transaction")

    def test_transaction_balance_validation_invalid(self):
        # Invalid transaction where credits != debits
        credits = sum([Decimal('100.00')])
        debits = sum([Decimal('50.00'), Decimal('49.99')])
        self.assertNotEqual(credits, debits, "Mismatching credits and debits should be detected")

    def test_floating_point_rounding(self):
        # Financial calculations should use precise rounding (e.g., HALF_UP)
        val1 = Decimal('1.005').quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        self.assertEqual(val1, Decimal('1.01'), "1.005 should round up to 1.01")

        val2 = Decimal('1.004').quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        self.assertEqual(val2, Decimal('1.00'), "1.004 should round down to 1.00")

    def test_tax_calculation_discrepancy(self):
        # Tax calculation should be precise to avoid discrepancies
        base_amount = Decimal('10.05')
        tax_rate = Decimal('0.05')  # 5%

        # 10.05 * 0.05 = 0.5025
        calculated_tax = (base_amount * tax_rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        self.assertEqual(calculated_tax, Decimal('0.50'), "Tax of 0.5025 should round to 0.50")

if __name__ == '__main__':
    unittest.main()
