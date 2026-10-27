"""
FastAPI Main Application — Multimodal Construction Intelligence Platform
Skill Wallet Capstone Project 1 | Platform ID: 6ac4c98d1dcde6d7857c1642
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from backend.routers import ppe_safety, crack_analysis, valuation, weather_advisory
from backend.services.gemini_service import is_demo_mode

load_dotenv()

# ─── Application Setup ────────────────────────────────────────────────────────

app = FastAPI(
    title="Multimodal Construction Intelligence Platform",
    description=(
        "AI-powered decision-support system for construction professionals. "
        "Analyzes site photos for PPE compliance, classifies concrete cracks, "
        "estimates real estate valuation in INR, and provides weather-aware safety protocols. "
        "Powered by Google Gemini 1.5 multimodal AI."
    ),
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# ─── CORS ────────────────────────────────────────────────────────────────────


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "https://skillwallet-kappa.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Routers ──────────────────────────────────────────────────────────────────

app.include_router(ppe_safety.router)
app.include_router(crack_analysis.router)
app.include_router(valuation.router)
app.include_router(weather_advisory.router)

# ─── Health Check ─────────────────────────────────────────────────────────────

@app.get("/api/health", tags=["System"])
async def health_check():
    """Platform health check and configuration status."""
    return JSONResponse({
        "status": "online",
        "platform": "Multimodal Construction Intelligence Platform",
        "platform_id": "6ac4c98d1dcde6d7857c1642",
        "version": "1.0.0",
        "mode": "demo" if is_demo_mode() else "live",
        "ai_model": "Google Gemini 1.5 Flash",
        "modules": {
            "ppe_safety": "active",
            "crack_diagnostics": "active",
            "real_estate_valuation": "active",
            "weather_advisory": "active",
            "chatbot": "active"
        },
        "standards": ["OSHA 29 CFR 1926", "IS 456:2000", "IS 3696", "IS 1786"]
    })


@app.get("/", tags=["System"])
async def root():
    return JSONResponse({
        "message": "Multimodal Construction Intelligence Platform API",
        "docs": "/api/docs",
        "health": "/api/health"
    })


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port, reload=True)
