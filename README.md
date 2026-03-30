#🚗 HMRC Mileage Tax Relief Calculator
A sleek, Flet-based desktop application designed to help UK drivers calculate their eligible tax relief for business mileage. This tool compares company compensation against official HMRC rates and provides a monthly savings estimate based on your tax band.

✨ Key Features
Reactive UI: Built with Python and Flet, featuring a dynamic interface that responds instantly to user input.

Smart Validation: Integrated error handling to ensure mileage and compensation values are valid integers before calculation.

Automated State Management: * "Calculate" and "Save" buttons enable/disable based on form completion.

A centralized Reset system that clears all inputs and result displays.

Excel Export: Save your monthly records directly to a timestamped Excel file (Records_2026.xlsx) for easy record-keeping. Error-proof: catches error if file is open upon pressing save button and warns the user. 

Dark/Light Mode: Toggle between themes for a comfortable user experience.

##🛠️ Technical Stack
Frontend: Flet (Flutter for Python)

Logic & Data: Python 3.12, Pandas (for Excel handling)

Testing: Pytest

Version Control: Git (Feature-branch workflow)

🧪 Testing & Quality Assurance
The core calculation logic is decoupled from the UI to ensure accuracy. We maintain a suite of unit tests covering various HMRC scenarios (pre-10k miles, post-10k miles, and threshold crossovers).

To run the tests:
cd [directory]
pytest
-------------------------------
Current Status: 8/8 Tests Passing ✅
-------------------------------

🚀 Installation & Setup
Clone the repository:
git clone https://github.com/Stratosss/HMRC_mileage_tax_relief_calculator.git
cd HMRC_mileage_tax_relief_calculator

Install dependencies:
pip install flet pandas openpyxl pytest

Run the application:
python main.py

📂 Project Structure
main.py: The entry point containing the Flet UI and event handlers.

logic.py: The "brain" of the app containing tax calculation and validation logic.

test_logic.py: Pytest suite for verifying calculation accuracy.

.gitignore: Configured to exclude generated Excel reports and Python cache.

📝 Disclaimer
This tool provides estimates based on standard HMRC guidance. It is not a substitute for professional tax advice. Always verify your final figures with official HMRC documentation.

Developed by Stratos Gialouris — 2026

![1](https://github.com/user-attachments/assets/6410878c-db98-4f17-aae2-6ec1c69ca4e6)
![2](https://github.com/user-attachments/assets/267a2ef0-0f02-4299-9009-ca8bd0f5e6e2)
![3](https://github.com/user-attachments/assets/8900da5b-c653-4e72-b83d-1d3e863c3335)
![4](https://github.com/user-attachments/assets/e7c65ba9-7fe2-4877-ac6d-e9906ed198ff)
![5](https://github.com/user-attachments/assets/9a50651e-fff4-459c-8601-afcee448c5cf)
![6](https://github.com/user-attachments/assets/dfa6bdf2-d53b-47e6-b3ab-a947d168bdb8)
![7](https://github.com/user-attachments/assets/2e5f342a-0e4b-4b70-97fa-62f692667cad)
![8](https://github.com/user-attachments/assets/a4113c40-0234-4732-9081-ab55ffc4a96c)



