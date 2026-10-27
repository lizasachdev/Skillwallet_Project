"""
Demo Service — Realistic mock data for demonstration mode.
Used when no Gemini API key is configured.
"""
import random
import hashlib


def get_demo_ppe_response(image_bytes: bytes = None) -> dict:
    rng = random.Random()
    if image_bytes:
        seed = int(hashlib.md5(image_bytes).hexdigest()[:8], 16)
        rng.seed(seed)
    else:
        rng.seed(42)

    score = rng.randint(62, 88)
    harness_detected = rng.choice([True, False])
    harness_compliant = rng.choice([True, False]) if harness_detected else False

    return {
        "safety_score": score,
        "overall_status": "Partial Compliance" if score < 75 else "Compliant",
        "ppe_detection_checklist": [
            {"item": "Hard Hat/Helmet", "detected": True, "compliant": True, "notes": "Yellow hard hat detected, properly worn"},
            {"item": "High-Vis Vest", "detected": True, "compliant": True, "notes": "Fluorescent orange vest visible on workers"},
            {"item": "Steel-Toe Boots", "detected": False, "compliant": False, "notes": "Footwear not clearly visible in image"},
            {"item": "Safety Harness", "detected": harness_detected, "compliant": harness_compliant, "notes": "Partial harness visible on elevated worker" if harness_detected else "Not detected"},
            {"item": "Safety Gloves", "detected": False, "compliant": False, "notes": "Gloves not detected during material handling"},
            {"item": "Eye Protection", "detected": True, "compliant": True, "notes": "Safety goggles present during cutting operation"},
        ],
        "site_hazards": [
            {"hazard": "Unsecured scaffolding on north face", "severity": "High", "corrective_remedy": "Immediately secure scaffolding per IS 3696 standards with guardrails and mid-rails"},
            {"hazard": "Exposed rebar protruding without caps", "severity": "Medium", "corrective_remedy": "Install mushroom-style rebar caps on all exposed vertical rebar ends"},
            {"hazard": "Inadequate housekeeping — debris accumulation", "severity": "Low", "corrective_remedy": "Daily site cleanup protocol; designate waste collection zones"},
            {"hazard": "No signage for electrical hazard zones", "severity": "High", "corrective_remedy": "Install OSHA-compliant electrical hazard warning signs within 24 hours"},
        ],
        "summary": f"Construction site safety score: {score}/100. Workers show partial PPE compliance with helmets and vests present but gaps in foot protection and gloves. Critical scaffolding safety violations require immediate attention per OSHA 29 CFR 1926.451.",
        "recommendation": "Conduct immediate toolbox talk on PPE requirements. Issue mandatory steel-toe boots and gloves to all site personnel. Scaffold inspection by certified engineer within 4 hours.",
        "standard_reference": "OSHA 29 CFR 1926 / IS 456:2000"
    }


def get_demo_crack_response(image_bytes: bytes = None) -> dict:
    rng = random.Random()
    if image_bytes:
        seed = int(hashlib.md5(image_bytes).hexdigest()[:8], 16)
        rng.seed(seed)
    else:
        rng.seed(42)

    crack_types = ["Hairline", "Settlement", "Structural Shear", "Thermal Expansion", "Spalling"]
    crack_type = rng.choice(crack_types)
    width = round(rng.uniform(0.5, 6.0), 2)
    risk = rng.randint(25, 80)
    severity = "Low" if risk < 35 else "Medium" if risk < 55 else "High" if risk < 75 else "Critical"

    return {
        "crack_type": crack_type,
        "estimated_crack_width_mm": width,
        "severity": severity,
        "urgency": "Immediate" if severity == "Critical" else "Within 1 week" if severity == "High" else "Within 1 month",
        "root_causes": [
            "Thermal expansion and contraction cycles causing stress accumulation",
            "Inadequate reinforcement cover per IS 456:2000 Clause 26.4",
            "Foundation differential settlement due to non-uniform soil bearing capacity",
        ],
        "repair_recommendations": [
            {
                "method": "Epoxy Injection",
                "description": "Low-viscosity epoxy resin injected under pressure to seal and bond crack faces, restoring tensile strength to 95% of original",
                "estimated_cost_inr": "₹15,000 – ₹45,000 per linear meter"
            },
            {
                "method": "Structural Re-grouting",
                "description": "Cement-polymer grout injection for wider cracks (>2mm). Includes routing, cleaning with air blast, and sealed port injection",
                "estimated_cost_inr": "₹8,000 – ₹25,000 per linear meter"
            },
            {
                "method": "Carbon Fibre Reinforcement",
                "description": "CFRP strips bonded externally to bridge crack and prevent propagation under live loads",
                "estimated_cost_inr": "₹35,000 – ₹1,20,000 per 5m strip"
            }
        ],
        "structural_risk_score": risk,
        "summary": f"Detected {crack_type} crack with estimated width of {width}mm. Severity classified as {severity}. Root cause analysis indicates thermal-structural origin. Immediate engineering assessment recommended per IS 456:2000 and ACI 224R.",
        "immediate_action": "Restrict access to 3m exclusion zone. Document crack pattern with photogrammetry. Engage structural engineer within 48 hours for load-bearing assessment."
    }


