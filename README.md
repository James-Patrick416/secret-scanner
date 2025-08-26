# Secret Scanner 🔍

A Python CLI tool that detects sensitive data (API keys, passwords, tokens) in files and prevents accidental leaks.

## Features

- Scans files for hardcoded secrets using regex patterns
- Stores scan history in SQLite database
- CLI interface with Click
- SQLAlchemy ORM with 3 tables (Users, Scans, Findings)
- Virtual environment management with Pipenv

## Project Structure
secret-scanner/
├── src/
│ └── secret_scanner/
│ ├── init.py
│ ├── cli/
│ │ └── cli.py # Click CLI commands
│ ├── db/
│ │ └── database.py # Database setup and session
│ ├── models/
│ │ └── models.py # SQLAlchemy models (User, Scan, Finding)
│ └── scanner/
│ └── scanner.py # Secret detection logic
├── app.py # Main entry point
├── Pipfile # Dependencies
└── test.txt # Example test file

## Installation

1. **Clone the repository:**
   ```bash
   git clone git@github.com:James-Patrick416/secret-scanner.git
   cd secret-scanner

2. **Install Dependencies with Pipenv:**
   ```bash
   pipenv install
   pipenv shell

3. **Usage -Scan a single file or a single directory:**
   ```bash
   python app.py scan path/to/file.txt  
   python app.py scan path/to/folder/

4. **Example:**
   ```bash
   python app.py scan test.txt

5. **Basic command structure.**
   ```bash
   python [PATH_TO_SCANNER] scan [TARGET_FILE_OR_FOLDER]

6. **Example(if secret-scanner is in your parent directory)**
7. **Scan current folder.**
   ```bash
   python ../secret-scanner/app.py scan .

8. **Scan specific file.**
   ```bash
   python ../secret-scanner/app.py scan src/app.jsx

9. **Scan specific folder.**
   ```bash
   python ../secret-scanner/app.py scan config/

10. **Example(if secret-scanner is two levels up)**
   ```bash
   python ../../secret-scanner/app.py scan .

11. **Using absolute paths (always works)**
   ```bash
   python ~/projects/secret-scanner/app.py scan /full/path/to/your/project

12. **QUICK START**
- Navigate to secret-scanner directory run pipenv shell
- Navigate to your project while still in the secret-scanner shell
- run the commands based on the position of your file you want to test as shown with the examples above  
- view results in terminal and data base
- works with python, javascript, react(.jsx), config files and any text files!   
      
   
## DataBase Schema
- Users - User information
- Scans -Scan history and metadata
- Findings- Detected secrets with locations

## Secret Patterns Detected
- API keys (e.g AKIA...)
- Password assignments (password ="...")
- 32+ character random strings

## Requirements
- Python 3.9+
- Pipenv
- Click
- SQLALchemy

## Development
The tool uses:
- Click for CLI interface
- SQLAlchemy for ORM and database
- Pipenv for virtual environment
- Regex patterns for secret detection

       

