import logic as lg
import pytest

# --- Validation Tests ---

def test_valid_input():
    assert lg.validate_inputs(45, 45, 25, 1000, 1200, 3000, 0.2) is None

def test_negative_input():
    result = lg.validate_inputs(-1, 45, 25, 1000, 1200, 3000, 0.2)
    assert result == "⚠️ Numbers must be non-negative"

def test_wrong_order_input():
    # Splitting the string check to be safer with line breaks
    result = lg.validate_inputs(45, 45, 25, 1000, 3000, 1200, 0.2)
    assert result == "⚠️ End mileage must be higher than start mileage which must be higher than start of year mileage"

# --- Calculation Tests ---
@pytest.mark.parametrize("rate, expected_savings", [
    (0.2, 13.96),
    (0.4, 27.94),
])

def test_calc_before_10k_40(rate, expected_savings):
    relief, savings, case = lg.calculate_tax_relief(21, 45, 25, 48166, 48166, 48457, rate)
    assert relief == 69.84
    assert pytest.approx(savings, 0.01) == expected_savings
    assert case == "less than 10k"

@pytest.mark.parametrize("rate, expected_savings", [
    (0.2, 10.85),
    (0.4, 21.70),
])

def test_calc_after_10k_40(rate, expected_savings):
    relief, savings, case = lg.calculate_tax_relief(21, 45, 25, 1000, 13900, 15256, rate)
    assert relief == 54.24
    assert pytest.approx(savings, 0.01) == expected_savings
    assert case == "only after 10k"

def test_calc_started_before_10k_ended_after():
    relief, savings, case = lg.calculate_tax_relief(21, 45, 25, 30000, 38000, 52000, 0.4)
    assert relief == 960.00
    assert savings == 384.00
    assert case == "started before 10k ended after 10k"