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