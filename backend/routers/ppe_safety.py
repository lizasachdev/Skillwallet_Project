"""
PPE Safety Router — Tab 1: Site Safety & PPE Audit (Epic 2)
"""
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from backend.models.schemas import PPESafetyResponse
from backend.services import gemini_service

router = APIRouter(prefix="/api/ppe-safety", tags=["PPE Safety"])


@router.post("/analyze", response_model=PPESafetyResponse)
async def analyze_site_safety(file: UploadFile = File(...)):
    """
    Upload a construction site photo (JPG/PNG) and receive:
    - PPE compliance checklist (helmet, vest, boots, harness, gloves, eye protection)
    - Safety score (0-100)
    - Site hazards with severity and corrective remedies
    """
    if file.content_type not in ["image/jpeg", "image/jpg", "image/png", "image/webp"]:
        raise HTTPException(status_code=400, detail="Only JPG, PNG, or WebP images are accepted.")

    try:
        image_bytes = await file.read()
        if len(image_bytes) > 10 * 1024 * 1024:  # 10MB limit
            raise HTTPException(status_code=413, detail="Image file too large. Maximum size is 10MB.")

        result = await gemini_service.analyze_ppe_safety(image_bytes, file.content_type)
        return JSONResponse(content=result)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.get("/demo")
async def get_demo_ppe():
    """Get demo PPE analysis without uploading an image."""
    from backend.services.demo_service import get_demo_ppe_response
    return get_demo_ppe_response()
