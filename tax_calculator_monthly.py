import flet as ft
import pandas as pd
import os
from datetime import datetime

contents_dict = {}
file_name = 'Records.xlsx'

            
def main(page: ft.Page):
    
    # Flet page configuration
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 1200
    page.window.height = 800
    # page.window.resizable = False 
    
    # Function to write results to Excel
    def write_to_excel(e):
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
        save_button.disabled = True
        saved_text.value = f"👉 Your results were saved to file: {file_name}!"
        saved_text.visible = True
        page.update()
        
    # Function to validate inputs
    def validate_inputs(cc, first10, after10, ys, ms, mf, tax_rate):
        if tax_rate == "":
            tax_relief_text.visible = False
            savings_text.visible = False
            saved_text.visible = False
            return "⚠️ Please choose your tax band"

        if any(x < 0 for x in [cc, first10, after10, ys, ms, mf]):
            tax_relief_text.visible = False
            savings_text.visible = False
            saved_text.visible = False
            return "⚠️ Numbers must be non-negative"

        if mf < ms or ms < ys:
            tax_relief_text.visible = False
            savings_text.visible = False
            saved_text.visible = False
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
    
       
    
    company_compensation = ft.TextField(
        label="Insert pence/mile compensation of your company",
        border=ft.InputBorder.NONE,
        filled=True,
        hint_text="Enter text here",
    )
    hmrc_first_10k = ft.TextField(
        label="Insert HMRC pence/mile for the first 10k miles",
        border=ft.InputBorder.NONE,
        filled=True,
        hint_text="Enter text here",
    )
    hmrc_rest = ft.TextField(
        label="Insert HMRC pence/mile for the rest of the miles",
        border=ft.InputBorder.NONE,
        filled=True,
        hint_text="Enter text here",
    )
    year_start_mileage = ft.TextField(
        label="Insert business mileage at the beginning of tax year",
        border=ft.InputBorder.NONE,
        filled=True,
        hint_text="Enter text here",
    )
    monthly_mileage_start = ft.TextField(
        label="Insert business mileage at the beginning of the month",
        border=ft.InputBorder.NONE,
        filled=True,
        hint_text="Enter text here",
    )
    monthly_mileage_finish = ft.TextField(
        label="Insert business mileage at the end of the month",
        border=ft.InputBorder.NONE,
        filled=True,
        hint_text="Enter text here",
    )        
        
    
    # Validation and calculation function    
    def validation(e):
        message_text.value = ""
        try:    #Initial validation for integers required here, outside of validation function because the data are received as strings
            cc = int(company_compensation.value)
            first10 = int(hmrc_first_10k.value)
            after10 = int(hmrc_rest.value)
            ys = int(year_start_mileage.value)
            ms = int(monthly_mileage_start.value)
            mf = int(monthly_mileage_finish.value)
            tr = tax_rate
           
            error = validate_inputs(cc, first10, after10, ys, ms, mf, tr)

            if error:
                message_text.value = error
                page.update()
                return   # ❌ STOP here if validation fails

            # ✅ VALIDATION PASSED 
            tax_relief, savings_result, case = calculate_tax_relief(cc, first10, after10, ys, ms, mf, tr)
            
            contents_dict.update({
                'cc': cc,
                'first10': first10,
                'after10': after10,
                'ys': ys,
                'ms': ms,
                'mf': mf,
                'tr': tr,
                'tax_relief': tax_relief,
                'savings_result': savings_result
            })
            
            tax_relief_text.value = f"💰 The amount you can claim relief on is: £{tax_relief:.2f}"
            tax_relief_text.visible = True
            savings_text.value = f"💰 Based on your tax band you save for this month: £{savings_result:.2f}"
            savings_text.visible = True
            save_button.disabled = False
            saved_text.visible = False
            page.update()
            
        except ValueError:
            message_text.value = "⚠️ Please enter valid integers"
            tax_relief_text.visible = False
            savings_text.visible = False
            saved_text.visible = False
            page.update()
                
    # Tax bands dropdown change handler
    def tax_bands_dropdown(e):
        nonlocal tax_rate
        selected = e.control.value
        tax_rate = float(selected.strip('%')) / 100
        
    tax_band = ft.Dropdown(
        label="Tax Band",
        options=[
            ft.dropdown.Option("20%"),
            ft.dropdown.Option("40%"),
        ],
        on_change=tax_bands_dropdown,    
    )
    
    # Theme change function
    def change_theme(e):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
            theme_button.icon = ft.Icons.DARK_MODE
            footer.content.color = ft.Colors.BLACK
            tax_relief_text.color = ft.Colors.GREEN_ACCENT_700
            savings_text.color = ft.Colors.GREEN_ACCENT_700
            saved_text.color = ft.Colors.BLACK

        else:
            page.theme_mode = ft.ThemeMode.DARK
            theme_button.icon = ft.Icons.LIGHT_MODE
            footer.content.color = ft.Colors.WHITE
            tax_relief_text.color = ft.Colors.GREEN_ACCENT_100
            savings_text.color = ft.Colors.GREEN_ACCENT_100
            saved_text.color = ft.Colors.WHITE

        page.update()
        
    #App Contents & Design
    tax_rate =""      
    message_text = ft.Text(color=ft.Colors.RED, weight=ft.FontWeight.BOLD)    
    tax_relief_text = ft.Text(visible=False, size=20, color=ft.Colors.GREEN_ACCENT_100, weight=ft.FontWeight.BOLD)
    savings_text = ft.Text(visible=False, size=20, color=ft.Colors.GREEN_ACCENT_100, weight=ft.FontWeight.NORMAL)
    saved_text = ft.Text(visible=False, size=16, italic=True, color=ft.Colors.WHITE, weight=ft.FontWeight.NORMAL)

    header = ft.Text(
        "Tax Relief Calculator!",
        size=40,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLUE_700
        )

    theme_button = ft.FilledButton(
        text=" ",
        on_click=change_theme,
        disabled=False,
        icon=ft.Icons.LIGHT_MODE
        )
    
    calculation_button = ft.FilledButton(
        text="Calculate", 
        on_click=validation,
        icon=ft.Icons.CALCULATE
        )
    
    save_button = ft.FilledButton(
        text="Save",
        on_click=write_to_excel,
        disabled=True,
        icon=ft.Icons.SAVE 
        )
    
    footer = ft.Container(
        content=ft.Text(
            "Disclaimer: This is an estimate, not tax advice. Always check with HMRC guidance.\n"
            "Developed by Stratos Gialouris - All rights reserved ©️2026",
            size=16,
            color=ft.Colors.WHITE,
            italic=True,
        ),
        alignment=ft.alignment.bottom_right,
        )

    page.add(
    ft.Column(
        controls=[
            header,
            theme_button,
            company_compensation,
            hmrc_first_10k,
            hmrc_rest,
            year_start_mileage,
            monthly_mileage_start,
            monthly_mileage_finish,
            tax_band,
            ft.Row(
            controls=[calculation_button,
            save_button]),
            message_text,  # Warning/result appears here
            tax_relief_text,
            savings_text,
            saved_text,
            footer
        ],
        spacing=10
    ),

    )
           
if __name__ == "__main__":
    ft.app(main) 
