import asyncio
import sys
import traceback

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from models import FlightSearchTask
import scraper

async def main():
    tasks = [
        FlightSearchTask(
            task_id="test_alice", traveler_name="Alice",
            origin_iata="LHR", origin_city="London",
            destination_iata="WAW", destination_city="Warsaw",
            outbound_date="2026-03-29", return_date="2026-04-01",
            max_travel_hours=10, max_stops=1,
            is_gateway_leg=False
        )
    ]
    
    def progress(msg):
        safe_msg = msg.encode('ascii', errors='replace').decode('ascii')
        print(f"[progress] {safe_msg}")
    
    try:
        results = await scraper.search_flights(tasks, progress)
        for r in results:
            print(f"Result: error={r.error}, price={r.price_eur}, airline={r.airline}, source={r.source}")
            if r.error:
                safe_reason = (r.error_reason or "").encode('ascii', errors='replace').decode('ascii')
                print(f"  Error reason: {safe_reason}")
    except Exception as e:
        tb = traceback.format_exc()
        safe_tb = tb.encode('ascii', errors='replace').decode('ascii')
        print(f"EXCEPTION: {safe_tb}")

asyncio.run(main())
