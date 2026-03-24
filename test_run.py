import asyncio
from models import OptimizeRequest, TripSettings, TravelerInput, FlightSearchTask
import scraper
import engine

async def main():
    req = OptimizeRequest(
        travelers=[TravelerInput(name="Alice", origin="London", max_travel_hours=12, max_stops=1),
                   TravelerInput(name="Bob", origin="Berlin", max_travel_hours=12, max_stops=1)],
        settings=TripSettings(earliest_departure="2024-12-01", latest_return="2024-12-05", duration_nights=3, vibes=[], destinations=["Barcelona", "Paris"])
    )
    tasks = [
        FlightSearchTask(task_id="1", traveler_name="Alice", origin_iata="LHR", origin_city="London", destination_iata="BCN", destination_city="Barcelona", outbound_date="2024-12-01", max_travel_hours=12, max_stops=1, is_gateway_leg=False),
        FlightSearchTask(task_id="2", traveler_name="Bob", origin_iata="BER", origin_city="Berlin", destination_iata="BCN", destination_city="Barcelona", outbound_date="2024-12-01", max_travel_hours=12, max_stops=1, is_gateway_leg=False),
        FlightSearchTask(task_id="3", traveler_name="Alice", origin_iata="LHR", origin_city="London", destination_iata="CDG", destination_city="Paris", outbound_date="2024-12-01", max_travel_hours=12, max_stops=1, is_gateway_leg=False),
        FlightSearchTask(task_id="4", traveler_name="Bob", origin_iata="BER", origin_city="Berlin", destination_iata="CDG", destination_city="Paris", outbound_date="2024-12-01", max_travel_hours=12, max_stops=1, is_gateway_leg=False)
    ]
    try:
        scraped = await scraper.search_flights(tasks)
        print("Scraped:", len(scraped))
        res = engine.optimize(scraped, tasks, req)
        print("Optimized Successfully:", res.keys() if isinstance(res, dict) else res)
    except Exception as e:
        import traceback
        traceback.print_exc()

asyncio.run(main())
