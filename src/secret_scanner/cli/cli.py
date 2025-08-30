import click
from src.secret_scanner.db.database import SessionLocal, init_db
from src.secret_scanner.scanner.scanner import scan_file
from src.secret_scanner.models.models import User, Scan, Finding

# Creating a Click GROUP - this is the main entry point for our CLI
# Groups allow us to organize commands into hierarchies
@click.group()
def cli():
    """Secret Scanner CLI"""
    pass

# -------------------
# Existing scan command
# -------------------
@cli.command()  # This decorator makes it a direct subcommand of the main group
@click.argument('target')  # Defines a required command-line argument
def scan(target):
    """Scan a file or directory for secrets"""
    click.echo(f"Scanning: {target}")
    
    # Initialize database - ensures tables exist before we try to use them
    init_db()
    
    # Create a database SESSION - this is our connection to the database
    db = SessionLocal()
    
    # Check if default user exists, create if not - using SQLAlchemy query
    # This shows how we use the ORM to interact with the database
    user = db.query(User).filter(User.username == "default_user").first()
    if not user:
        user = User(username="default_user")
        db.add(user)        # Add to session
        db.commit()         # Save to database
        db.refresh(user)    # Refresh with database-generated ID
    
    # Create a new SCAN record using the ORM model
    scan_record = Scan(
        target_path=target,
        scan_type="file",
        user_id=user.id  # Using the Foreign Key relationship
    )
    db.add(scan_record)
    db.commit()
    db.refresh(scan_record)  # Now scan_record has its database ID
    
    # Actually scan the file using our scanner module
    # This returns a LIST of finding dictionaries
    findings = scan_file(target)
    
    # Process each finding and save to database
    for finding_data in findings:  # Iterating through the list of findings
        # Create a Finding object from the dictionary data
        finding = Finding(
            scan_id=scan_record.id,  # Foreign Key to the scan
            file_path=finding_data['file_path'],
            line_number=finding_data['line_number'],
            secret_type=finding_data['secret_type'],
            secret_value=finding_data['secret_value']
        )
        db.add(finding)  # Add each finding to the session
    
    db.commit()  # Save all findings at once
    
    # Display results to the user
    if findings:
        click.echo(f"Found {len(findings)} potential secrets:")
        for finding in findings:  # Another list iteration for display
            click.echo(f"  - {finding['secret_type']}: {finding['secret_value']}")
        click.echo(f"Results saved to database (Scan ID: {scan_record.id})")
    else:
        click.echo("No secrets found!")
    
    db.close()  # Always clean up our database connection


# -------------------
# Minimal CRUD commands
# -------------------

# --- User Commands ---
# Creating a SUBGROUP for user-related commands
@cli.group()
def user():
    """Manage users"""
    pass

# 'user create' command - demonstrates CREATE operation
@user.command("create")
@click.argument("username")
def create_user(username):
    init_db()
    # Using our model's class method for clean abstraction
    user = User.create(username=username)
    click.echo(f"User created: {user.username} (ID: {user.id})")

# 'user list' command - demonstrates READ operation
@user.command("list")
def list_users():
    init_db()
    users = User.get_all()  # Returns a LIST of User objects
    if not users:
        click.echo("No users found.")
    for u in users:  # Iterating through the list
        click.echo(f"{u.id}: {u.username} (Created {u.created_at})")

# 'user delete' command - demonstrates DELETE operation
@user.command("delete")
@click.argument("user_id", type=int)  # Type conversion for safety
def delete_user(user_id):
    User.delete(user_id)
    click.echo(f"User with ID {user_id} deleted (if existed).")


# --- Scan Commands ---
@cli.group()
def scanmgr():
    """Manage scans"""
    pass

@scanmgr.command("list")
def list_scans():
    scans = Scan.get_all()  # LIST of Scan objects
    if not scans:
        click.echo("No scans found.")
    for s in scans:  # List iteration with formatted output
        click.echo(f"{s.id}: Path={s.target_path}, UserID={s.user_id}, Status={s.status}")

@scanmgr.command("delete")
@click.argument("scan_id", type=int)
def delete_scan(scan_id):
    Scan.delete(scan_id)
    click.echo(f"Scan with ID {scan_id} deleted (if existed).")


# --- Finding Commands ---
@cli.group()
def finding():
    """Manage findings"""
    pass

@finding.command("list")
def list_findings():
    findings = Finding.get_all()  # LIST of Finding objects
    if not findings:
        click.echo("No findings found.")
    for f in findings:  # Complex string formatting for clear output
        click.echo(
            f"{f.id}: ScanID={f.scan_id}, File={f.file_path}, "
            f"Line={f.line_number}, Type={f.secret_type}"
        )

@finding.command("delete")
@click.argument("finding_id", type=int)
def delete_finding(finding_id):
    Finding.delete(finding_id)
    click.echo(f"Finding with ID {finding_id} deleted (if existed).")