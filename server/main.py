import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from cost_engine import calculate_cost_breakdown
from models import CostBreakdown, DeploymentInput
from pricing import (
    AZURE_AI_SEARCH_TIERS,
    AZURE_OPENAI_MODELS,
    AZURE_OPENAI_PTU_HOURLY_RATE,
    DEFAULT_IMPLEMENTATION_HOURLY_RATE,
    DEFAULT_SUPPORT_HOURLY_RATE,
    M365_COPILOT_LICENSE,
)

app = FastAPI(title="Microsoft AI Deployment Cost Modeling API")

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
        "licensing": M365_COPILOT_LICENSE,
        "azure_openai_models": AZURE_OPENAI_MODELS,
        "azure_openai_ptu_hourly_rate": AZURE_OPENAI_PTU_HOURLY_RATE,
        "azure_ai_search_tiers": AZURE_AI_SEARCH_TIERS,
        "default_implementation_hourly_rate": DEFAULT_IMPLEMENTATION_HOURLY_RATE,
        "default_support_hourly_rate": DEFAULT_SUPPORT_HOURLY_RATE,
    }


@app.post("/api/calculate", response_model=CostBreakdown)
def calculate(deployment: DeploymentInput):
    return calculate_cost_breakdown(deployment)
