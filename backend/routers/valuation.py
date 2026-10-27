"""
Valuation Router — Tab 3: Project Planning & Real Estate Valuation (Epic 3)
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from backend.models.schemas import ValuationRequest, ValuationResponse, LocationTier, StructureType

router = APIRouter(prefix="/api/valuation", tags=["Real Estate Valuation"])

# Cost per sqft by structure type and tier (INR)
COST_MATRIX = {
    "Residential": {"Tier 1": 2200, "Tier 2": 1800, "Tier 3": 1400},
    "Commercial":  {"Tier 1": 3800, "Tier 2": 3200, "Tier 3": 2600},
    "Industrial":  {"Tier 1": 2800, "Tier 2": 2200, "Tier 3": 1800},
    "Mixed Use":   {"Tier 1": 3200, "Tier 2": 2600, "Tier 3": 2100},
    "Institutional": {"Tier 1": 3000, "Tier 2": 2400, "Tier 3": 1900},
}

# Market multipliers for asset valuation
MARKET_MULTIPLIER = {
    "Tier 1": 1.85,
    "Tier 2": 1.45,
    "Tier 3": 1.20,
}

MILESTONES = [
    ("Site Preparation & Foundation", 15),
    ("Sub-structure (Basement/Plinth)", 30),
    ("Super-structure (RCC Frame)", 55),
    ("Masonry & Plastering", 70),
    ("MEP Rough-in & Finishing", 85),
    ("Interior Works & Handover", 100),
]

def format_inr(amount: float) -> str:
    if amount >= 1e7:
        return f"₹{amount/1e7:.2f} Cr"
    elif amount >= 1e5:
        return f"₹{amount/1e5:.2f} L"
    else:
        return f"₹{amount:,.0f}"


@router.post("/calculate", response_model=ValuationResponse)
async def calculate_valuation(req: ValuationRequest):
    """
    Calculate construction budget, CapEx, real estate valuation,
    material requirements, and milestone progress.
    """
    try:
        cost_per_sqft = COST_MATRIX[req.structure_type][req.location_tier]
        total_sqft = req.built_up_sqft * req.floors
        total_budget = total_sqft * cost_per_sqft
        capex_incurred = total_budget * (req.completion_percentage / 100)
        asset_valuation = total_budget * MARKET_MULTIPLIER[req.location_tier]

        # Material requirements (simplified IS 456 thumb rules)
        concrete_volume = total_sqft * 0.05  # approx m³
        steel_kg = total_sqft * 4.5 * req.floors  # ~4.5 kg/sqft
        cement_bags = concrete_volume * 8.0  # M25 grade
        sand_tonnes = concrete_volume * 0.55
        aggregate_tonnes = concrete_volume * 0.85

        materials = [
            {
                "material": "Steel Reinforcement (Fe 500D)",
                "quantity": f"{steel_kg/1000:.1f}",
                "unit": "Tonnes",
                "estimated_cost_inr": format_inr(steel_kg * 65)  # ₹65/kg
            },
            {
                "material": "Cement (OPC 53 Grade)",
                "quantity": f"{cement_bags:.0f}",
                "unit": "Bags (50kg)",
                "estimated_cost_inr": format_inr(cement_bags * 400)  # ₹400/bag
            },
            {
                "material": "Fine Sand (River Sand)",
                "quantity": f"{sand_tonnes:.1f}",
                "unit": "Tonnes",
                "estimated_cost_inr": format_inr(sand_tonnes * 1800)
            },
            {
                "material": "Coarse Aggregate (20mm)",
                "quantity": f"{aggregate_tonnes:.1f}",
                "unit": "Tonnes",
                "estimated_cost_inr": format_inr(aggregate_tonnes * 1500)
            },
            {
                "material": "Concrete Blocks / Bricks",
                "quantity": f"{total_sqft * 8:.0f}",
                "unit": "Nos",
                "estimated_cost_inr": format_inr(total_sqft * 8 * 12)
            },
        ]

        milestone_progress = [
            {
                "milestone": name,
                "percentage": float(pct),
                "completed": req.completion_percentage >= pct
            }
            for name, pct in MILESTONES
        ]

        roi = ((asset_valuation - total_budget) / total_budget) * 100

        # Architectural rendering prompt for Pollinations AI
        arch_prompt = (
            f"Photorealistic architectural rendering of a modern {req.structure_type.lower()} building, "
            f"{req.floors} floor{'s' if req.floors > 1 else ''}, {req.built_up_sqft:.0f} sqft, "
            f"Indian city {req.location_tier} urban setting, contemporary design with glass facades, "
            f"green landscaping, daytime lighting, professional architectural visualization, 8K quality"
        )

        return JSONResponse(content={
            "total_project_budget_inr": format_inr(total_budget),
            "capital_expenditure_incurred_inr": format_inr(capex_incurred),
            "current_market_asset_valuation_inr": format_inr(asset_valuation),
            "cost_per_sqft_inr": cost_per_sqft,
            "material_requirements": materials,
            "milestone_progress": milestone_progress,
            "roi_estimate_percent": round(roi, 1),
            "summary": (
                f"{req.project_name or req.structure_type + ' Project'}: {total_sqft:,.0f} sqft "
                f"in {req.location_tier} city. Total budget {format_inr(total_budget)} with "
                f"{req.completion_percentage}% completion ({format_inr(capex_incurred)} CapEx incurred). "
                f"Estimated market valuation: {format_inr(asset_valuation)}. ROI: {roi:.1f}%."
            ),
            "architectural_prompt": arch_prompt
        })

    except KeyError as e:
        raise HTTPException(status_code=422, detail=f"Invalid structure type or location tier: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Valuation failed: {str(e)}")
