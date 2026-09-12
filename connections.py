from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from pathlib import Path
import os


# Get the directory where connection.py is located
BASE_DIR = Path(__file__).resolve().parent

# Load .env from the project directory
ENV_FILE = BASE_DIR / ".env"

print("Loading .env from:", ENV_FILE)

load_dotenv(ENV_FILE)

# Get database URL
DATABASE_URL = os.getenv("DATABASE_URL")

print("DATABASE_URL loaded:", DATABASE_URL is not None)

if not DATABASE_URL:
    raise RuntimeError(
        f"DATABASE_URL is not set. Make sure .env exists at: {ENV_FILE}"
    )


# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)


# Create database session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Base class for SQLAlchemy models
Base = declarative_base()
