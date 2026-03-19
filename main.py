from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from database import engine, get_db
import models
import schemas
from datetime import datetime

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Raven Eye RFID Backend")

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Room mapping for frontend
# -------------------------------
ROOM_NAMES = {
    "OR": "Operating Room",
    "STORAGE": "Storage",
    "STERILIZATION": "Sterilization"
}

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
    new_scan = models.Scan(rfid_tag=scan.rfid_tag, room=room)
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
            "room": ROOM_NAMES.get(scan.room, scan.room),
            "timestamp": scan.timestamp
        })
    return result

# -------------------------------
# Alerts
# -------------------------------
@app.get("/alerts")
def get_alerts(db: Session = Depends(get_db)):
    alerts = []
    instruments = db.query(models.Instrument).all()
    for instrument in instruments:
        if instrument.status == "Missing":
            alerts.append({
                "id": instrument.id,
                "title": "Instrument Missing",
                "message": f"{instrument.name} not returned",
                "type": "critical",
                "time": datetime.utcnow().isoformat() + "Z"
            })
        if instrument.status == "In Use" and instrument.location != "OR":
            alerts.append({
                "id": instrument.id + 1000,
                "title": "Instrument Outside OR",
                "message": f"{instrument.name} scanned in {instrument.location}",
                "type": "warning",
                "time": datetime.utcnow().isoformat() + "Z"
            })
    return alerts
