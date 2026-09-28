import json
from datetime import datetime #import it from main.py?


def open_json():
    try:
        with open("settings.json", "r") as my_file:
            print("file found and loaded")
            settings = json.load(my_file) #parses the JSON data and returns it as a Python dictionary
        return settings
    except FileNotFoundError as e:
        print("file not found")
        data = {
                "app_version": "1.1.0",
                "tax_year": f"{datetime.now().year}/{datetime.now().year + 1}",
                "starting_mileage": "" #given mileage
                }
        json_str = json.dumps(data, indent=4)
        with open("settings.json", "w") as my_file:
            my_file.write(json_str)
        return data

def reset_json(json__file, miles, day_of_the_month, month_number,year):
        if day_of_the_month == 6 and month_number == 4: #The new tax year in the UK begins on 6 April every year
            json__file["tax_year"] = f"{year}/{year + 1}"
            json__file["starting_mileage"] = miles #resetting the starting mileage to the provided value
            print(f"Updated Json file: {json__file}")
            json_str = json.dumps(json__file, indent=4)
            with open("settings.json", "w") as my_file:
                my_file.write(json_str)
                print("rwrite json file")
            print(f"Is in here: {json__file['tax_year']}")

        print(f"{day_of_the_month}/{month_number}")





