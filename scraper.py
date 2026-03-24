import asyncio
import random
import re
from typing import List, Optional
from playwright.async_api import async_playwright, BrowserContext, Page
from playwright_stealth import stealth_async

from models import FlightSearchTask, FlightSearchResult
from data import skyscanner_flight_link

# Max 3 concurrent browser contexts
semaphore = asyncio.Semaphore(3)
init_lock = asyncio.Lock()

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
]

VIEWPORTS = [
    {"width": 1920, "height": 1080},
    {"width": 1440, "height": 900},
    {"width": 1366, "height": 768},
    {"width": 1280, "height": 800}
]

EXCHANGE_RATES_TO_EUR = {
    "EUR": 1.0, "€": 1.0,
    "GBP": 1.16, "£": 1.16,
    "USD": 0.92, "$": 0.92,
    "PLN": 0.23, "ZL": 0.23,
    "CHF": 1.02,
    "SEK": 0.089,
    "DKK": 0.13,
    "NOK": 0.086,
    "HUF": 0.0025,
    "CZK": 0.040
}


async def random_delay(page=None):
    delay = random.uniform(1500, 4000)
    if page:
        await page.wait_for_timeout(delay)
    else:
        await asyncio.sleep(delay / 1000.0)


async def init_context(browser) -> BrowserContext:
    vp = random.choice(VIEWPORTS)
    ua = random.choice(USER_AGENTS)
    return await browser.new_context(
        viewport=vp, user_agent=ua,
        locale="en-US", timezone_id="Europe/London"
    )


def parse_time(t_str: str) -> Optional[str]:
    m = re.search(r'(\d{1,2}):(\d{2})([\s\u202f]*[APap][Mm])?', t_str)
    if m:
        h, mn = int(m.group(1)), int(m.group(2))
        ampm = m.group(3)
        if ampm:
            ampm = ampm.strip().lower()
            if ampm == 'pm' and h < 12: h += 12
            if ampm == 'am' and h == 12: h = 0
        return f"{h:02d}:{mn:02d}"
    return None


def parse_duration(d_str: str) -> Optional[int]:
    hr = mn = 0
    hm = re.search(r'(\d+)[\s\u202f]*[hH]', d_str)
    mm = re.search(r'(\d+)[\s\u202f]*[mM]', d_str)
    if hm: hr = int(hm.group(1))
    if mm: mn = int(mm.group(1))
    return hr * 60 + mn if hr > 0 or mn > 0 else None


def parse_price(p_str: str) -> Optional[float]:
    """Extract price from text, auto-converting to EUR."""
    currencies = "|".join(re.escape(k) for k in EXCHANGE_RATES_TO_EUR.keys())
    # Symbol/code BEFORE number
    match = re.search(rf'({currencies})\s*([\d,\.]+)', p_str, re.IGNORECASE)
    if match:
        curr = match.group(1).upper()
        val = float(match.group(2).replace(',', ''))
        return val * EXCHANGE_RATES_TO_EUR.get(curr, 1.0)
    # Number BEFORE symbol/code
    match = re.search(rf'([\d,\.]+)\s*({currencies})', p_str, re.IGNORECASE)
    if match:
        curr = match.group(2).upper()
        val = float(match.group(1).replace(',', ''))
        return val * EXCHANGE_RATES_TO_EUR.get(curr, 1.0)
    return None


# ─────────────────────────────────────────────────────────────
# Google Flights – Playwright Locator-based extraction
# ─────────────────────────────────────────────────────────────

async def _dismiss_consent(page: Page):
    """Click away Google's GDPR consent overlay."""
    for label in ["Reject all", "Accept all"]:
        try:
            btn = page.get_by_role("button", name=label)
            if await btn.count() > 0:
                await btn.first.click()
                print(f"  [consent] Clicked '{label}'")
                await page.wait_for_timeout(2000)
                return
        except Exception:
            pass


