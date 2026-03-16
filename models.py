# models.py
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# -------------------------------
# Instrument Table
# -------------------------------
class Instrument(Base):
    __tablename__ = "instruments"

    id = Column(Integer, primary_key=True, index=True)
    rfid_tag = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    status = Column(String, nullable=False)
    location = Column(String, nullable=False)

# -------------------------------
# Scan Table
# -------------------------------
class Scan(Base):
    __tablename__ = "scans"

    id = Column(Integer, primary_key=True, index=True)
    rfid_tag = Column(String, nullable=False)
    room = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
