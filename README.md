# 🚦 Traffic Signal Intelligence API

A production-ready REST API that serves ML models to predict **signal clearance distance** for emergency vehicles — built on top of the [Emergency Vehicle Routing System](https://github.com/AryanKanchi/Emergency_Vehicle_Routing_System).

---

## 🎯 What it does

When an ambulance approaches a signal, this API answers:

> *"At what distance should the signal turn green so the road is already clear when the EV arrives?"*

Send traffic parameters → get back a clearance distance, a signal action, and an incident probability.

---

## 🔗 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/predict/clearance` | Predict clearance distance (km) |
| `POST` | `/predict/incident` | Detect incident probability |
| `GET` | `/docs` | Interactive Swagger UI |
| `GET` | `/frontend/index.html` | Web UI |

---

## 📥 Example Request

```bash
curl -X POST "http://localhost:8000/predict/clearance" \
     -H "Content-Type: application/json" \
     -d '{
       "queue_length_m": 200,
       "estimated_flow_speed_kmph": 15,
       "car_count": 140,
       "bike_count": 90,
       "bus_count": 4,
       "truck_count": 10,
       "weighted_traffic_index": 540,
       "ev_distance_from_signal_km": 1.5,
       "cycle_position_sec": 30,
       "model_name": "XGBoost"
     }'
```

## 📤 Example Response

```json
{
  "clearance_distance_km": 1.124,
  "signal_action": "Hold RED - turn GREEN when EV is 1.124 km away",
  "model_used": "XGBoost"
}
```

---

## 🚀 Getting Started

## 🌐 Live API
**Base URL:** https://traffic-signal-api.onrender.com
**Docs:** https://traffic-signal-api.onrender.com/docs

### 1. Clone the repo
```bash
git clone https://github.com/AryanKanchi/traffic-signal-api.git
cd traffic-signal-api
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add trained models (optional)
Place `.joblib` files from the EV Routing System into the `models/` folder.
The API works without them using a physics-based fallback formula.

### 4. Run the server
```bash
uvicorn main:app --reload
```

### 5. Open the UI
```
http://localhost:8000/frontend/index.html
```
Or explore the interactive docs at:
```
http://localhost:8000/docs
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| API Framework | FastAPI |
| ML Models | XGBoost, Random Forest (scikit-learn) |
| Data Processing | Pandas, NumPy |
| Server | Uvicorn (ASGI) |
| Frontend | Vanilla HTML / CSS / JS |

---

## 🔌 Related Project

This API extends the **Emergency Vehicle Routing System** — an ML-powered traffic simulation with A* routing and animated signal preemption.

👉 [Emergency Vehicle Routing System](https://github.com/AryanKanchi/Emergency_Vehicle_Routing_System)

---

*Built as part of a Minor Project — Computer Science Engineering*
