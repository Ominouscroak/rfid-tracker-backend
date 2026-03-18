from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List

from fastapi.middleware.cors import CORSMiddleware

from database import engine, get_db
import models
import schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Raven Eye RFID Backend")

# ✅ CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Instruments
# -------------------------------

@app.post("/instruments", response_model=schemas.InstrumentSchema)
def create_instrument(instrument: schemas.InstrumentSchema, db: Session = Depends(get_db)):
    db_instrument = models.Instrument(**instrument.dict())
    db.add(db_instrument)
    db.commit()
    db.refresh(db_instrument)
    return db_instrument

@app.get("/instruments", response_model=List[schemas.InstrumentSchema])
def get_instruments(db: Session = Depends(get_db)):
    return db.query(models.Instrument).all()

# -------------------------------
# Scan
# -------------------------------

@app.post("/scan", response_model=schemas.ScanSchema)
def create_scan(scan: schemas.ScanSchema, db: Session = Depends(get_db)):

    room = scan.room.upper()

    new_scan = models.Scan(
        rfid_tag=scan.rfid_tag,
        room=room
    )
    db.add(new_scan)

    instrument = db.query(models.Instrument).filter_by(rfid_tag=scan.rfid_tag).first()

    if instrument:
        instrument.location = room

        if room == "OR":
            instrument.status = "In Use"
        elif room == "STERILIZATION":
            instrument.status = "Sterile"
        elif room == "STORAGE":
            instrument.status = "Available"

    db.commit()
    db.refresh(new_scan)
    return new_scan

@app.get("/scans")
def get_scans(db: Session = Depends(get_db)):
    scans = db.query(models.Scan).order_by(models.Scan.timestamp.desc()).all()

    result = []
    for scan in scans:
        instrument = db.query(models.Instrument).filter_by(rfid_tag=scan.rfid_tag).first()

        result.append({
            "id": scan.id,
            "rfid_tag": scan.rfid_tag,
            "instrument": instrument.name if instrument else "Unknown",
            "room": scan.room,
            "timestamp": scan.timestamp
        })

    return result

# -------------------------------
# Alerts
# -------------------------------

@app.get("/alerts")
def get_alerts():
    return [
        {
            "id": 1,
            "title": "Instrument Missing",
            "message": "Scalpel not returned",
            "type": "critical",
            "time": "2026-03-16T18:47:50Z"
        },
        {
            "id": 2,
            "title": "Instrument Outside OR",
            "message": "Forceps scanned in hallway",
            "type": "warning",
            "time": "2026-03-16T18:50:12Z"
        }
    ]
