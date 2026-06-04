from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from schemas import TrafficInput, ClearanceResponse, IncidentResponse
from predictor import predict_clearance, predict_incident

app = FastAPI(
    title="Traffic Signal Intelligence API",
    description=(
        "ML-powered REST API for emergency vehicle signal preemption. "
        "Predicts the clearance distance at which a traffic signal should "
        "turn green so the road is clear by the time the EV arrives."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")


@app.get("/", tags=["Health"])
def health_check():
    return {
        "status":  "online",
        "message": "Traffic Signal Intelligence API is running",
        "docs":    "/docs",
        "ui":      "/frontend/index.html",
    }


@app.post("/predict/clearance", response_model=ClearanceResponse, tags=["Prediction"])
def clearance_prediction(data: TrafficInput):
    """
    Predict the clearance distance (km) at which the signal should turn green.
    Supports XGBoost, Tuned XGBoost, and Random Forest models.
    Falls back to a physics-based formula if model files are not present.
    """
    return predict_clearance(data)


@app.post("/predict/incident", response_model=IncidentResponse, tags=["Prediction"])
def incident_prediction(data: TrafficInput):
    """
    Estimate the probability of a traffic incident based on
    queue length, flow speed, and traffic density.
    """
    return predict_incident(data)
