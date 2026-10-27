# 🏗️ Multimodal Construction Intelligence Platform
**Skill Wallet Capstone Project 1 | Platform ID: 6ac4c98d1dcde6d7857c1642**

> An AI-powered full-stack decision-support system for construction professionals. Analyzes site photos for PPE compliance, classifies concrete cracks, estimates real estate valuation in INR, and provides weather-aware safety protocols — powered by **Google Gemini 1.5 Flash**.

[![Category](https://img.shields.io/badge/Category-Generative%20AI%20%7C%20Real%20Estate-blue)](.)
[![Tech](https://img.shields.io/badge/Tech-Python%20%7C%20FastAPI%20%7C%20React%20%7C%20Streamlit-green)](.)
[![AI](https://img.shields.io/badge/AI-Google%20Gemini%201.5%20Flash-orange)](.)

---

## 📋 Features

| Module | Epic | Description |
|--------|------|-------------|
| 🦺 PPE Safety Audit | Epic 2 | OSHA / IS 456:2000 compliance analysis from site photos |
| 🔍 Crack Diagnostics | Epic 2 | Structural crack classification with repair recommendations |
| 🏗️ Real Estate Valuation | Epic 3 | Budget, CapEx, material estimation in INR |
| 🌤️ Weather Advisory + Chatbot | Epic 5 | Dynamic safety protocols + AI construction assistant |

---

## 🚀 Quick Start

### Option 1: Streamlit App (Recommended — 1-click deployment)

```bash
# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run streamlit_app.py
```

Open http://localhost:8501

### Option 2: Full Stack (FastAPI + React)

**Terminal 1 — Backend:**
```bash
# Install backend dependencies
pip install -r backend/requirements.txt

# Start FastAPI server
uvicorn backend.main:app --reload --port 8000
```

**Terminal 2 — Frontend:**
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

---

## 🔑 Configuration

Create a `.env` file from the template:
```bash
cp .env.example .env
```

Edit `.env` and add your Gemini API key:
```
GEMINI_API_KEY=your_key_here
```

> **No API key?** The app runs in **Demo Mode** with realistic mock data automatically. Get a free key at [Google AI Studio](https://aistudio.google.com/app/apikey).

---

## 🏛️ Architecture

```
┌─────────────────────────────────────┐
│  React 18 + Vite Frontend           │
│  (localhost:5173)                   │
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐       │
│  │PPE │ │Crack│ │Val.│ │Chat│       │
└──┴────┴─┴────┴─┴────┴─┴────┴───────┘
                  │ /api/*
┌─────────────────────────────────────┐
│  FastAPI Backend (localhost:8000)   │
│  ┌─────────────────────────────┐    │
│  │  Google Gemini 1.5 Flash   │    │
│  │  Multimodal Vision + Text  │    │
│  └─────────────────────────────┘    │
└─────────────────────────────────────┘
```

---

## 📁 Project Structure

```
Skillwallet_project/
├── streamlit_app.py          # Streamlit app (deploy on Community Cloud)
├── requirements.txt          # Streamlit dependencies
├── .env.example
│
├── backend/                  # FastAPI backend
│   ├── main.py               # FastAPI entry point
│   ├── requirements.txt
│   ├── models/schemas.py     # Pydantic JSON contracts
│   ├── services/
│   │   ├── gemini_service.py # Gemini AI integration
│   │   └── demo_service.py   # Demo fallback data
│   └── routers/
│       ├── ppe_safety.py
│       ├── crack_analysis.py
│       ├── valuation.py
│       └── weather_advisory.py
│
└── frontend/                 # React + Vite frontend
    ├── src/
    │   ├── App.jsx
    │   ├── index.css
    │   └── components/
    │       ├── Sidebar.jsx
    │       ├── tabs/
    │       │   ├── PPESafety.jsx
    │       │   ├── CrackDiagnostics.jsx
    │       │   ├── RealEstateValuation.jsx
    │       │   └── WeatherAdvisory.jsx
    │       └── ui/
    └── vite.config.js
```

---

## 📐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/ppe-safety/analyze` | PPE compliance analysis (image upload) |
| GET | `/api/ppe-safety/demo` | Demo PPE response |
| POST | `/api/crack-analysis/analyze` | Crack diagnostics (image upload) |
| GET | `/api/crack-analysis/demo` | Demo crack response |
| POST | `/api/valuation/calculate` | Budget + valuation calculation |
| GET | `/api/weather-advisory/advisory/{condition}` | Weather safety protocols (optional `?location=city` for live Open-Meteo observations) |
| POST | `/api/weather-advisory/chat` | AI construction chatbot |
| GET | `/api/health` | System health check |
| GET | `/api/docs` | Swagger UI |

---

## 📏 Compliance Standards

- **OSHA 29 CFR 1926** — Construction Industry Safety and Health Standards
- **IS 456:2000** — Plain and Reinforced Concrete Code of Practice
- **IS 3696** — Scaffolding and Ladders — Safety Code
- **IS 1786** — High Strength Deformed Steel Bars
- **IS 2925** — Industrial Safety Helmets
- **RERA** — Real Estate (Regulation and Development) Act, 2016

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, Vite, Axios, CSS |
| Backend | Python 3.9+, FastAPI, Uvicorn |
| Streamlit | Streamlit 1.35 |
| AI | Google Gemini 1.5 Flash |
| Image Gen | Pollinations AI (architectural renders) |
| Data Contracts | Pydantic v2 |
| Styling | Custom CSS Design System |

---

*Built for Skill Wallet Capstone Project 1 · Category: Generative AI | Real Estate Decision Support*
