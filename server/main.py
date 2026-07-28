import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from cost_engine import calculate_cost_breakdown
from models import CostBreakdown, DeploymentInput
from pricing import (
    DEFAULT_IMPLEMENTATION_HOURLY_RATE,
    DEFAULT_SUPPORT_HOURLY_RATE,
    INFRASTRUCTURE_CATALOG,
    LICENSE_CATALOG,
    MODEL_CATALOG,
    PROVIDERS,
    RESERVED_THROUGHPUT_HOURLY_RATE,
)

app = FastAPI(title="AI Deployment Cost Modeling API")

cors_origins = os.environ.get("CORS_ORIGINS", "*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins.split(",") if cors_origins != "*" else ["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/pricing-reference")
def pricing_reference():
    return {
        "providers": PROVIDERS,
        "licensing": LICENSE_CATALOG,
        "models": MODEL_CATALOG,
        "reserved_throughput_hourly_rate": RESERVED_THROUGHPUT_HOURLY_RATE,
        "infrastructure": INFRASTRUCTURE_CATALOG,
        "default_implementation_hourly_rate": DEFAULT_IMPLEMENTATION_HOURLY_RATE,
        "default_support_hourly_rate": DEFAULT_SUPPORT_HOURLY_RATE,
    }


@app.post("/api/calculate", response_model=CostBreakdown)
def calculate(deployment: DeploymentInput):
    return calculate_cost_breakdown(deployment)
