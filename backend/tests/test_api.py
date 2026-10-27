"""
Integration and Unit Tests for Multimodal Construction Intelligence Platform
Tests all 4 module endpoints: PPE Safety, Crack Diagnostics, Valuation, and Weather Advisory (including Open-Meteo Location integration)
"""
import asyncio
from unittest.mock import patch
import httpx
from backend.main import app
from backend.services import gemini_service

async def run_all_tests():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        print("[TEST 1] System Health Check...", flush=True)
        r = await client.get("/api/health")
        assert r.status_code == 200, f"Health check failed: {r.text}"
        data = r.json()
        assert data["status"] == "online"
        assert "platform_id" in data
        assert "modules" in data
        print(f"         PASSED (Status: {data['status']}, Mode: {data['mode']})", flush=True)

        print("[TEST 2] PPE Safety Demo Endpoint...", flush=True)
        r = await client.get("/api/ppe-safety/demo")
        assert r.status_code == 200, f"PPE demo failed: {r.text}"
        data = r.json()
        assert "safety_score" in data
        assert 0 <= data["safety_score"] <= 100
        assert "overall_status" in data
        assert len(data["ppe_detection_checklist"]) > 0
        print(f"         PASSED (Score: {data['safety_score']}, Status: {data['overall_status']})", flush=True)

        print("[TEST 3] Crack Diagnostics Demo Endpoint...", flush=True)
        r = await client.get("/api/crack-analysis/demo")
        assert r.status_code == 200, f"Crack demo failed: {r.text}"
        data = r.json()
        assert "crack_type" in data
        assert "estimated_crack_width_mm" in data
        assert "severity" in data
        assert len(data["repair_recommendations"]) > 0
        print(f"         PASSED (Type: {data['crack_type']}, Width: {data['estimated_crack_width_mm']}mm)", flush=True)

        print("[TEST 4] Real Estate Valuation Calculation...", flush=True)
        val_payload = {
            "structure_type": "Residential",
            "built_up_sqft": 2500,
            "location_tier": "Tier 1",
            "completion_percentage": 60,
            "floors": 3,
            "project_name": "Skyline Heights"
        }
        r = await client.post("/api/valuation/calculate", json=val_payload)
        assert r.status_code == 200, f"Valuation failed: {r.text}"
        data = r.json()
        assert "total_project_budget_inr" in data
        assert "capital_expenditure_incurred_inr" in data
        assert "material_requirements" in data
        safe_budget = data['total_project_budget_inr'].replace('\u20b9', 'INR ')
        print(f"         PASSED (Budget: {safe_budget}, ROI: {data['roi_estimate_percent']}%)", flush=True)

        print("[TEST 5] Weather Advisory (Standard Condition Without Location)...", flush=True)
        for cond in ["Normal", "High Wind", "Heavy Rain", "Extreme Heat"]:
            r = await client.get(f"/api/weather-advisory/advisory/{cond}")
            assert r.status_code == 200, f"Advisory {cond} failed: {r.text}"
            data = r.json()
            assert data["condition"] == cond
            assert "overall_risk_level" in data
            assert data.get("weather_observation") is None
        print("         PASSED (All 4 weather conditions verified)", flush=True)

        print("[TEST 6] Weather Advisory With Location (Indore)...", flush=True)
        r = await client.get("/api/weather-advisory/advisory/Normal?location=Indore")
        assert r.status_code == 200, f"Location advisory failed: {r.text}"
        data = r.json()
        obs = data.get("weather_observation")
        assert obs is not None, "Expected weather_observation"
        assert "Indore" in obs.get("location_name", "")
        assert "temperature_c" in obs
        assert "apparent_temperature_c" in obs
        assert "wind_speed_kmh" in obs
        assert "precipitation_mm" in obs
        assert "observation_time" in obs
        assert data.get("is_demo_advice") is True  # Demo mode
        assert data.get("is_live_weather") is True
        print(f"         PASSED (Live weather for {obs['location_name']}: {obs['temperature_c']}C, {obs['wind_speed_kmh']}km/h)", flush=True)

        print("[TEST 7] Weather Advisory With Invalid Location (Expect 404)...", flush=True)
        r = await client.get("/api/weather-advisory/advisory/Normal?location=xyzinvalidnonexistent123456")
        assert r.status_code == 404, f"Expected 404, got {r.status_code}"
        print(f"         PASSED (Got 404: {r.json().get('detail')})", flush=True)

        print("[TEST 8] Weather Advisory With Blank Location (Expect 400)...", flush=True)
        r = await client.get("/api/weather-advisory/advisory/Normal?location=%20%20")
        assert r.status_code == 400, f"Expected 400, got {r.status_code}"
        print(f"         PASSED (Got 400: {r.json().get('detail')})", flush=True)

        print("[TEST 9] Weather Advisory Weather Provider Timeout (Expect 503)...", flush=True)
        with patch("backend.services.gemini_service.fetch_open_meteo_weather", side_effect=gemini_service.WeatherServiceError("Weather service timed out.")):
            r = await client.get("/api/weather-advisory/advisory/Normal?location=Indore")
            assert r.status_code == 503, f"Expected 503, got {r.status_code}"
            print(f"         PASSED (Got 503: {r.json().get('detail')})", flush=True)

        print("[TEST 10] Construction AI Assistant Chatbot...", flush=True)
        chat_req = {
            "message": "What safety precautions are necessary for scaffolding work during high winds?",
            "weather_condition": "High Wind"
        }
        r = await client.post("/api/weather-advisory/chat", json=chat_req)
        assert r.status_code == 200, f"Chat failed: {r.text}"
        data = r.json()
        assert "response" in data
        assert len(data["response"]) > 0
        print(f"         PASSED (Received {len(data['response'])} character response)", flush=True)

        print("\n=======================================================", flush=True)
        print("  ALL 10 COMPREHENSIVE INTEGRATION TESTS PASSED!       ", flush=True)
        print("=======================================================", flush=True)

if __name__ == "__main__":
    asyncio.run(run_all_tests())
