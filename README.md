# Secret Scanner 🔍

A Python CLI tool that detects sensitive data (API keys, passwords, tokens) in files and prevents accidental leaks, the project demonstrates file scanning, database persistense and CRUD operations

## Features

- Detects common secrets in files (password, API_KEY, AWS keys, etc.).
- Stores scan history in SQLite database
- CLI interface with Click
- SQLAlchemy ORM with 3 tables (Users, Scans, Findings)
- Virtual environment management with Pipenv
- Support listing, scans, findings and users

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

4. **list all  scans**
   ```bash
   python app.py scanmgr list

5. **List all findings**
   ```bash
   python app.py finding list 

6. ***List users**
   ```bash
   python app.py user list

7. **Database(SQLite)**
   Enter database:
   ```bash
   sqlite3 secret_scanner.db 

8. **CRUD Examples(Create)**
   ```bash
   INSERT INTO scans (path, type, status, created_at, user_id)
   VALUES ('demo.txt', 'file', 'pending', datetime('now'), 1);

   SELECT * FROM scans;

   UPDATE scans SET status='archieved' WHERE id=1;

   DELETE FROM findings WHERE id=2;

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

10. **Example (if secret-scanner is two levels up)**  
bash
python ../../secret-scanner/app.py scan .

11. **Using absolute paths (always works)**  
bash
python ~/projects/secret-scanner/app.py scan /full/path/to/your/project

12. **QUICK START**
- Navigate to `secret-scanner` directory and run `pipenv shell`
- Navigate to your project while still in the secret-scanner shell
- Run the commands based on the position of your file you want to test (see examples above)  
- View results in terminal and database  
- Works with Python, JavaScript, React (.jsx), config files, and any text files  

---

## Database Schema
- **Users** – User information  
- **Scans** – Scan history and metadata  
- **Findings** – Detected secrets with locations  

## Secret Patterns Detected
- API keys (e.g., `AKIA...`)  
- Password assignments (`password="..."`)  
- 32+ character random strings  

## Requirements
- Python 3.9+  
- Pipenv  
- Click  
- SQLAlchemy  

## Development
The tool uses:
- Click for CLI interface  
- SQLAlchemy for ORM and database  
- Pipenv for virtual environment  
- Regex patterns for secret detection
