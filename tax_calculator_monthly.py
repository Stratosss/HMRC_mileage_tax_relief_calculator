import pyperclip
import flet as ft



def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK

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
    tax_rate =""      
    message_text = ft.Text(color=ft.Colors.RED)    
    tax_relief_text = ft.Text(visible=False, size=20, color=ft.Colors.GREEN_ACCENT_100, weight=ft.FontWeight.BOLD)
    savings_text = ft.Text(visible=False, size=20, color=ft.Colors.GREEN_ACCENT_100, weight=ft.FontWeight.NORMAL)
    copied_text = ft.Text(visible=False, size=16, italic=True, color=ft.Colors.GREY)    
    
    
    def is_int(e):
        try:
            cc = int(company_compensation.value)
            first10 = int(hmrc_first_10k.value)
            after10 = int(hmrc_rest.value)
            ys = int(year_start_mileage.value)
            ms = int(monthly_mileage_start.value)
            mf = int(monthly_mileage_finish.value)
            tr = tax_rate

            if all(x >= 0 for x in [cc, first10, after10, ys, ms, mf]):
                if mf < ms or ms < ys:
                    message_text.value = "⚠️ End mileage must be higher than start mileage which must be higher than start of year mileage" 
                else:
                    message_text.value = ""
                    calculation(cc, first10, after10, ys, ms, mf, tr)
            else:
                message_text.value = "⚠️ Numbers must be non-negative"

        except ValueError:
            message_text.value = "⚠️ Please enter valid integers"
        except TypeError:
            message_text.value = "⚠️ Please choose your tax band"
            print(e)

        page.update()
                
        
    def calculation(compensation, first10_rate, after10_rate,year_start_miles, miles_start, miles_finish, tax_band):
        monthly_miles = miles_finish - miles_start
        diff_start = miles_start - year_start_miles
        diff_finish = miles_finish - year_start_miles
       
       # Protection from negative relief (HMRC never gives negative allowances)
        def relief_per_band(hmrc_rate, company_rate, miles):
            return max(hmrc_rate - company_rate, 0) * miles / 100

        # Case 1: Entire month below 10k
        if  diff_start < 10000 and diff_finish <= 10000: 
            tax_relief = relief_per_band(first10_rate, compensation, monthly_miles)
            print("less than 10k")
            
        # Case 2: Entire month above 10k
        elif diff_start > 10000:
            tax_relief = relief_per_band(after10_rate, compensation, monthly_miles)
            print("only after 10k")
            
        # Case 3: Month crosses 10k threshold
        else:
            miles_before_10k = 10000 - diff_start
            miles_after_10k = diff_finish - 10000
            
            relief_before = relief_per_band(first10_rate, compensation, miles_before_10k)
            relief_after = relief_per_band(after10_rate, compensation, miles_after_10k)

            tax_relief = relief_before + relief_after
            print("started before 10k ended after 10k")
               
    
        savings_result = tax_relief * tax_band
        
        tax_relief_text.value = f"💰 The amount you can claim relief on is: £{tax_relief:.2f}"
        tax_relief_text.visible = True
        savings_text.value = f"💰 Based on your tax band you save for this month: £{savings_result:.2f}"
        savings_text.visible = True
        copied_text.value = "👉 Your tax relief amount was copied to clipboard!"
        copied_text.visible = True
        pyperclip.copy(tax_relief)
        page.update()
    
    
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
    
    
    page.add(
    ft.Column(
        controls=[
            ft.Text(
                "Tax Relief Calculator!",
                size=40,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_700
            ),
            company_compensation,
            hmrc_first_10k,
            hmrc_rest,
            year_start_mileage,
            monthly_mileage_start,
            monthly_mileage_finish,
            tax_band,
            ft.FilledButton(text="Calculate", on_click=is_int),
            message_text,  # Warning/result appears here
            tax_relief_text,
            savings_text,
            copied_text,
            ft.Container(
                content=ft.Text(
                    "Disclaimer: This is an estimate, not tax advice. Always check with HMRC guidance.\n"
                    "Developed by Stratos Gialouris - All rights reserved ©️",
                    size=16,
                    color=ft.Colors.WHITE,
                    italic=True,
                ),
                alignment=ft.alignment.bottom_right,
                padding=10,
            )
        ],
        spacing=10
    )
    )
 
ft.app(main)

