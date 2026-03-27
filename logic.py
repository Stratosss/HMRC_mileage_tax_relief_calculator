import main as script

# Function to validate inputs
def validate_inputs(cc, first10, after10, ys, ms, mf, tax_rate):
        if tax_rate == "":
            return "⚠️ Please choose your tax band"

        if any(x < 0 for x in [cc, first10, after10, ys, ms, mf]):
            return "⚠️ Numbers must be non-negative"

        if mf < ms or ms < ys:
            return "⚠️ End mileage must be higher than start mileage which must be higher than start of year mileage"
            
        return None # ✅ VALID

# Function to calculate tax relief
def calculate_tax_relief(compensation, first10_rate, after10_rate,year_start_miles, miles_start, miles_finish, tax_band):
    monthly_miles = miles_finish - miles_start
    diff_start = miles_start - year_start_miles
    diff_finish = miles_finish - year_start_miles
    
    # Protection from negative relief (HMRC never gives negative allowances)
    def relief_per_band(hmrc_rate, company_rate, miles):
        return max(hmrc_rate - company_rate, 0) * miles / 100

    # Case 1: Entire month below 10k
    if  diff_start < 10000 and diff_finish <= 10000: 
        tax_relief = relief_per_band(first10_rate, compensation, monthly_miles)
        case ="less than 10k"
        
    # Case 2: Entire month above 10k
    elif diff_start > 10000:
        tax_relief = relief_per_band(after10_rate, compensation, monthly_miles)
        case ="only after 10k"

    # Case 3: Month crosses 10k threshold
    else:
        miles_before_10k = 10000 - diff_start
        miles_after_10k = diff_finish - 10000
        
        relief_before = relief_per_band(first10_rate, compensation, miles_before_10k)
        relief_after = relief_per_band(after10_rate, compensation, miles_after_10k)

        tax_relief = relief_before + relief_after
        case = "started before 10k ended after 10k"

    savings = tax_relief * tax_band
    
    return tax_relief, savings , case