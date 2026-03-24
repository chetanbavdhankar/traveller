import asyncio
import uuid
import sys
from typing import Dict, List, Set

# Force UTF-8 output on Windows to prevent UnicodeEncodeError from surrogates
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json

from models import OptimizeRequest, FlightSearchTask
from data import CITIES
import scraper
import engine

app = FastAPI(title="Hodophile API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Session-ID"]
)

session_queues: Dict[str, asyncio.Queue] = {}

def push_progress(session_id: str, stage: str, message: str, percent: int):
    # Strip surrogates that crash Windows console encoding
    message = message.encode('utf-8', errors='replace').decode('utf-8')
    if session_id in session_queues:
        event = {
            "stage": stage,
            "message": message,
            "percent": percent
        }
        session_queues[session_id].put_nowait(event)

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>index.html not found</h1>"

@app.get("/cities")
async def get_cities():
    cities_list = []
    for k, v in CITIES.items():
        cities_list.append({
            "name": v["name"],
            "country": v["country"]
        })
    return {"cities": sorted(cities_list, key=lambda x: x["name"])}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/optimize/progress")
async def progress_stream(session_id: str, request: Request):
    if session_id not in session_queues:
        session_queues[session_id] = asyncio.Queue()

    async def event_generator():
        q = session_queues[session_id]
        try:
            while True:
                if await request.is_disconnected():
                    break
                event = await q.get()
                yield f"data: {json.dumps(event, ensure_ascii=True)}\n\n"
                if event.get("percent") == 100 or event.get("stage") == "error" or event.get("stage") == "done":
                    break
        except asyncio.CancelledError:
            pass
        finally:
            if session_id in session_queues:
                del session_queues[session_id]
                
    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.post("/optimize")
async def optimize_endpoint(request: OptimizeRequest):
    import datetime
    try:
        out_dt = datetime.datetime.strptime(request.settings.earliest_departure, "%Y-%m-%d")
        ret_dt = datetime.datetime.strptime(request.settings.latest_return, "%Y-%m-%d")
        if out_dt >= ret_dt:
            raise HTTPException(status_code=422, detail="latest_return must be strictly after earliest_departure")
        if (ret_dt - out_dt).days < request.settings.duration_nights:
            raise HTTPException(status_code=422, detail="Date window is too small for requested duration_nights")
    except ValueError as e:
        raise HTTPException(status_code=422, detail="Invalid date format, YYYY-MM-DD required")

    session_id = str(uuid.uuid4())
    
    if session_id not in session_queues:
        session_queues[session_id] = asyncio.Queue()
        
    def progress_cb(msg: str):
        push_progress(session_id, "scout", msg, 50)
        
    try:
        push_progress(session_id, "scout", "Generating search tasks...", 5)
        
        tasks_to_run = []
        seen_keys = set()
        
        candidate_cities = request.settings.destinations
        if not candidate_cities:
            candidate_cities = list(CITIES.keys())
            
        for t_in in request.travelers:
            origin_city_name = t_in.origin
            origin_iata = origin_city_name
            if origin_city_name in CITIES:
                origin_iata = CITIES[origin_city_name]["primary_iata"]
            else:
                for k, v in CITIES.items():
                    if origin_city_name.upper() in [i.upper() for i in v["iata_codes"]]:
                        origin_iata = origin_city_name.upper()
                        origin_city_name = k
                        break
            
            for dest_c in candidate_cities:
                city_data = CITIES.get(dest_c)
                if not city_data: continue
                dest_iata = city_data["primary_iata"]
                
                out_dt = datetime.datetime.strptime(request.settings.earliest_departure, "%Y-%m-%d")
                
                def add_task(d_iata: str, is_gw: bool, gw_link: str=None):
                    key = (t_in.name, origin_iata, d_iata, request.settings.earliest_departure)
                    if key not in seen_keys:
                        seen_keys.add(key)
                        t_id = str(uuid.uuid4())
                        ret_date = (out_dt + datetime.timedelta(days=request.settings.duration_nights)).strftime("%Y-%m-%d")
                        
                        tasks_to_run.append(FlightSearchTask(
                            task_id=t_id + "_outbound",
                            traveler_name=t_in.name,
                            origin_iata=origin_iata,
                            origin_city=origin_city_name,
                            destination_iata=d_iata,
                            destination_city=dest_c,
                            outbound_date=request.settings.earliest_departure,
                            return_date=ret_date,
                            direction="outbound",
                            max_travel_hours=t_in.max_travel_hours,
                            max_stops=t_in.max_stops,
                            cabin_bags=t_in.cabin_bags,
                            checked_bags=t_in.checked_bags,
                            is_gateway_leg=is_gw,
                            gateway_ground_link=gw_link
                        ))
                        
                        tasks_to_run.append(FlightSearchTask(
                            task_id=t_id + "_return",
                            traveler_name=t_in.name,
                            origin_iata=d_iata,
                            origin_city=dest_c,
                            destination_iata=origin_iata,
                            destination_city=origin_city_name,
                            outbound_date=ret_date,
                            return_date=request.settings.earliest_departure,
                            direction="return",
                            max_travel_hours=t_in.max_travel_hours,
                            max_stops=t_in.max_stops,
                            cabin_bags=t_in.cabin_bags,
                            checked_bags=t_in.checked_bags,
                            is_gateway_leg=is_gw,
                            gateway_ground_link=gw_link
                        ))
                        
                add_task(dest_iata, False)
                for gw in city_data.get("gateway_airports", []):
                    gw_link = gw.get("trainline_link") or gw.get("flixbus_link")
                    add_task(gw["iata"], True, gw_link)
                    
        push_progress(session_id, "scout", f"Executing {len(tasks_to_run)} search tasks...", 10)
        
        scraped_results = await scraper.search_flights(tasks_to_run, progress_cb)
        
        push_progress(session_id, "matchmaker", "Building cost matrix and routing...", 70)
        await asyncio.sleep(0.5)
        
        push_progress(session_id, "neighborhood", "Scoring neighborhoods against vibes...", 85)
        await asyncio.sleep(0.5)
        
        push_progress(session_id, "optimizer", "Ranking destinations...", 95)
        
        engine_res = engine.optimize(scraped_results, tasks_to_run, request)
        
        push_progress(session_id, "done", "Optimization complete!", 100)
        
        from fastapi.responses import Response
        from fastapi.encoders import jsonable_encoder
        encoded = jsonable_encoder(engine_res)
        body = json.dumps(encoded, ensure_ascii=True)
        return Response(content=body, media_type="application/json", headers={"X-Session-ID": session_id})
        
    except Exception as e:
        import traceback
        try:
            traceback.print_exc()
        except UnicodeEncodeError:
            print("[server] Traceback contained non-encodable characters, skipping print.")
        push_progress(session_id, "error", str(e).encode('ascii', errors='replace').decode('ascii'), 100)
        raise HTTPException(status_code=500, detail="Scraping failed unexpectedly. Please retry.")

if __name__ == "__main__":
    import webbrowser
    import threading
    import time
    
    def open_browser():
        time.sleep(1.5)
        webbrowser.open("http://localhost:8345/")

    threading.Thread(target=open_browser, daemon=True).start()
    uvicorn.run("server:app", host="0.0.0.0", port=8345, reload=False)
