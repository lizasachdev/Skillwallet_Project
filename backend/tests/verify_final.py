import asyncio
from unittest.mock import patch
import httpx
from backend.main import app
from backend.services import gemini_service

async def run_detailed_verification():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        print("=== 1. VERIFY WEATHER ENDPOINT: MISSING LOCATION ===", flush=True)
        r = await client.get("/api/weather-advisory/advisory/Normal")
        assert r.status_code == 200
        d = r.json()
        assert d["condition"] == "Normal"
        assert d["weather_observation"] is None
        assert d["is_live_weather"] is False
        print("PASS: Missing location returns 200, weather_observation is None, no fabrication.", flush=True)

        print("\n=== 2. VERIFY WEATHER ENDPOINT: VALID CITIES ===", flush=True)
        for city in ["Indore", "Mumbai", "Delhi"]:
            r = await client.get(f"/api/weather-advisory/advisory/Normal?location={city}")
            assert r.status_code == 200
            d = r.json()
            obs = d["weather_observation"]
            assert obs is not None
            assert city.lower() in obs["location_name"].lower()
            assert isinstance(obs["temperature_c"], (int, float))
            assert isinstance(obs["apparent_temperature_c"], (int, float))
            assert isinstance(obs["wind_speed_kmh"], (int, float))
            assert isinstance(obs["precipitation_mm"], (int, float))
            assert d["is_live_weather"] is True
            assert d["is_demo_advice"] is True
            print(f"PASS: Valid city '{city}' -> {obs['location_name']}, Temp: {obs['temperature_c']}C, Wind: {obs['wind_speed_kmh']}km/h", flush=True)

        print("\n=== 3. VERIFY WEATHER ENDPOINT: INVALID CITY ===", flush=True)
        r = await client.get("/api/weather-advisory/advisory/Normal?location=NonExistentCity99999XYZ")
        assert r.status_code == 404
        assert "not found" in r.json()["detail"].lower()
        print(f"PASS: Invalid city returned 404 cleanly: {r.json()['detail']}", flush=True)

        print("\n=== 4. VERIFY PROVIDER FAILURE & TIMEOUT (NO FABRICATION) ===", flush=True)
        with patch("backend.services.gemini_service.fetch_open_meteo_weather", side_effect=gemini_service.WeatherServiceError("Weather service timed out.")):
            r = await client.get("/api/weather-advisory/advisory/Normal?location=Indore")
            assert r.status_code == 503
            assert "timed out" in r.json()["detail"]
            print("PASS: Upstream timeout returned 503 with informative message, zero fabricated data.", flush=True)

        print("\n=== 5. VERIFY ALL 4 WEATHER CONDITION BUTTONS ===", flush=True)
        expected_risks = {
            "Normal": "Low",
            "High Wind": "Critical",
            "Heavy Rain": "High",
            "Extreme Heat": "High"
        }
        for cond, expected_risk in expected_risks.items():
            r = await client.get(f"/api/weather-advisory/advisory/{cond}")
            assert r.status_code == 200
            d = r.json()
            assert d["condition"] == cond
            assert d["overall_risk_level"] == expected_risk
            assert len(d["safety_alerts"]) > 0
            assert len(d["daily_checklist"]) > 0
            assert "Emergency Services" in d["emergency_contacts"]
            print(f"PASS: Condition '{cond}' -> Risk Level '{d['overall_risk_level']}', {len(d['safety_alerts'])} alert(s)", flush=True)

        print("\n=== 6. VERIFY CHATBOT ENDPOINT ===", flush=True)
        r = await client.post("/api/weather-advisory/chat", json={
            "message": "What is the concrete curing procedure during heavy rain?",
            "weather_condition": "Heavy Rain"
        })
        assert r.status_code == 200
        d = r.json()
        assert "response" in d and len(d["response"]) > 50
        assert len(d.get("suggested_followups", [])) > 0
        print(f"PASS: Chatbot responded successfully ({len(d['response'])} chars, {len(d['suggested_followups'])} suggestions)", flush=True)

        print("\n=== 7. VERIFY PPE SAFETY (DEMO & ANALYZE) ===", flush=True)
        r_demo = await client.get("/api/ppe-safety/demo")
        assert r_demo.status_code == 200
        d_demo = r_demo.json()
        assert "safety_score" in d_demo
        assert len(d_demo["ppe_detection_checklist"]) == 6
        assert len(d_demo["site_hazards"]) > 0

        # Test upload endpoint with sample bytes
        fake_img = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\rIDATx\x9cc`\x00\x00\x00\x02\x00\x01H\xaf\xa4q\x00\x00\x00\x00IEND\xaeB`\x82"
        r_upload = await client.post("/api/ppe-safety/analyze", files={"file": ("test.png", fake_img, "image/png")})
        assert r_upload.status_code == 200
        d_up = r_upload.json()
        assert "safety_score" in d_up
        print(f"PASS: PPE Safety Demo & Analyze active (Score: {d_demo['safety_score']}, Status: {d_demo['overall_status']})", flush=True)

        print("\n=== 8. VERIFY CRACK DIAGNOSTICS (DEMO & ANALYZE) ===", flush=True)
        r_crack_demo = await client.get("/api/crack-analysis/demo")
        assert r_crack_demo.status_code == 200
        d_crack = r_crack_demo.json()
        assert "crack_type" in d_crack
        assert "estimated_crack_width_mm" in d_crack
        assert len(d_crack["repair_recommendations"]) > 0

        r_crack_up = await client.post("/api/crack-analysis/analyze", files={"file": ("crack.png", fake_img, "image/png")})
        assert r_crack_up.status_code == 200
        print(f"PASS: Crack Diagnostics Demo & Analyze active (Type: {d_crack['crack_type']}, Severity: {d_crack['severity']})", flush=True)

        print("\n=== 9. VERIFY PROPERTY VALUATION CALCULATIONS ===", flush=True)
        for stype in ["Residential", "Commercial", "Industrial", "Mixed Use", "Institutional"]:
            r_val = await client.post("/api/valuation/calculate", json={
                "structure_type": stype,
                "built_up_sqft": 3000,
                "location_tier": "Tier 1",
                "completion_percentage": 75,
                "floors": 4,
                "project_name": f"{stype} Project"
            })
            assert r_val.status_code == 200
            d_val = r_val.json()
            assert "total_project_budget_inr" in d_val
            assert "capital_expenditure_incurred_inr" in d_val
            assert "current_market_asset_valuation_inr" in d_val
            assert len(d_val["material_requirements"]) == 5
            assert len(d_val["milestone_progress"]) == 6
            safe_budget = d_val["total_project_budget_inr"].replace("\u20b9", "INR ")
            print(f"PASS: Valuation for {stype} -> Budget: {safe_budget}, ROI: {d_val['roi_estimate_percent']}%", flush=True)

        print("\n=======================================================", flush=True)
        print("  ALL 9 TARGETED VERIFICATIONS COMPLETED & PASSED!     ", flush=True)
        print("=======================================================", flush=True)

if __name__ == "__main__":
    asyncio.run(run_detailed_verification())
