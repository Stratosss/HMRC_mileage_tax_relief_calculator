import json
from datetime import datetime #import it from main.py?

day_of_the_month = datetime.now().day
month = datetime.now().month
# day_of_the_month = 6
# month = 4

def open_json(starting_mileage):
    try:
        with open("settings.json", "r") as my_file:
            print("file found and loaded")
            settings = json.load(my_file) #parses the JSON data and returns it as a Python dictionary
            reset_json(settings, starting_mileage) #call the reset_json function to check if the tax year needs to be updated
        return settings
    except FileNotFoundError as e:
        print("file not found")
        data = {
                "app_version": "1.1.0",
                "tax_year": f"{datetime.now().year}/{datetime.now().year + 1}",
                "starting_mileage": starting_mileage #given mileage
                }
        json_str = json.dumps(data, indent=4)
        with open("settings.json", "w") as my_file:
            my_file.write(json_str)
        return None

def reset_json(json__file, miles):
        if day_of_the_month == 6 and month == 4: #The new tax year in the UK begins on 6 April every year
            json__file["tax_year"] = f"{datetime.now().year}/{datetime.now().year + 1}"
            json__file["starting_mileage"] = miles #resetting the starting mileage to the provided value
            print(json__file)
            json_str = json.dumps(json__file, indent=4)
            with open("settings.json", "w") as my_file:
                my_file.write(json_str)
            print(f"Is in here: {json__file['tax_year']}")

        print(f"{day_of_the_month}/{month}")




open_json(56448)
