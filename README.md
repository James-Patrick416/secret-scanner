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

## DataBase Schema
-users - User information
-scans -Scan history and metadata
-findings- Detected secrets with locations

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
       

