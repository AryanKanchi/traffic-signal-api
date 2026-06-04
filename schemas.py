from pydantic import BaseModel

class TrafficInput(BaseModel):
    queue_length_m: float = 120.0
    estimated_flow_speed_kmph: float = 20.0
    car_count: int = 140
    bike_count: int = 90
    bus_count: int = 4
    truck_count: int = 10
    weighted_traffic_index: float = 540.0
    ev_distance_from_signal_km: float = 1.5
    cycle_position_sec: int = 30
    model_name: str = "XGBoost"

class ClearanceResponse(BaseModel):
    clearance_distance_km: float
    signal_action: str
    model_used: str

class IncidentResponse(BaseModel):
    incident_probability: float
    incident_detected: bool
    reason: str
