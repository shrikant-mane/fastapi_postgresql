from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# dont use this type of connection pool at production
DATABASE_URL = "postgresql://<user>:<password>@<host>:<port>/<db_name>"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)

Base = declarative_base()


