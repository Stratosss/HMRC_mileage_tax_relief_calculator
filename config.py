import json
from datetime import datetime #import it from main.py?


def open_json():
    try:
        with open("settings.json", "r") as my_file:
            print("file found and loaded")
            settings = json.load(my_file) #parses the JSON data and returns it as a Python dictionary
        return settings
    except FileNotFoundError as e:
        print("file not found- Proceed with creation of default settings.json file")
        data = {
                "app_version": "1.2.0",
                "tax_year": f"{datetime.now().year}/{datetime.now().year + 1}",
                }
        json_str = json.dumps(data, indent=4)
        with open("settings.json", "w") as my_file:
            my_file.write(json_str)
        return data

def reset_json(json_file, miles, day_of_the_month, month_number,year):
        if day_of_the_month == 6 and month_number == 4: #The new tax year in the UK begins on 6 April every year
            json_file["tax_year"] = f"{year}/{year + 1}"
            json_file["starting_mileage"] = miles #resetting the starting mileage to the provided value
            print(f"Updated Json file: {json_file}")
            json_str = json.dumps(json_file, indent=4) # Convert the updated dictionary back to a JSON string with indentation for readability
            print(json_str)
            with open("settings.json", "w") as my_file:
                my_file.write(json_str)
                print("rewrite json file")
            print(f"Is in here: {json_file['tax_year']}")

        print(f"{day_of_the_month}/{month_number}")





