import main as script
import pandas as pd
import os
from datetime import datetime

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
   
        
    # Case 2: Entire month above 10k
    elif diff_start > 10000:
        tax_relief = relief_per_band(after10_rate, compensation, monthly_miles)


    # Case 3: Month crosses 10k threshold
    else:
        miles_before_10k = 10000 - diff_start
        miles_after_10k = diff_finish - 10000
        
        relief_before = relief_per_band(first10_rate, compensation, miles_before_10k)
        relief_after = relief_per_band(after10_rate, compensation, miles_after_10k)

        tax_relief = relief_before + relief_after


    savings = tax_relief * tax_band
    
    return tax_relief, savings

# Function to write results to Excel
def write_to_excel(contents_dict, file_name):
    try:
        current_month = datetime.now().strftime("%B")
        current_year = datetime.now().year
        date = f"{current_month} {current_year}"    
        
        row = {
                'Month' : date,
                'Company Compensation (p/mile)' : contents_dict["cc"],
                'HMRC First 10k (p/mile)' : contents_dict["first10"],
                'HMRC After 10k (p/mile)' : contents_dict["after10"],
                'Year Start Mileage' : contents_dict["ys"],
                'Month Start Mileage' : contents_dict["ms"],
                'Month End Mileage' : contents_dict["mf"],
                'Tax Band (%)' : contents_dict["tr"] * 100,
                'Tax Relief (£)' : contents_dict["tax_relief"],
                'Savings (£)' : round(contents_dict["savings_result"], 2)
            }
        df = pd.DataFrame([row])
        if not os.path.isfile(file_name):
            df.to_excel(file_name, index=False, engine="openpyxl")
        else:
            df_existing = pd.read_excel(file_name, engine="openpyxl", index_col=None)
            df_updated = pd.concat([df_existing, df], ignore_index=True)
            df_updated.to_excel(file_name, index=False, engine="openpyxl")
        return f"👉 Your results were saved to file: {file_name}!"
    except PermissionError:
        return f"❌ Error: Could not save! Please close '{file_name}' and try again."
    except Exception as e:
        return f"⚠️ An unexpected error occurred: {e}"
    