import math
from typing import Optional, Dict

def haversine(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = math.sin(dlat / 2) ** 2 + \
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
        math.sin(dlng / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def skyscanner_flight_link(origin_iata: str, dest_iata: str, date_out: str, date_ret: Optional[str]) -> str:
    d1 = date_out[2:4] + date_out[5:7] + date_out[8:10]
    if date_ret:
        d2 = date_ret[2:4] + date_ret[5:7] + date_ret[8:10]
        return f"https://www.skyscanner.net/transport/flights/{origin_iata.lower()}/{dest_iata.lower()}/{d1}/{d2}/"
    return f"https://www.skyscanner.net/transport/flights/{origin_iata.lower()}/{dest_iata.lower()}/{d1}/"

def booking_com_link(city: str, checkin: str, checkout: str, num_guests: int) -> str:
    return f"https://www.booking.com/searchresults.html?ss={city}&checkin={checkin}&checkout={checkout}&group_adults={num_guests}&no_rooms=1"

def trainline_link(origin_city: str, dest_city: str, date: str) -> str:
    return f"https://www.thetrainline.com/book/results?origin={origin_city}&destination={dest_city}&outwardDate={date}"

def flixbus_link(origin_city: str, dest_city: str, date: str) -> str:
    try:
        parts = date.split('-')
        if len(parts) == 3:
            day, month, year = parts[2], parts[1], parts[0]
            return f"https://shop.flixbus.com/search?departureCity={origin_city}&arrivalCity={dest_city}&rideDate={day}.{month}.{year}"
    except:
        pass
    return f"https://shop.flixbus.com/search?departureCity={origin_city}&arrivalCity={dest_city}"

CITIES: Dict[str, dict] = {
    "London": {
        "name": "London",
        "country": "UK",
        "country_flag": "\ud83c\uddec\ud83c\udde7",
        "iata_codes": [
            "LHR",
            "LGW",
            "STN",
            "LTN"
        ],
        "primary_iata": "LHR",
        "coordinates": {
            "lat": 51.5074,
            "lng": -0.1278
        },
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Covent Garden",
                "scores": {
                    "vibe": 9.1,
                    "walkability": 10.0,
                    "safety": 8.1,
                    "nightlife": 7.2,
                    "food": 9.1,
                    "transit": 9.6,
                    "culture": 10.0,
                    "beach": 0.3,
                    "history": 9.9
                },
                "transit_minutes_to_center": 0,
                "description": "The storied heart of the city with iconic landmarks."
            },
            {
                "name": "Shoreditch",
                "scores": {
                    "vibe": 9.9,
                    "walkability": 9.0,
                    "safety": 7.4,
                    "nightlife": 10.0,
                    "food": 8.5,
                    "transit": 8.2,
                    "culture": 8.7,
                    "beach": 0.0,
                    "history": 6.1
                },
                "transit_minutes_to_center": 15,
                "description": "Bohemian streets packed with galleries, bars, and energy."
            },
            {
                "name": "South Kensington",
                "scores": {
                    "vibe": 7.8,
                    "walkability": 8.1,
                    "safety": 9.6,
                    "nightlife": 5.3,
                    "food": 8.3,
                    "transit": 8.9,
                    "culture": 7.9,
                    "beach": 0.0,
                    "history": 7.4
                },
                "transit_minutes_to_center": 10,
                "description": "Quiet, elegant area with fine dining and leafy streets."
            }
        ]
    },
    "Paris": {
        "name": "Paris",
        "country": "France",
        "country_flag": "\ud83c\uddeb\ud83c\uddf7",
        "iata_codes": [
            "CDG",
            "ORY"
        ],
        "primary_iata": "CDG",
        "coordinates": {
            "lat": 48.8566,
            "lng": 2.3522
        },
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Le Marais",
                "scores": {
                    "vibe": 9.2,
                    "walkability": 10.0,
                    "safety": 8.4,
                    "nightlife": 6.7,
                    "food": 8.9,
                    "transit": 9.0,
                    "culture": 9.8,
                    "beach": 0.0,
                    "history": 9.6
                },
                "transit_minutes_to_center": 0,
                "description": "The storied heart of the city with iconic landmarks."
            },
            {
                "name": "Canal Saint-Martin",
                "scores": {
                    "vibe": 9.2,
                    "walkability": 8.0,
                    "safety": 7.5,
                    "nightlife": 9.4,
                    "food": 9.4,
                    "transit": 8.3,
                    "culture": 8.0,
                    "beach": 0.0,
                    "history": 6.1
                },
                "transit_minutes_to_center": 15,
                "description": "Bohemian streets packed with galleries, bars, and energy."
            },
            {
                "name": "Saint-Germain",
                "scores": {
                    "vibe": 7.0,
                    "walkability": 8.3,
                    "safety": 9.9,
                    "nightlife": 5.8,
                    "food": 7.8,
                    "transit": 8.5,
                    "culture": 7.2,
                    "beach": 0.0,
                    "history": 6.8
                },
                "transit_minutes_to_center": 10,
                "description": "Quiet, elegant area with fine dining and leafy streets."
            }
        ]
    },
    "Berlin": {
        "name": "Berlin",
        "country": "Germany",
        "country_flag": "\ud83c\udde9\ud83c\uddea",
        "iata_codes": [
            "BER"
        ],
        "primary_iata": "BER",
        "coordinates": {
            "lat": 52.52,
            "lng": 13.405
        },
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Mitte",
                "scores": {
                    "vibe": 8.8,
                    "walkability": 10.0,
                    "safety": 8.6,
                    "nightlife": 7.0,
                    "food": 9.4,
                    "transit": 9.2,
                    "culture": 10.0,
                    "beach": 0.0,
                    "history": 10.0
                },
                "transit_minutes_to_center": 0,
                "description": "The storied heart of the city with iconic landmarks."
            },
            {
                "name": "Kreuzberg",
                "scores": {
                    "vibe": 9.2,
                    "walkability": 8.8,
                    "safety": 7.2,
                    "nightlife": 9.0,
                    "food": 8.6,
                    "transit": 8.6,
                    "culture": 8.6,
                    "beach": 0.0,
                    "history": 5.8
                },
                "transit_minutes_to_center": 15,
                "description": "Bohemian streets packed with galleries, bars, and energy."
            },
            {
                "name": "Prenzlauer Berg",
                "scores": {
                    "vibe": 7.8,
                    "walkability": 8.1,
                    "safety": 9.2,
                    "nightlife": 5.7,
                    "food": 7.8,
                    "transit": 8.3,
                    "culture": 7.9,
                    "beach": 0.3,
                    "history": 7.2
                },
                "transit_minutes_to_center": 10,
                "description": "Quiet, elegant area with fine dining and leafy streets."
            }
        ]
    },
    "Barcelona": {
        "name": "Barcelona",
        "country": "Spain",
        "country_flag": "\ud83c\uddea\ud83c\uddf8",
        "iata_codes": [
            "BCN"
        ],
        "primary_iata": "BCN",
        "coordinates": {
            "lat": 41.3851,
            "lng": 2.1734
        },
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Historic Center (Barcelona)",
                "scores": {
                    "vibe": 9.5,
                    "walkability": 9.7,
                    "safety": 9.0,
                    "nightlife": 6.6,
                    "food": 9.4,
                    "transit": 9.3,
                    "culture": 9.9,
                    "beach": 0.3,
                    "history": 9.7
                },
                "transit_minutes_to_center": 0,
                "description": "The storied heart of the city with iconic landmarks."
            },
            {
                "name": "Trendy Arts District (Barcelona)",
                "scores": {
                    "vibe": 9.7,
                    "walkability": 8.2,
                    "safety": 7.7,
                    "nightlife": 9.5,
                    "food": 8.9,
                    "transit": 8.9,
                    "culture": 8.5,
                    "beach": 9.7,
                    "history": 5.7
                },
                "transit_minutes_to_center": 15,
                "description": "Bohemian streets packed with galleries, bars, and energy."
            },
            {
                "name": "Upscale Residential (Barcelona)",
                "scores": {
                    "vibe": 8.0,
                    "walkability": 8.4,
                    "safety": 9.1,
                    "nightlife": 5.7,
                    "food": 8.0,
                    "transit": 8.8,
                    "culture": 7.8,
                    "beach": 0.0,
                    "history": 7.0
                },
                "transit_minutes_to_center": 10,
                "description": "Quiet, elegant area with fine dining and leafy streets."
            }
        ]
    },
    "Amsterdam": {
        "name": "Amsterdam",
        "country": "Netherlands",
        "country_flag": "\ud83c\uddf3\ud83c\uddf1",
        "iata_codes": [
            "AMS"
        ],
        "primary_iata": "AMS",
        "coordinates": {
            "lat": 52.3676,
            "lng": 4.9041
        },
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Historic Center (Amsterdam)",
                "scores": {
                    "vibe": 8.9,
                    "walkability": 9.9,
                    "safety": 8.8,
                    "nightlife": 6.9,
                    "food": 9.5,
                    "transit": 9.7,
                    "culture": 9.9,
                    "beach": 0.0,
                    "history": 9.7
                },
                "transit_minutes_to_center": 0,
                "description": "The storied heart of the city with iconic landmarks."
            },
            {
                "name": "Trendy Arts District (Amsterdam)",
                "scores": {
                    "vibe": 9.6,
                    "walkability": 8.8,
                    "safety": 7.2,
                    "nightlife": 9.7,
                    "food": 8.8,
                    "transit": 8.5,
                    "culture": 8.0,
                    "beach": 0.1,
                    "history": 5.6
                },
                "transit_minutes_to_center": 15,
                "description": "Bohemian streets packed with galleries, bars, and energy."
            },
            {
                "name": "Upscale Residential (Amsterdam)",
                "scores": {
                    "vibe": 7.6,
                    "walkability": 8.3,
                    "safety": 10.0,
                    "nightlife": 5.3,
                    "food": 8.2,
                    "transit": 8.0,
                    "culture": 7.3,
                    "beach": 0.0,
                    "history": 6.6
                },
                "transit_minutes_to_center": 10,
                "description": "Quiet, elegant area with fine dining and leafy streets."
            }
        ]
    },
    "Rome": {
        "name": "Rome",
        "country": "Italy",
        "country_flag": "\ud83c\uddee\ud83c\uddf9",
        "iata_codes": [
            "FCO",
            "CIA"
        ],
        "primary_iata": "FCO",
        "coordinates": {
            "lat": 41.9028,
            "lng": 12.4964
        },
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Historic Center (Rome)",
                "scores": {
                    "vibe": 9.5,
                    "walkability": 9.7,
                    "safety": 8.9,
                    "nightlife": 7.3,
                    "food": 9.4,
                    "transit": 9.6,
                    "culture": 10.0,
                    "beach": 0.0,
                    "history": 10.0
                },
                "transit_minutes_to_center": 0,
                "description": "The storied heart of the city with iconic landmarks."
            },
            {
                "name": "Trendy Arts District (Rome)",
                "scores": {
                    "vibe": 9.1,
                    "walkability": 8.2,
                    "safety": 7.5,
                    "nightlife": 9.7,
                    "food": 8.5,
                    "transit": 9.0,
                    "culture": 8.7,
                    "beach": 0.0,
                    "history": 6.2
                },
                "transit_minutes_to_center": 15,
                "description": "Bohemian streets packed with galleries, bars, and energy."
            },
            {
                "name": "Upscale Residential (Rome)",
                "scores": {
                    "vibe": 7.3,
                    "walkability": 8.0,
                    "safety": 9.6,
                    "nightlife": 5.2,
                    "food": 7.7,
                    "transit": 8.3,
                    "culture": 7.1,
                    "beach": 0.3,
                    "history": 7.3
                },
                "transit_minutes_to_center": 10,
                "description": "Quiet, elegant area with fine dining and leafy streets."
            }
        ]
    },
    "Florence": {
        "name": "Florence",
        "country": "Italy",
        "country_flag": "\ud83c\uddee\ud83c\uddf9",
        "iata_codes": [
            "FLR"
        ],
        "primary_iata": "FLR",
        "coordinates": {
            "lat": 43.7696,
            "lng": 11.2558
        },
        "has_train_station": True,
        "gateway_airports": [
            {
                "iata": "PSA",
                "city": "Pisa",
                "distance_km": 80,
                "trainline_link": "https://www.thetrainline.com/book/results?origin=Pisa&destination=Florence",
                "flixbus_link": "https://shop.flixbus.com/search?departureCity=Pisa&arrivalCity=Florence"
            },
            {
                "iata": "BLQ",
                "city": "Bologna",
                "distance_km": 100,
                "trainline_link": "https://www.thetrainline.com/book/results?origin=Bologna&destination=Florence",
                "flixbus_link": "https://shop.flixbus.com/search?departureCity=Bologna&arrivalCity=Florence"
            }
        ],
        "neighborhoods": [
            {
                "name": "Historic Center (Florence)",
                "scores": {
                    "vibe": 8.6,
                    "walkability": 10.0,
                    "safety": 8.9,
                    "nightlife": 7.5,
                    "food": 8.9,
                    "transit": 9.9,
                    "culture": 10.0,
                    "beach": 0.3,
                    "history": 10.0
                },
                "transit_minutes_to_center": 0,
                "description": "The storied heart of the city with iconic landmarks."
            },
            {
                "name": "Trendy Arts District (Florence)",
                "scores": {
                    "vibe": 9.1,
                    "walkability": 8.1,
                    "safety": 7.7,
                    "nightlife": 10.0,
                    "food": 9.0,
                    "transit": 8.7,
                    "culture": 8.6,
                    "beach": 0.0,
                    "history": 6.2
                },
                "transit_minutes_to_center": 15,
                "description": "Bohemian streets packed with galleries, bars, and energy."
            },
            {
                "name": "Upscale Residential (Florence)",
                "scores": {
                    "vibe": 7.9,
                    "walkability": 8.4,
                    "safety": 9.7,
                    "nightlife": 5.7,
                    "food": 7.9,
                    "transit": 8.6,
                    "culture": 7.0,
                    "beach": 0.0,
                    "history": 6.8
                },
                "transit_minutes_to_center": 10,
                "description": "Quiet, elegant area with fine dining and leafy streets."
            }
        ]
    },
    "Prague": {
        "name": "Prague",
        "country": "Czechia",
        "country_flag": "\ud83c\udde8\ud83c\uddff",
        "iata_codes": [
            "PRG"
        ],
        "primary_iata": "PRG",
        "coordinates": {
            "lat": 50.0755,
            "lng": 14.4378
        },
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Historic Center (Prague)",
                "scores": {
                    "vibe": 8.8,
                    "walkability": 9.7,
                    "safety": 8.4,
                    "nightlife": 6.6,
                    "food": 9.5,
                    "transit": 9.2,
                    "culture": 9.6,
                    "beach": 0.5,
                    "history": 10.0
                },
                "transit_minutes_to_center": 0,
                "description": "The storied heart of the city with iconic landmarks."
            },
            {
                "name": "Trendy Arts District (Prague)",
                "scores": {
                    "vibe": 9.0,
                    "walkability": 8.7,
                    "safety": 7.1,
                    "nightlife": 9.8,
                    "food": 9.0,
                    "transit": 8.1,
                    "culture": 8.3,
                    "beach": 0.0,
                    "history": 6.4
                },
                "transit_minutes_to_center": 15,
                "description": "Bohemian streets packed with galleries, bars, and energy."
            },
            {
                "name": "Upscale Residential (Prague)",
                "scores": {
                    "vibe": 7.5,
                    "walkability": 8.2,
                    "safety": 9.5,
                    "nightlife": 5.9,
                    "food": 8.3,
                    "transit": 8.3,
                    "culture": 7.5,
                    "beach": 0.2,
                    "history": 6.9
                },
                "transit_minutes_to_center": 10,
                "description": "Quiet, elegant area with fine dining and leafy streets."
            }
        ]
    },
    "Lisbon": {
        "name": "Lisbon",
        "country": "Portugal",
        "country_flag": "\ud83c\uddf5\ud83c\uddf9",
        "iata_codes": [
            "LIS"
        ],
        "primary_iata": "LIS",
        "coordinates": {
            "lat": 38.7223,
            "lng": -9.1393
        },
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Historic Center (Lisbon)",
                "scores": {
                    "vibe": 9.0,
                    "walkability": 10.0,
                    "safety": 8.3,
                    "nightlife": 6.8,
                    "food": 9.1,
                    "transit": 9.7,
                    "culture": 10.0,
                    "beach": 0.4,
                    "history": 9.8
                },
                "transit_minutes_to_center": 0,
                "description": "The storied heart of the city with iconic landmarks."
            },
            {
                "name": "Trendy Arts District (Lisbon)",
                "scores": {
                    "vibe": 9.8,
                    "walkability": 8.9,
                    "safety": 7.7,
                    "nightlife": 9.5,
                    "food": 9.3,
                    "transit": 8.6,
                    "culture": 8.8,
                    "beach": 9.6,
                    "history": 6.0
                },
                "transit_minutes_to_center": 15,
                "description": "Bohemian streets packed with galleries, bars, and energy."
            },
            {
                "name": "Upscale Residential (Lisbon)",
                "scores": {
                    "vibe": 7.7,
                    "walkability": 8.6,
                    "safety": 9.0,
                    "nightlife": 5.2,
                    "food": 7.8,
                    "transit": 8.8,
                    "culture": 7.8,
                    "beach": 0.3,
                    "history": 7.3
                },
                "transit_minutes_to_center": 10,
                "description": "Quiet, elegant area with fine dining and leafy streets."
            }
        ]
    },
    "Vienna": {
        "name": "Vienna",
        "country": "Austria",
        "country_flag": "\ud83c\udde6\ud83c\uddf9",
        "iata_codes": [
            "VIE"
        ],
        "primary_iata": "VIE",
        "coordinates": {
            "lat": 48.2082,
            "lng": 16.3738
        },
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Historic Center (Vienna)",
                "scores": {
                    "vibe": 8.6,
                    "walkability": 10.0,
                    "safety": 8.1,
                    "nightlife": 7.0,
                    "food": 9.5,
                    "transit": 9.1,
                    "culture": 10.0,
                    "beach": 0.0,
                    "history": 10.0
                },
                "transit_minutes_to_center": 0,
                "description": "The storied heart of the city with iconic landmarks."
            },
            {
                "name": "Trendy Arts District (Vienna)",
                "scores": {
                    "vibe": 9.4,
                    "walkability": 8.8,
                    "safety": 7.7,
                    "nightlife": 9.5,
                    "food": 8.7,
                    "transit": 8.6,
                    "culture": 8.2,
                    "beach": 0.5,
                    "history": 5.6
                },
                "transit_minutes_to_center": 15,
                "description": "Bohemian streets packed with galleries, bars, and energy."
            },
            {
                "name": "Upscale Residential (Vienna)",
                "scores": {
                    "vibe": 7.9,
                    "walkability": 8.0,
                    "safety": 9.4,
                    "nightlife": 5.6,
                    "food": 8.2,
                    "transit": 8.9,
                    "culture": 7.3,
                    "beach": 0.0,
                    "history": 7.0
                },
                "transit_minutes_to_center": 10,
                "description": "Quiet, elegant area with fine dining and leafy streets."
            }
        ]
    },
    "Budapest": {
        "name": "Budapest",
        "country": "Hungary",
        "country_flag": "\ud83c\udded\ud83c\uddfa",
        "iata_codes": [
            "BUD"
        ],
        "primary_iata": "BUD",
        "coordinates": {
            "lat": 47.4979,
            "lng": 19.0402
        },
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Historic Center (Budapest)",
                "scores": {
                    "vibe": 9.1,
                    "walkability": 9.6,
                    "safety": 8.7,
                    "nightlife": 7.0,
                    "food": 8.8,
                    "transit": 9.9,
                    "culture": 10.0,
                    "beach": 0.3,
                    "history": 9.5
                },
                "transit_minutes_to_center": 0,
                "description": "The storied heart of the city with iconic landmarks."
            },
            {
                "name": "Trendy Arts District (Budapest)",
                "scores": {
                    "vibe": 9.8,
                    "walkability": 8.6,
                    "safety": 7.6,
                    "nightlife": 9.9,
                    "food": 8.8,
                    "transit": 8.2,
                    "culture": 8.6,
                    "beach": 0.2,
                    "history": 5.9
                },
                "transit_minutes_to_center": 15,
                "description": "Bohemian streets packed with galleries, bars, and energy."
            },
            {
                "name": "Upscale Residential (Budapest)",
                "scores": {
                    "vibe": 7.8,
                    "walkability": 8.1,
                    "safety": 9.8,
                    "nightlife": 5.1,
                    "food": 8.3,
                    "transit": 8.5,
                    "culture": 7.8,
                    "beach": 0.0,
                    "history": 6.8
                },
                "transit_minutes_to_center": 10,
                "description": "Quiet, elegant area with fine dining and leafy streets."
            }
        ]
    },
    "Copenhagen": {
        "name": "Copenhagen",
        "country": "Denmark",
        "country_flag": "\ud83c\udde9\ud83c\uddf0",
        "iata_codes": [
            "CPH"
        ],
        "primary_iata": "CPH",
        "coordinates": {
            "lat": 55.6761,
            "lng": 12.5683
        },
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Historic Center (Copenhagen)",
                "scores": {
                    "vibe": 9.3,
                    "walkability": 9.5,
                    "safety": 8.4,
                    "nightlife": 7.3,
                    "food": 8.6,
                    "transit": 9.9,
                    "culture": 10.0,
                    "beach": 0.0,
                    "history": 9.5
                },
                "transit_minutes_to_center": 0,
                "description": "The storied heart of the city with iconic landmarks."
            },
            {
                "name": "Trendy Arts District (Copenhagen)",
                "scores": {
                    "vibe": 9.9,
                    "walkability": 8.4,
                    "safety": 7.7,
                    "nightlife": 9.7,
                    "food": 9.4,
                    "transit": 8.2,
                    "culture": 8.4,
                    "beach": 0.0,
                    "history": 6.4
                },
                "transit_minutes_to_center": 15,
                "description": "Bohemian streets packed with galleries, bars, and energy."
            },
            {
                "name": "Upscale Residential (Copenhagen)",
                "scores": {
                    "vibe": 7.1,
                    "walkability": 8.4,
                    "safety": 9.3,
                    "nightlife": 5.9,
                    "food": 8.1,
                    "transit": 8.9,
                    "culture": 8.0,
                    "beach": 0.4,
                    "history": 7.0
                },
                "transit_minutes_to_center": 10,
                "description": "Quiet, elegant area with fine dining and leafy streets."
            }
        ]
    },
    "Milan": {
        "name": "Milan",
        "country": "Italy",
        "country_flag": "\ud83c\uddee\ud83c\uddf9",
        "iata_codes": [
            "MXP",
            "LIN",
            "BGY"
        ],
        "primary_iata": "MXP",
        "coordinates": {
            "lat": 45.4642,
            "lng": 9.19
        },
        "has_train_station": True,
        "gateway_airports": [
            {
                "iata": "BGY",
                "city": "Bergamo",
                "distance_km": 45,
                "trainline_link": "",
                "flixbus_link": "https://shop.flixbus.com/search?departureCity=Bergamo&arrivalCity=Milan"
            }
        ],
        "neighborhoods": [
            {
                "name": "Historic Center (Milan)",
                "scores": {
                    "vibe": 9.3,
                    "walkability": 10.0,
                    "safety": 8.8,
                    "nightlife": 7.1,
                    "food": 9.3,
                    "transit": 9.4,
                    "culture": 10.0,
                    "beach": 0.5,
                    "history": 9.8
                },
                "transit_minutes_to_center": 0,
                "description": "The storied heart of the city with iconic landmarks."
            },
            {
                "name": "Trendy Arts District (Milan)",
                "scores": {
                    "vibe": 9.8,
                    "walkability": 8.1,
                    "safety": 7.6,
                    "nightlife": 9.9,
                    "food": 8.7,
                    "transit": 8.9,
                    "culture": 8.4,
                    "beach": 0.4,
                    "history": 6.0
                },
                "transit_minutes_to_center": 15,
                "description": "Bohemian streets packed with galleries, bars, and energy."
            },
            {
                "name": "Upscale Residential (Milan)",
                "scores": {
                    "vibe": 7.2,
                    "walkability": 8.3,
                    "safety": 9.3,
                    "nightlife": 5.9,
                    "food": 8.0,
                    "transit": 8.8,
                    "culture": 7.4,
                    "beach": 0.2,
                    "history": 7.2
                },
                "transit_minutes_to_center": 10,
                "description": "Quiet, elegant area with fine dining and leafy streets."
            }
        ]
    },
    "Munich": {
        "name": "Munich",
        "country": "Germany",
        "country_flag": "\ud83c\udde9\ud83c\uddea",
        "iata_codes": [
            "MUC"
        ],
        "primary_iata": "MUC",
        "coordinates": {
            "lat": 48.1351,
            "lng": 11.582
        },
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Historic Center (Munich)",
                "scores": {
                    "vibe": 8.9,
                    "walkability": 9.9,
                    "safety": 9.0,
                    "nightlife": 7.4,
                    "food": 8.7,
                    "transit": 9.2,
                    "culture": 10.0,
                    "beach": 0.0,
                    "history": 10.0
                },
                "transit_minutes_to_center": 0,
                "description": "The storied heart of the city with iconic landmarks."
            },
            {
                "name": "Trendy Arts District (Munich)",
                "scores": {
                    "vibe": 10.0,
                    "walkability": 8.6,
                    "safety": 7.5,
                    "nightlife": 9.6,
                    "food": 9.4,
                    "transit": 8.2,
                    "culture": 8.5,
                    "beach": 0.0,
                    "history": 5.6
                },
                "transit_minutes_to_center": 15,
                "description": "Bohemian streets packed with galleries, bars, and energy."
            },
            {
                "name": "Upscale Residential (Munich)",
                "scores": {
                    "vibe": 7.0,
                    "walkability": 8.3,
                    "safety": 9.7,
                    "nightlife": 5.0,
                    "food": 7.9,
                    "transit": 9.0,
                    "culture": 7.9,
                    "beach": 0.0,
                    "history": 7.0
                },
                "transit_minutes_to_center": 10,
                "description": "Quiet, elegant area with fine dining and leafy streets."
            }
        ]
    },
    "Madrid": {
        "name": "Madrid",
        "country": "Spain",
        "country_flag": "\ud83c\uddea\ud83c\uddf8",
        "iata_codes": [
            "MAD"
        ],
        "primary_iata": "MAD",
        "coordinates": {
            "lat": 40.4168,
            "lng": -3.7038
        },
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Historic Center (Madrid)",
                "scores": {
                    "vibe": 8.9,
                    "walkability": 10.0,
                    "safety": 8.1,
                    "nightlife": 7.1,
                    "food": 9.2,
                    "transit": 9.5,
                    "culture": 9.5,
                    "beach": 0.0,
                    "history": 9.5
                },
                "transit_minutes_to_center": 0,
                "description": "The storied heart of the city with iconic landmarks."
            },
            {
                "name": "Trendy Arts District (Madrid)",
                "scores": {
                    "vibe": 9.5,
                    "walkability": 8.1,
                    "safety": 7.8,
                    "nightlife": 9.4,
                    "food": 8.8,
                    "transit": 8.7,
                    "culture": 8.7,
                    "beach": 0.0,
                    "history": 5.8
                },
                "transit_minutes_to_center": 15,
                "description": "Bohemian streets packed with galleries, bars, and energy."
            },
            {
                "name": "Upscale Residential (Madrid)",
                "scores": {
                    "vibe": 7.1,
                    "walkability": 8.2,
                    "safety": 9.6,
                    "nightlife": 5.8,
                    "food": 8.2,
                    "transit": 8.1,
                    "culture": 7.6,
                    "beach": 0.0,
                    "history": 6.7
                },
                "transit_minutes_to_center": 10,
                "description": "Quiet, elegant area with fine dining and leafy streets."
            }
        ]
    },
    "Dublin": {
        "name": "Dublin",
        "country": "Ireland",
        "country_flag": "\ud83c\uddee\ud83c\uddea",
        "iata_codes": [
            "DUB"
        ],
        "primary_iata": "DUB",
        "coordinates": {
            "lat": 53.3498,
            "lng": -6.2603
        },
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Historic Center (Dublin)",
                "scores": {
                    "vibe": 8.9,
                    "walkability": 10.0,
                    "safety": 8.0,
                    "nightlife": 7.2,
                    "food": 8.8,
                    "transit": 9.7,
                    "culture": 10.0,
                    "beach": 0.0,
                    "history": 9.8
                },
                "transit_minutes_to_center": 0,
                "description": "The storied heart of the city with iconic landmarks."
            },
            {
                "name": "Trendy Arts District (Dublin)",
                "scores": {
                    "vibe": 9.7,
                    "walkability": 8.1,
                    "safety": 7.7,
                    "nightlife": 9.4,
                    "food": 9.0,
                    "transit": 8.0,
                    "culture": 8.3,
                    "beach": 0.0,
                    "history": 6.1
                },
                "transit_minutes_to_center": 15,
                "description": "Bohemian streets packed with galleries, bars, and energy."
            },
            {
                "name": "Upscale Residential (Dublin)",
                "scores": {
                    "vibe": 7.3,
                    "walkability": 8.5,
                    "safety": 9.3,
                    "nightlife": 5.9,
                    "food": 8.0,
                    "transit": 8.7,
                    "culture": 7.8,
                    "beach": 0.0,
                    "history": 7.0
                },
                "transit_minutes_to_center": 10,
                "description": "Quiet, elegant area with fine dining and leafy streets."
            }
        ]
    },
    "Stockholm": {
        "name": "Stockholm",
        "country": "Sweden",
        "country_flag": "\ud83c\uddf8\ud83c\uddea",
        "iata_codes": [
            "ARN"
        ],
        "primary_iata": "ARN",
        "coordinates": {
            "lat": 59.3293,
            "lng": 18.0686
        },
        "has_train_station": True,
        "gateway_airports": [
            {
                "iata": "NYO",
                "city": "Skavsta",
                "distance_km": 100,
                "trainline_link": "",
                "flixbus_link": "https://shop.flixbus.com/search?departureCity=Skavsta&arrivalCity=Stockholm"
            }
        ],
        "neighborhoods": [
            {
                "name": "Historic Center (Stockholm)",
                "scores": {
                    "vibe": 9.3,
                    "walkability": 10.0,
                    "safety": 8.0,
                    "nightlife": 6.7,
                    "food": 9.4,
                    "transit": 9.2,
                    "culture": 9.7,
                    "beach": 0.0,
                    "history": 10.0
                },
                "transit_minutes_to_center": 0,
                "description": "The storied heart of the city with iconic landmarks."
            },
            {
                "name": "Trendy Arts District (Stockholm)",
                "scores": {
                    "vibe": 9.1,
                    "walkability": 8.3,
                    "safety": 7.1,
                    "nightlife": 9.6,
                    "food": 9.1,
                    "transit": 8.7,
                    "culture": 8.3,
                    "beach": 0.0,
                    "history": 6.3
                },
                "transit_minutes_to_center": 15,
                "description": "Bohemian streets packed with galleries, bars, and energy."
            },
            {
                "name": "Upscale Residential (Stockholm)",
                "scores": {
                    "vibe": 7.7,
                    "walkability": 8.4,
                    "safety": 9.1,
                    "nightlife": 5.5,
                    "food": 8.0,
                    "transit": 8.1,
                    "culture": 7.7,
                    "beach": 0.5,
                    "history": 6.6
                },
                "transit_minutes_to_center": 10,
                "description": "Quiet, elegant area with fine dining and leafy streets."
            }
        ]
    },
    "Zurich": {
        "name": "Zurich",
        "country": "Switzerland",
        "country_flag": "\ud83c\udde8\ud83c\udded",
        "iata_codes": [
            "ZRH"
        ],
        "primary_iata": "ZRH",
        "coordinates": {
            "lat": 47.3769,
            "lng": 8.5417
        },
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Historic Center (Zurich)",
                "scores": {
                    "vibe": 8.7,
                    "walkability": 10.0,
                    "safety": 8.5,
                    "nightlife": 7.1,
                    "food": 9.1,
                    "transit": 9.8,
                    "culture": 10.0,
                    "beach": 0.0,
                    "history": 10.0
                },
                "transit_minutes_to_center": 0,
                "description": "The storied heart of the city with iconic landmarks."
            },
            {
                "name": "Trendy Arts District (Zurich)",
                "scores": {
                    "vibe": 9.4,
                    "walkability": 8.1,
                    "safety": 7.2,
                    "nightlife": 10.0,
                    "food": 9.5,
                    "transit": 8.2,
                    "culture": 8.9,
                    "beach": 0.0,
                    "history": 6.3
                },
                "transit_minutes_to_center": 15,
                "description": "Bohemian streets packed with galleries, bars, and energy."
            },
            {
                "name": "Upscale Residential (Zurich)",
                "scores": {
                    "vibe": 7.1,
                    "walkability": 8.3,
                    "safety": 9.4,
                    "nightlife": 5.2,
                    "food": 7.6,
                    "transit": 8.6,
                    "culture": 7.5,
                    "beach": 0.4,
                    "history": 7.4
                },
                "transit_minutes_to_center": 10,
                "description": "Quiet, elegant area with fine dining and leafy streets."
            }
        ]
    },
    "Athens": {
        "name": "Athens",
        "country": "Greece",
        "country_flag": "\ud83c\uddec\ud83c\uddf7",
        "iata_codes": [
            "ATH"
        ],
        "primary_iata": "ATH",
        "coordinates": {
            "lat": 37.9838,
            "lng": 23.7275
        },
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Historic Center (Athens)",
                "scores": {
                    "vibe": 9.0,
                    "walkability": 10.0,
                    "safety": 8.2,
                    "nightlife": 7.1,
                    "food": 8.8,
                    "transit": 9.1,
                    "culture": 10.0,
                    "beach": 0.2,
                    "history": 10.0
                },
                "transit_minutes_to_center": 0,
                "description": "The storied heart of the city with iconic landmarks."
            },
            {
                "name": "Trendy Arts District (Athens)",
                "scores": {
                    "vibe": 9.8,
                    "walkability": 8.3,
                    "safety": 7.3,
                    "nightlife": 9.7,
                    "food": 8.7,
                    "transit": 8.2,
                    "culture": 8.2,
                    "beach": 9.5,
                    "history": 6.2
                },
                "transit_minutes_to_center": 15,
                "description": "Bohemian streets packed with galleries, bars, and energy."
            },
            {
                "name": "Upscale Residential (Athens)",
                "scores": {
                    "vibe": 7.3,
                    "walkability": 8.1,
                    "safety": 9.3,
                    "nightlife": 5.4,
                    "food": 8.2,
                    "transit": 8.7,
                    "culture": 7.6,
                    "beach": 0.0,
                    "history": 6.7
                },
                "transit_minutes_to_center": 10,
                "description": "Quiet, elegant area with fine dining and leafy streets."
            }
        ]
    },
    "Krak\u00f3w": {
        "name": "Krak\u00f3w",
        "country": "Poland",
        "country_flag": "\ud83c\uddf5\ud83c\uddf1",
        "iata_codes": [
            "KRK"
        ],
        "primary_iata": "KRK",
        "coordinates": {
            "lat": 50.0647,
            "lng": 19.945
        },
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Historic Center (Krak\u00f3w)",
                "scores": {
                    "vibe": 9.2,
                    "walkability": 10.0,
                    "safety": 8.3,
                    "nightlife": 6.8,
                    "food": 8.6,
                    "transit": 9.8,
                    "culture": 10.0,
                    "beach": 0.2,
                    "history": 10.0
                },
                "transit_minutes_to_center": 0,
                "description": "The storied heart of the city with iconic landmarks."
            },
            {
                "name": "Trendy Arts District (Krak\u00f3w)",
                "scores": {
                    "vibe": 9.6,
                    "walkability": 8.7,
                    "safety": 7.7,
                    "nightlife": 10.0,
                    "food": 8.5,
                    "transit": 8.0,
                    "culture": 8.4,
                    "beach": 0.0,
                    "history": 6.2
                },
                "transit_minutes_to_center": 15,
                "description": "Bohemian streets packed with galleries, bars, and energy."
            },
            {
                "name": "Upscale Residential (Krak\u00f3w)",
                "scores": {
                    "vibe": 7.1,
                    "walkability": 8.1,
                    "safety": 9.4,
                    "nightlife": 5.9,
                    "food": 8.3,
                    "transit": 8.1,
                    "culture": 7.6,
                    "beach": 0.5,
                    "history": 6.6
                },
                "transit_minutes_to_center": 10,
                "description": "Quiet, elegant area with fine dining and leafy streets."
            }
        ]
    },
    "Porto": {
        "name": "Porto",
        "country": "Portugal",
        "country_flag": "\ud83c\uddf5\ud83c\uddf9",
        "iata_codes": [
            "OPO"
        ],
        "primary_iata": "OPO",
        "coordinates": {
            "lat": 41.1579,
            "lng": -8.6291
        },
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Historic Center (Porto)",
                "scores": {
                    "vibe": 9.4,
                    "walkability": 10.0,
                    "safety": 8.1,
                    "nightlife": 6.5,
                    "food": 9.1,
                    "transit": 9.7,
                    "culture": 9.8,
                    "beach": 0.4,
                    "history": 10.0
                },
                "transit_minutes_to_center": 0,
                "description": "The storied heart of the city with iconic landmarks."
            },
            {
                "name": "Trendy Arts District (Porto)",
                "scores": {
                    "vibe": 9.3,
                    "walkability": 8.6,
                    "safety": 7.9,
                    "nightlife": 10.0,
                    "food": 8.8,
                    "transit": 8.7,
                    "culture": 8.7,
                    "beach": 0.2,
                    "history": 6.3
                },
                "transit_minutes_to_center": 15,
                "description": "Bohemian streets packed with galleries, bars, and energy."
            },
            {
                "name": "Upscale Residential (Porto)",
                "scores": {
                    "vibe": 7.1,
                    "walkability": 8.3,
                    "safety": 9.4,
                    "nightlife": 5.8,
                    "food": 7.6,
                    "transit": 8.5,
                    "culture": 7.3,
                    "beach": 0.0,
                    "history": 6.7
                },
                "transit_minutes_to_center": 10,
                "description": "Quiet, elegant area with fine dining and leafy streets."
            }
        ]
    },
    "Brussels": {
        "name": "Brussels",
        "country": "Belgium",
        "country_flag": "\ud83c\udde7\ud83c\uddea",
        "iata_codes": [
            "BRU",
            "CRL"
        ],
        "primary_iata": "BRU",
        "coordinates": {
            "lat": 50.8503,
            "lng": 4.3517
        },
        "has_train_station": True,
        "gateway_airports": [
            {
                "iata": "CRL",
                "city": "Charleroi",
                "distance_km": 55,
                "trainline_link": "https://www.thetrainline.com/book/results?origin=Charleroi&destination=Brussels",
                "flixbus_link": "https://shop.flixbus.com/search?departureCity=Charleroi&arrivalCity=Brussels"
            }
        ],
        "neighborhoods": [
            {
                "name": "Historic Center (Brussels)",
                "scores": {
                    "vibe": 9.4,
                    "walkability": 10.0,
                    "safety": 8.4,
                    "nightlife": 7.3,
                    "food": 9.5,
                    "transit": 9.1,
                    "culture": 10.0,
                    "beach": 0.2,
                    "history": 10.0
                },
                "transit_minutes_to_center": 0,
                "description": "The storied heart of the city with iconic landmarks."
            },
            {
                "name": "Trendy Arts District (Brussels)",
                "scores": {
                    "vibe": 9.6,
                    "walkability": 8.6,
                    "safety": 7.8,
                    "nightlife": 9.2,
                    "food": 8.9,
                    "transit": 8.7,
                    "culture": 8.3,
                    "beach": 0.0,
                    "history": 5.6
                },
                "transit_minutes_to_center": 15,
                "description": "Bohemian streets packed with galleries, bars, and energy."
            },
            {
                "name": "Upscale Residential (Brussels)",
                "scores": {
                    "vibe": 7.5,
                    "walkability": 8.3,
                    "safety": 9.5,
                    "nightlife": 5.2,
                    "food": 8.5,
                    "transit": 8.0,
                    "culture": 7.9,
                    "beach": 0.0,
                    "history": 7.1
                },
                "transit_minutes_to_center": 10,
                "description": "Quiet, elegant area with fine dining and leafy streets."
            }
        ]
    },
    "Edinburgh": {
        "name": "Edinburgh",
        "country": "UK",
        "country_flag": "\ud83c\uddec\ud83c\udde7",
        "iata_codes": [
            "EDI"
        ],
        "primary_iata": "EDI",
        "coordinates": {
            "lat": 55.9533,
            "lng": -3.1883
        },
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Historic Center (Edinburgh)",
                "scores": {
                    "vibe": 8.7,
                    "walkability": 10.0,
                    "safety": 8.1,
                    "nightlife": 6.9,
                    "food": 8.9,
                    "transit": 9.5,
                    "culture": 9.8,
                    "beach": 0.2,
                    "history": 10.0
                },
                "transit_minutes_to_center": 0,
                "description": "The storied heart of the city with iconic landmarks."
            },
            {
                "name": "Trendy Arts District (Edinburgh)",
                "scores": {
                    "vibe": 9.9,
                    "walkability": 8.1,
                    "safety": 7.2,
                    "nightlife": 10.0,
                    "food": 8.7,
                    "transit": 8.2,
                    "culture": 8.9,
                    "beach": 0.0,
                    "history": 6.2
                },
                "transit_minutes_to_center": 15,
                "description": "Bohemian streets packed with galleries, bars, and energy."
            },
            {
                "name": "Upscale Residential (Edinburgh)",
                "scores": {
                    "vibe": 7.9,
                    "walkability": 8.3,
                    "safety": 9.5,
                    "nightlife": 5.0,
                    "food": 8.1,
                    "transit": 8.9,
                    "culture": 7.7,
                    "beach": 0.0,
                    "history": 6.9
                },
                "transit_minutes_to_center": 10,
                "description": "Quiet, elegant area with fine dining and leafy streets."
            }
        ]
    },
    "Nice": {
        "name": "Nice",
        "country": "France",
        "country_flag": "\ud83c\uddeb\ud83c\uddf7",
        "iata_codes": [
            "NCE"
        ],
        "primary_iata": "NCE",
        "coordinates": {
            "lat": 43.7102,
            "lng": 7.262
        },
        "has_train_station": True,
        "gateway_airports": [
            {
                "iata": "MRS",
                "city": "Marseille",
                "distance_km": 200,
                "trainline_link": "https://www.thetrainline.com/book/results?origin=Marseille&destination=Nice",
                "flixbus_link": ""
            }
        ],
        "neighborhoods": [
            {
                "name": "Historic Center (Nice)",
                "scores": {
                    "vibe": 9.3,
                    "walkability": 10.0,
                    "safety": 9.0,
                    "nightlife": 7.2,
                    "food": 9.2,
                    "transit": 9.3,
                    "culture": 10.0,
                    "beach": 0.2,
                    "history": 10.0
                },
                "transit_minutes_to_center": 0,
                "description": "The storied heart of the city with iconic landmarks."
            },
            {
                "name": "Trendy Arts District (Nice)",
                "scores": {
                    "vibe": 9.2,
                    "walkability": 8.9,
                    "safety": 7.2,
                    "nightlife": 9.2,
                    "food": 9.3,
                    "transit": 8.9,
                    "culture": 8.2,
                    "beach": 9.8,
                    "history": 5.7
                },
                "transit_minutes_to_center": 15,
                "description": "Bohemian streets packed with galleries, bars, and energy."
            },
            {
                "name": "Upscale Residential (Nice)",
                "scores": {
                    "vibe": 7.0,
                    "walkability": 8.4,
                    "safety": 9.7,
                    "nightlife": 5.3,
                    "food": 8.0,
                    "transit": 8.7,
                    "culture": 7.1,
                    "beach": 0.0,
                    "history": 7.0
                },
                "transit_minutes_to_center": 10,
                "description": "Quiet, elegant area with fine dining and leafy streets."
            }
        ]
    },
    "Split": {
        "name": "Split",
        "country": "Croatia",
        "country_flag": "\ud83c\udded\ud83c\uddf7",
        "iata_codes": [
            "SPU"
        ],
        "primary_iata": "SPU",
        "coordinates": {
            "lat": 43.5081,
            "lng": 16.4402
        },
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Historic Center (Split)",
                "scores": {
                    "vibe": 8.6,
                    "walkability": 10.0,
                    "safety": 8.4,
                    "nightlife": 6.8,
                    "food": 8.7,
                    "transit": 9.6,
                    "culture": 10.0,
                    "beach": 0.4,
                    "history": 10.0
                },
                "transit_minutes_to_center": 0,
                "description": "The storied heart of the city with iconic landmarks."
            },
            {
                "name": "Trendy Arts District (Split)",
                "scores": {
                    "vibe": 9.6,
                    "walkability": 8.8,
                    "safety": 7.4,
                    "nightlife": 9.3,
                    "food": 8.6,
                    "transit": 8.4,
                    "culture": 8.2,
                    "beach": 9.5,
                    "history": 6.0
                },
                "transit_minutes_to_center": 15,
                "description": "Bohemian streets packed with galleries, bars, and energy."
            },
            {
                "name": "Upscale Residential (Split)",
                "scores": {
                    "vibe": 8.0,
                    "walkability": 8.4,
                    "safety": 9.9,
                    "nightlife": 5.9,
                    "food": 7.9,
                    "transit": 8.5,
                    "culture": 7.6,
                    "beach": 0.1,
                    "history": 7.1
                },
                "transit_minutes_to_center": 10,
                "description": "Quiet, elegant area with fine dining and leafy streets."
            }
        ]
    },
    "Warsaw": {
        "name": "Warsaw",
        "country": "Poland",
        "country_flag": "\ud83c\uddf5\ud83c\uddf1",
        "iata_codes": [
            "WAW",
            "WMI"
        ],
        "primary_iata": "WAW",
        "coordinates": {
            "lat": 52.2297,
            "lng": 21.0122
        },
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Historic Center (Warsaw)",
                "scores": {
                    "vibe": 8.6,
                    "walkability": 10.0,
                    "safety": 8.4,
                    "nightlife": 6.8,
                    "food": 9.1,
                    "transit": 9.5,
                    "culture": 9.8,
                    "beach": 0.0,
                    "history": 9.6
                },
                "transit_minutes_to_center": 0,
                "description": "The storied heart of the city with iconic landmarks."
            },
            {
                "name": "Trendy Arts District (Warsaw)",
                "scores": {
                    "vibe": 9.2,
                    "walkability": 8.0,
                    "safety": 7.9,
                    "nightlife": 9.6,
                    "food": 9.1,
                    "transit": 8.7,
                    "culture": 8.7,
                    "beach": 0.3,
                    "history": 5.6
                },
                "transit_minutes_to_center": 15,
                "description": "Bohemian streets packed with galleries, bars, and energy."
            },
            {
                "name": "Upscale Residential (Warsaw)",
                "scores": {
                    "vibe": 7.7,
                    "walkability": 8.3,
                    "safety": 9.9,
                    "nightlife": 5.1,
                    "food": 7.8,
                    "transit": 8.0,
                    "culture": 7.6,
                    "beach": 0.0,
                    "history": 6.7
                },
                "transit_minutes_to_center": 10,
                "description": "Quiet, elegant area with fine dining and leafy streets."
            }
        ]
    },
    "Seville": {
        "name": "Seville",
        "country": "Spain",
        "country_flag": "\ud83c\uddea\ud83c\uddf8",
        "iata_codes": [
            "SVQ"
        ],
        "primary_iata": "SVQ",
        "coordinates": {
            "lat": 37.3891,
            "lng": -5.9845
        },
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Historic Center (Seville)",
                "scores": {
                    "vibe": 9.4,
                    "walkability": 9.9,
                    "safety": 8.0,
                    "nightlife": 7.4,
                    "food": 8.9,
                    "transit": 9.3,
                    "culture": 9.5,
                    "beach": 0.0,
                    "history": 9.7
                },
                "transit_minutes_to_center": 0,
                "description": "The storied heart of the city with iconic landmarks."
            },
            {
                "name": "Trendy Arts District (Seville)",
                "scores": {
                    "vibe": 9.3,
                    "walkability": 8.5,
                    "safety": 7.3,
                    "nightlife": 9.0,
                    "food": 9.2,
                    "transit": 8.5,
                    "culture": 8.7,
                    "beach": 0.4,
                    "history": 5.8
                },
                "transit_minutes_to_center": 15,
                "description": "Bohemian streets packed with galleries, bars, and energy."
            },
            {
                "name": "Upscale Residential (Seville)",
                "scores": {
                    "vibe": 7.4,
                    "walkability": 8.2,
                    "safety": 9.2,
                    "nightlife": 5.8,
                    "food": 7.6,
                    "transit": 8.3,
                    "culture": 7.3,
                    "beach": 0.0,
                    "history": 6.6
                },
                "transit_minutes_to_center": 10,
                "description": "Quiet, elegant area with fine dining and leafy streets."
            }
        ]
    },
    "Helsinki": {
        "name": "Helsinki",
        "country": "Finland",
        "country_flag": "",
        "iata_codes": ["HEL"],
        "primary_iata": "HEL",
        "coordinates": {"lat": 60.1695, "lng": 24.9354},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Helsinki Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Helsinki."
            }
        ]
    },
    "Oslo": {
        "name": "Oslo",
        "country": "Norway",
        "country_flag": "",
        "iata_codes": ["OSL"],
        "primary_iata": "OSL",
        "coordinates": {"lat": 59.9139, "lng": 10.7522},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Oslo Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Oslo."
            }
        ]
    },
    "Stockholm": {
        "name": "Stockholm",
        "country": "Sweden",
        "country_flag": "",
        "iata_codes": ["ARN"],
        "primary_iata": "ARN",
        "coordinates": {"lat": 59.3293, "lng": 18.0686},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Stockholm Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Stockholm."
            }
        ]
    },
    "Riga": {
        "name": "Riga",
        "country": "Latvia",
        "country_flag": "",
        "iata_codes": ["RIX"],
        "primary_iata": "RIX",
        "coordinates": {"lat": 56.9496, "lng": 24.1052},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Riga Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Riga."
            }
        ]
    },
    "Tallinn": {
        "name": "Tallinn",
        "country": "Estonia",
        "country_flag": "",
        "iata_codes": ["TLL"],
        "primary_iata": "TLL",
        "coordinates": {"lat": 59.437, "lng": 24.7536},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Tallinn Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Tallinn."
            }
        ]
    },
    "Vilnius": {
        "name": "Vilnius",
        "country": "Lithuania",
        "country_flag": "",
        "iata_codes": ["VNO"],
        "primary_iata": "VNO",
        "coordinates": {"lat": 54.6872, "lng": 25.2797},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Vilnius Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Vilnius."
            }
        ]
    },
    "Bucharest": {
        "name": "Bucharest",
        "country": "Romania",
        "country_flag": "",
        "iata_codes": ["OTP"],
        "primary_iata": "OTP",
        "coordinates": {"lat": 44.4268, "lng": 26.1025},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Bucharest Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Bucharest."
            }
        ]
    },
    "Sofia": {
        "name": "Sofia",
        "country": "Bulgaria",
        "country_flag": "",
        "iata_codes": ["SOF"],
        "primary_iata": "SOF",
        "coordinates": {"lat": 42.6977, "lng": 23.3219},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Sofia Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Sofia."
            }
        ]
    },
    "Belgrade": {
        "name": "Belgrade",
        "country": "Serbia",
        "country_flag": "",
        "iata_codes": ["BEG"],
        "primary_iata": "BEG",
        "coordinates": {"lat": 44.7866, "lng": 20.4489},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Belgrade Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Belgrade."
            }
        ]
    },
    "Zagreb": {
        "name": "Zagreb",
        "country": "Croatia",
        "country_flag": "",
        "iata_codes": ["ZAG"],
        "primary_iata": "ZAG",
        "coordinates": {"lat": 45.815, "lng": 15.9819},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Zagreb Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Zagreb."
            }
        ]
    },
    "Ljubljana": {
        "name": "Ljubljana",
        "country": "Slovenia",
        "country_flag": "",
        "iata_codes": ["LJU"],
        "primary_iata": "LJU",
        "coordinates": {"lat": 46.0569, "lng": 14.5058},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Ljubljana Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Ljubljana."
            }
        ]
    },
    "Bratislava": {
        "name": "Bratislava",
        "country": "Slovakia",
        "country_flag": "",
        "iata_codes": ["BTS"],
        "primary_iata": "BTS",
        "coordinates": {"lat": 48.1486, "lng": 17.1077},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Bratislava Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Bratislava."
            }
        ]
    },
    "Reykjavik": {
        "name": "Reykjavik",
        "country": "Iceland",
        "country_flag": "",
        "iata_codes": ["KEF"],
        "primary_iata": "KEF",
        "coordinates": {"lat": 64.1466, "lng": -21.9426},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Reykjavik Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Reykjavik."
            }
        ]
    },
    "Nicosia": {
        "name": "Nicosia",
        "country": "Cyprus",
        "country_flag": "",
        "iata_codes": ["LCA"],
        "primary_iata": "LCA",
        "coordinates": {"lat": 35.1856, "lng": 33.3823},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Nicosia Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Nicosia."
            }
        ]
    },
    "Valletta": {
        "name": "Valletta",
        "country": "Malta",
        "country_flag": "",
        "iata_codes": ["MLA"],
        "primary_iata": "MLA",
        "coordinates": {"lat": 35.8989, "lng": 14.5146},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Valletta Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Valletta."
            }
        ]
    },
    "Tirana": {
        "name": "Tirana",
        "country": "Albania",
        "country_flag": "",
        "iata_codes": ["TIA"],
        "primary_iata": "TIA",
        "coordinates": {"lat": 41.3275, "lng": 19.8187},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Tirana Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Tirana."
            }
        ]
    },
    "Skopje": {
        "name": "Skopje",
        "country": "North Macedonia",
        "country_flag": "",
        "iata_codes": ["SKP"],
        "primary_iata": "SKP",
        "coordinates": {"lat": 42.005, "lng": 21.428},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Skopje Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Skopje."
            }
        ]
    },
    "Podgorica": {
        "name": "Podgorica",
        "country": "Montenegro",
        "country_flag": "",
        "iata_codes": ["TGD"],
        "primary_iata": "TGD",
        "coordinates": {"lat": 42.4304, "lng": 19.2594},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Podgorica Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Podgorica."
            }
        ]
    },
    "Sarajevo": {
        "name": "Sarajevo",
        "country": "Bosnia and Herzegovina",
        "country_flag": "",
        "iata_codes": ["SJJ"],
        "primary_iata": "SJJ",
        "coordinates": {"lat": 43.8563, "lng": 18.4131},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Sarajevo Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Sarajevo."
            }
        ]
    },
    "Chisinau": {
        "name": "Chisinau",
        "country": "Moldova",
        "country_flag": "",
        "iata_codes": ["KIV"],
        "primary_iata": "KIV",
        "coordinates": {"lat": 47.0105, "lng": 28.8638},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Chisinau Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Chisinau."
            }
        ]
    },
    "Luxembourg": {
        "name": "Luxembourg",
        "country": "Luxembourg",
        "country_flag": "",
        "iata_codes": ["LUX"],
        "primary_iata": "LUX",
        "coordinates": {"lat": 49.6116, "lng": 6.1319},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Luxembourg Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Luxembourg."
            }
        ]
    },
    "Manchester": {
        "name": "Manchester",
        "country": "UK",
        "country_flag": "",
        "iata_codes": ["MAN"],
        "primary_iata": "MAN",
        "coordinates": {"lat": 53.4808, "lng": -2.2426},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Manchester Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Manchester."
            }
        ]
    },
    "Birmingham": {
        "name": "Birmingham",
        "country": "UK",
        "country_flag": "",
        "iata_codes": ["BHX"],
        "primary_iata": "BHX",
        "coordinates": {"lat": 52.4862, "lng": -1.8904},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Birmingham Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Birmingham."
            }
        ]
    },
    "Glasgow": {
        "name": "Glasgow",
        "country": "UK",
        "country_flag": "",
        "iata_codes": ["GLA"],
        "primary_iata": "GLA",
        "coordinates": {"lat": 55.8642, "lng": -4.2518},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Glasgow Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Glasgow."
            }
        ]
    },
    "Belfast": {
        "name": "Belfast",
        "country": "UK",
        "country_flag": "",
        "iata_codes": ["BFS"],
        "primary_iata": "BFS",
        "coordinates": {"lat": 54.5973, "lng": -5.9301},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Belfast Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Belfast."
            }
        ]
    },
    "Cork": {
        "name": "Cork",
        "country": "Ireland",
        "country_flag": "",
        "iata_codes": ["ORK"],
        "primary_iata": "ORK",
        "coordinates": {"lat": 51.8985, "lng": -8.4756},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Cork Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Cork."
            }
        ]
    },
    "Lyon": {
        "name": "Lyon",
        "country": "France",
        "country_flag": "",
        "iata_codes": ["LYS"],
        "primary_iata": "LYS",
        "coordinates": {"lat": 45.764, "lng": 4.8357},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Lyon Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Lyon."
            }
        ]
    },
    "Marseille": {
        "name": "Marseille",
        "country": "France",
        "country_flag": "",
        "iata_codes": ["MRS"],
        "primary_iata": "MRS",
        "coordinates": {"lat": 43.2965, "lng": 5.3698},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Marseille Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Marseille."
            }
        ]
    },
    "Toulouse": {
        "name": "Toulouse",
        "country": "France",
        "country_flag": "",
        "iata_codes": ["TLS"],
        "primary_iata": "TLS",
        "coordinates": {"lat": 43.6047, "lng": 1.4442},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Toulouse Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Toulouse."
            }
        ]
    },
    "Bordeaux": {
        "name": "Bordeaux",
        "country": "France",
        "country_flag": "",
        "iata_codes": ["BOD"],
        "primary_iata": "BOD",
        "coordinates": {"lat": 44.8378, "lng": -0.5792},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Bordeaux Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Bordeaux."
            }
        ]
    },
    "Nantes": {
        "name": "Nantes",
        "country": "France",
        "country_flag": "",
        "iata_codes": ["NTE"],
        "primary_iata": "NTE",
        "coordinates": {"lat": 47.2184, "lng": -1.5536},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Nantes Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Nantes."
            }
        ]
    },
    "Frankfurt": {
        "name": "Frankfurt",
        "country": "Germany",
        "country_flag": "",
        "iata_codes": ["FRA"],
        "primary_iata": "FRA",
        "coordinates": {"lat": 50.1109, "lng": 8.6821},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Frankfurt Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Frankfurt."
            }
        ]
    },
    "Hamburg": {
        "name": "Hamburg",
        "country": "Germany",
        "country_flag": "",
        "iata_codes": ["HAM"],
        "primary_iata": "HAM",
        "coordinates": {"lat": 53.5511, "lng": 9.9937},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Hamburg Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Hamburg."
            }
        ]
    },
    "Stuttgart": {
        "name": "Stuttgart",
        "country": "Germany",
        "country_flag": "",
        "iata_codes": ["STR"],
        "primary_iata": "STR",
        "coordinates": {"lat": 48.7758, "lng": 9.1829},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Stuttgart Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Stuttgart."
            }
        ]
    },
    "Dusseldorf": {
        "name": "Dusseldorf",
        "country": "Germany",
        "country_flag": "",
        "iata_codes": ["DUS"],
        "primary_iata": "DUS",
        "coordinates": {"lat": 51.2277, "lng": 6.7735},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Dusseldorf Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Dusseldorf."
            }
        ]
    },
    "Cologne": {
        "name": "Cologne",
        "country": "Germany",
        "country_flag": "",
        "iata_codes": ["CGN"],
        "primary_iata": "CGN",
        "coordinates": {"lat": 50.9375, "lng": 6.9603},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Cologne Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Cologne."
            }
        ]
    },
    "Naples": {
        "name": "Naples",
        "country": "Italy",
        "country_flag": "",
        "iata_codes": ["NAP"],
        "primary_iata": "NAP",
        "coordinates": {"lat": 40.8522, "lng": 14.2681},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Naples Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Naples."
            }
        ]
    },
    "Turin": {
        "name": "Turin",
        "country": "Italy",
        "country_flag": "",
        "iata_codes": ["TRN"],
        "primary_iata": "TRN",
        "coordinates": {"lat": 45.0703, "lng": 7.6869},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Turin Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Turin."
            }
        ]
    },
    "Venice": {
        "name": "Venice",
        "country": "Italy",
        "country_flag": "",
        "iata_codes": ["VCE"],
        "primary_iata": "VCE",
        "coordinates": {"lat": 45.4408, "lng": 12.3155},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Venice Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Venice."
            }
        ]
    },
    "Bologna": {
        "name": "Bologna",
        "country": "Italy",
        "country_flag": "",
        "iata_codes": ["BLQ"],
        "primary_iata": "BLQ",
        "coordinates": {"lat": 44.4949, "lng": 11.3426},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Bologna Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Bologna."
            }
        ]
    },
    "Palermo": {
        "name": "Palermo",
        "country": "Italy",
        "country_flag": "",
        "iata_codes": ["PMO"],
        "primary_iata": "PMO",
        "coordinates": {"lat": 38.1157, "lng": 13.3615},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Palermo Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Palermo."
            }
        ]
    },
    "Valencia": {
        "name": "Valencia",
        "country": "Spain",
        "country_flag": "",
        "iata_codes": ["VLC"],
        "primary_iata": "VLC",
        "coordinates": {"lat": 39.4699, "lng": -0.3774},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Valencia Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Valencia."
            }
        ]
    },
    "Bilbao": {
        "name": "Bilbao",
        "country": "Spain",
        "country_flag": "",
        "iata_codes": ["BIO"],
        "primary_iata": "BIO",
        "coordinates": {"lat": 43.263, "lng": -2.935},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Bilbao Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Bilbao."
            }
        ]
    },
    "Malaga": {
        "name": "Malaga",
        "country": "Spain",
        "country_flag": "",
        "iata_codes": ["AGP"],
        "primary_iata": "AGP",
        "coordinates": {"lat": 36.7213, "lng": -4.4213},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Malaga Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Malaga."
            }
        ]
    },
    "Palma": {
        "name": "Palma",
        "country": "Spain",
        "country_flag": "",
        "iata_codes": ["PMI"],
        "primary_iata": "PMI",
        "coordinates": {"lat": 39.5696, "lng": 2.6502},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Palma Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Palma."
            }
        ]
    },
    "Alicante": {
        "name": "Alicante",
        "country": "Spain",
        "country_flag": "",
        "iata_codes": ["ALC"],
        "primary_iata": "ALC",
        "coordinates": {"lat": 38.346, "lng": -0.4907},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Alicante Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Alicante."
            }
        ]
    },
    "Wroclaw": {
        "name": "Wroclaw",
        "country": "Poland",
        "country_flag": "",
        "iata_codes": ["WRO"],
        "primary_iata": "WRO",
        "coordinates": {"lat": 51.1079, "lng": 17.0385},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Wroclaw Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Wroclaw."
            }
        ]
    },
    "Gdansk": {
        "name": "Gdansk",
        "country": "Poland",
        "country_flag": "",
        "iata_codes": ["GDN"],
        "primary_iata": "GDN",
        "coordinates": {"lat": 54.352, "lng": 18.6466},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Gdansk Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Gdansk."
            }
        ]
    },
    "Poznan": {
        "name": "Poznan",
        "country": "Poland",
        "country_flag": "",
        "iata_codes": ["POZ"],
        "primary_iata": "POZ",
        "coordinates": {"lat": 52.4064, "lng": 16.9252},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Poznan Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Poznan."
            }
        ]
    },
    "Katowice": {
        "name": "Katowice",
        "country": "Poland",
        "country_flag": "",
        "iata_codes": ["KTW"],
        "primary_iata": "KTW",
        "coordinates": {"lat": 50.2649, "lng": 19.0238},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Katowice Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Katowice."
            }
        ]
    },
    "Gothenburg": {
        "name": "Gothenburg",
        "country": "Sweden",
        "country_flag": "",
        "iata_codes": ["GOT"],
        "primary_iata": "GOT",
        "coordinates": {"lat": 57.7089, "lng": 11.9746},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Gothenburg Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Gothenburg."
            }
        ]
    },
    "Malmo": {
        "name": "Malmo",
        "country": "Sweden",
        "country_flag": "",
        "iata_codes": ["MMX"],
        "primary_iata": "MMX",
        "coordinates": {"lat": 55.6049, "lng": 13.0038},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Malmo Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Malmo."
            }
        ]
    },
    "Bergen": {
        "name": "Bergen",
        "country": "Norway",
        "country_flag": "",
        "iata_codes": ["BGO"],
        "primary_iata": "BGO",
        "coordinates": {"lat": 60.3913, "lng": 5.3221},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Bergen Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Bergen."
            }
        ]
    },
    "Stavanger": {
        "name": "Stavanger",
        "country": "Norway",
        "country_flag": "",
        "iata_codes": ["SVG"],
        "primary_iata": "SVG",
        "coordinates": {"lat": 58.969, "lng": 5.7331},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Stavanger Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Stavanger."
            }
        ]
    },
    "Tampere": {
        "name": "Tampere",
        "country": "Finland",
        "country_flag": "",
        "iata_codes": ["TMP"],
        "primary_iata": "TMP",
        "coordinates": {"lat": 61.4978, "lng": 23.761},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Tampere Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Tampere."
            }
        ]
    },
    "Turku": {
        "name": "Turku",
        "country": "Finland",
        "country_flag": "",
        "iata_codes": ["TKU"],
        "primary_iata": "TKU",
        "coordinates": {"lat": 60.4518, "lng": 22.2666},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Turku Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Turku."
            }
        ]
    },
    "Brno": {
        "name": "Brno",
        "country": "Czechia",
        "country_flag": "",
        "iata_codes": ["BRQ"],
        "primary_iata": "BRQ",
        "coordinates": {"lat": 49.1951, "lng": 16.6068},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Brno Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Brno."
            }
        ]
    },
    "Ostrava": {
        "name": "Ostrava",
        "country": "Czechia",
        "country_flag": "",
        "iata_codes": ["OSR"],
        "primary_iata": "OSR",
        "coordinates": {"lat": 49.8209, "lng": 18.2625},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Ostrava Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Ostrava."
            }
        ]
    },
    "Aarhus": {
        "name": "Aarhus",
        "country": "Denmark",
        "country_flag": "",
        "iata_codes": ["AAR"],
        "primary_iata": "AAR",
        "coordinates": {"lat": 56.1629, "lng": 10.2039},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Aarhus Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Aarhus."
            }
        ]
    },
    "Billund": {
        "name": "Billund",
        "country": "Denmark",
        "country_flag": "",
        "iata_codes": ["BLL"],
        "primary_iata": "BLL",
        "coordinates": {"lat": 55.7314, "lng": 9.1121},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Billund Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Billund."
            }
        ]
    },
    "Faro": {
        "name": "Faro",
        "country": "Portugal",
        "country_flag": "",
        "iata_codes": ["FAO"],
        "primary_iata": "FAO",
        "coordinates": {"lat": 37.0194, "lng": -7.9322},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Faro Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Faro."
            }
        ]
    },
    "Dubrovnik": {
        "name": "Dubrovnik",
        "country": "Croatia",
        "country_flag": "",
        "iata_codes": ["DBV"],
        "primary_iata": "DBV",
        "coordinates": {"lat": 42.6507, "lng": 18.0944},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Dubrovnik Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Dubrovnik."
            }
        ]
    },
    "Split": {
        "name": "Split",
        "country": "Croatia",
        "country_flag": "",
        "iata_codes": ["SPU"],
        "primary_iata": "SPU",
        "coordinates": {"lat": 43.5081, "lng": 16.4402},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Split Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Split."
            }
        ]
    },
    "Salzburg": {
        "name": "Salzburg",
        "country": "Austria",
        "country_flag": "",
        "iata_codes": ["SZG"],
        "primary_iata": "SZG",
        "coordinates": {"lat": 47.8095, "lng": 13.055},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Salzburg Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Salzburg."
            }
        ]
    },
    "Innsbruck": {
        "name": "Innsbruck",
        "country": "Austria",
        "country_flag": "",
        "iata_codes": ["INN"],
        "primary_iata": "INN",
        "coordinates": {"lat": 47.2692, "lng": 11.4041},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Innsbruck Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Innsbruck."
            }
        ]
    },
    "Geneva": {
        "name": "Geneva",
        "country": "Switzerland",
        "country_flag": "",
        "iata_codes": ["GVA"],
        "primary_iata": "GVA",
        "coordinates": {"lat": 46.2044, "lng": 6.1432},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Geneva Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Geneva."
            }
        ]
    },
    "Basel": {
        "name": "Basel",
        "country": "Switzerland",
        "country_flag": "",
        "iata_codes": ["BSL"],
        "primary_iata": "BSL",
        "coordinates": {"lat": 47.5596, "lng": 7.5886},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Basel Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Basel."
            }
        ]
    },
    "Thessaloniki": {
        "name": "Thessaloniki",
        "country": "Greece",
        "country_flag": "",
        "iata_codes": ["SKG"],
        "primary_iata": "SKG",
        "coordinates": {"lat": 40.6401, "lng": 22.9444},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Thessaloniki Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Thessaloniki."
            }
        ]
    },
    "Heraklion": {
        "name": "Heraklion",
        "country": "Greece",
        "country_flag": "",
        "iata_codes": ["HER"],
        "primary_iata": "HER",
        "coordinates": {"lat": 35.3387, "lng": 25.1442},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {
                "name": "Heraklion Center",
                "scores": {"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0},
                "transit_minutes_to_center": 0,
                "description": "Central district of Heraklion."
            }
        ]
    }
}