"""
Gemini AI Service — Multimodal Construction Intelligence Platform
Handles all Google Gemini API interactions with graceful demo fallback.
"""
import os
import json
import base64
import re
from typing import Optional
import httpx
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
DEMO_MODE = not bool(GEMINI_API_KEY)

# Attempt to import Gemini SDK
try:
    import google.generativeai as genai
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


def is_demo_mode() -> bool:
    return DEMO_MODE or not GEMINI_AVAILABLE


def _clean_json_response(text: str) -> str:
    """Strip markdown code fences from Gemini response."""
    text = re.sub(r"```json\s*", "", text)
    text = re.sub(r"```\s*", "", text)
    return text.strip()


def get_available_gemini_models() -> list:
    """Retrieve usable models in order of performance and availability."""
    preferred_models = [
        "gemini-3.8-flash",
        "gemini-3-flash",
        "gemini-3.5-flash",
        "gemini-2.5-flash",
        "gemini-2.0-flash",
        "gemini-1.5-flash-latest",
        "gemini-1.5-flash",
        "gemini-2.0-flash-lite",
        "gemini-1.5-pro",
        "gemini-pro-vision",
        "gemini-pro"
    ]
    try:
        remote_models = [
            m.name.replace("models/", "")
            for m in genai.list_models()
            if "generateContent" in m.supported_generation_methods
        ]
        matched = [m for m in preferred_models if m in remote_models]
        if matched:
            return matched
        if remote_models:
            return remote_models
    except Exception:
        pass
    return preferred_models


async def analyze_ppe_safety(image_bytes: bytes, mime_type: str = "image/jpeg") -> dict:
    """Analyze construction site image for PPE compliance using Gemini Vision."""
    if is_demo_mode():
        from backend.services.demo_service import get_demo_ppe_response
        return get_demo_ppe_response(image_bytes)

    models_to_try = get_available_gemini_models()
    image_part = {"mime_type": mime_type, "data": image_bytes}
    generation_config = {"temperature": 0.1, "top_p": 0.95}

    prompt = """You are a certified construction safety auditor (OSHA 29 CFR 1926 / IS 456:2000).
Analyze this construction site image for PPE compliance and safety hazards.

Return ONLY valid JSON with this exact structure:
{
  "safety_score": <integer 0-100>,
  "overall_status": "<Compliant|Non-Compliant|Partial Compliance>",
  "ppe_detection_checklist": [
    {"item": "Hard Hat/Helmet", "detected": <bool>, "compliant": <bool>, "notes": "<string>"},
    {"item": "High-Vis Vest", "detected": <bool>, "compliant": <bool>, "notes": "<string>"},
    {"item": "Steel-Toe Boots", "detected": <bool>, "compliant": <bool>, "notes": "<string>"},
    {"item": "Safety Harness", "detected": <bool>, "compliant": <bool>, "notes": "<string>"},
    {"item": "Safety Gloves", "detected": <bool>, "compliant": <bool>, "notes": "<string>"},
    {"item": "Eye Protection", "detected": <bool>, "compliant": <bool>, "notes": "<string>"}
  ],
  "site_hazards": [
    {"hazard": "<string>", "severity": "<Low|Medium|High|Critical>", "corrective_remedy": "<string>"}
  ],
  "summary": "<2-3 sentence summary>",
  "recommendation": "<actionable recommendation>",
  "standard_reference": "OSHA 29 CFR 1926 / IS 456:2000"
}"""

    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name, generation_config=generation_config)
            response = model.generate_content([prompt, image_part])
            clean_text = _clean_json_response(response.text)
            match = re.search(r"\{.*\}", clean_text, re.DOTALL)
            if match:
                clean_text = match.group(0)
            return json.loads(clean_text)
        except Exception:
            continue

    from backend.services.demo_service import get_demo_ppe_response
    return get_demo_ppe_response(image_bytes)


