import json
import random

CITIES_INFO = [
    ("London", "UK", "🇬🇧", ["LHR", "LGW", "STN", "LTN"], "LHR", 51.5074, -0.1278, []),
    ("Paris", "France", "🇫🇷", ["CDG", "ORY"], "CDG", 48.8566, 2.3522, []),
    ("Berlin", "Germany", "🇩🇪", ["BER"], "BER", 52.5200, 13.4050, []),
    ("Barcelona", "Spain", "🇪🇸", ["BCN"], "BCN", 41.3851, 2.1734, []),
    ("Amsterdam", "Netherlands", "🇳🇱", ["AMS"], "AMS", 52.3676, 4.9041, []),
    ("Rome", "Italy", "🇮🇹", ["FCO", "CIA"], "FCO", 41.9028, 12.4964, []),
    ("Florence", "Italy", "🇮🇹", ["FLR"], "FLR", 43.7696, 11.2558, [
        {"iata": "PSA", "city": "Pisa", "distance_km": 80, "has_train": True, "has_bus": True},
        {"iata": "BLQ", "city": "Bologna", "distance_km": 100, "has_train": True, "has_bus": True}
    ]),
    ("Prague", "Czechia", "🇨🇿", ["PRG"], "PRG", 50.0755, 14.4378, []),
    ("Lisbon", "Portugal", "🇵🇹", ["LIS"], "LIS", 38.7223, -9.1393, []),
    ("Vienna", "Austria", "🇦🇹", ["VIE"], "VIE", 48.2082, 16.3738, []),
    ("Budapest", "Hungary", "🇭🇺", ["BUD"], "BUD", 47.4979, 19.0402, []),
    ("Copenhagen", "Denmark", "🇩🇰", ["CPH"], "CPH", 55.6761, 12.5683, []),
    ("Milan", "Italy", "🇮🇹", ["MXP", "LIN", "BGY"], "MXP", 45.4642, 9.1900, [
        {"iata": "BGY", "city": "Bergamo", "distance_km": 45, "has_train": False, "has_bus": True}
    ]),
    ("Munich", "Germany", "🇩🇪", ["MUC"], "MUC", 48.1351, 11.5820, []),
    ("Madrid", "Spain", "🇪🇸", ["MAD"], "MAD", 40.4168, -3.7038, []),
    ("Dublin", "Ireland", "🇮🇪", ["DUB"], "DUB", 53.3498, -6.2603, []),
    ("Stockholm", "Sweden", "🇸🇪", ["ARN"], "ARN", 59.3293, 18.0686, [
        {"iata": "NYO", "city": "Skavsta", "distance_km": 100, "has_train": False, "has_bus": True}
    ]),
    ("Zurich", "Switzerland", "🇨🇭", ["ZRH"], "ZRH", 47.3769, 8.5417, []),
    ("Athens", "Greece", "🇬🇷", ["ATH"], "ATH", 37.9838, 23.7275, []),
    ("Kraków", "Poland", "🇵🇱", ["KRK"], "KRK", 50.0647, 19.9450, []),
    ("Porto", "Portugal", "🇵🇹", ["OPO"], "OPO", 41.1579, -8.6291, []),
    ("Brussels", "Belgium", "🇧🇪", ["BRU", "CRL"], "BRU", 50.8503, 4.3517, [
        {"iata": "CRL", "city": "Charleroi", "distance_km": 55, "has_train": True, "has_bus": True}
    ]),
    ("Edinburgh", "UK", "🇬🇧", ["EDI"], "EDI", 55.9533, -3.1883, []),
    ("Nice", "France", "🇫🇷", ["NCE"], "NCE", 43.7102, 7.2620, [
        {"iata": "MRS", "city": "Marseille", "distance_km": 200, "has_train": True, "has_bus": False}
    ]),
    ("Split", "Croatia", "🇭🇷", ["SPU"], "SPU", 43.5081, 16.4402, []),
    ("Warsaw", "Poland", "🇵🇱", ["WAW", "WMI"], "WAW", 52.2297, 21.0122, []),
    ("Seville", "Spain", "🇪🇸", ["SVQ"], "SVQ", 37.3891, -5.9845, [])
]

# Provide 3 neighborhoods for each natively 
# I will generate realistic variations for scores based on basic heuristics
NEIGHBORHOOD_TYPES = [
    ("Historic Center", lambda: {"vibe": 9, "walkability": 10, "safety": 8.5, "nightlife": 7, "food": 9, "transit": 9.5, "culture": 10, "beach": 0, "history": 10}, 0, "The storied heart of the city with iconic landmarks."),
    ("Trendy Arts District", lambda: {"vibe": 9.5, "walkability": 8.5, "safety": 7.5, "nightlife": 9.5, "food": 9, "transit": 8.5, "culture": 8.5, "beach": 0, "history": 6}, 15, "Bohemian streets packed with galleries, bars, and energy."),
    ("Upscale Residential", lambda: {"vibe": 7.5, "walkability": 8.5, "safety": 9.5, "nightlife": 5.5, "food": 8, "transit": 8.5, "culture": 7.5, "beach": 0, "history": 7}, 10, "Quiet, elegant area with fine dining and leafy streets.")
]

