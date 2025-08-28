import sys
from src.secret_scanner.db.database import init_db
from src.secret_scanner.cli.cli import cli

def main():
    """Entry point for the Secret Scanner application."""
    # Ensure database tables exist
    init_db()

    # Pass CLI args through to click
    cli(prog_name="secret-scanner")

if __name__ == "__main__":
    main()
