import flet as ft
import pandas as pd
from datetime import datetime
import logic as lg


            
def main(page: ft.Page):
    
    contents_dict = {}
    file_name =f'Records_{datetime.now().year}.xlsx'
    tax_rate ="" 
    
    # Flet page configuration
    page.theme_mode = ft.ThemeMode.DARK
    page.window.min_width = 800
    page.window.min_height = 800
    page.window.height = 800
    page.window.width = 800
    # page.window.resizable = False 
    
    
    def write_to_excel_handler(e):
        saved_text.value = lg.write_to_excel(contents_dict, file_name)
        save_button.disabled = True
        saved_text.visible = True
        
        page.update()
    
    def handle_text_change(e):
    # If they change input after calculation, we should disable save button
        save_button.disabled = True  # 👈 They must click 'Calculate' again
  
        all_fields = [company_compensation, hmrc_first_10k, hmrc_rest, 
                    year_start_mileage, monthly_mileage_start, monthly_mileage_finish,tax_band]
       
        if any(textObject.value for textObject in all_fields):  # 👈 If any field has text, enable reset button
            reset_button.disabled = False
        else:
            reset_button.disabled = True      
        page.update()
   
   
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
            tax_relief, savings_result = lg.calculate_tax_relief(cc, first10, after10, ys, ms, mf, tr)
            
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
    
    def reset_values(e):
        nonlocal tax_rate
        
        company_compensation.value = ""
        hmrc_first_10k.value = ""
        hmrc_rest.value = ""
        year_start_mileage.value = ""
        monthly_mileage_start.value = ""
        monthly_mileage_finish.value = ""
        tax_band.value = None
        tax_rate = ""
        message_text.value = ""
        tax_relief_text.value = ""
        savings_text.value = ""
        tax_relief_text.visible = False
        savings_text.visible = False
        saved_text.visible = False
        save_button.disabled = True
        reset_button.disabled = True
        
        page.update()    
                
    # Tax bands dropdown change handler
    def handle_dropdown_select(e: ft.Event[ft.Dropdown]):
        nonlocal tax_rate
        print(e.control.value)  # Debug: Check selected value
        selected = e.control.value
        tax_rate = float(selected.strip('%')) / 100
        save_button.disabled = True  # 👈 They must click 'Calculate' again after changing tax band
        handle_text_change(None)  # 👈 Check if reset button should be enabled based on current field values
        page.update()
    
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
    company_compensation = ft.TextField(
        label="Insert pence/mile compensation of your company",
        border=ft.InputBorder.NONE,
        filled=True,
        hint_text="Enter text here",
        expand=True,
        on_change=handle_text_change
    )
    hmrc_first_10k = ft.TextField(
        label="Insert HMRC pence/mile for the first 10k miles",
        border=ft.InputBorder.NONE,
        filled=True,
        hint_text="Enter text here",
        expand=True,
        on_change=handle_text_change
    )
    hmrc_rest = ft.TextField(
        label="Insert HMRC pence/mile for the rest of the miles",
        border=ft.InputBorder.NONE,
        filled=True,
        hint_text="Enter text here",
        expand=True,
        on_change=handle_text_change
    )
    year_start_mileage = ft.TextField(
        label="Insert business mileage at the beginning of tax year",
        border=ft.InputBorder.NONE,
        filled=True,
        hint_text="Enter text here",
        expand=True,
        on_change=handle_text_change
    )
    monthly_mileage_start = ft.TextField(
        label="Insert business mileage at the beginning of the month",
        border=ft.InputBorder.NONE,
        filled=True,
        hint_text="Enter text here",
        expand=True,
        on_change=handle_text_change
    )
    monthly_mileage_finish = ft.TextField(
        label="Insert business mileage at the end of the month",
        border=ft.InputBorder.NONE,
        filled=True,
        hint_text="Enter text here",
        expand=True,
        on_change=handle_text_change
    )        
            
    tax_band = ft.Dropdown(
        label="Tax Band",
        options=[
            ft.dropdown.Option("20%"),
            ft.dropdown.Option("40%"),
        ],
        on_select=handle_dropdown_select
    )
           
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
    
    reset_button = ft.FilledButton(
        content="Clear all",
        on_click=reset_values,
        disabled=True,
        icon=ft.Icons.REFRESH,
        bgcolor=ft.Colors.RED,
        )
    
    calculation_button = ft.FilledButton(
        content="Calculate", 
        on_click=validation,
        icon=ft.Icons.CALCULATE
        )
        
    save_button = ft.FilledButton(
        content="Save",
        on_click=write_to_excel_handler,
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
            ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=
            [theme_button,
            reset_button]),
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
