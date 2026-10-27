import asyncio
from unittest.mock import patch
import httpx
from backend.main import app
from backend.services import gemini_service

async def run_tests():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        print("1. Testing advisory without location...", flush=True)
        r1 = await client.get("/api/weather-advisory/advisory/Normal")
        assert r1.status_code == 200, f"Expected 200, got {r1.status_code}: {r1.text}"
        data1 = r1.json()
        assert data1["condition"] == "Normal"
        assert data1.get("weather_observation") is None
        print("   [PASS] condition Normal, weather_observation is None", flush=True)

        print("2. Testing advisory with location=Indore...", flush=True)
        r2 = await client.get("/api/weather-advisory/advisory/Normal?location=Indore")
        assert r2.status_code == 200, f"Expected 200, got {r2.status_code}: {r2.text}"
        data2 = r2.json()
        assert data2.get("weather_observation") is not None
        obs = data2["weather_observation"]
        print(f"   [PASS] Resolved: {obs.get('location_name')}", flush=True)
        print(f"          Temperature: {obs.get('temperature_c')} C, Feels like: {obs.get('apparent_temperature_c')} C", flush=True)
        print(f"          Wind speed: {obs.get('wind_speed_kmh')} km/h, Precip: {obs.get('precipitation_mm')} mm", flush=True)
        print(f"          Obs time: {obs.get('observation_time')}", flush=True)
        print(f"          is_demo_advice: {data2.get('is_demo_advice')}, is_live_weather: {data2.get('is_live_weather')}", flush=True)

        print("3. Testing invalid location...", flush=True)
        r3 = await client.get("/api/weather-advisory/advisory/Normal?location=xyzinvalidnonexistent123456")
        assert r3.status_code == 404, f"Expected 404, got {r3.status_code}: {r3.text}"
        print(f"   [PASS] Got 404: {r3.json().get('detail')}", flush=True)

        print("4. Testing blank location...", flush=True)
        r4 = await client.get("/api/weather-advisory/advisory/Normal?location=%20%20")
        assert r4.status_code == 400, f"Expected 400, got {r4.status_code}: {r4.text}"
        print(f"   [PASS] Got 400: {r4.json().get('detail')}", flush=True)

        print("5. Testing simulated timeout / WeatherServiceError...", flush=True)
        with patch("backend.services.gemini_service.fetch_open_meteo_weather", side_effect=gemini_service.WeatherServiceError("Weather service timed out.")):
            r5 = await client.get("/api/weather-advisory/advisory/Normal?location=Indore")
            assert r5.status_code == 503, f"Expected 503, got {r5.status_code}: {r5.text}"
            print(f"   [PASS] Got 503 on timeout: {r5.json().get('detail')}", flush=True)

        print("6. Testing invalid weather condition...", flush=True)
        r6 = await client.get("/api/weather-advisory/advisory/Hurricane")
        assert r6.status_code == 422, f"Expected 422, got {r6.status_code}: {r6.text}"
        print(f"   [PASS] Got 422: {r6.json().get('detail')}", flush=True)

        print("7. Testing chatbot endpoint...", flush=True)
        r7 = await client.post("/api/weather-advisory/chat", json={"message": "What is mandatory PPE on site?", "weather_condition": "Normal"})
        assert r7.status_code == 200, f"Expected 200, got {r7.status_code}: {r7.text}"
        print(f"   [PASS] Chat responded ({len(r7.json().get('response', ''))} chars)", flush=True)

        print("\n>>> ALL 7 BACKEND INTEGRATION TESTS PASSED SUCCESSFULLY!", flush=True)

if __name__ == "__main__":
    asyncio.run(run_tests())
