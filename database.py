# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# -------------------------------
# PostgreSQL connection string
# -------------------------------
DATABASE_URL = "postgresql://raven:raven123@localhost/raven_eye"

# -------------------------------
# Create engine and session
# -------------------------------
engine = create_engine(
    DATABASE_URL,
    echo=True  # Set to False if you don't want SQL logs
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# -------------------------------
# Dependency for FastAPI
# -------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
