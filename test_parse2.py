from bs4 import BeautifulSoup
import re

with open("google_dump_postconsent.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "lxml")
cards = soup.find_all("li")

def parse_price(p_str: str):
    match = re.search(r'(?:€|EUR|£|GBP)\s*([\d,\.]+)', p_str)
    if match: return float(match.group(1).replace(',', ''))
    match = re.search(r'([\d,\.]+)\s*(?:€|EUR|£|GBP)', p_str)
    if match: return float(match.group(1).replace(',', ''))
    return None

results = []
for card in cards:
    text = card.get_text(separator=' ', strip=True)
    if ('hr' in text or ' h ' in text) and ('min' in text or ' m ' in text or 'm' in text):
        price = parse_price(text)
        if price is None:
            continue
        print("PARSED CARD:", text)
        results.append(price)

print("Parsed prices:", results)
