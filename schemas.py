# schemas.py
from pydantic import BaseModel
from typing import List

# -------------------------------
# Instrument Schemas
# -------------------------------

class InstrumentSchema(BaseModel):
    rfid_tag: str
    name: str
    status: str
    location: str

    class Config:
        orm_mode = True

class InstrumentListSchema(BaseModel):
    instruments: List[InstrumentSchema]

# -------------------------------
# Scan Schemas
# -------------------------------

class ScanSchema(BaseModel):
    rfid_tag: str
    room: str

    class Config:
        orm_mode = True

# -------------------------------
# Alert Schema (optional for future)
# -------------------------------

class AlertSchema(BaseModel):
    id: int
    title: str
    message: str
    type: str
    time: str
