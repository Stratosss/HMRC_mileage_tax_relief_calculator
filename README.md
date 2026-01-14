# HMRC_mileage_tax_relief_calculator (Monthly)
This project focuses on the development of an application to help the users calculate their HMRC tax relief amount stemming from their business mileage for each financial year.

The user inserts the following values:
- Pence/mile compensation of their company.
- Pence/mile compensation from HMRC for the first 10k miles.
- Pence/mile compensation from HMRC for the rest of the miles.
- Tax band (20% / 40%) of the individual.

Then, the app calculates the amount the user can claim relief on. It also calculates the amount they save based on their tax band. 
The app checks for correct user input (positive integers are accepted) and gives warning if the "calculate" button is pressed when cells are empty, or inappropirate input is given.

11/1/2026: Added a LIGHT / DARK theme button as well as some icons to make it more user-friendly and appealing. <br/>
The user has now the option to save the results in an excel file. If the file exists, it appends the latest values - the file has to be in the same directory as the app. If the file does not exist it creates it in the same directory as the app and appends the values. 
The save button is disabled until all validations pass and results are displayed. When the User presses the Save button, a message appears saying the values were saved on file: "Records.xlsx" and becomes disabled again, until new calculations are made.

![1](https://github.com/user-attachments/assets/707e01c5-cdb9-46fc-8f2e-1c8a20911fd6)
![2](https://github.com/user-attachments/assets/060b489f-8c4e-40fc-ac34-c25b10477fec)
![3](https://github.com/user-attachments/assets/4b4a51fc-cbd3-4b05-a783-c6d4ebb9eb5f)
![4](https://github.com/user-attachments/assets/f7694b7c-3fb5-4bf2-9f53-b9353055c2fe)
![5](https://github.com/user-attachments/assets/2260f3af-b5b3-4b74-8512-3fe9e4150a95)
![6](https://github.com/user-attachments/assets/77fe35ca-15ed-4214-a31f-b695686cd6dc)
![7](https://github.com/user-attachments/assets/a479938f-959b-4465-aa15-1564b00c953f)


