import unittest
import tax_calculator_monthly as script


class TestValidationFunction(unittest.TestCase):
    def test_valid(self):
        self.assertIsNone(
            script.validate_inputs(45, 45, 25, 1000, 1200, 3000, 0.2)
        )

    def test_negative(self):
        self.assertEqual(
            script.validate_inputs(-1, 45, 25, 1000, 1200, 3000, 0.2),
            "⚠️ Numbers must be non-negative"
        )

    def test_wrong_order(self):
        self.assertEqual(
            script.validate_inputs(45, 45, 25, 1000, 3000, 1200, 0.2),
            "⚠️ End mileage must be higher than start mileage "
            "which must be higher than start of year mileage"
        )
        
    def test_calc_before_10k_40(self):
        relief, savings, case = script.calculate_tax_relief(21, 45, 25, 48166, 48166, 48457, 0.4)
        self.assertEqual(relief,69.84)
        self.assertAlmostEqual(savings,27.94, delta=0.01)
        self.assertEqual(case, "less than 10k")
    
    def test_calc_before_10k_20(self):
        relief, savings, case = script.calculate_tax_relief(21, 45, 25, 48166, 48166, 48457, 0.2)
        self.assertEqual(relief,69.84)
        self.assertAlmostEqual(savings,13.96, delta=0.01)
        self.assertEqual(case, "less than 10k")
            
    def test_calc_after_10k_40(self):
        relief, savings, case = script.calculate_tax_relief(21, 45, 25, 1000, 13900, 15256, 0.4)
        self.assertEqual(relief,54.24)
        self.assertAlmostEqual(savings,21.70, delta=0.01)
        self.assertEqual(case, "only after 10k")
        
    def test_calc_after_10k_20(self):
        relief, savings, case = script.calculate_tax_relief(21, 45, 25, 1000, 13900, 15256, 0.2)
        self.assertEqual(relief,54.24)
        self.assertAlmostEqual(savings,10.85, delta=0.01)
        self.assertEqual(case, "only after 10k")
        
    def test_calc_started_before_10k_ended_after(self):
        relief, savings, case  = script.calculate_tax_relief(21, 45, 25, 30000, 38000, 52000, 0.4)
        self.assertEqual(relief,960.00)
        self.assertEqual(savings,384.00)
        self.assertEqual(case, "started before 10k ended after 10k")
    


if __name__ == "__main__":
    unittest.main()