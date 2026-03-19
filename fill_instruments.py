from sqlalchemy.orm import Session
from database import SessionLocal
import models

# 15 Instruments
instruments = [
    {"rfid_tag": "RFID001", "name": "Scalpel", "status": "Available", "location": "STORAGE"},
    {"rfid_tag": "RFID002", "name": "Forceps", "status": "Available", "location": "STORAGE"},
    {"rfid_tag": "RFID003", "name": "Retractor", "status": "Available", "location": "STORAGE"},
    {"rfid_tag": "RFID004", "name": "Clamp", "status": "Available", "location": "STORAGE"},
    {"rfid_tag": "RFID005", "name": "Scissors", "status": "Available", "location": "STORAGE"},
    {"rfid_tag": "RFID006", "name": "Tweezers", "status": "Available", "location": "STORAGE"},
    {"rfid_tag": "RFID007", "name": "Hemostat", "status": "Available", "location": "STORAGE"},
    {"rfid_tag": "RFID008", "name": "Needle Holder", "status": "Available", "location": "STORAGE"},
    {"rfid_tag": "RFID009", "name": "Retractor Small", "status": "Available", "location": "STORAGE"},
    {"rfid_tag": "RFID010", "name": "Retractor Large", "status": "Available", "location": "STORAGE"},
    {"rfid_tag": "RFID011", "name": "Suction", "status": "Available", "location": "STORAGE"},
    {"rfid_tag": "RFID012", "name": "Speculum", "status": "Available", "location": "STORAGE"},
    {"rfid_tag": "RFID013", "name": "Scalpel Handle", "status": "Available", "location": "STORAGE"},
    {"rfid_tag": "RFID014", "name": "Forceps Small", "status": "Available", "location": "STORAGE"},
    {"rfid_tag": "RFID015", "name": "Forceps Large", "status": "Available", "location": "STORAGE"},
]

def main():
    db: Session = SessionLocal()
    for ins in instruments:
        existing = db.query(models.Instrument).filter_by(rfid_tag=ins["rfid_tag"]).first()
        if not existing:
            db_ins = models.Instrument(**ins)
            db.add(db_ins)
    db.commit()
    db.close()
    print("Database prefilled with 15 instruments.")

if __name__ == "__main__":
    main()