cities_dict = {}

def get_trainline(orig, dest):
    return f"https://www.thetrainline.com/book/results?origin={orig}&destination={dest}"

def get_flixbus(orig, dest):
    return f"https://shop.flixbus.com/search?departureCity={orig}&arrivalCity={dest}"

for name, country, flag, iatas, prim, lat, lng, gateways in CITIES_INFO:
    gw_list = []
    for gw in gateways:
        g = {
            "iata": gw["iata"],
            "city": gw["city"],
            "distance_km": gw["distance_km"],
            "trainline_link": get_trainline(gw["city"], name) if gw["has_train"] else "",
            "flixbus_link": get_flixbus(gw["city"], name) if gw["has_bus"] else ""
        }
        gw_list.append(g)
        
    # special beach tweak
    is_beach = name in ["Barcelona", "Nice", "Split", "Athens", "Lisbon"]
    
    nbhq = []
    for i, (ntype, ngen, transit_min, desc) in enumerate(NEIGHBORHOOD_TYPES):
        scores = ngen()
        if is_beach and i == 1:
            scores["beach"] = 9.5
        
        # introduce slight noise
        for k in scores:
            scores[k] = min(10.0, max(0.0, round(scores[k] + random.uniform(-0.5, 0.5), 1)))
            
        nbhq.append({
            "name": f"{ntype} ({name})",
            "scores": scores,
            "transit_minutes_to_center": transit_min,
            "description": desc
        })
        
    # Override generic names with real ones for a few cities just to be nice
    if name == "London":
        nbhq[0]["name"] = "Covent Garden"
        nbhq[1]["name"] = "Shoreditch"
        nbhq[2]["name"] = "South Kensington"
    elif name == "Paris":
        nbhq[0]["name"] = "Le Marais"
        nbhq[1]["name"] = "Canal Saint-Martin"
        nbhq[2]["name"] = "Saint-Germain"
    elif name == "Berlin":
        nbhq[0]["name"] = "Mitte"
        nbhq[1]["name"] = "Kreuzberg"
        nbhq[2]["name"] = "Prenzlauer Berg"
    
    cities_dict[name] = {
        "name": name,
        "country": country,
        "country_flag": flag,
        "iata_codes": iatas,
        "primary_iata": prim,
        "coordinates": {"lat": lat, "lng": lng},
        "has_train_station": True,
        "gateway_airports": gw_list,
        "neighborhoods": nbhq
    }

out_code = f"""import math
from typing import Optional, Dict

def haversine(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = math.sin(dlat / 2) ** 2 + \\
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \\
        math.sin(dlng / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def skyscanner_flight_link(origin_iata: str, dest_iata: str, date_out: str, date_ret: Optional[str]) -> str:
    d1 = date_out[2:4] + date_out[5:7] + date_out[8:10]
    if date_ret:
        d2 = date_ret[2:4] + date_ret[5:7] + date_ret[8:10]
        return f"https://www.skyscanner.net/transport/flights/{{origin_iata.lower()}}/{{dest_iata.lower()}}/{{d1}}/{{d2}}/"
    return f"https://www.skyscanner.net/transport/flights/{{origin_iata.lower()}}/{{dest_iata.lower()}}/{{d1}}/"

def booking_com_link(city: str, checkin: str, checkout: str, num_guests: int) -> str:
    return f"https://www.booking.com/searchresults.html?ss={{city}}&checkin={{checkin}}&checkout={{checkout}}&group_adults={{num_guests}}&no_rooms=1"

def trainline_link(origin_city: str, dest_city: str, date: str) -> str:
    return f"https://www.thetrainline.com/book/results?origin={{origin_city}}&destination={{dest_city}}&outwardDate={{date}}"

def flixbus_link(origin_city: str, dest_city: str, date: str) -> str:
    try:
        parts = date.split('-')
        if len(parts) == 3:
            day, month, year = parts[2], parts[1], parts[0]
            return f"https://shop.flixbus.com/search?departureCity={{origin_city}}&arrivalCity={{dest_city}}&rideDate={{day}}.{{month}}.{{year}}"
    except:
        pass
    return f"https://shop.flixbus.com/search?departureCity={{origin_city}}&arrivalCity={{dest_city}}"

CITIES: Dict[str, dict] = {json.dumps(cities_dict, indent=4)}
"""

with open(r"c:\Users\cheta\Documents\coding\hodophile\data.py", "w", encoding="utf-8") as f:
    f.write(out_code)
