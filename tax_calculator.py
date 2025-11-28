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
    annual_mileage = ft.TextField(
        label="Insert annual business mileage",
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
            am = int(annual_mileage.value)
            tb = tax_rate

            if all(x >= 0 for x in [cc, first10, after10, am]):
                message_text.value = ""
                calculation(cc, first10, after10, am, tb)
            else:
                message_text.value = "⚠️ Numbers must be non-negative"

        except ValueError:
            message_text.value = "⚠️ Please enter valid integers"
        except TypeError:
            message_text.value = "⚠️ Please choose your tax band"

        page.update()
                
        
    def calculation(compensation, first10_rate, after10_rate, mileage, tb):
        if mileage <10001:
            tax_relief_result = ((first10_rate-compensation)*mileage)/100
        else:
            tax_relief_result  = ((10000*first10_rate + ((mileage-10000)*after10_rate)) - (mileage*compensation))/100
            
        savings_result = tax_relief_result *tb
        
        tax_relief_text.value = f"💰 The amount you can claim relief on is: £{tax_relief_result:.2f}"
        tax_relief_text.visible = True
        savings_text.value = f"💰 Based on your tax band you save: £{savings_result:.2f} / year"
        savings_text.visible = True
        copied_text.value = "👉 Your tax relief amount was copied to clipboard!"
        copied_text.visible = True
        pyperclip.copy(tax_relief_result)
        page.update()
    
    
    def dropdown_changed(e):
        nonlocal tax_rate
        selected = e.control.value
        tax_rate = float(selected.strip('%')) / 100
        
    tax_band = ft.Dropdown(
        label="Tax Band",
        options=[
            ft.dropdown.Option("20%"),
            ft.dropdown.Option("40%"),
        ],
        on_change=dropdown_changed,
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
            annual_mileage,
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
