from sqlalchemy.orm import Session
import models


def get_instruments(db: Session):
    return db.query(models.Instrument).all()


def get_scans(db: Session):
    return db.query(models.Scan).all()


def get_alerts(db: Session):
    return db.query(models.Alert).all()


def create_scan(db: Session, rfid_tag: str, room: str):
    scan = models.Scan(rfid_tag=rfid_tag, room=room)
    db.add(scan)
    db.commit()
    db.refresh(scan)
    return scan
