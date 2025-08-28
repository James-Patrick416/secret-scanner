from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    scans = relationship('Scan', back_populates='user')

class Scan(Base):
    __tablename__ = 'scans'
    id = Column(Integer, primary_key=True)
    target_path = Column(String, nullable=False)
    scan_type = Column(String, nullable=False)
    status = Column(String, default='completed')
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='scans')
    findings = relationship('Finding', back_populates='scan')

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from src.secret_scanner.db.database import SessionLocal

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    scans = relationship('Scan', back_populates='user')

    # --- Minimal ORM helpers ---
    @classmethod
    def create(cls, username):
        db = SessionLocal()
        user = cls(username=username)
        db.add(user)
        db.commit()
        db.refresh(user)
        db.close()
        return user

    @classmethod
    def get_all(cls):
        db = SessionLocal()
        users = db.query(cls).all()
        db.close()
        return users

    @classmethod
    def find_by_id(cls, user_id):
        db = SessionLocal()
        user = db.query(cls).filter_by(id=user_id).first()
        db.close()
        return user

    @classmethod
    def delete(cls, user_id):
        db = SessionLocal()
        user = db.query(cls).filter_by(id=user_id).first()
        if user:
            db.delete(user)
            db.commit()
        db.close()


class Scan(Base):
    __tablename__ = 'scans'
    id = Column(Integer, primary_key=True)
    target_path = Column(String, nullable=False)
    scan_type = Column(String, nullable=False)
    status = Column(String, default='completed')
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='scans')
    findings = relationship('Finding', back_populates='scan')

    # --- Minimal ORM helpers ---
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


class Finding(Base):
    __tablename__ = 'findings'
    id = Column(Integer, primary_key=True)
    scan_id = Column(Integer, ForeignKey('scans.id'))
    file_path = Column(String, nullable=False)
    line_number = Column(Integer)
    secret_type = Column(String, nullable=False)
    secret_value = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    scan = relationship('Scan', back_populates='findings')

    # --- Minimal ORM helpers ---
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