def get_demo_weather_response(condition: str) -> dict:
    protocols = {
        "Normal": {
            "alerts": [
                {
                    "alert_type": "Routine Safety Briefing",
                    "condition": "Normal",
                    "protocol": "Standard site operations. Conduct morning toolbox talk. Verify all PPE in place. Ensure adequate hydration stations are set up.",
                    "severity": "Low",
                    "suspended_operations": []
                }
            ],
            "checklist": [
                "✅ Morning safety briefing completed",
                "✅ All PPE inspected and issued",
                "✅ Scaffolding daily inspection done",
                "✅ Emergency exits clear and marked",
                "✅ First aid kit stocked and accessible",
                "✅ Fire extinguishers checked",
                "✅ Electrical panels inspected"
            ],
            "risk_level": "Low"
        },
        "High Wind": {
            "alerts": [
                {
                    "alert_type": "Wind Hazard Alert",
                    "condition": "High Wind",
                    "protocol": "Wind speeds above 35 km/h: Suspend crane operations immediately. Secure all loose materials and debris. Workers on elevated platforms must use double-lanyard fall arrest systems.",
                    "severity": "Critical",
                    "suspended_operations": ["Tower Crane Operations", "Elevated Platform Work above 10m", "Precast Panel Erection", "Roofing Work", "Scaffolding Modification"]
                },
                {
                    "alert_type": "Electrical Hazard Mitigation",
                    "condition": "High Wind",
                    "protocol": "De-energize all temporary power lines within 2m of work zones. Ground all electrical equipment. Inspect overhead power line clearances.",
                    "severity": "High",
                    "suspended_operations": ["Overhead Electrical Work", "Antenna/Tower Installation"]
                }
            ],
            "checklist": [
                "🚨 Crane operations SUSPENDED — Wind >35 km/h",
                "⚠️ Secure all loose materials (formwork, sheets, lumber)",
                "⚠️ Double-lanyard fall arrest for all heights >2m",
                "⚠️ De-energize temporary power lines near work zones",
                "✅ Notify all subcontractors of wind warning",
                "✅ Document wind speed every hour",
                "✅ Structural engineer on standby for scaffold inspection"
            ],
            "risk_level": "Critical"
        },
        "Heavy Rain": {
            "alerts": [
                {
                    "alert_type": "Concrete Curing Protocol",
                    "condition": "Heavy Rain",
                    "protocol": "HALT all fresh concrete pours. Cover all freshly poured slabs with waterproof curing blankets. Maintain water-cement ratio records. Rain-affected concrete must be tested per IS 516.",
                    "severity": "High",
                    "suspended_operations": ["Fresh Concrete Pouring", "Masonry Laying", "Painting Operations", "Grouting"]
                },
                {
                    "alert_type": "Electrical Safety Protocol",
                    "condition": "Heavy Rain",
                    "protocol": "ALL electrical tools must be GFCI-protected. Shut down non-waterproofed electrical panels. Mandatory rubber-soled boots for all workers. Inspect temporary electrical connections.",
                    "severity": "Critical",
                    "suspended_operations": ["Non-GFCI Electrical Tools", "Open-Panel Electrical Work", "Welding in Open Areas"]
                },
                {
                    "alert_type": "Slope & Excavation Stability",
                    "condition": "Heavy Rain",
                    "protocol": "Inspect all excavations for water accumulation and slope erosion. Install dewatering pumps. No workers in excavations deeper than 1.2m without engineer sign-off.",
                    "severity": "High",
                    "suspended_operations": ["Deep Excavation Work", "Slope Grading"]
                }
            ],
            "checklist": [
                "🚨 ALL concrete pours HALTED",
                "🚨 GFCI protection verified on ALL electrical tools",
                "⚠️ Fresh concrete covered with waterproof sheeting",
                "⚠️ Excavations inspected for water accumulation",
                "⚠️ Dewatering pumps operational",
                "✅ Workers wearing rubber-soled boots",
                "✅ Temporary drainage channels cleared",
                "✅ Material storage elevated off ground level"
            ],
            "risk_level": "High"
        },
        "Extreme Heat": {
            "alerts": [
                {
                    "alert_type": "Heat Stroke Prevention Protocol",
                    "condition": "Extreme Heat",
                    "protocol": "Mandatory 10-minute rest breaks every 45 minutes. Provide 250ml water per worker per hour. Establish shaded rest stations. Rotate workers between sun-exposed and shaded tasks. Wet-bulb temperature monitoring required.",
                    "severity": "High",
                    "suspended_operations": ["Heavy Manual Labour 12pm-3pm", "Roof Work During Peak Hours", "Asphalt Paving 11am-4pm"]
                },
                {
                    "alert_type": "Concrete Curing Heat Protocol",
                    "condition": "Extreme Heat",
                    "protocol": "Increase concrete curing water frequency to every 2 hours. Use white-coloured curing blankets. Pre-cool mixing water with ice. Avoid pouring concrete when ambient temp >38°C per IS 7861.",
                    "severity": "Medium",
                    "suspended_operations": ["Concrete Pours above 38°C Ambient", "Bituminous Work in Peak Heat"]
                }
            ],
            "checklist": [
                "🚨 Mandatory rest breaks every 45 minutes",
                "🚨 250ml water per worker per hour — enforce hydration",
                "⚠️ Heavy manual work STOPPED 12pm–3pm",
                "⚠️ Shade stations erected at all work zones",
                "⚠️ Wet-bulb temperature logged hourly",
                "✅ First aid trained for heat stroke on site",
                "✅ Cold water storage in shaded coolers",
                "✅ Workers checking on buddy system every 30 min"
            ],
            "risk_level": "High"
        }
    }

    data = protocols.get(condition, protocols["Normal"])
    return {
        "condition": condition,
        "safety_alerts": data["alerts"],
        "daily_checklist": data["checklist"],
        "emergency_contacts": {
            "Site Safety Officer": "1800-200-5959",
            "Emergency Services": "112",
            "Fire Department": "101",
            "Medical Emergency": "108",
            "Poison Control": "1800-116-117"
        },
        "overall_risk_level": data["risk_level"]
    }


