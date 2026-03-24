import json
import re

new_cities = [
    # Capitals
    ("Helsinki", "Finland", "FI", "HEL", 60.1695, 24.9354),
    ("Oslo", "Norway", "NO", "OSL", 59.9139, 10.7522),
    ("Stockholm", "Sweden", "SE", "ARN", 59.3293, 18.0686),
    ("Riga", "Latvia", "LV", "RIX", 56.9496, 24.1052),
    ("Tallinn", "Estonia", "EE", "TLL", 59.4370, 24.7536),
    ("Vilnius", "Lithuania", "LT", "VNO", 54.6872, 25.2797),
    ("Bucharest", "Romania", "RO", "OTP", 44.4268, 26.1025),
    ("Sofia", "Bulgaria", "BG", "SOF", 42.6977, 23.3219),
    ("Belgrade", "Serbia", "RS", "BEG", 44.7866, 20.4489),
    ("Zagreb", "Croatia", "HR", "ZAG", 45.8150, 15.9819),
    ("Ljubljana", "Slovenia", "SI", "LJU", 46.0569, 14.5058),
    ("Bratislava", "Slovakia", "SK", "BTS", 48.1486, 17.1077),
    ("Reykjavik", "Iceland", "IS", "KEF", 64.1466, -21.9426),
    ("Nicosia", "Cyprus", "CY", "LCA", 35.1856, 33.3823),
    ("Valletta", "Malta", "MT", "MLA", 35.8989, 14.5146),
    ("Tirana", "Albania", "AL", "TIA", 41.3275, 19.8187),
    ("Skopje", "North Macedonia", "MK", "SKP", 42.0050, 21.4280),
    ("Podgorica", "Montenegro", "ME", "TGD", 42.4304, 19.2594),
    ("Sarajevo", "Bosnia and Herzegovina", "BA", "SJJ", 43.8563, 18.4131),
    ("Chisinau", "Moldova", "MD", "KIV", 47.0105, 28.8638),
    ("Luxembourg", "Luxembourg", "LU", "LUX", 49.6116, 6.1319),
    # Additional major cities in UK/Ireland
    ("Manchester", "UK", "GB", "MAN", 53.4808, -2.2426),
    ("Birmingham", "UK", "GB", "BHX", 52.4862, -1.8904),
    ("Glasgow", "UK", "GB", "GLA", 55.8642, -4.2518),
    ("Belfast", "UK", "GB", "BFS", 54.5973, -5.9301),
    ("Cork", "Ireland", "IE", "ORK", 51.8985, -8.4756),
    # France
    ("Lyon", "France", "FR", "LYS", 45.7640, 4.8357),
    ("Marseille", "France", "FR", "MRS", 43.2965, 5.3698),
    ("Toulouse", "France", "FR", "TLS", 43.6047, 1.4442),
    ("Bordeaux", "France", "FR", "BOD", 44.8378, -0.5792),
    ("Nantes", "France", "FR", "NTE", 47.2184, -1.5536),
    # Germany
    ("Frankfurt", "Germany", "DE", "FRA", 50.1109, 8.6821),
    ("Hamburg", "Germany", "DE", "HAM", 53.5511, 9.9937),
    ("Stuttgart", "Germany", "DE", "STR", 48.7758, 9.1829),
    ("Dusseldorf", "Germany", "DE", "DUS", 51.2277, 6.7735),
    ("Cologne", "Germany", "DE", "CGN", 50.9375, 6.9603),
    # Italy
    ("Naples", "Italy", "IT", "NAP", 40.8522, 14.2681),
    ("Turin", "Italy", "IT", "TRN", 45.0703, 7.6869),
    ("Venice", "Italy", "IT", "VCE", 45.4408, 12.3155),
    ("Bologna", "Italy", "IT", "BLQ", 44.4949, 11.3426),
    ("Palermo", "Italy", "IT", "PMO", 38.1157, 13.3615),
    # Spain
    ("Valencia", "Spain", "ES", "VLC", 39.4699, -0.3774),
    ("Bilbao", "Spain", "ES", "BIO", 43.2630, -2.9350),
    ("Malaga", "Spain", "ES", "AGP", 36.7213, -4.4213),
    ("Palma", "Spain", "ES", "PMI", 39.5696, 2.6502),
    ("Alicante", "Spain", "ES", "ALC", 38.3460, -0.4907),
    # Poland
    ("Wroclaw", "Poland", "PL", "WRO", 51.1079, 17.0385),
    ("Gdansk", "Poland", "PL", "GDN", 54.3520, 18.6466),
    ("Poznan", "Poland", "PL", "POZ", 52.4064, 16.9252),
    ("Katowice", "Poland", "PL", "KTW", 50.2649, 19.0238),
    # Others
    ("Gothenburg", "Sweden", "SE", "GOT", 57.7089, 11.9746),
    ("Malmo", "Sweden", "SE", "MMX", 55.6049, 13.0038),
    ("Bergen", "Norway", "NO", "BGO", 60.3913, 5.3221),
    ("Stavanger", "Norway", "NO", "SVG", 58.9690, 5.7331),
    ("Tampere", "Finland", "FI", "TMP", 61.4978, 23.7610),
    ("Turku", "Finland", "FI", "TKU", 60.4518, 22.2666),
    ("Brno", "Czechia", "CZ", "BRQ", 49.1951, 16.6068),
    ("Ostrava", "Czechia", "CZ", "OSR", 49.8209, 18.2625),
    ("Aarhus", "Denmark", "DK", "AAR", 56.1629, 10.2039),
    ("Billund", "Denmark", "DK", "BLL", 55.7314, 9.1121),
    ("Faro", "Portugal", "PT", "FAO", 37.0194, -7.9322),
    ("Dubrovnik", "Croatia", "HR", "DBV", 42.6507, 18.0944),
    ("Split", "Croatia", "HR", "SPU", 43.5081, 16.4402), 
    ("Salzburg", "Austria", "AT", "SZG", 47.8095, 13.0550),
    ("Innsbruck", "Austria", "AT", "INN", 47.2692, 11.4041),
    ("Geneva", "Switzerland", "CH", "GVA", 46.2044, 6.1432),
    ("Basel", "Switzerland", "CH", "BSL", 47.5596, 7.5886),
    ("Thessaloniki", "Greece", "GR", "SKG", 40.6401, 22.9444),
    ("Heraklion", "Greece", "GR", "HER", 35.3387, 25.1442)
]

