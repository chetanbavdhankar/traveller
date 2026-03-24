from pydantic import BaseModel, Field
from typing import Optional, List, Literal

class FlightSearchTask(BaseModel):
    task_id: str
    traveler_name: str
    origin_iata: str
    origin_city: str
    destination_iata: str
    destination_city: str
    outbound_date: str
    return_date: Optional[str] = None
    direction: Literal["outbound", "return"] = "outbound"
    max_travel_hours: float
    max_stops: int
    cabin_bags: int = 0
    checked_bags: int = 0
    is_gateway_leg: bool
    gateway_ground_link: Optional[str] = None

class FlightSearchResult(BaseModel):
    task_id: str
    traveler_name: str
    origin: str
    destination: str
    is_gateway_route: bool
    gateway_ground_link: Optional[str] = None
    airline: Optional[str] = None
    price_eur: Optional[float] = None
    departure_time: Optional[str] = None
    arrival_time: Optional[str] = None
    duration_minutes: Optional[int] = None
    stops: Optional[int] = None
    layover_airports: List[str] = Field(default_factory=list)
    layover_duration_minutes: int = 0
    booking_link: str
    source: str
    error: bool = False
    error_reason: Optional[str] = None

class TravelerInput(BaseModel):
    name: str
    origin: str
    not_before: str = "00:00"
    arrive_by: str = "23:59"
    max_travel_hours: float = 24.0
    max_stops: int = 2
    cabin_bags: int = 0
    checked_bags: int = 0

class TripSettings(BaseModel):
    earliest_departure: str
    latest_return: str
    duration_nights: int
    budget_per_person: Optional[float] = None
    destinations: Optional[List[str]] = None

class OptimizeRequest(BaseModel):
    travelers: List[TravelerInput]
    settings: TripSettings

class NeighborhoodResult(BaseModel):
    name: str
    score: float
    is_perfect_spot: bool
    highlights: List[str]
    description: str

class FlightLeg(BaseModel):
    airline: str
    departure_time: str
    arrival_time: str
    duration_minutes: int
    stops: int
    layover_airports: List[str] = Field(default_factory=list)
    layover_duration_minutes: int = 0

class DirectOption(BaseModel):
    price_eur: float
    outbound_leg: FlightLeg
    return_leg: FlightLeg
    booking_link: str
    source: str

class GatewayOption(BaseModel):
    gateway_city: str
    flight_price_eur: float
    outbound_leg: FlightLeg
    return_leg: FlightLeg
    flight_booking_link: str
    ground_transport_link: str
    ground_transport_note: str
    source: str

class TravelerRouteOptions(BaseModel):
    name: str
    direct_option: Optional[DirectOption] = None
    gateway_options: List[GatewayOption] = Field(default_factory=list)

class DateWindow(BaseModel):
    outbound_date: str
    return_date: str

class Recommendation(BaseModel):
    rank: int
    composite_score: float
    destination: str
    country: str
    country_flag: str
    neighborhood: NeighborhoodResult
    travelers: List[TravelerRouteOptions]
    total_group_flight_cost: float
    per_person_flight_cost: float
    within_budget: Optional[bool] = None
    best_window: DateWindow
    accommodation_search_link: str

class ScrapeWarning(BaseModel):
    traveler: str
    route: str
    reason: str

class OptimizeResponseOk(BaseModel):
    status: Literal["ok"] = "ok"
    recommendations: List[Recommendation]
    total_searched: int
    scrape_warnings: List[ScrapeWarning] = Field(default_factory=list)

class OptimizeResponseAbort(BaseModel):
    status: Literal["abort"] = "abort"
    reason: str
    affected_traveler: str
    recommendations: List[dict] = Field(default_factory=list)