def get_demo_chat_response(message: str) -> dict:
    msg_lower = message.lower()

    if any(w in msg_lower for w in ["ppe", "helmet", "safety", "vest", "harness"]):
        response = """**PPE Requirements (OSHA 29 CFR 1926 / IS 456:2000):**

On all Indian construction sites, the following PPE is mandatory:
- 🪖 **Hard Hat (IS 2925)** — Class B for electrical hazards
- 🦺 **High-Visibility Vest** — ANSI/ISEA 107 Class 2 minimum
- 👟 **Steel-Toe Boots (IS 15298)** — Puncture-resistant sole required
- 🧤 **Safety Gloves** — Material-specific (cut-resistant for rebar, chemical for solvents)
- 👓 **Eye Protection (IS 5983)** — Z87.1 rated safety glasses
- 🔗 **Full-Body Harness** — Mandatory above 1.8m height (IS 3521)

**Penalty for Non-Compliance:** ₹2 lakh fine + site shutdown under Building & Other Construction Workers Act, 1996."""

    elif any(w in msg_lower for w in ["cost", "budget", "price", "estimate", "valuation", "inr"]):
        response = """**Construction Cost Estimates (India 2024):**

| Structure Type | Cost/sqft (INR) |
|---|---|
| Residential (Basic) | ₹1,200 – ₹1,800 |
| Residential (Premium) | ₹2,000 – ₹3,500 |
| Commercial | ₹2,500 – ₹4,000 |
| Industrial | ₹1,500 – ₹2,500 |

**Key Cost Components:**
- Civil work: ~45% of total budget
- Steel reinforcement: ~15% (@ ₹62,000–68,000/tonne)
- Cement (OPC 53 Grade): ~8% (@ ₹380–420/bag)
- Finishing & MEP: ~32%

Use Tab 3 (Real Estate Valuation) for detailed project-specific estimates."""

    elif any(w in msg_lower for w in ["crack", "structural", "repair", "foundation"]):
        response = """**Concrete Crack Assessment Guide (IS 456:2000):**

**Crack Width Classifications:**
- < 0.1mm: Aesthetic concern only, surface sealing sufficient
- 0.1–0.3mm: Hairline — Apply polymer-modified mortar
- 0.3–1mm: Minor structural — Epoxy injection required
- 1–3mm: Moderate — Structural grouting + investigation
- > 3mm: Major — Immediate structural engineer assessment

**Emergency Protocol for Critical Cracks:**
1. Evacuate affected zone (3m exclusion)
2. Install crack monitors/tell-tales
3. Engage structural engineer within 24 hours
4. Submit report under RERA Section 14 warranty

Upload crack images to Tab 2 for AI-powered diagnosis."""

    elif any(w in msg_lower for w in ["weather", "rain", "wind", "heat", "temperature"]):
        response = """**Weather-Based Construction Protocols (India):**

🌧️ **Heavy Rain:** Halt concrete pours, GFCI all electrical tools, inspect excavations for flooding
💨 **High Wind (>35 km/h):** Suspend crane operations, secure loose materials, double-lanyard for height work
🌡️ **Extreme Heat (>38°C):** 45-min work/10-min rest cycles, 250ml water/hour/worker, avoid concrete pouring
✅ **Normal:** Standard operations with daily PPE checks and toolbox talks

Switch to Tab 4 for real-time weather advisory and dynamic safety protocols."""

    elif any(w in msg_lower for w in ["material", "cement", "steel", "rebar", "concrete"]):
        response = """**Material Specifications (IS Standards):**

**Cement:**
- OPC 53 Grade (IS 12269): General RCC work
- PPC (IS 1489): Marine environments, sulfate resistance
- Quantity: 350–400 kg/m³ for M25 grade concrete

**Steel Reinforcement:**
- Fe 415 (IS 1786): Standard residential
- Fe 500D: High-seismic zones (Zone III-V)
- Coverage: 40mm clear cover for columns (IS 456 Cl.26.4.2)

**Concrete Mix Design (IS 10262):**
- M20: 1:1.5:3 (Residential slabs)
- M25: Columns and beams
- M30+: Foundations in aggressive soil

**Slump Requirements:**
- Slabs: 75–100mm
- Columns: 50–75mm
- Mass concrete: 25–50mm"""

    else:
        response = f"""I'm your **Construction Intelligence Assistant** 🏗️

I can help you with:
- **PPE Requirements** — OSHA/IS 456 compliance standards
- **Structural Analysis** — Crack types, repair methods, IS codes
- **Cost Estimation** — Budget planning in INR, material quantities
- **Weather Protocols** — Site safety for rain, wind, extreme heat
- **Material Specs** — Cement grades, steel standards, concrete mixes
- **Regulatory Compliance** — RERA, Building Codes, Labour Laws

You asked: *"{message}"*

Could you provide more specifics? For example:
- What type of structure are you working on?
- What is the current weather condition at your site?
- Are you facing a specific safety or structural challenge?"""

    return {
        "response": response,
        "suggested_followups": [
            "What PPE is mandatory on my construction site?",
            "How do I estimate material quantities for M25 concrete?",
            "What safety measures are needed during heavy rain?",
            "Explain crack classification per IS 456:2000"
        ]
    }