async def scrape_google_flights(page: Page, task: FlightSearchTask) -> List[dict]:
    """Use Playwright locators to extract flight cards from Google Flights."""
    print(f"[{task.traveler_name}] Waiting for flight results to render...")
    await page.wait_for_timeout(5000)
    await page.evaluate("window.scrollBy(0, 800)")
    await random_delay(page)

    # Google wraps each flight result in an <li> inside a list with role="list"
    cards = page.locator('li').filter(has=page.locator('span[role="text"]'))
    card_count = await cards.count()
    print(f"[{task.traveler_name}] Found {card_count} flight card elements via locator.")

    results = []
    for i in range(min(card_count, 15)):
        try:
            card = cards.nth(i)
            text = await card.inner_text()
            text = text.replace('\n', ' ').replace('\xa0', ' ')

            # Price — from aria-label on spans with role="text"
            price = None
            price_spans = card.locator('span[role="text"]')
            price_count = await price_spans.count()
            for j in range(price_count):
                aria = await price_spans.nth(j).get_attribute("aria-label") or ""
                span_text = await price_spans.nth(j).inner_text()
                # aria-label like "229 euros" or "198 British pounds"
                aria_price = re.search(r'([\d,]+)\s+(?:euro|pound|dollar|zlot|kron|franc)', aria, re.IGNORECASE)
                if aria_price:
                    raw_val = float(aria_price.group(1).replace(',', ''))
                    if 'euro' in aria.lower():
                        price = raw_val
                    elif 'pound' in aria.lower():
                        price = raw_val * 1.16
                    elif 'dollar' in aria.lower():
                        price = raw_val * 0.92
                    elif 'zlot' in aria.lower():
                        price = raw_val * 0.23
                    elif 'kron' in aria.lower():
                        price = raw_val * 0.089
                    elif 'franc' in aria.lower():
                        price = raw_val * 1.02
                    else:
                        price = raw_val
                    break
                # Fallback: parse the visible text of the span
                p = parse_price(span_text)
                if p:
                    price = p
                    break

            if price is None:
                # Last fallback: parse the full card text
                price = parse_price(text)

            if price is None or price < 5:
                continue

            # Times
            times = re.findall(r'(\d{1,2}:\d{2}[\s\u202f]*(?:[APap][Mm])?)', text)
            if len(times) < 2:
                continue
            departure_time = parse_time(times[0])
            arrival_time = parse_time(times[1])

            # Duration
            duration_minutes = parse_duration(text)

            # Stops
            stops = 0
            stop_match = re.search(r'(\d+)\s*stop', text, re.IGNORECASE)
            if stop_match:
                stops = int(stop_match.group(1))
            elif 'nonstop' in text.lower() or 'direct' in text.lower():
                stops = 0

            # Layover Duration
            layover_duration_minutes = 0
            # Matches formats like "1 hr 30 min layover in FRA"
            for m in re.finditer(r'(?:(?:(\d+)\s*hr)?\s*(?:(\d+)\s*min)?)\s*layover', text, re.IGNORECASE):
                hr = int(m.group(1)) if m.group(1) else 0
                mn = int(m.group(2)) if m.group(2) else 0
                layover_duration_minutes += (hr * 60 + mn)

            # Airline — typically appears after the time block
            airline = "Unknown Airline"
            airline_match = re.search(r'(?:AM|PM|am|pm)\s+(.+?)\s+\d+\s*h', text)
            if airline_match:
                airline = airline_match.group(1).strip()[:30] or "Unknown Airline"

            results.append({
                "price_eur": round(price, 2),
                "airline": airline,
                "departure_time": departure_time,
                "arrival_time": arrival_time,
                "duration_minutes": duration_minutes,
                "stops": stops,
                "layover_airports": [],
                "layover_duration_minutes": layover_duration_minutes
            })
        except Exception as ex:
            print(f"[{task.traveler_name}] Card {i} parse error: {ex}")
            continue

    # Deduplicate
    deduped, seen = [], set()
    for r in results:
        key = (r['price_eur'], r['departure_time'], r['duration_minutes'])
        if key not in seen:
            seen.add(key)
            deduped.append(r)
    return sorted(deduped, key=lambda x: x['price_eur'])[:8]


# ─────────────────────────────────────────────────────────────
# Skyscanner fallback (kept simple, same locator approach)
# ─────────────────────────────────────────────────────────────

async def scrape_skyscanner(page: Page, task: FlightSearchTask) -> List[dict]:
    """Fallback scraper for Skyscanner."""
    await page.wait_for_timeout(5000)
    await random_delay(page)

    # Skyscanner uses various div wrappers — grab all text and parse
    from bs4 import BeautifulSoup
    html = await page.content()
    soup = BeautifulSoup(html, 'lxml')
    cards = soup.find_all('div', class_=re.compile('Ticket|Card', re.I))
    if not cards:
        cards = soup.find_all('div', attrs={"role": "button"})

    results = []
    for card in cards:
        text = card.get_text(separator=' ', strip=True)
        price = parse_price(text)
        if price is None or price < 5:
            continue
        times = re.findall(r'(\d{1,2}:\d{2})', text)
        if len(times) < 2:
            continue
        duration_minutes = parse_duration(text)
        if not duration_minutes:
            continue
        stops = 0
        if '1 stop' in text.lower(): stops = 1
        elif '2 stop' in text.lower(): stops = 2
        results.append({
            "price_eur": round(price, 2),
            "airline": "Skyscanner Flight",
            "departure_time": parse_time(times[0]),
            "arrival_time": parse_time(times[1]),
            "duration_minutes": duration_minutes,
            "stops": stops,
            "layover_airports": [],
            "layover_duration_minutes": 0
        })

    deduped, seen = [], set()
    for r in results:
        key = (r['price_eur'], r['departure_time'])
        if key not in seen:
            seen.add(key)
            deduped.append(r)
    return sorted(deduped, key=lambda x: x['price_eur'])[:8]