async def analyze_crack(image_bytes: bytes, mime_type: str = "image/jpeg") -> dict:
    """Classify concrete/wall crack and provide engineering repair recommendations."""
    if is_demo_mode():
        from backend.services.demo_service import get_demo_crack_response
        return get_demo_crack_response(image_bytes)

    models_to_try = get_available_gemini_models()
    image_part = {"mime_type": mime_type, "data": image_bytes}
    generation_config = {"temperature": 0.1, "top_p": 0.95}

    prompt = """You are a structural engineer specializing in concrete diagnostics.
Analyze this concrete/wall surface image for cracks and structural issues.

Return ONLY valid JSON with this exact structure:
{
  "crack_type": "<Hairline|Settlement|Structural Shear|Thermal Expansion|Spalling|Unknown>",
  "estimated_crack_width_mm": <float>,
  "severity": "<Low|Medium|High|Critical>",
  "urgency": "<string, e.g. Immediate|Within 1 week|Within 1 month|Monitor>",
  "root_causes": ["<cause1>", "<cause2>"],
  "repair_recommendations": [
    {"method": "<e.g. Epoxy Injection>", "description": "<details>", "estimated_cost_inr": "<range>"},
    {"method": "<e.g. Structural Re-grouting>", "description": "<details>", "estimated_cost_inr": "<range>"}
  ],
  "structural_risk_score": <integer 0-100>,
  "summary": "<2-3 sentence engineering assessment>",
  "immediate_action": "<string>"
}"""

    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name, generation_config=generation_config)
            response = model.generate_content([prompt, image_part])
            clean_text = _clean_json_response(response.text)
            match = re.search(r"\{.*\}", clean_text, re.DOTALL)
            if match:
                clean_text = match.group(0)
            return json.loads(clean_text)
        except Exception:
            continue

    from backend.services.demo_service import get_demo_crack_response
    return get_demo_crack_response(image_bytes)


class LocationNotFoundError(Exception):
    """Raised when geocoding fails to resolve a location."""
    pass


class WeatherServiceError(Exception):
    """Raised when Open-Meteo API fails, times out, or encounters network errors."""
    pass


async def fetch_open_meteo_weather(location: str) -> dict:
    """
    Fetch live weather observation from Open-Meteo for a given city/location name.
    Does not require a paid API key.
    """
    clean_loc = location.strip()
    if not clean_loc:
        raise LocationNotFoundError("Location name cannot be blank.")

    async with httpx.AsyncClient(timeout=8.0) as client:
        # Step 1: Geocode city name
        try:
            geo_resp = await client.get(
                "https://geocoding-api.open-meteo.com/v1/search",
                params={"name": clean_loc, "count": 1, "language": "en", "format": "json"}
            )
        except httpx.TimeoutException:
            raise WeatherServiceError("Weather geocoding service timed out. Please try again.")
        except httpx.RequestError as exc:
            raise WeatherServiceError(f"Network error connecting to weather geocoding service: {str(exc)}")

        if geo_resp.status_code != 200:
            raise WeatherServiceError("Geocoding service returned an unexpected response.")

        geo_data = geo_resp.json()
        results = geo_data.get("results")
        if not results:
            raise LocationNotFoundError(f"Location '{clean_loc}' not found. Please check the spelling or enter a nearby city.")

        loc = results[0]
        lat = loc.get("latitude")
        lon = loc.get("longitude")
        name = loc.get("name", clean_loc)
        admin1 = loc.get("admin1")
        country = loc.get("country")

        parts = [name]
        if admin1 and admin1 != name:
            parts.append(admin1)
        if country:
            parts.append(country)
        resolved_name = ", ".join(parts)

        # Step 2: Fetch current weather readings
        try:
            weather_resp = await client.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": lat,
                    "longitude": lon,
                    "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,wind_speed_10m",
                    "timezone": "auto"
                }
            )
        except httpx.TimeoutException:
            raise WeatherServiceError("Weather observation service timed out. Please try again.")
        except httpx.RequestError as exc:
            raise WeatherServiceError(f"Network error connecting to weather forecast service: {str(exc)}")

        if weather_resp.status_code != 200:
            raise WeatherServiceError("Weather forecast service returned an unexpected response.")

        current = weather_resp.json().get("current", {})

        return {
            "location_name": resolved_name,
            "latitude": round(float(lat), 4) if lat is not None else 0.0,
            "longitude": round(float(lon), 4) if lon is not None else 0.0,
            "country": country,
            "admin1": admin1,
            "temperature_c": current.get("temperature_2m"),
            "apparent_temperature_c": current.get("apparent_temperature"),
            "relative_humidity_pct": current.get("relative_humidity_2m"),
            "wind_speed_kmh": current.get("wind_speed_10m"),
            "precipitation_mm": current.get("precipitation"),
            "observation_time": current.get("time", ""),
            "is_live": True
        }


