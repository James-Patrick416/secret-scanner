from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# -------------------
# Database config
# -------------------
DATABASE_URL = "sqlite:///./secret_scanner.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# -------------------
# Init + helpers
# -------------------
def init_db():
    """Create tables if they don't exist."""
    import src.secret_scanner.models.models  # ensure models are imported
    Base.metadata.create_all(bind=engine)

def get_db():
    """Provide a database session (for use in context managers)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def reset_db():
    """Drop and recreate all tables (for development/testing)."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
