from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# -------------------
# Database config
# -------------------
# Using a STRING constant for the database URL - SQLite in this case
DATABASE_URL = "sqlite:///./secret_scanner.db"

# Creating the database ENGINE - this is the main connection point to the database
# The engine manages connection pooling and translates Python to SQL commands
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Required for SQLite to work in multi-threaded apps
)

# Creating a SESSION FACTORY - this generates new database sessions
# Sessions are like conversations with the database where we can execute queries
SessionLocal = sessionmaker(
    autocommit=False,    # Don't auto-commit after every operation
    autoflush=False,     # Don't auto-flush changes to database
    bind=engine          # Bind this session maker to our engine
)

# BASE CLASS for all our SQLAlchemy models - this is the foundation
# All our model classes will inherit from this Base class
Base = declarative_base()

# -------------------
# Init + helpers
# -------------------
def init_db():
    """Create tables if they don't exist."""
    # Importing models here to ensure they're registered with Base before table creation
    import src.secret_scanner.models.models  # ensure models are imported
    
    # This creates ALL tables defined by models that inherit from Base
    # metadata.create_all() is smart - it only creates tables that don't exist
    Base.metadata.create_all(bind=engine)

def get_db():
    """Provide a database session (for use in context managers)."""
    # Creating a new session from our session factory
    db = SessionLocal()
    try:
        # Yielding the session - this makes it work with FastAPI's dependency system
        # The session stays open while being used
        yield db
    finally:
        # This block ALWAYS runs, ensuring we close the session even if errors occur
        db.close()  # Clean up the session and return connection to pool

def reset_db():
    """Drop and recreate all tables (for development/testing)."""
    # First drop ALL tables - be careful, this destroys all data!
    Base.metadata.drop_all(bind=engine)
    # Then recreate them fresh - useful for testing or development resets
    Base.metadata.create_all(bind=engine)