async def get_weather_advisory(condition: str, location: Optional[str] = None) -> dict:
    """Generate weather-aware safety protocols for construction site, optionally incorporating live observations."""
    weather_obs = None
    if location and location.strip():
        weather_obs = await fetch_open_meteo_weather(location.strip())

    if is_demo_mode():
        from backend.services.demo_service import get_demo_weather_response
        result = get_demo_weather_response(condition)
        result["weather_observation"] = weather_obs
        result["is_demo_advice"] = True
        result["is_live_weather"] = weather_obs is not None
        return result

    obs_context = ""
    if weather_obs:
        obs_context = (
            f"\nLive Site Weather Observations at {weather_obs['location_name']}:\n"
            f"- Temperature: {weather_obs.get('temperature_c')}°C (Apparent / Feels-like: {weather_obs.get('apparent_temperature_c')}°C)\n"
            f"- Wind Speed: {weather_obs.get('wind_speed_kmh')} km/h\n"
            f"- Precipitation: {weather_obs.get('precipitation_mm')} mm\n"
            f"- Relative Humidity: {weather_obs.get('relative_humidity_pct')}%\n"
            f"- Observed Time: {weather_obs.get('observation_time')}\n"
        )

    prompt = f"""You are a construction site safety officer (OSHA 29 CFR 1926 / IS 456:2000).
Generate a comprehensive safety advisory for weather condition: {condition}
{obs_context}
Return ONLY valid JSON:
{{
  "condition": "{condition}",
  "safety_alerts": [
    {{
      "alert_type": "<type>",
      "condition": "{condition}",
      "protocol": "<detailed safety protocol>",
      "severity": "<Low|Medium|High|Critical>",
      "suspended_operations": ["<op1>", "<op2>"]
    }}
  ],
  "daily_checklist": ["<item1>", "<item2>", "<item3>", "<item4>", "<item5>"],
  "emergency_contacts": {{
    "Site Safety Officer": "1800-XXX-XXXX",
    "Emergency Services": "112",
    "Fire Department": "101",
    "Medical Emergency": "108"
  }},
  "overall_risk_level": "<Low|Medium|High|Critical>"
}}"""

    models_to_try = get_available_gemini_models()
    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            parsed = json.loads(_clean_json_response(response.text))
            parsed["weather_observation"] = weather_obs
            parsed["is_demo_advice"] = False
            parsed["is_live_weather"] = weather_obs is not None
            return parsed
        except Exception:
            continue

    from backend.services.demo_service import get_demo_weather_response
    result = get_demo_weather_response(condition)
    result["weather_observation"] = weather_obs
    result["is_demo_advice"] = True
    result["is_live_weather"] = weather_obs is not None
    return result


async def chat_with_assistant(message: str, history: list, weather: str) -> dict:
    """Multi-turn construction engineering chatbot."""
    if is_demo_mode():
        from backend.services.demo_service import get_demo_chat_response
        return get_demo_chat_response(message)

    models_to_try = get_available_gemini_models()

    system_ctx = f"""You are an expert construction engineering assistant for the Multimodal Construction Intelligence Platform.
You specialize in: structural engineering, PPE safety (OSHA/IS 456), construction planning, cost estimation in INR, 
material specifications, and weather-aware construction protocols. Current site weather: {weather}.
Provide concise, actionable, technically accurate answers. Always reference Indian construction standards where relevant."""

    # Build conversation
    conversation_text = system_ctx + "\n\n"
    for msg in history[-6:]:  # last 3 turns
        role_label = "User" if msg.get("role") == "user" else "Assistant"
        conversation_text += f"{role_label}: {msg.get('content', '')}\n"
    conversation_text += f"User: {message}\n\nAssistant:"

    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(conversation_text)
            reply = response.text.strip()
            return {
                "response": reply,
                "suggested_followups": [
                    "What are the safety protocols for this weather?",
                    "Estimate material costs for a 2000 sqft structure",
                    "What PPE is mandatory on site today?"
                ]
            }
        except Exception:
            continue

    from backend.services.demo_service import get_demo_chat_response
    return get_demo_chat_response(message)
