import urllib.request
import json

req = urllib.request.Request(
    'http://localhost:8345/optimize',
    data=json.dumps({
        'travelers': [
            {'name': 'Alice', 'origin': 'London', 'max_travel_hours': 10, 'max_stops': 1},
            {'name': 'Bob', 'origin': 'Berlin', 'max_travel_hours': 10, 'max_stops': 1}
        ],
        'settings': {
            'earliest_departure': '2026-03-29',
            'latest_return': '2026-04-01',
            'duration_nights': 3,
            'destinations': ['Warsaw']
        }
    }).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)
try:
    with urllib.request.urlopen(req, timeout=120) as response:
        data = json.loads(response.read().decode('utf-8'))
        print(json.dumps(data, indent=2, default=str)[:2000])
except Exception as e:
    body = e.read().decode('utf-8') if hasattr(e, 'read') else str(e)
    print('Error:', body[:500])
