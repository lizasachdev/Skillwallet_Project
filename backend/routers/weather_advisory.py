"""
Weather Advisory Router — Tab 4: Daily Site Assistant & Weather-Aware Advisory (Epic 5)
"""
from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from backend.models.schemas import ChatRequest, ChatResponse, WeatherCondition, WeatherAdvisoryResponse
from backend.services import gemini_service

router = APIRouter(prefix="/api/weather-advisory", tags=["Weather Advisory"])


@router.get("/advisory/{condition}")
async def get_weather_advisory(
    condition: str,
    location: Optional[str] = Query(None, description="Optional city or location name (e.g. Indore)")
):
    """
    Get weather-aware safety protocols and daily checklist.
    Optionally accepts a city/location name to retrieve live observations via Open-Meteo.
    Conditions: Normal, High Wind, Heavy Rain, Extreme Heat
    """
    valid_conditions = [c.value for c in WeatherCondition]
    if condition not in valid_conditions:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid condition. Choose from: {valid_conditions}"
        )

    clean_location = None
    if location is not None:
        clean_location = location.strip()
        if not clean_location:
            raise HTTPException(
                status_code=400,
                detail="Location cannot be blank. Please enter a valid city or location name."
            )

    try:
        result = await gemini_service.get_weather_advisory(condition, location=clean_location)
        return JSONResponse(content=result)
    except gemini_service.LocationNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except gemini_service.WeatherServiceError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Weather advisory generation failed. Please try again.")


@router.post("/chat", response_model=ChatResponse)
async def chat_with_assistant(req: ChatRequest):
    """
    Multi-turn construction engineering chatbot with weather context.
    """
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    try:
        history_dicts = [{"role": m.role, "content": m.content} for m in req.history]
        result = await gemini_service.chat_with_assistant(
            req.message,
            history_dicts,
            req.weather_condition.value
        )
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")
