import click
from src.secret_scanner.db.database import SessionLocal, init_db
from src.secret_scanner.scanner.scanner import scan_file
from src.secret_scanner.models.models import User, Scan, Finding

@click.group()
def cli():
    """Secret Scanner CLI"""
    pass

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