import click
from src.secret_scanner.db.database import SessionLocal, init_db
from src.secret_scanner.scanner.scanner import scan_file
from src.secret_scanner.models.models import User, Scan, Finding

@click.group()
def cli():
    """Secret Scanner CLI"""
    pass

# -------------------
# Existing scan command
# -------------------
@cli.command()
@click.argument('target')
def scan(target):
    """Scan a file or directory for secrets"""
    click.echo(f"Scanning: {target}")
    
    # Initialize database
    init_db()
    db = SessionLocal()
    
    # Create a default user for this scan
    user = db.query(User).filter(User.username == "default_user").first()
    if not user:
        user = User(username="default_user")
        db.add(user)
        db.commit()
        db.refresh(user)
    
    # Create scan record
    scan_record = Scan(
        target_path=target,
        scan_type="file",
        user_id=user.id
    )
    db.add(scan_record)
    db.commit()
    db.refresh(scan_record)
    
    # Scan the file
    findings = scan_file(target)
    
    # Save findings to database
    for finding_data in findings:
        finding = Finding(
            scan_id=scan_record.id,
            file_path=finding_data['file_path'],
            line_number=finding_data['line_number'],
            secret_type=finding_data['secret_type'],
            secret_value=finding_data['secret_value']
        )
        db.add(finding)
    
    db.commit()
    
    # Display results
    if findings:
        click.echo(f"Found {len(findings)} potential secrets:")
        for finding in findings:
            click.echo(f"  - {finding['secret_type']}: {finding['secret_value']}")
        click.echo(f"Results saved to database (Scan ID: {scan_record.id})")
    else:
        click.echo("No secrets found!")
    
    db.close()


# -------------------
# Minimal CRUD commands
# -------------------

# --- User Commands ---
@cli.group()
def user():
    """Manage users"""
    pass

@user.command("create")
@click.argument("username")
def create_user(username):
    init_db()
    user = User.create(username=username)
    click.echo(f"User created: {user.username} (ID: {user.id})")

@user.command("list")
def list_users():
    init_db()
    users = User.get_all()
    if not users:
        click.echo("No users found.")
    for u in users:
        click.echo(f"{u.id}: {u.username} (Created {u.created_at})")

@user.command("delete")
@click.argument("user_id", type=int)
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
    scans = Scan.get_all()
    if not scans:
        click.echo("No scans found.")
    for s in scans:
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
    findings = Finding.get_all()
    if not findings:
        click.echo("No findings found.")
    for f in findings:
        click.echo(
            f"{f.id}: ScanID={f.scan_id}, File={f.file_path}, "
            f"Line={f.line_number}, Type={f.secret_type}"
        )

@finding.command("delete")
@click.argument("finding_id", type=int)
def delete_finding(finding_id):
    Finding.delete(finding_id)
    click.echo(f"Finding with ID {finding_id} deleted (if existed).")
