import flet as ft
import pandas as pd
import os
from datetime import datetime
import logic as lg

contents_dict = {}
file_name = 'Records.xlsx'

            
def main(page: ft.Page):
    
    # Flet page configuration
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 800
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
   
    company_compensation = ft.TextField(
        label="Insert pence/mile compensation of your company",
        border=ft.InputBorder.NONE,
        filled=True,
        hint_text="Enter text here",
        expand=True
    )
    hmrc_first_10k = ft.TextField(
        label="Insert HMRC pence/mile for the first 10k miles",
        border=ft.InputBorder.NONE,
        filled=True,
        hint_text="Enter text here",
        expand=True
    )
    hmrc_rest = ft.TextField(
        label="Insert HMRC pence/mile for the rest of the miles",
        border=ft.InputBorder.NONE,
        filled=True,
        hint_text="Enter text here",
        expand=True
    )
    year_start_mileage = ft.TextField(
        label="Insert business mileage at the beginning of tax year",
        border=ft.InputBorder.NONE,
        filled=True,
        hint_text="Enter text here",
        expand=True
    )
    monthly_mileage_start = ft.TextField(
        label="Insert business mileage at the beginning of the month",
        border=ft.InputBorder.NONE,
        filled=True,
        hint_text="Enter text here",
        expand=True
    )
    monthly_mileage_finish = ft.TextField(
        label="Insert business mileage at the end of the month",
        border=ft.InputBorder.NONE,
        filled=True,
        hint_text="Enter text here",
        expand=True
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
           
            error_msg = lg.validate_inputs(cc, first10, after10, ys, ms, mf, tr)

            if error_msg:
                tax_relief_text.visible = False
                savings_text.visible = False
                saved_text.visible = False
                message_text.value = error_msg
                page.update()
                return   # ❌ STOP here if validation fails

            # ✅ VALIDATION PASSED 
            tax_relief, savings_result, case = lg.calculate_tax_relief(cc, first10, after10, ys, ms, mf, tr)
            
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
    
    def handle_dropdown_select(e: ft.Event[ft.Dropdown]):
        nonlocal tax_rate
        print(e.control.value)  # Debug: Check selected value
        # Use an empty string as a fallback so .strip() always exists
        selected = e.control.value or ""
        tax_rate = float(selected.strip('%')) / 100
        page.update()
            
    tax_band = ft.Dropdown(
        label="Tax Band",
        options=[
            ft.dropdown.Option("20%"),
            ft.dropdown.Option("40%"),
        ],
        on_select=handle_dropdown_select
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
        content=" ",
        on_click=change_theme,
        disabled=False,
        icon=ft.Icons.LIGHT_MODE
        )
    
    calculation_button = ft.FilledButton(
        content="Calculate", 
        on_click=validation,
        icon=ft.Icons.CALCULATE
        )
    
    save_button = ft.FilledButton(
        content="Save",
        on_click=write_to_excel,
        disabled=True,
        icon=ft.Icons.SAVE 
        )
    
    footer = ft.Container(
        content=ft.Text(
            "Disclaimer: This is an estimate, not tax advice. Always check with HMRC guidance.\n"
            f"Developed by Stratos Gialouris - All rights reserved © {datetime.now().year}",
            size=12,
            color=ft.Colors.WHITE,
            italic=True,
        ),
        alignment=ft.Alignment.BOTTOM_RIGHT
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
            
        ],
        spacing=10
    ),
    ft.Container(expand=True), # This container will take up all the remaining space, pushing the footer to the bottom when the message text and info tile are not visible
    footer
    )
           
if __name__ == "__main__":
    ft.app(main) 
