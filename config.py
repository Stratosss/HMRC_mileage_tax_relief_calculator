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
                "current_year": 0,
                "tax_year": "",
                "new_user": True,
                }
        json_str = json.dumps(data, indent=4)
        with open("settings.json", "w") as my_file:
            my_file.write(json_str)
        return data


def reset_json_condition(json_file, miles, day_of_the_month, month_number,year): 
    if json_file["new_user"]:
        json_file["new_user"] = False # Set the "new_user" flag to False to indicate that the user has been initialized
        print("new user detected. Setting new_user flag to False and checking for new tax year.")
        
        if month_number == 4 and day_of_the_month < 6: #setting up new tax year for the first time; then it will be used to determine the result of the new tax year validation funciton.
            json_file["new_tax_year"] = False
        elif month_number < 4:
            json_file["new_tax_year"] = False
        else:
            json_file["new_tax_year"] = True
            
        reset_json(json_file, miles, year) 
         
    elif new_tax_year_validation(json_file, day_of_the_month, month_number,year):
        reset_json(json_file, miles, year)
        
    else:
        print(f"Not a new tax year yet. Current tax year: {json_file['tax_year']}")


        
def new_tax_year_validation(json_file, day_of_the_month, month_number,year):
    if year > json_file["current_year"]:
        outcome = determine_tax_year(json_file, day_of_the_month, month_number)
        return outcome
    else:
        if not json_file["new_tax_year"]: 
            outcome = determine_tax_year(json_file, day_of_the_month, month_number)
            return outcome
    return False


def determine_tax_year(json_file, day_of_the_month, month_number):
    if month_number == 4 and day_of_the_month > 5:
            json_file["new_tax_year"] = True # Set the "new_tax_year" flag to True to indicate that a new tax year has started
            print("month number is 4 and day of the month is greater than 5")
            return True
    elif month_number > 4:
        json_file["new_tax_year"] = True
        print("month number is greater than 4")
        return True
    
    return False
    

def reset_json(json_file, miles, year):   
    if json_file["new_tax_year"]:
        json_file["tax_year"] = f"{year}-{year + 1}"
        print("New tax year detected. Resetting JSON file with new tax year and starting mileage.")
    else:
        json_file["tax_year"] = f"{year-1}-{year}"
        
    json_file["starting_mileage"] = miles #resetting the starting mileage to the provided value
    json_file["current_year"] = year # Update the current year in the JSON file to the new year
    
    json_str = json.dumps(json_file, indent=4) # Convert the updated dictionary back to a JSON string with indentation for readability
    
    with open("settings.json", "w") as my_file:
        my_file.write(json_str)
        print("Overwrite json file")