# ─────────────────────────────────────────────────────────────
# Task Execution
# ─────────────────────────────────────────────────────────────

async def execute_task(browser, task: FlightSearchTask, push_progress_cb=None) -> FlightSearchResult:
    booking_link = skyscanner_flight_link(task.origin_iata, task.destination_iata, task.outbound_date, task.return_date)

    base_res = {
        "task_id": task.task_id,
        "traveler_name": task.traveler_name,
        "origin": task.origin_iata,
        "destination": task.destination_iata,
        "is_gateway_route": task.is_gateway_leg,
        "gateway_ground_link": task.gateway_ground_link,
        "booking_link": booking_link,
    }

    url_google = f"https://www.google.com/travel/flights?q=Flights+from+{task.origin_iata}+to+{task.destination_iata}+on+{task.outbound_date}"

    def format_ss_date(d_str: str) -> str:
        parts = d_str.split('-')
        return parts[2] + parts[1] + parts[0][2:]

    url_skyscanner = f"https://www.skyscanner.net/transport/flights/{task.origin_iata.lower()}/{task.destination_iata.lower()}/{format_ss_date(task.outbound_date)}/"
    if task.return_date:
        url_skyscanner += f"{format_ss_date(task.return_date)}/"

    if push_progress_cb:
        push_progress_cb(f"Scraping {task.traveler_name}: {task.origin_iata} -> {task.destination_iata}")

    context = None
    for attempt in range(1, 4):
        try:
            async with init_lock:
                context = await init_context(browser)
                page = await context.new_page()
                await stealth_async(page)

            print(f"[{task.traveler_name}] Google Flights (Att {attempt}): {task.origin_iata}->{task.destination_iata}")
            r = await page.goto(url_google, timeout=30000, wait_until="domcontentloaded")
            print(f"[{task.traveler_name}] GOTO completed")

            await _dismiss_consent(page)
            
            if task.cabin_bags > 0 or task.checked_bags > 0:
                print(f"[{task.traveler_name}] Setting Baggage: Cabin={task.cabin_bags}, Checked={task.checked_bags}")
                try:
                    bags_btn = page.locator('button[aria-label="Bags"], button:has-text("Bags")').first
                    await bags_btn.wait_for(state="visible", timeout=5000)
                    await bags_btn.click()
                    
                    if task.cabin_bags > 0:
                        add_cabin_btn = page.locator('button[aria-label="Add a carry-on bag"], button[aria-label="Increase carry-on bags"]').first
                        for _ in range(task.cabin_bags):
                            await add_cabin_btn.click()
                            await page.wait_for_timeout(300)
                            
                    if task.checked_bags > 0:
                        add_check_btn = page.locator('button[aria-label="Add a checked bag"], button[aria-label="Increase checked bags"]').first
                        for _ in range(task.checked_bags):
                            await add_check_btn.click()
                            await page.wait_for_timeout(300)
                            
                    done_btn = page.locator('button:has-text("Done")').last
                    await done_btn.click()
                    await page.wait_for_timeout(3000)
                except Exception as ex:
                    print(f"[{task.traveler_name}] Baggage filter warning: {ex}")

            if r and r.status == 429:
                print(f"[{task.traveler_name}] 429 Rate limit. Sleep 60s.")
                await asyncio.sleep(60)
                await context.close()
                continue

            title = await page.title()
            if "unusual traffic" in title.lower() or await page.locator(".g-recaptcha, iframe[src*='recaptcha']").count() > 0:
                print(f"[{task.traveler_name}] CAPTCHA detected, waiting 45s (Att {attempt}/3)")
                await asyncio.sleep(45)
                await context.close()
                continue

            # Check for "No flights found"
            body_text = ""
            try:
                body_text = await page.locator('body').inner_text(timeout=5000)
            except Exception:
                pass

            if "No flights found" in body_text or "Try adjusting your search" in body_text:
                print(f"[{task.traveler_name}] 'No flights found' on Google. Trying Skyscanner...")
                google_results = []
            else:
                print(f"[{task.traveler_name}] Extracting flights via Playwright locators...")
                google_results = await scrape_google_flights(page, task)
                print(f"[{task.traveler_name}] Extracted {len(google_results)} flights from Google.")

            if google_results:
                best = google_results[0]
                await context.close()
                if push_progress_cb:
                    push_progress_cb(f"Found EUR {best['price_eur']} for {task.traveler_name}: {task.origin_iata} -> {task.destination_iata}")
                return FlightSearchResult(**base_res, **best, source="google_flights")

            # Skyscanner fallback
            print(f"[{task.traveler_name}] Falling back to Skyscanner: {task.origin_iata}->{task.destination_iata}")
            r2 = await page.goto(url_skyscanner, timeout=30000)
            if r2 and r2.status == 429:
                await asyncio.sleep(60)
                await context.close()
                continue

            ss_results = await scrape_skyscanner(page, task)
            if ss_results:
                best = ss_results[0]
                await context.close()
                if push_progress_cb:
                    push_progress_cb(f"Found EUR {best['price_eur']} for {task.traveler_name}: {task.origin_iata} -> {task.destination_iata} (Skyscanner)")
                return FlightSearchResult(**base_res, **best, source="skyscanner")

            await context.close()
            reason = f"No flights found on Google Flights or Skyscanner for {task.origin_iata} -> {task.destination_iata} on {task.outbound_date}"
            if push_progress_cb:
                push_progress_cb(f"No flights found for {task.traveler_name}: {task.origin_iata} -> {task.destination_iata}")
            return FlightSearchResult(**base_res, source="none", error=True, error_reason=reason)

        except Exception as e:
            print(f"[{task.traveler_name}] Exception on {task.origin_iata}->{task.destination_iata}: {e}")
            if context:
                try: await context.close()
                except: pass
            if attempt == 3:
                if push_progress_cb:
                    push_progress_cb(f"Error for {task.traveler_name}: {task.origin_iata} -> {task.destination_iata}")
                return FlightSearchResult(**base_res, source="none", error=True, error_reason=str(e))

    return FlightSearchResult(**base_res, source="none", error=True, error_reason="Max retries reached")


