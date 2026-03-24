import datetime
from typing import List
from models import (
    FlightSearchTask, FlightSearchResult, OptimizeRequest,
    NeighborhoodResult, DirectOption, GatewayOption, FlightLeg,
    TravelerRouteOptions, Recommendation, OptimizeResponseAbort, DateWindow
)
from data import CITIES, booking_com_link


def optimize(scraped_results: List[FlightSearchResult], tasks: List[FlightSearchTask], request: OptimizeRequest):
    travelers = request.travelers
    settings = request.settings

    # ABORT RULE -- if any traveler has zero usable results, abort early
    for t_in in travelers:
        t_tasks = [t for t in tasks if t.traveler_name == t_in.name]
        task_ids = {t.task_id for t in t_tasks}
        t_results = [r for r in scraped_results if r.task_id in task_ids]

        if not t_results or all(r.error for r in t_results):
            reason = ""
            if t_results:
                e_res = next((r for r in t_results if r.error_reason), None)
                if e_res: reason = e_res.error_reason
            return OptimizeResponseAbort(
                reason=f"No flight data could be retrieved for {t_in.name}. Please retry -- this is usually caused by temporary bot detection on the scraping sources. Detail: {reason}",
                affected_traveler=t_in.name
            )

    candidate_cities = settings.destinations or list(CITIES.keys())
    task_map = {t.task_id: t for t in tasks}

    # Build per-city per-traveler results
    city_traveler_results = {c: {t.name: {'direct': {'outbound': [], 'return': []}, 'gateway': {'outbound': [], 'return': []}} for t in travelers} for c in candidate_cities}

    for r in scraped_results:
        t = task_map.get(r.task_id)
        if not t: continue
        
        target_city = t.destination_city if t.direction == "outbound" else t.origin_city
        if target_city not in candidate_cities: continue
        if r.error: continue
        t_in = next((x for x in travelers if x.name == t.traveler_name), None)
        if not t_in: continue
        
        if t.direction == "outbound":
            if r.departure_time and r.departure_time < t_in.not_before: continue
            if r.arrival_time and r.arrival_time > t_in.arrive_by: continue

        category = 'gateway' if t.is_gateway_leg else 'direct'
        city_traveler_results[target_city][t.traveler_name][category][t.direction].append((r, t))

    feasible_destinations = []

    for city in candidate_cities:
        city_data = CITIES.get(city)
        if not city_data: continue

        all_feasible = True
        city_traveler_opts = []
        group_flight_cost = 0.0

        for t_in in travelers:
            opts = city_traveler_results[city][t_in.name]
            
            outbound_directs = sorted(opts['direct']['outbound'], key=lambda x: x[0].price_eur or 99999)
            return_directs = sorted(opts['direct']['return'], key=lambda x: x[0].price_eur or 99999)
            
            outbound_gateways = sorted(opts['gateway']['outbound'], key=lambda x: x[0].price_eur or 99999)
            return_gateways = sorted(opts['gateway']['return'], key=lambda x: x[0].price_eur or 99999)
            
            best_out_direct = outbound_directs[0] if outbound_directs else None
            best_ret_direct = return_directs[0] if return_directs else None
            
            best_out_gw = outbound_gateways[0] if outbound_gateways else None
            best_ret_gw = return_gateways[0] if return_gateways else None

            if not (best_out_direct and best_ret_direct) and not (best_out_gw and best_ret_gw):
                all_feasible = False
                break

            direct_opt = None
            if best_out_direct and best_ret_direct:
                out_r, out_t = best_out_direct
                ret_r, ret_t = best_ret_direct
                
                out_leg = FlightLeg(
                    airline=out_r.airline or "Unknown",
                    departure_time=out_r.departure_time or "00:00",
                    arrival_time=out_r.arrival_time or "00:00",
                    duration_minutes=out_r.duration_minutes or 0,
                    stops=out_r.stops or 0,
                    layover_airports=out_r.layover_airports,
                    layover_duration_minutes=getattr(out_r, 'layover_duration_minutes', 0)
                )
                ret_leg = FlightLeg(
                    airline=ret_r.airline or "Unknown",
                    departure_time=ret_r.departure_time or "00:00",
                    arrival_time=ret_r.arrival_time or "00:00",
                    duration_minutes=ret_r.duration_minutes or 0,
                    stops=ret_r.stops or 0,
                    layover_airports=ret_r.layover_airports,
                    layover_duration_minutes=getattr(ret_r, 'layover_duration_minutes', 0)
                )
                
                direct_opt = DirectOption(
                    price_eur=(out_r.price_eur or 0.0) + (ret_r.price_eur or 0.0),
                    outbound_leg=out_leg,
                    return_leg=ret_leg,
                    booking_link=out_r.booking_link,
                    source=out_r.source
                )

            gateway_opts = []
            if best_out_gw and best_ret_gw:
                out_r, out_t = best_out_gw
                ret_r, ret_t = best_ret_gw
                gw_city_name = next((g["city"] for g in city_data["gateway_airports"] if g["iata"] == out_r.destination), out_r.destination)
                
                out_leg = FlightLeg(
                    airline=out_r.airline or "Unknown",
                    departure_time=out_r.departure_time or "00:00",
                    arrival_time=out_r.arrival_time or "00:00",
                    duration_minutes=out_r.duration_minutes or 0,
                    stops=out_r.stops or 0,
                    layover_airports=out_r.layover_airports,
                    layover_duration_minutes=getattr(out_r, 'layover_duration_minutes', 0)
                )
                ret_leg = FlightLeg(
                    airline=ret_r.airline or "Unknown",
                    departure_time=ret_r.departure_time or "00:00",
                    arrival_time=ret_r.arrival_time or "00:00",
                    duration_minutes=ret_r.duration_minutes or 0,
                    stops=ret_r.stops or 0,
                    layover_airports=ret_r.layover_airports,
                    layover_duration_minutes=getattr(ret_r, 'layover_duration_minutes', 0)
                )

                gateway_opts.append(GatewayOption(
                    gateway_city=gw_city_name,
                    flight_price_eur=(out_r.price_eur or 0.0) + (ret_r.price_eur or 0.0),
                    outbound_leg=out_leg,
                    return_leg=ret_leg,
                    flight_booking_link=out_r.booking_link,
                    ground_transport_link=out_r.gateway_ground_link or "",
                    ground_transport_note="Train/bus to city center -- check link",
                    source=out_r.source
                ))

            min_direct_price = direct_opt.price_eur if direct_opt else float('inf')
            min_gw_price = min((g.flight_price_eur for g in gateway_opts), default=float('inf'))
            cheapest = min(min_direct_price, min_gw_price)
            group_flight_cost += cheapest

            city_traveler_opts.append(TravelerRouteOptions(
                name=t_in.name,
                direct_option=direct_opt,
                gateway_options=gateway_opts
            ))

        if all_feasible:
            # Pick the best neighborhood by base scores only (no vibes)
            best_hood = None
            best_hood_score = -1
            for nb in city_data["neighborhoods"]:
                if nb["transit_minutes_to_center"] > 50:
                    continue
                scores = nb["scores"]
                base_score = (
                    scores.get("vibe", 0) * 1.5 +
                    scores.get("walkability", 0) * 1.2 +
                    scores.get("safety", 0) * 1.0 +
                    scores.get("transit", 0) * 0.8
                )
                max_base = 10*1.5 + 10*1.2 + 10*1.0 + 10*0.8
                final_score = (base_score / max_base) * 10 if max_base > 0 else 0

                if final_score > best_hood_score:
                    best_hood_score = final_score
                    sorted_dims = sorted(scores.items(), key=lambda x: x[1], reverse=True)
                    highlights = [k.capitalize() for k, v in sorted_dims[:3]]
                    best_hood = NeighborhoodResult(
                        name=nb["name"],
                        score=round(final_score, 1),
                        is_perfect_spot=(final_score >= 8.5),
                        highlights=highlights,
                        description=nb["description"]
                    )

            feasible_destinations.append({
                "city": city,
                "city_data": city_data,
                "travelers_opts": city_traveler_opts,
                "group_flight_cost": group_flight_cost,
                "best_hood": best_hood
            })

    # Scoring -- simple cost-based ranking
    costs = [d["group_flight_cost"] for d in feasible_destinations]
    min_cost = min(costs) if costs else 0
    max_cost = max(costs) if costs else 0

    for dest in feasible_destinations:
        hood = dest["best_hood"]
        hood_score = hood.score if hood else 0.0
        perfect_bonus = 0.5 if hood and hood.is_perfect_spot else 0.0
        per_person = dest["group_flight_cost"] / len(travelers)
        within_budget = None

        if settings.budget_per_person:
            within_budget = per_person <= settings.budget_per_person
            cost_score = max(0.0, 10.0 - ((per_person / settings.budget_per_person) * 10.0))
        else:
            cost_score = 10.0 if max_cost == min_cost else 10.0 - ((dest["group_flight_cost"] - min_cost) / (max_cost - min_cost) * 10.0)

        composite = (cost_score * 0.50) + (hood_score * 0.35) + (perfect_bonus * 0.15)
        dest["composite_score"] = composite
        dest["per_person"] = per_person
        dest["within_budget"] = within_budget

    feasible_destinations.sort(key=lambda x: x["composite_score"], reverse=True)

    outbound_date = settings.earliest_departure
    out_dt = datetime.datetime.strptime(outbound_date, "%Y-%m-%d")
    ret_dt = out_dt + datetime.timedelta(days=settings.duration_nights)
    ret_str = ret_dt.strftime("%Y-%m-%d")

    recommendations = []
    for i, dest in enumerate(feasible_destinations[:10]):
        city_data = dest["city_data"]
        acc_link = booking_com_link(
            city=dest["city"], checkin=outbound_date,
            checkout=ret_str, num_guests=len(travelers)
        )
        recommendations.append(Recommendation(
            rank=i+1,
            composite_score=round(dest["composite_score"], 2),
            destination=dest["city"],
            country=city_data["country"],
            country_flag=city_data["country_flag"],
            neighborhood=dest["best_hood"] or NeighborhoodResult(name="Unknown", score=0, is_perfect_spot=False, highlights=[], description=""),
            travelers=dest["travelers_opts"],
            total_group_flight_cost=round(dest["group_flight_cost"], 2),
            per_person_flight_cost=round(dest["per_person"], 2),
            within_budget=dest["within_budget"],
            best_window=DateWindow(outbound_date=outbound_date, return_date=ret_str),
            accommodation_search_link=acc_link
        ))

    return {
        "status": "ok",
        "recommendations": recommendations,
        "total_searched": len(candidate_cities),
        "scrape_warnings": []
    }
