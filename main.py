# main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List

from database import engine, get_db
import models
import schemas

# Create all tables if they don't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Raven Eye RFID Backend")

# -------------------------------
# Instruments Endpoints
# -------------------------------

@app.post("/instruments", response_model=schemas.InstrumentSchema)
def create_instrument(instrument: schemas.InstrumentSchema, db: Session = Depends(get_db)):
    db_instrument = models.Instrument(
        rfid_tag=instrument.rfid_tag,
        name=instrument.name,
        status=instrument.status,
        location=instrument.location
    )
    db.add(db_instrument)
    db.commit()
    db.refresh(db_instrument)
    return db_instrument

@app.post("/instruments/bulk", response_model=List[schemas.InstrumentSchema])
def create_instruments_bulk(data: schemas.InstrumentListSchema, db: Session = Depends(get_db)):
    created = []
    for item in data.instruments:
        instrument = models.Instrument(
            rfid_tag=item.rfid_tag,
            name=item.name,
            status=item.status,
            location=item.location
        )
        db.add(instrument)
        created.append(instrument)
    db.commit()
    return created

@app.get("/instruments", response_model=List[schemas.InstrumentSchema])
def get_instruments(db: Session = Depends(get_db)):
    return db.query(models.Instrument).all()

# -------------------------------
# Scan Endpoints
# -------------------------------

@app.post("/scan", response_model=schemas.ScanSchema)
def create_scan(scan: schemas.ScanSchema, db: Session = Depends(get_db)):
    # Log the scan
    new_scan = models.Scan(
        rfid_tag=scan.rfid_tag,
        room=scan.room
    )
    db.add(new_scan)

    # Update instrument location and status
    instrument = db.query(models.Instrument).filter_by(rfid_tag=scan.rfid_tag).first()
    if instrument:
        instrument.location = scan.room
        if scan.room.lower() == "or":
            instrument.status = "In Use"
        elif scan.room.lower() == "sterilization":
            instrument.status = "Sterile"
        elif scan.room.lower() == "storage":
            instrument.status = "Available"

    db.commit()
    db.refresh(new_scan)
    return new_scan

@app.get("/scans", response_model=List[schemas.ScanSchema])
def get_scans(db: Session = Depends(get_db)):
    return db.query(models.Scan).order_by(models.Scan.timestamp.desc()).all()

# -------------------------------
# Alerts Endpoint (Placeholder)
# -------------------------------

@app.get("/alerts")
def get_alerts(db: Session = Depends(get_db)):
    # For now, return static example alerts
    return [
        {"id": 1, "title": "Instrument Missing", "message": "Scalpel not returned", "type": "critical", "time": "2026-03-16T18:47:50Z"},
        {"id": 2, "title": "Instrument Outside OR", "message": "Forceps scanned in hallway", "type": "warning", "time": "2026-03-16T18:50:12Z"}
    ]