def iso_to_emoji(iso_code: str) -> str:
    return "".join(chr(ord(c) + 127397) for c in iso_code.upper())

cities_dict_entries = []

for city, country, iso_code, iata, lat, lng in new_cities:
    emoji_flag = ""
    # We will format this into the dictionary format of CITIES
    block = f'''    "{city}": {{
        "name": "{city}",
        "country": "{country}",
        "country_flag": "{emoji_flag}",
        "iata_codes": ["{iata}"],
        "primary_iata": "{iata}",
        "coordinates": {{"lat": {lat}, "lng": {lng}}},
        "has_train_station": True,
        "gateway_airports": [],
        "neighborhoods": [
            {{
                "name": "{city} Center",
                "scores": {{"vibe": 8.0, "walkability": 8.5, "safety": 8.5, "transit": 8.0}},
                "transit_minutes_to_center": 0,
                "description": "Central district of {city}."
            }}
        ]
    }}'''
    cities_dict_entries.append(block)

new_content = ",\n".join(cities_dict_entries)

with open("data.py", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the last `}\n}` with `},\n` + new_content + `\n}`
# Using regex to match the end of the file safely
content = re.sub(r'}\s*}\s*$', '},\n' + new_content + '\n}', content)

with open("data.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Successfully injected 60+ new cities into data.py")
