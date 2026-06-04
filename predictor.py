import numpy as np
import pandas as pd
from pathlib import Path

MODELS_DIR = Path(__file__).parent / "models"

MODEL_FILES = {
    "XGBoost":       "xgb_clearance_model.joblib",
    "Tuned XGBoost": "xgb_clearance_model_tuned.joblib",
    "Random Forest": "rf_clearance_model.joblib",
}

FEATURE_FILES = {
    "XGBoost":       "xgb_feature_columns.joblib",
    "Tuned XGBoost": "xgb_feature_columns.joblib",
    "Random Forest": "rf_feature_columns.joblib",
}


def load_model(model_name):
    try:
        import joblib
        model_path   = MODELS_DIR / MODEL_FILES[model_name]
        feature_path = MODELS_DIR / FEATURE_FILES[model_name]
        if not model_path.exists() or not feature_path.exists():
            return None, None
        return joblib.load(model_path), joblib.load(feature_path)
    except Exception:
        return None, None


def formula_fallback(data):
    """Physics-based approximation when .joblib models are not present."""
    base           = 0.50
    queue_factor   = (data.queue_length_m / 500) * 0.80
    speed_factor   = ((60 - data.estimated_flow_speed_kmph) / 60) * 0.40
    vehicle_factor = (data.car_count + data.bus_count * 3 + data.truck_count * 2) / 500 * 0.30
    return round(base + queue_factor + speed_factor + vehicle_factor, 4)


def predict_clearance(data):
    model, feature_cols = load_model(data.model_name)

    if model is None:
        clearance  = formula_fallback(data)
        model_used = f"{data.model_name} (formula fallback - place .joblib files in models/)"
    else:
        input_dict = {
            "Queue_Length_m":             data.queue_length_m,
            "Estimated_Flow_Speed_kmph":  data.estimated_flow_speed_kmph,
            "CarCount":                   data.car_count,
            "BikeCount":                  data.bike_count,
            "BusCount":                   data.bus_count,
            "TruckCount":                 data.truck_count,
            "Weighted_Traffic_Index":     data.weighted_traffic_index,
            "EV_Distance_From_Signal_km": data.ev_distance_from_signal_km,
            "Cycle_Position_sec":         data.cycle_position_sec,
        }
        df = pd.DataFrame([input_dict])
        df = pd.get_dummies(df, drop_first=True)
        for col in feature_cols:
            if col not in df.columns:
                df[col] = 0
        df        = df[feature_cols]
        clearance  = round(float(model.predict(df)[0]), 4)
        model_used = data.model_name

    if data.ev_distance_from_signal_km <= clearance:
        action = "Turn GREEN now - EV is within clearance distance"
    else:
        action = f"Hold RED - turn GREEN when EV is {clearance:.3f} km away"

    return {
        "clearance_distance_km": clearance,
        "signal_action":         action,
        "model_used":            model_used,
    }


def predict_incident(data):
    score = 0.0

    if data.queue_length_m > 300:
        score += 0.40
    elif data.queue_length_m > 150:
        score += 0.20

    if data.estimated_flow_speed_kmph < 10:
        score += 0.40
    elif data.estimated_flow_speed_kmph < 20:
        score += 0.20

    if data.weighted_traffic_index > 400:
        score += 0.20

    score = min(round(score, 3), 1.0)

    reason = (
        "High queue length and low speed indicate a possible incident"
        if score > 0.5
        else "Normal traffic conditions detected"
    )

    return {
        "incident_probability": score,
        "incident_detected":    score > 0.5,
        "reason":               reason,
    }
