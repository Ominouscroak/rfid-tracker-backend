import requests
import random
import time
from datetime import datetime

# -------------------------------
# Backend URL
# -------------------------------
BASE_URL = "http://127.0.0.1:8000"

# -------------------------------
# Dummy instruments (RFID tags)
# -------------------------------
instruments = [
    {"rfid_tag": "RFID001", "name": "Scalpel", "location": "Tray A"},
    {"rfid_tag": "RFID002", "name": "Forceps", "location": "Operating Room 1"},
    {"rfid_tag": "RFID003", "name": "Retractor", "location": "Tray B"},
    {"rfid_tag": "RFID004", "name": "Clamp", "location": "Tray C"},
    {"rfid_tag": "RFID005", "name": "Scissors", "location": "Tray A"}
]

# -------------------------------
# Simulation loop
# -------------------------------
def simulate_scan():
    while True:
        # Pick a random instrument
        instrument = random.choice(instruments)

        # Create scan payload
        payload = {
            "rfid_tag": instrument["rfid_tag"],
            "instrument": instrument["name"],
            "room": instrument["location"],
            "timestamp": datetime.utcnow().isoformat()
        }

        try:
            response = requests.post(f"{BASE_URL}/scan", json=payload)
            if response.status_code == 200:
                print(f"Scanned: {instrument['name']} at {instrument['location']}")
            else:
                print(f"Error posting scan: {response.status_code} {response.text}")
        except Exception as e:
            print(f"Connection error: {e}")

        # Wait 2-5 seconds before next scan
        time.sleep(random.randint(2, 5))


if __name__ == "__main__":
    simulate_scan()
