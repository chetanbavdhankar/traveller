# Traveller

Find the mathematical minimum for group travel. Traveller syncs traveler schedules and uses real-time scraping of Google Flights to find the best central meeting hub.

## Architecture
- **Backend**: FastAPI (Python 3.11+) orchestrating 4 AI agents (Scout, Matchmaker, Neighborhood, Optimizer).
- **Data Source**: Live parallel web scraping via async Playwright (`playwright-stealth`).
- **Frontend**: Single-file vanilla HTML/JS with SSE streams for progress updates. Dark glassmorphism UI.

## Setup Instructions
```bash
# 1. Install dependencies
pip install -r requirements.txt
playwright install chromium

# 2. Run the server
python server.py
# Server will start on http://localhost:8345 and open your browser automatically.
```

## Usage Examples
1. The app will automatically open `http://localhost:8345` in your browser.
2. Add your travelers (Name, Origin City, earliest departure time, max flight length).
3. Set your trip duration and dates.
4. Input your single targeted Destination City.
5. Hit "Find Global Minimum".

## Recent Changes
- **Why**: Transitioned from multi-destination "vibe" search to a targeted single-destination model to streamline search and improve scraper reliability. Fixed persistent 500 errors caused by Windows Unicode encoding of surrogate characters.
- **How**: 
  - Rewrote scraping logic in `scraper.py` using robust Playwright native locators (reading `aria-label`s) instead of BeautifulSoup to accurately parse dynamic Google Flights pricing in multiple currencies.
  - Simplified frontend (`index.html`) and backend (`engine.py`, `models.py`) to process a single destination input instead of multi-city vibe metrics.
  - Enforced UTF-8 encoding on `sys.stdout` and `ensure_ascii=True` on JSON serialization in `server.py` to prevent Windows console crashes from emoji flags.
- **Impact**: Dramatically improved data extraction stability, eliminated server-side crashes on Windows, and provided a cleaner, faster user experience focused on a specific meeting point. Scalability remains tightly bound by CAPTCHA limits unless rotating proxies are introduced.

## End-to-End Test Checklist
- [x] Server starts, `GET /health` returns `{"status": "ok"}`
- [x] UI loads correctly at `http://localhost:8345`, form validation triggers correctly
- [x] Two travelers added (if testing)
- [x] Accommodation links point correctly to `booking.com` with real date ranges pre-filled
- [x] Disconnecting internet cleanly aborts search

## Technical Debt Log
- **Selector Fragility**: While Playwright locators using `aria-label`s are much more robust than older regex approaches, Google Flights and Skyscanner DOMs still evolve. Locators may need occasional updates if the UI structure changes drastically.
- **Captcha Blocks**: Google will throw hard blocks after 20-30 successive proxy-less scrapes. Rotating proxy integration is recommended if scaling.

## Troubleshooting
**1. CAPTCHA / bot block**
- **Symptom**: Repeated output of "CAPTCHA detected" in terminal.
- **Fix**: The scraper will naturally backoff for 45 seconds and rotate user agents.

**2. Slow page load / selector timeout**
- **Symptom**: `PlaywrightTimeoutError`.
- **Fix**: Check terminal logs. The algorithm skips these safely.

**3. Zero results returned despite flights existing**
- **Symptom**: "No flights found" consistently.
- **Fix**: Ensure the departure date is in the future.
