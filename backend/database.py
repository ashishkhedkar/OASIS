from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Use sqlite for local development/testing initially, can swap to MySQL later
SQLALCHEMY_DATABASE_URL = "sqlite:///./oasis.db"
# SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://user:password@localhost/oasis"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
