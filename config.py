import json


def open_json(year):
    try:
        with open("settings.json", "r") as my_file:
            print("JSON file found and loaded")
            settings = json.load(my_file) #parses the JSON data and returns it as a Python dictionary
        return settings
    except FileNotFoundError as e:
        print("JSON file not found- Proceed with creation of default settings.json file")
        data = {
                "app_version": "1.2.0",
                "current_year": 0, # Starts with the current year to compare for the reset condition, will be updated when the tax year changes
                "tax_year": f"{year}-{year + 1}",
                "first time user": True,    
                "New_tax_year": False
                }
        json_str = json.dumps(data, indent=4)
        with open("settings.json", "w") as my_file:
            my_file.write(json_str)
        return data

def reset_json_condition(json_file, miles, day_of_the_month, month_number,year): #Checks if the current year is greater than the year stored in the JSON file, and if so, checks if the current date is after April 5th (the start of the new tax year). If both conditions are met, it calls reset_json to update the JSON file with the new tax year and starting mileage. If not, it prints a message indicating that it's not a new tax year yet.
    if json_file["first time user"]: #performs a reset when the user runs the program for the first time, regardless of the date or year.
        reset_json(json_file, miles, year)
        print("First time user detected. Resetting JSON file with new tax year and starting mileage.")
    else:
        if new_tax_year_validation(json_file, day_of_the_month, month_number,year):
            reset_json(json_file, miles, year)
        else:
            print(f"Not a new tax year yet. Current tax year: {json_file['tax_year']}")

        
def new_tax_year_validation(json_file, day_of_the_month, month_number,year):
    if year > json_file["current_year"]:
        if month_number == 4:
            if day_of_the_month > 5:
                json_file["New_tax_year"] = True # Set the "New_tax_year" flag to True to indicate that a new tax year has started
                return True
        elif month_number > 4:
            json_file["New_tax_year"] = True
            return True
    else:
        if not json_file["New_tax_year"]: # If the "New_tax_year" flag is not already set to True, check if the current date is after April 5th of the current year. If so, set the flag to True and return True.
            if month_number == 4:
                if day_of_the_month > 5:
                    json_file["New_tax_year"] = True
                    return True
                elif month_number > 4:
                    json_file["New_tax_year"] = True
                    return True
    return False

    
def reset_json(json_file, miles, year):
    if json_file["first time user"]:
        json_file["first time user"] = False # Set the "first time user" flag to False after the first use and reset
    
    if json_file["New_tax_year"]:
        json_file["tax_year"] = f"{year}-{year + 1}"
        json_file["starting_mileage"] = ""
        print("New tax year detected. Resetting JSON file with new tax year and starting mileage.")
    else:
        json_file["tax_year"] = f"{year-1}-{year}"
        
    json_file["starting_mileage"] = miles #resetting the starting mileage to the provided value
    json_file["current_year"] = year # Update the current year in the JSON file to the new year
    json_file["New_tax_year"] = False # Set the "New_tax_year" flag to False to indicate that a new tax year is ongoing
    
    json_str = json.dumps(json_file, indent=4) # Convert the updated dictionary back to a JSON string with indentation for readability
    
    with open("settings.json", "w") as my_file:
        my_file.write(json_str)
        print("Overwrite json file")



