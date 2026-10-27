"""
Crack Analysis Router — Tab 2: Crack Diagnostics & Structural Integrity (Epic 2)
"""
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from backend.models.schemas import CrackDiagnosticsResponse
from backend.services import gemini_service

router = APIRouter(prefix="/api/crack-analysis", tags=["Crack Diagnostics"])


@router.post("/analyze", response_model=CrackDiagnosticsResponse)
async def analyze_crack(file: UploadFile = File(...)):
    """
    Upload a concrete/wall surface photo and receive:
    - Crack type classification (Hairline, Settlement, Structural Shear, etc.)
    - Estimated crack width in mm
    - Root causes and recommended repairs (epoxy injection, re-grouting)
    - Structural risk score (0-100) and urgency level
    """
    if file.content_type not in ["image/jpeg", "image/jpg", "image/png", "image/webp"]:
        raise HTTPException(status_code=400, detail="Only JPG, PNG, or WebP images are accepted.")

    try:
        image_bytes = await file.read()
        if len(image_bytes) > 10 * 1024 * 1024:
            raise HTTPException(status_code=413, detail="Image file too large. Maximum size is 10MB.")

        result = await gemini_service.analyze_crack(image_bytes, file.content_type)
        return JSONResponse(content=result)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.get("/demo")
async def get_demo_crack():
    """Get demo crack analysis without uploading an image."""
    from backend.services.demo_service import get_demo_crack_response
    return get_demo_crack_response()