async def search_task_wrapper(browser, task: FlightSearchTask, push_progress_cb=None) -> FlightSearchResult:
    async with semaphore:
        res = await execute_task(browser, task, push_progress_cb)
        if not res.error:
            if res.duration_minutes is not None and res.duration_minutes > task.max_travel_hours * 60:
                res.error = True
                res.error_reason = f"Duration {res.duration_minutes}m exceeds max {task.max_travel_hours}h"
            elif res.stops is not None and res.stops > task.max_stops:
                res.error = True
                res.error_reason = f"Stops {res.stops} exceeds max {task.max_stops}"
        return res


async def search_flights(tasks: List[FlightSearchTask], push_progress_cb=None) -> List[FlightSearchResult]:
    import copy
    
    # Group tasks by identical route to avoid redundant scraping
    grouped_tasks = {}
    for t in tasks:
        key = (t.origin_iata, t.destination_iata, t.outbound_date, t.return_date, t.is_gateway_leg, t.direction, t.cabin_bags, t.checked_bags)
        if key not in grouped_tasks:
            grouped_tasks[key] = []
        grouped_tasks[key].append(t)
        
    unique_tasks = [group[0] for group in grouped_tasks.values()]
    
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        cors = [search_task_wrapper(browser, t, push_progress_cb) for t in unique_tasks]
        unique_results = await asyncio.gather(*cors, return_exceptions=True)
        await browser.close()

    task_res_map = {t.task_id: res for t, res in zip(unique_tasks, unique_results)}
    final_results = []
    
    for t in tasks:
        key = (t.origin_iata, t.destination_iata, t.outbound_date, t.return_date, t.is_gateway_leg, t.direction, t.cabin_bags, t.checked_bags)
        rep_task_id = grouped_tasks[key][0].task_id
        res = task_res_map[rep_task_id]
        
        if isinstance(res, Exception):
            booking_link = skyscanner_flight_link(t.origin_iata, t.destination_iata, t.outbound_date, t.return_date)
            final_results.append(FlightSearchResult(
                task_id=t.task_id, traveler_name=t.traveler_name,
                origin=t.origin_iata, destination=t.destination_iata,
                is_gateway_route=t.is_gateway_leg, gateway_ground_link=t.gateway_ground_link,
                booking_link=booking_link, source="none", error=True, error_reason=str(res)
            ))
        else:
            cloned_res = copy.deepcopy(res)
            cloned_res.task_id = t.task_id
            cloned_res.traveler_name = t.traveler_name
            # Re-apply strict constraints per-traveler since bounds might differ
            if cloned_res.duration_minutes is not None and cloned_res.duration_minutes > t.max_travel_hours * 60:
                cloned_res.error = True
                cloned_res.error_reason = f"Duration {cloned_res.duration_minutes}m exceeds max {t.max_travel_hours}h"
            elif cloned_res.stops is not None and cloned_res.stops > t.max_stops:
                cloned_res.error = True
                cloned_res.error_reason = f"Stops {cloned_res.stops} exceeds max {t.max_stops}"
            final_results.append(cloned_res)
            
    return final_results
