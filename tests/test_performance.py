import unittest
import time
from decimal import Decimal, ROUND_HALF_UP

class TestPerformance(unittest.TestCase):
    def test_ledger_calculation_performance(self):
        start_time = time.time()

        # Simulate a large number of ledger calculations
        iterations = 100_000
        for _ in range(iterations):
            val1 = Decimal('1.005').quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            val2 = Decimal('1.004').quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

            credits = Decimal('100.00')
            debits = Decimal('50.00') + Decimal('50.00')

            base_amount = Decimal('10.05')
            tax_rate = Decimal('0.05')
            calculated_tax = (base_amount * tax_rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        end_time = time.time()
        execution_time = end_time - start_time

        # Assert that execution time is within acceptable bounds (e.g., < 1.0 seconds)
        self.assertLess(execution_time, 1.0, f"Execution time {execution_time} exceeded 1.0 seconds")

if __name__ == '__main__':
    unittest.main()
