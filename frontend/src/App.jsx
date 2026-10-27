import { useState, useEffect } from 'react'
import Sidebar from './components/Sidebar'
import PPESafety from './components/tabs/PPESafety'
import CrackDiagnostics from './components/tabs/CrackDiagnostics'
import RealEstateValuation from './components/tabs/RealEstateValuation'
import WeatherAdvisory from './components/tabs/WeatherAdvisory'
import { apiUrl } from './api'

const TABS = [
  {
    id: 'ppe',
    label: 'PPE Safety Audit',
    subtitle: 'Epic 2 — OSHA / IS 456',
    icon: '🦺',
    epic: 'E2',
    header: 'Site Safety & PPE Audit',
    description: 'AI-powered PPE compliance analysis and hazard detection using Google Gemini Vision',
    component: PPESafety,
  },
  {
    id: 'crack',
    label: 'Crack Diagnostics',
    subtitle: 'Epic 2 — Structural Integrity',
    icon: '🔍',
    epic: 'E2',
    header: 'Crack Diagnostics & Structural Integrity',
    description: 'Classify concrete defects, estimate crack width, and get AI-driven repair recommendations',
    component: CrackDiagnostics,
  },
  {
    id: 'valuation',
    label: 'Project Valuation',
    subtitle: 'Epic 3 — Real Estate & Planning',
    icon: '🏗️',
    epic: 'E3',
    header: 'Planning & Real Estate Valuation',
    description: 'Construction budgeting, CapEx tracking, asset valuation in INR, and architectural rendering',
    component: RealEstateValuation,
  },
  {
    id: 'weather',
    label: 'Site Assistant',
    subtitle: 'Epic 5 — Weather Advisory',
    icon: '🌤️',
    epic: 'E5',
    header: 'Daily Site Assistant & Weather Advisory',
    description: 'Real-time weather-aware safety protocols and multi-turn construction engineering chatbot',
    component: WeatherAdvisory,
  },
]

export default function App() {
  const [activeTab, setActiveTab] = useState('ppe')
  const [apiKey, setApiKey] = useState(localStorage.getItem('gemini_api_key') || '')
  const [isDemo, setIsDemo] = useState(true)
  const [backendStatus, setBackendStatus] = useState('checking')

  async function checkBackendHealth() {
    try {
      const res = await fetch(apiUrl('/api/health'))
      if (res.ok) {
        const data = await res.json()
        setIsDemo(data.mode === 'demo')
        setBackendStatus('online')
      } else {
        setBackendStatus('offline')
      }
    } catch {
      setBackendStatus('offline')
    }
  }

  useEffect(() => {
    if (apiKey) localStorage.setItem('gemini_api_key', apiKey)
    checkBackendHealth()
  }, [apiKey])

  const currentTab = TABS.find(t => t.id === activeTab)
  const TabComponent = currentTab.component

  return (
    <div className="app-shell">
      <Sidebar
        tabs={TABS}
        activeTab={activeTab}
        onTabChange={setActiveTab}
        apiKey={apiKey}
        onApiKeyChange={setApiKey}
        isDemo={isDemo}
        backendStatus={backendStatus}
      />

      <main className="main-content">
        <header className="page-header">
          <div className="page-header-left">
            <h2>{currentTab.header}</h2>
            <p>{currentTab.description}</p>
          </div>
          <div className="header-status-chips">
            <span
              className="status-pill"
              style={{
                background: backendStatus === 'online'
                  ? 'rgba(16,185,129,0.12)'
                  : 'rgba(244,63,94,0.12)',
                color: backendStatus === 'online' ? '#10b981' : '#f43f5e',
                borderColor: backendStatus === 'online'
                  ? 'rgba(16,185,129,0.3)'
                  : 'rgba(244,63,94,0.3)',
              }}
            >
              <span style={{
                width: 6, height: 6, borderRadius: '50%',
                background: 'currentColor', display: 'inline-block',
                animation: 'pulse 2s infinite'
              }} />
              {backendStatus === 'online' ? 'API Online' : 'Demo Mode'}
            </span>
            <span className={`mode-badge ${isDemo ? 'demo' : 'live'}`}>
              <span className="dot" />
              {isDemo ? 'Demo Mode' : 'Live AI'}
            </span>
          </div>
        </header>

        <div className="page-content fade-in">
          <TabComponent apiKey={apiKey} isDemo={isDemo} />
        </div>
      </main>
    </div>
  )
}
