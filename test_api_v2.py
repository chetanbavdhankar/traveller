import requests
import json
import sys

# 1. Start Server
PORT = 8345
base_url = f"http://localhost:{PORT}"

print(f"Testing 1 traveler from HELSINKI to OSLO with Request Deduplication")

req_payload = {
    "travelers": [
        {
            "name": "SoloTraveler",
            "origin": "Helsinki",
            "not_before": "06:00",
            "arrive_by": "23:59",
            "max_travel_hours": 12,
            "max_stops": 1
        },
        {
            "name": "DuplicateTraveler",
            "origin": "Helsinki",
            "not_before": "06:00",
            "arrive_by": "23:59",
            "max_travel_hours": 12,
            "max_stops": 1
        }
    ],
    "settings": {
        "earliest_departure": "2026-05-10",
        "latest_return": "2026-05-15",
        "duration_nights": 3,
        "destinations": ["Oslo"]
    }
}

try:
    print(f"POST {base_url}/optimize")
    response = requests.post(f"{base_url}/optimize", json=req_payload)
    if response.status_code == 200:
        data = response.json()
        print("SUCCESS! Data:")
        print(json.dumps(data, indent=2))
        
        recs = data.get("recommendations", [])
        if recs:
            t_opts = recs[0].get("travelers", [])
            print(f"Found {len(t_opts)} traveler route options in recommendation.")
            if len(t_opts) == 2:
                print("Deduplication successfully mapped both travelers!")
    else:
        print(f"FAILED (Status {response.status_code})")
        print(response.text)
        sys.exit(1)
except Exception as e:
    print(f"Connection Exception: {e}")
    sys.exit(1)

print("\nAll tests passed!")
