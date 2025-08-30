# --- SQLAlchemy imports for defining models ---
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from src.secret_scanner.db.database import SessionLocal

# Base class for all models
Base = declarative_base()


# --- USER MODEL ---
class User(Base):
    __tablename__ = 'users'   # maps this class to "users" table in the database

    # Columns = table fields
    id = Column(Integer, primary_key=True)                       # Primary Key
    username = Column(String, unique=True, nullable=False)       # Unique username
    created_at = Column(DateTime, default=datetime.utcnow)       # Auto timestamp
    scans = relationship('Scan', back_populates='user')          # One-to-many relation: User -> Scans

    # --- ORM Helper methods ---
    # These methods show SQLAlchemy CRUD operations (Create, Read, Delete)
    @classmethod
    def create(cls, username):
        db = SessionLocal()                  # start DB session
        user = cls(username=username)        # create User object
        db.add(user)                         # add to DB session
        db.commit()                          # save changes
        db.refresh(user)                     # refresh with DB state
        db.close()
        return user

    @classmethod
    def get_all(cls):
        db = SessionLocal()
        users = db.query(cls).all()          # SELECT * FROM users
        db.close()
        return users

    @classmethod
    def find_by_id(cls, user_id):
        db = SessionLocal()
        user = db.query(cls).filter_by(id=user_id).first()   # SELECT * WHERE id = ?
        db.close()
        return user

    @classmethod
    def delete(cls, user_id):
        db = SessionLocal()
        user = db.query(cls).filter_by(id=user_id).first()
        if user:
            db.delete(user)   # DELETE user
            db.commit()
        db.close()


# --- SCAN MODEL ---
class Scan(Base):
    __tablename__ = 'scans'   # maps to "scans" table

    id = Column(Integer, primary_key=True)
    target_path = Column(String, nullable=False)    # Path scanned
    scan_type = Column(String, nullable=False)      # e.g. "secrets", "vulnerabilities"
    status = Column(String, default='completed')    # scan status
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'))   # Foreign Key → users.id
    user = relationship('User', back_populates='scans') # Many-to-one: Scan -> User
    findings = relationship('Finding', back_populates='scan') # One-to-many: Scan -> Findings

    # CRUD helper methods
    @classmethod
    def create(cls, target_path, scan_type, user_id):
        db = SessionLocal()
        scan = cls(target_path=target_path, scan_type=scan_type, user_id=user_id)
        db.add(scan)
        db.commit()
        db.refresh(scan)
        db.close()
        return scan

    @classmethod
    def get_all(cls):
        db = SessionLocal()
        scans = db.query(cls).all()
        db.close()
        return scans

    @classmethod
    def find_by_id(cls, scan_id):
        db = SessionLocal()
        scan = db.query(cls).filter_by(id=scan_id).first()
        db.close()
        return scan

    @classmethod
    def delete(cls, scan_id):
        db = SessionLocal()
        scan = db.query(cls).filter_by(id=scan_id).first()
        if scan:
            db.delete(scan)
            db.commit()
        db.close()


# --- FINDING MODEL ---
class Finding(Base):
    __tablename__ = 'findings'   # maps to "findings" table

    id = Column(Integer, primary_key=True)
    scan_id = Column(Integer, ForeignKey('scans.id'))   # Foreign Key → scans.id
    file_path = Column(String, nullable=False)          # file where secret found
    line_number = Column(Integer)                       # line number in file
    secret_type = Column(String, nullable=False)        # e.g. "API Key"
    secret_value = Column(String, nullable=False)       # the actual secret
    created_at = Column(DateTime, default=datetime.utcnow)
    scan = relationship('Scan', back_populates='findings') # Many-to-one: Finding -> Scan

    # CRUD helper methods
    @classmethod
    def create(cls, scan_id, file_path, line_number, secret_type, secret_value):
        db = SessionLocal()
        finding = cls(
            scan_id=scan_id,
            file_path=file_path,
            line_number=line_number,
            secret_type=secret_type,
            secret_value=secret_value
        )
        db.add(finding)
        db.commit()
        db.refresh(finding)
        db.close()
        return finding

    @classmethod
    def get_all(cls):
        db = SessionLocal()
        findings = db.query(cls).all()
        db.close()
        return findings

    @classmethod
    def find_by_id(cls, finding_id):
        db = SessionLocal()
        finding = db.query(cls).filter_by(id=finding_id).first()
        db.close()
        return finding

    @classmethod
    def delete(cls, finding_id):
        db = SessionLocal()
        finding = db.query(cls).filter_by(id=finding_id).first()
        if finding:
            db.delete(finding)
            db.commit()
        db.close()
