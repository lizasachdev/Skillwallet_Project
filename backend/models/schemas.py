from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


# ─── Shared ───────────────────────────────────────────────────────────────────

class SeverityLevel(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class OverallStatus(str, Enum):
    COMPLIANT = "Compliant"
    NON_COMPLIANT = "Non-Compliant"
    PARTIAL = "Partial Compliance"
    SAFE = "Safe"
    UNSAFE = "Unsafe"
    WARNING = "Warning"


# ─── PPE Safety ───────────────────────────────────────────────────────────────

class PPEItem(BaseModel):
    item: str
    detected: bool
    compliant: bool
    notes: str = ""


class SiteHazard(BaseModel):
    hazard: str
    severity: SeverityLevel
    corrective_remedy: str


class PPESafetyResponse(BaseModel):
    safety_score: int = Field(..., ge=0, le=100)
    overall_status: OverallStatus
    ppe_detection_checklist: List[PPEItem]
    site_hazards: List[SiteHazard]
    summary: str
    recommendation: str
    standard_reference: str = "OSHA 29 CFR 1926 / IS 456:2000"


# ─── Crack Diagnostics ────────────────────────────────────────────────────────

class CrackType(str, Enum):
    HAIRLINE = "Hairline"
    SETTLEMENT = "Settlement"
    STRUCTURAL_SHEAR = "Structural Shear"
    THERMAL_EXPANSION = "Thermal Expansion"
    SPALLING = "Spalling"
    UNKNOWN = "Unknown"


class RepairMethod(BaseModel):
    method: str
    description: str
    estimated_cost_inr: str


class CrackDiagnosticsResponse(BaseModel):
    crack_type: CrackType
    estimated_crack_width_mm: float
    severity: SeverityLevel
    urgency: str
    root_causes: List[str]
    repair_recommendations: List[RepairMethod]
    structural_risk_score: int = Field(..., ge=0, le=100)
    summary: str
    immediate_action: str


# ─── Valuation ────────────────────────────────────────────────────────────────

class LocationTier(str, Enum):
    TIER_1 = "Tier 1"
    TIER_2 = "Tier 2"
    TIER_3 = "Tier 3"


class StructureType(str, Enum):
    RESIDENTIAL = "Residential"
    COMMERCIAL = "Commercial"
    INDUSTRIAL = "Industrial"
    MIXED_USE = "Mixed Use"
    INSTITUTIONAL = "Institutional"


class ValuationRequest(BaseModel):
    structure_type: StructureType
    built_up_sqft: float = Field(..., gt=0)
    location_tier: LocationTier
    completion_percentage: float = Field(..., ge=0, le=100)
    floors: int = Field(default=1, ge=1)
    project_name: str = ""


class MaterialRequirement(BaseModel):
    material: str
    quantity: str
    unit: str
    estimated_cost_inr: str


class MilestoneProgress(BaseModel):
    milestone: str
    percentage: float
    completed: bool


class ValuationResponse(BaseModel):
    total_project_budget_inr: str
    capital_expenditure_incurred_inr: str
    current_market_asset_valuation_inr: str
    cost_per_sqft_inr: float
    material_requirements: List[MaterialRequirement]
    milestone_progress: List[MilestoneProgress]
    roi_estimate_percent: float
    summary: str
    architectural_prompt: str  # For Pollinations AI rendering


# ─── Weather Advisory ─────────────────────────────────────────────────────────

class WeatherCondition(str, Enum):
    NORMAL = "Normal"
    HIGH_WIND = "High Wind"
    HEAVY_RAIN = "Heavy Rain"
    EXTREME_HEAT = "Extreme Heat"


class SafetyAlert(BaseModel):
    alert_type: str
    condition: str
    protocol: str
    severity: SeverityLevel
    suspended_operations: List[str]


class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    message: str
    history: List[ChatMessage] = []
    weather_condition: WeatherCondition = WeatherCondition.NORMAL


class ChatResponse(BaseModel):
    response: str
    suggested_followups: List[str] = []


class WeatherObservation(BaseModel):
    location_name: str
    latitude: float
    longitude: float
    country: Optional[str] = None
    admin1: Optional[str] = None
    temperature_c: Optional[float] = None
    apparent_temperature_c: Optional[float] = None
    relative_humidity_pct: Optional[float] = None
    wind_speed_kmh: Optional[float] = None
    precipitation_mm: Optional[float] = None
    observation_time: str = ""
    is_live: bool = True


class WeatherAdvisoryResponse(BaseModel):
    condition: WeatherCondition
    safety_alerts: List[SafetyAlert]
    daily_checklist: List[str]
    emergency_contacts: Dict[str, str]
    overall_risk_level: SeverityLevel
    weather_observation: Optional[WeatherObservation] = None
    is_demo_advice: bool = True
    is_live_weather: bool = False
