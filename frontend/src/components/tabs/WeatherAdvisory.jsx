import { useState, useEffect, useRef } from 'react'
import axios from 'axios'
import { apiUrl } from '../../api'

const WEATHER_CONDITIONS = [
  { id: 'Normal', icon: '☀️', label: 'Normal', desc: 'Standard operations' },
  { id: 'High Wind', icon: '💨', label: 'High Wind', desc: 'Wind > 35 km/h' },
  { id: 'Heavy Rain', icon: '🌧️', label: 'Heavy Rain', desc: 'Rainfall alert' },
  { id: 'Extreme Heat', icon: '🌡️', label: 'Extreme Heat', desc: 'Temp > 38°C' },
]

const SUGGESTED_QUESTIONS = [
  'What PPE is mandatory on my construction site today?',
  'How do I estimate concrete quantity for M25 grade?',
  'What safety protocols apply for high wind conditions?',
  'Explain crack classification per IS 456:2000',
  'What is the rate of steel reinforcement in India 2024?',
  'How to prevent heat stroke on construction site?',
]

function formatMarkdown(text) {
  return text
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/`(.+?)`/g, '<code>$1</code>')
    .replace(/\n/g, '<br/>')
}

export default function WeatherAdvisory() {
  const [weather, setWeather] = useState('Normal')
  const [locationInput, setLocationInput] = useState('')
  const [activeLocation, setActiveLocation] = useState('')
  const [locationError, setLocationError] = useState(null)
  const [advisory, setAdvisory] = useState(null)
  const [advisoryLoading, setAdvisoryLoading] = useState(false)
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: '👋 Hello! I\'m your **Construction Intelligence Assistant**.\n\nI specialize in construction engineering, PPE safety standards, structural analysis, material specifications, and weather-aware site protocols. How can I help you today?\n\nYou can ask me about:\n- PPE requirements and OSHA/IS 456 standards\n- Crack assessment and repair methods\n- Construction cost estimation in INR\n- Material specifications and quantities\n- Weather-specific safety protocols'
    }
  ])
  const [chatInput, setChatInput] = useState('')
  const [chatLoading, setChatLoading] = useState(false)
  const messagesEndRef = useRef(null)

  useEffect(() => {
    fetchAdvisory('Normal', '')
  }, [])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  async function fetchAdvisory(condition, loc = activeLocation) {
    setAdvisoryLoading(true)
    setLocationError(null)
    try {
      const url = loc
        ? `/api/weather-advisory/advisory/${encodeURIComponent(condition)}?location=${encodeURIComponent(loc)}`
        : `/api/weather-advisory/advisory/${encodeURIComponent(condition)}`
     const res = await axios.get(apiUrl(url))
      setAdvisory(res.data)
    } catch (err) {
      const detail = err.response?.data?.detail || 'Failed to retrieve weather advisory. Please check connection.'
      setLocationError(detail)
      setAdvisory(null)
    } finally {
      setAdvisoryLoading(false)
    }
  }

  function handleLocationSubmit(e) {
    if (e) e.preventDefault()
    const trimmed = locationInput.trim()
    if (!trimmed) {
      setLocationError('Please enter a city or location name.')
      return
    }
    setLocationError(null)
    setActiveLocation(trimmed)
    fetchAdvisory(weather, trimmed)
  }

  function handleConditionClick(conditionId) {
    setWeather(conditionId)
    fetchAdvisory(conditionId, activeLocation)
  }

  function handleClearLocation() {
    setLocationInput('')
    setActiveLocation('')
    setLocationError(null)
    fetchAdvisory(weather, '')
  }

  async function sendMessage(text) {
    const msg = text || chatInput.trim()
    if (!msg) return

    setChatInput('')
    const userMsg = { role: 'user', content: msg }
    const newMessages = [...messages, userMsg]
    setMessages(newMessages)
    setChatLoading(true)

    try {
      const history = newMessages.slice(0, -1).map(m => ({ role: m.role, content: m.content }))
      const res = await axios.post(apiUrl('/api/weather-advisory/chat'), {
        message: msg,
        history,
        weather_condition: weather,
      })
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: res.data.response,
        followups: res.data.suggested_followups || [],
      }])
    } catch {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: '⚠️ **Connection Error**: Could not reach the backend server. Please ensure the FastAPI server is running on port 8000.\n\n**Start command:** `uvicorn backend.main:app --reload`'
      }])
    } finally {
      setChatLoading(false)
    }
  }

  function handleKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  const riskColor = level => ({
    Low: 'var(--clr-severity-low)',
    Medium: 'var(--clr-severity-medium)',
    High: 'var(--clr-severity-high)',
    Critical: 'var(--clr-severity-critical)',
  }[level] || 'var(--clr-text-muted)')

  const obs = advisory?.weather_observation

  return (
    <div className="fade-in">
      <div className="grid-2">
        {/* LEFT: Weather Advisory */}
        <div>
          {/* Weather Selector & Location Input */}
          <div className="card mb-24">
            <div className="card-header">
              <div className="card-header-icon" style={{ background: 'rgba(245,158,11,0.15)' }}>🌤️</div>
              <div className="card-header-text">
                <h3>Site Weather Condition & Location</h3>
                <p>Retrieve live atmospheric readings via Open-Meteo or select standard safety protocols</p>
              </div>
            </div>

            {/* City/Location Search Bar */}
            <form onSubmit={handleLocationSubmit} className="mb-20">
              <label className="form-label" htmlFor="location-input">
                Site Location (Live Open-Meteo Observations)
              </label>
              <div style={{ display: 'flex', gap: '8px', alignItems: 'stretch' }}>
                <div style={{ position: 'relative', flex: 1 }}>
                  <input
                    id="location-input"
                    type="text"
                    className="form-control"
                    placeholder="Enter city or location (e.g. Indore)"
                    value={locationInput}
                    onChange={e => {
                      setLocationInput(e.target.value)
                      if (locationError) setLocationError(null)
                    }}
                    disabled={advisoryLoading}
                  />
                </div>
                <button
                  id="get-weather-advisory-btn"
                  type="submit"
                  className="btn btn-primary"
                  disabled={advisoryLoading}
                  style={{ whiteSpace: 'nowrap' }}
                >
                  {advisoryLoading ? '⏳ Fetching...' : 'Get Weather Advisory'}
                </button>
                {activeLocation && (
                  <button
                    type="button"
                    className="btn btn-secondary"
                    onClick={handleClearLocation}
                    disabled={advisoryLoading}
                    title="Clear location"
                  >
                    ✕ Reset
                  </button>
                )}
              </div>
            </form>

            {/* Error Message */}
            {locationError && (
              <div className="alert-card critical mb-16">
                <span className="alert-card-icon">⚠️</span>
                <div className="alert-card-body">
                  <div className="alert-card-title">Location Weather Alert</div>
                  <div className="alert-card-text">{locationError}</div>
                </div>
              </div>
            )}

            {/* Preset Weather Condition Cards */}
            <div style={{ fontSize: '11px', color: 'var(--clr-text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '8px', fontWeight: 600 }}>
              Safety Protocol Scenario
            </div>
            <div className="weather-selector">
              {WEATHER_CONDITIONS.map(w => (
                <button
                  key={w.id}
                  id={`weather-btn-${w.id.replace(' ', '-').toLowerCase()}`}
                  className={`weather-btn ${weather === w.id ? 'active' : ''}`}
                  onClick={() => handleConditionClick(w.id)}
                  disabled={advisoryLoading}
                  type="button"
                >
                  <span className="weather-icon">{w.icon}</span>
                  <span className="weather-label">{w.label}</span>
                  <span style={{ fontSize: '10px', color: 'var(--clr-text-muted)' }}>{w.desc}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Loading Indicator */}
          {advisoryLoading && (
            <div className="card mb-24">
              <div className="loading-overlay" style={{ padding: '32px' }}>
                <div className="spinner" style={{ borderTopColor: 'var(--clr-accent-amber)' }} />
                <div className="loading-text">
                  {activeLocation ? `Fetching live weather observations for ${activeLocation}...` : 'Loading safety advisory...'}
                </div>
              </div>
            </div>
          )}

          {/* Live Weather Observation Display */}
          {obs && !advisoryLoading && (
            <div className="weather-obs-card fade-in">
              <div className="weather-obs-header">
                <div>
                  <div className="weather-obs-title">
                    <span>📍</span>
                    <span>{obs.location_name}</span>
                  </div>
                  <div className="weather-obs-time">
                    Coordinates: {obs.latitude}° N, {obs.longitude}° E
                    {obs.observation_time && ` · Observed: ${obs.observation_time}`}
                  </div>
                </div>
                <div>
                  {advisory?.is_demo_advice ? (
                    <span className="weather-badge-demo" title="Live observations active; safety advice in Demo Mode">
                      ⚡ Live Weather · Demo Advice
                    </span>
                  ) : (
                    <span className="weather-badge-live" title="Live observations and Gemini AI active">
                      ✨ Live Weather + Live AI
                    </span>
                  )}
                </div>
              </div>

              {/* Demo Mode Notice */}
              {advisory?.is_demo_advice && (
                <div style={{
                  fontSize: '11px',
                  color: 'var(--clr-text-secondary)',
                  background: 'rgba(245, 158, 11, 0.08)',
                  border: '1px solid rgba(245, 158, 11, 0.2)',
                  borderRadius: '6px',
                  padding: '6px 10px',
                  marginBottom: '12px',
                  lineHeight: '1.4'
                }}>
                  ℹ️ <strong>Live Atmospheric Readings:</strong> Data retrieved from Open-Meteo. Safety recommendations below are demo-generated per OSHA 29 CFR 1926 / IS 456:2000 standards.
                </div>
              )}

              {/* Weather Metrics Grid */}
              <div className="weather-obs-grid">
                <div className="weather-obs-item">
                  <div className="weather-obs-item-label">Temperature</div>
                  <div className="weather-obs-item-val" style={{ color: 'var(--clr-accent-amber)' }}>
                    {obs.temperature_c != null ? `${obs.temperature_c}°C` : '--'}
                  </div>
                </div>
                <div className="weather-obs-item">
                  <div className="weather-obs-item-label">Feels Like</div>
                  <div className="weather-obs-item-val" style={{ color: 'var(--clr-accent-orange)' }}>
                    {obs.apparent_temperature_c != null ? `${obs.apparent_temperature_c}°C` : '--'}
                  </div>
                </div>
                <div className="weather-obs-item">
                  <div className="weather-obs-item-label">Wind Speed</div>
                  <div className="weather-obs-item-val" style={{ color: 'var(--clr-accent-cyan)' }}>
                    {obs.wind_speed_kmh != null ? `${obs.wind_speed_kmh} km/h` : '--'}
                  </div>
                </div>
                <div className="weather-obs-item">
                  <div className="weather-obs-item-label">Precipitation</div>
                  <div className="weather-obs-item-val" style={{ color: 'var(--clr-primary)' }}>
                    {obs.precipitation_mm != null ? `${obs.precipitation_mm} mm` : '0 mm'}
                  </div>
                </div>
                {obs.relative_humidity_pct != null && (
                  <div className="weather-obs-item">
                    <div className="weather-obs-item-label">Humidity</div>
                    <div className="weather-obs-item-val" style={{ color: 'var(--clr-accent-emerald)' }}>
                      {obs.relative_humidity_pct}%
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Advisory Content */}
          {advisory && !advisoryLoading && (
            <div className="fade-in">
              {/* Risk Level Banner */}
              <div className="card mb-16" style={{
                background: `linear-gradient(135deg, ${riskColor(advisory.overall_risk_level)}15, transparent)`,
                borderColor: `${riskColor(advisory.overall_risk_level)}40`,
              }}>
                <div className="flex items-center justify-between">
                  <div>
                    <div style={{ fontSize: '12px', color: 'var(--clr-text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em' }}>
                      Overall Risk Level
                    </div>
                    <div style={{ fontSize: '24px', fontWeight: 800, color: riskColor(advisory.overall_risk_level), marginTop: '4px' }}>
                      {advisory.overall_risk_level}
                    </div>
                  </div>
                  <div style={{ fontSize: '40px' }}>
                    {WEATHER_CONDITIONS.find(w => w.id === weather)?.icon}
                  </div>
                </div>
              </div>

              {/* Safety Alerts */}
              <div className="card mb-16">
                <div className="card-header" style={{ marginBottom: '12px', paddingBottom: '12px' }}>
                  <div className="card-header-text">
                    <h3>🚨 Safety Alerts</h3>
                  </div>
                </div>
                {advisory.safety_alerts.map((alert, i) => (
                  <div key={i} className={`alert-card ${alert.severity.toLowerCase()}`}>
                    <span className="alert-card-icon">
                      {alert.severity === 'Critical' ? '🔴' : alert.severity === 'High' ? '🟠' : '🟡'}
                    </span>
                    <div className="alert-card-body">
                      <div className="flex items-center gap-8" style={{ marginBottom: '6px' }}>
                        <div className="alert-card-title">{alert.alert_type}</div>
                        <span className={`severity-badge ${alert.severity.toLowerCase()}`}>{alert.severity}</span>
                      </div>
                      <div className="alert-card-text">{alert.protocol}</div>
                      {alert.suspended_operations && alert.suspended_operations.length > 0 && (
                        <div className="alert-card-suspended">
                          <div style={{ fontSize: '11px', color: 'var(--clr-text-muted)', marginBottom: '4px' }}>
                            🚫 Suspended Operations:
                          </div>
                          <div className="suspended-ops">
                            {alert.suspended_operations.map((op, j) => (
                              <span key={j} className="suspended-tag">{op}</span>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>

              {/* Daily Checklist */}
              <div className="card mb-16">
                <div className="card-header" style={{ marginBottom: '12px', paddingBottom: '12px' }}>
                  <div className="card-header-text"><h3>📋 Daily Safety Checklist</h3></div>
                </div>
                <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                  {advisory.daily_checklist.map((item, i) => (
                    <li key={i} style={{
                      fontSize: '13px',
                      color: 'var(--clr-text-secondary)',
                      padding: '8px 12px',
                      background: 'var(--clr-bg-surface)',
                      borderRadius: '8px',
                      border: '1px solid var(--clr-border)',
                      lineHeight: '1.4'
                    }}>
                      {item}
                    </li>
                  ))}
                </ul>
              </div>

              {/* Emergency Contacts */}
              <div className="card">
                <div className="card-header" style={{ marginBottom: '12px', paddingBottom: '12px' }}>
                  <div className="card-header-text"><h3>📞 Emergency Contacts</h3></div>
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                  {Object.entries(advisory.emergency_contacts).map(([name, number]) => (
                    <div key={name} style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      padding: '8px 12px',
                      background: 'var(--clr-bg-surface)',
                      borderRadius: '8px',
                      border: '1px solid var(--clr-border)'
                    }}>
                      <span style={{ fontSize: '13px', color: 'var(--clr-text-secondary)' }}>{name}</span>
                      <span style={{
                        fontFamily: 'var(--font-mono)', fontSize: '13px',
                        color: 'var(--clr-accent-emerald)', fontWeight: 600
                      }}>{number}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>

        {/* RIGHT: Chatbot */}
        <div>
          <div className="card" style={{ padding: '0', overflow: 'hidden' }}>
            <div style={{ padding: '18px 20px', borderBottom: '1px solid var(--clr-border)', background: 'rgba(59,130,246,0.05)' }}>
              <div className="flex items-center gap-12">
                <div style={{
                  width: '38px', height: '38px', borderRadius: '50%',
                  background: 'linear-gradient(135deg, var(--clr-accent-violet), var(--clr-primary))',
                  display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '18px'
                }}>🤖</div>
                <div>
                  <div style={{ fontWeight: 600, fontSize: '14px', color: 'var(--clr-text-primary)' }}>
                    Construction AI Assistant
                  </div>
                  <div style={{ fontSize: '11px', color: 'var(--clr-accent-emerald)' }}>
                    ● Online · Powered by Gemini 1.5 Flash
                  </div>
                </div>
              </div>
            </div>

            <div className="chat-messages" style={{ height: '400px' }} id="chat-messages">
              {messages.map((msg, i) => (
                <div key={i}>
                  <div className={`chat-message ${msg.role}`}>
                    <div className="chat-avatar">
                      {msg.role === 'user' ? '👤' : '🤖'}
                    </div>
                    <div
                      className="chat-bubble"
                      dangerouslySetInnerHTML={{ __html: formatMarkdown(msg.content) }}
                    />
                  </div>
                  {msg.followups?.length > 0 && (
                    <div className="followup-chips" style={{ marginLeft: '44px' }}>
                      {msg.followups.map((fq, j) => (
                        <button
                          key={j}
                          className="followup-chip"
                          onClick={() => sendMessage(fq)}
                        >
                          {fq}
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              ))}

              {chatLoading && (
                <div className="chat-message assistant">
                  <div className="chat-avatar">🤖</div>
                  <div className="chat-bubble">
                    <div className="typing-indicator">
                      <div className="typing-dot" />
                      <div className="typing-dot" />
                      <div className="typing-dot" />
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>

            {/* Suggested questions */}
            <div style={{
              padding: '10px 16px',
              borderTop: '1px solid var(--clr-border)',
              background: 'var(--clr-bg-surface)',
              display: 'flex',
              gap: '6px',
              flexWrap: 'wrap'
            }}>
              {SUGGESTED_QUESTIONS.slice(0, 3).map((q, i) => (
                <button
                  key={i}
                  className="followup-chip"
                  onClick={() => sendMessage(q)}
                  disabled={chatLoading}
                >
                  {q}
                </button>
              ))}
            </div>

            <div className="chat-input-area">
              <div className="chat-input-row">
                <textarea
                  id="chat-input"
                  className="chat-input"
                  rows={2}
                  value={chatInput}
                  onChange={e => setChatInput(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Ask about PPE, safety protocols, cost estimation, IS codes..."
                  disabled={chatLoading}
                />
                <button
                  id="chat-send-btn"
                  className="chat-send-btn"
                  onClick={() => sendMessage()}
                  disabled={!chatInput.trim() || chatLoading}
                  title="Send message (Enter)"
                >
                  {chatLoading ? '⏳' : '➤'}
                </button>
              </div>
            </div>
          </div>

          {/* More suggestions */}
          <div className="card mt-16">
            <div style={{ fontSize: '11px', color: 'var(--clr-text-muted)', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '10px' }}>
              💡 More Questions to Try
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
              {SUGGESTED_QUESTIONS.slice(3).map((q, i) => (
                <button
                  key={i}
                  className="followup-chip"
                  style={{ textAlign: 'left', padding: '8px 12px', borderRadius: '8px' }}
                  onClick={() => sendMessage(q)}
                >
                  {q}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
