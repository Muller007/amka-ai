"""
AMKA — Database Configuration
SQLAlchemy database setup and session management.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
from models import Base

load_dotenv()

# Get database URL from environment or use default
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///amka.db')

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={'check_same_thread': False} if 'sqlite' in DATABASE_URL else {},
    echo=False  # Set to True for SQL logging
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize the database (create all tables)."""
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized successfully")


def get_session() -> Session:
    """Get a new database session."""
    return SessionLocal()


def close_session(session: Session):
    """Close a database session."""
    if session:
        session.close()


if __name__ == '__main__':
    # Initialize the database when this script runs
    init_db()