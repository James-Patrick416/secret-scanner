from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.secret_scanner.models.models import Base

engine = create_engine('sqlite:///secret_scanner.db')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)