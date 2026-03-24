from bs4 import BeautifulSoup
import re

with open("google_dump_postconsent.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "lxml")
cards = soup.find_all("li")

print("Found", len(cards), "LIs")
valid = 0
for c in cards:
    text = c.get_text(separator=" ", strip=True)
    if "LHR" in text or "WAW" in text:
        if len(text) > 20 and len(text) < 500:
            print("--- LI MATCH ---")
            print(text)
            valid += 1
            if valid > 5: break

if valid == 0:
    print("No matching LIs. Checking DIVs...")
    divs = soup.find_all("div")
    for d in divs:
         text = d.get_text(separator=" ", strip=True)
         if "LHR" in text and "WAW" in text and re.search(r"\d+:\d+", text):
             if len(text) > 20 and len(text) < 200:
                 print("--- DIV MATCH ---")
                 print(text)
                 valid += 1
                 if valid > 5: break
