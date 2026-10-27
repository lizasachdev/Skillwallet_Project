import asyncio
import httpx
from backend.main import app

async def main():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        print("1. Testing /api/health...", flush=True)
        res = await client.get("/api/health")
        assert res.status_code == 200, f"Health check failed: {res.text}"
        data = res.json()
        print(f"   [PASS] Status: {data['status']}, Platform ID: {data['platform_id']}", flush=True)

        print("2. Testing /api/ppe-safety/demo...", flush=True)
        res = await client.get("/api/ppe-safety/demo")
        assert res.status_code == 200, f"PPE demo failed: {res.text}"
        ppe = res.json()
        print(f"   [PASS] Safety score: {ppe['safety_score']}/100, Hazards: {len(ppe['site_hazards'])}", flush=True)

        print("3. Testing /api/crack-analysis/demo...", flush=True)
        res = await client.get("/api/crack-analysis/demo")
        assert res.status_code == 200, f"Crack demo failed: {res.text}"
        crack = res.json()
        print(f"   [PASS] Crack type: {crack['crack_type']}, Width: {crack['estimated_crack_width_mm']}mm", flush=True)

        print("4. Testing /api/valuation/calculate...", flush=True)
        val_payload = {
            "structure_type": "Residential",
            "built_up_sqft": 2500,
            "location_tier": "Tier 1",
            "completion_percentage": 60,
            "floors": 3,
            "project_name": "Skyline Heights"
        }
        res = await client.post("/api/valuation/calculate", json=val_payload)
        assert res.status_code == 200, f"Valuation failed: {res.text}"
        val = res.json()
        print(f"   [PASS] Budget: {val['total_project_budget_inr']}, CapEx: {val['capital_expenditure_incurred_inr']}", flush=True)

        print("5. Testing /api/weather-advisory/advisory/High Wind...", flush=True)
        res = await client.get("/api/weather-advisory/advisory/High Wind")
        assert res.status_code == 200, f"Weather advisory failed: {res.text}"
        weather = res.json()
        print(f"   [PASS] Weather risk: {weather['overall_risk_level']}, Alerts: {len(weather['safety_alerts'])}", flush=True)

        print("6. Testing /api/weather-advisory/chat...", flush=True)
        chat_payload = {
            "message": "What is the recommended rebar cover per IS 456?",
            "weather_condition": "Normal"
        }
        res = await client.post("/api/weather-advisory/chat", json=chat_payload)
        assert res.status_code == 200, f"Chat failed: {res.text}"
        chat = res.json()
        print(f"   [PASS] Chat response received ({len(chat['response'])} chars)", flush=True)

        print("\n==========================================", flush=True)
        print(" ALL 6 BACKEND API TESTS PASSED! ", flush=True)
        print("==========================================", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
