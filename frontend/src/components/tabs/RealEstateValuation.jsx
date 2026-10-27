import { useState } from 'react'
import axios from 'axios'
import MetricCard from '../ui/MetricCard'
import { apiUrl } from '../../api'

const STRUCTURE_TYPES = ['Residential', 'Commercial', 'Industrial', 'Mixed Use', 'Institutional']
const LOCATION_TIERS = ['Tier 1', 'Tier 2', 'Tier 3']

const TIER_EXAMPLES = {
  'Tier 1': 'Mumbai, Delhi, Bengaluru, Chennai, Hyderabad, Pune',
  'Tier 2': 'Ahmedabad, Jaipur, Kochi, Lucknow, Nagpur, Surat',
  'Tier 3': 'Mysuru, Vadodara, Coimbatore, Jodhpur, Kanpur',
}

const STRUCTURE_ICONS = {
  Residential: '🏠', Commercial: '🏢', Industrial: '🏭', 'Mixed Use': '🏙️', Institutional: '🏛️'
}

export default function RealEstateValuation() {
  const [form, setForm] = useState({
    structure_type: 'Residential',
    built_up_sqft: 2000,
    location_tier: 'Tier 1',
    completion_percentage: 65,
    floors: 3,
    project_name: 'Skyline Residency',
  })
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [renderImg, setRenderImg] = useState(null)
  const [renderLoading, setRenderLoading] = useState(false)

  function handleChange(field, value) {
    setForm(prev => ({ ...prev, [field]: value }))
    setResult(null)
  }

  async function calculate() {
    setLoading(true)
    setError(null)
    try {
      const payload = {
        ...form,
        built_up_sqft: parseFloat(form.built_up_sqft),
        completion_percentage: parseFloat(form.completion_percentage),
        floors: parseInt(form.floors),
      }
      const res = await axios.post(apiUrl('/api/valuation/calculate'), payload)
      setResult(res.data)
      // Trigger architectural render
      loadArchRender(res.data.architectural_prompt)
    } catch (e) {
      setError(e.response?.data?.detail || 'Calculation failed. Please check backend connection.')
    } finally {
      setLoading(false)
    }
  }

  async function loadArchRender(prompt) {
    setRenderLoading(true)
    setRenderImg(null)
    try {
      const encoded = encodeURIComponent(prompt)
      const url = `https://image.pollinations.ai/prompt/${encoded}?width=800&height=450&seed=42&nologo=true`
      setRenderImg(url)
    } catch {
      // silently fail for render
    } finally {
      setRenderLoading(false)
    }
  }

  function downloadReport() {
    if (!result) return
    const report = { ...result, inputs: form, generated_at: new Date().toISOString() }
    const blob = new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `valuation_${form.project_name || 'report'}_${Date.now()}.json`
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="fade-in">
      {/* Input Form */}
      <div className="card mb-24">
        <div className="card-header">
          <div className="card-header-icon" style={{ background: 'rgba(16,185,129,0.15)' }}>🏗️</div>
          <div className="card-header-text">
            <h3>Project Parameters</h3>
            <p>Enter construction details for budget estimation, valuation, and material planning</p>
          </div>
        </div>

        <div className="form-row mb-16">
          <div className="form-group">
            <label className="form-label" htmlFor="project-name">Project Name</label>
            <input
              id="project-name"
              className="form-control"
              type="text"
              value={form.project_name}
              onChange={e => handleChange('project_name', e.target.value)}
              placeholder="e.g. Skyline Residency"
            />
          </div>
          <div className="form-group">
            <label className="form-label" htmlFor="structure-type">Structure Type</label>
            <select
              id="structure-type"
              className="form-control"
              value={form.structure_type}
              onChange={e => handleChange('structure_type', e.target.value)}
            >
              {STRUCTURE_TYPES.map(t => (
                <option key={t} value={t}>{STRUCTURE_ICONS[t]} {t}</option>
              ))}
            </select>
          </div>
        </div>

        <div className="form-row mb-16">
          <div className="form-group">
            <label className="form-label" htmlFor="builtup-sqft">Built-up Area (sqft)</label>
            <input
              id="builtup-sqft"
              className="form-control"
              type="number"
              min="100"
              max="1000000"
              value={form.built_up_sqft}
              onChange={e => handleChange('built_up_sqft', e.target.value)}
            />
          </div>
          <div className="form-group">
            <label className="form-label" htmlFor="floors">Number of Floors</label>
            <input
              id="floors"
              className="form-control"
              type="number"
              min="1"
              max="100"
              value={form.floors}
              onChange={e => handleChange('floors', e.target.value)}
            />
          </div>
        </div>

        <div className="form-group mb-16">
          <label className="form-label" htmlFor="location-tier">Location Tier</label>
          <select
            id="location-tier"
            className="form-control"
            value={form.location_tier}
            onChange={e => handleChange('location_tier', e.target.value)}
          >
            {LOCATION_TIERS.map(t => (
              <option key={t} value={t}>{t} — {TIER_EXAMPLES[t]}</option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label className="form-label">
            Completion Percentage
            <span className="slider-value" style={{ float: 'right', fontSize: '16px' }}>{form.completion_percentage}%</span>
          </label>
          <input
            id="completion-slider"
            className="slider-control"
            type="range"
            min="0"
            max="100"
            value={form.completion_percentage}
            onChange={e => handleChange('completion_percentage', parseFloat(e.target.value))}
            style={{
              background: `linear-gradient(to right, var(--clr-primary) 0%, var(--clr-primary) ${form.completion_percentage}%, rgba(255,255,255,0.1) ${form.completion_percentage}%, rgba(255,255,255,0.1) 100%)`
            }}
          />
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '10px', color: 'var(--clr-text-muted)', marginTop: '4px' }}>
            <span>0% — Planning</span>
            <span>50% — Superstructure</span>
            <span>100% — Handover</span>
          </div>
        </div>

        {error && (
          <div className="alert-card medium mt-16" style={{ marginBottom: 0 }}>
            <span className="alert-card-icon">⚠️</span>
            <div className="alert-card-body">
              <div className="alert-card-title">Error</div>
              <div className="alert-card-text">{error}</div>
            </div>
          </div>
        )}

        <button
          id="valuation-calculate-btn"
          className="btn btn-primary mt-16"
          onClick={calculate}
          disabled={loading}
          style={{ background: 'linear-gradient(135deg, var(--clr-accent-emerald), #047857)', boxShadow: '0 4px 15px rgba(16,185,129,0.3)' }}
        >
          {loading ? '⏳ Calculating...' : '💰 Calculate Valuation'}
        </button>
      </div>

      {/* Loading */}
      {loading && (
        <div className="card">
          <div className="loading-overlay">
            <div className="spinner" style={{ borderTopColor: 'var(--clr-accent-emerald)' }} />
            <div className="loading-text">Calculating construction budget and valuation...</div>
          </div>
        </div>
      )}

      {/* Results */}
      {result && !loading && (
        <div className="fade-in">
          {/* Financial Metric Cards */}
          <div className="metrics-grid mb-24">
            <MetricCard
              icon="💰"
              label="Total Project Budget"
              value={result.total_project_budget_inr}
              sub="construction cost"
              accentColor="var(--clr-accent-emerald)"
            />
            <MetricCard
              icon="📊"
              label="CapEx Incurred"
              value={result.capital_expenditure_incurred_inr}
              sub={`${form.completion_percentage}% complete`}
              accentColor="var(--clr-primary)"
            />
            <MetricCard
              icon="🏦"
              label="Market Valuation"
              value={result.current_market_asset_valuation_inr}
              sub="current asset value"
              accentColor="var(--clr-accent-amber)"
            />
            <MetricCard
              icon="📈"
              label="Est. ROI"
              value={`${result.roi_estimate_percent}%`}
              sub="return on investment"
              accentColor="var(--clr-accent-violet)"
            />
          </div>

          {/* Summary + Completion */}
          <div className="grid-2 mb-24">
            <div className="card">
              <div className="card-header" style={{ marginBottom: '12px', paddingBottom: '12px' }}>
                <div className="card-header-text"><h3>Project Summary</h3></div>
              </div>
              <p style={{ fontSize: '13px', color: 'var(--clr-text-secondary)', lineHeight: '1.7', marginBottom: '16px' }}>
                {result.summary}
              </p>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
                {[
                  ['Cost/sqft', `₹${result.cost_per_sqft_inr.toLocaleString('en-IN')}`],
                  ['Total Area', `${(parseFloat(form.built_up_sqft) * parseInt(form.floors)).toLocaleString()} sqft`],
                  ['Location', `${form.location_tier} City`],
                  ['Structure', form.structure_type],
                ].map(([label, val]) => (
                  <div key={label} style={{
                    background: 'var(--clr-bg-surface)', borderRadius: '8px',
                    padding: '10px 12px', border: '1px solid var(--clr-border)'
                  }}>
                    <div style={{ fontSize: '10px', color: 'var(--clr-text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em' }}>{label}</div>
                    <div style={{ fontSize: '14px', fontWeight: 600, color: 'var(--clr-text-primary)', marginTop: '2px' }}>{val}</div>
                  </div>
                ))}
              </div>
            </div>

            {/* Milestone Progress */}
            <div className="card">
              <div className="card-header" style={{ marginBottom: '12px', paddingBottom: '12px' }}>
                <div className="card-header-text"><h3>Milestone Progress</h3></div>
              </div>
              <ul className="milestone-list">
                {result.milestone_progress.map((m, i) => (
                  <li key={i} className="milestone-item">
                    <div className={`milestone-dot ${m.completed ? 'completed' : 'pending'}`}>
                      {m.completed ? '✓' : i + 1}
                    </div>
                    <div className="milestone-text">
                      <div className="milestone-name">{m.milestone}</div>
                      <div className="milestone-pct">{m.percentage}% mark</div>
                    </div>
                    {m.completed && (
                      <span className="severity-badge low">Done</span>
                    )}
                  </li>
                ))}
              </ul>
              <div className="progress-bar-container mt-16">
                <div className="progress-bar-label">
                  <span>Overall Completion</span>
                  <span style={{ color: 'var(--clr-primary)', fontWeight: 600 }}>{form.completion_percentage}%</span>
                </div>
                <div className="progress-bar-track">
                  <div className="progress-bar-fill" style={{ width: `${form.completion_percentage}%` }} />
                </div>
              </div>
            </div>
          </div>

          {/* Material Requirements */}
          <div className="card mb-24">
            <div className="card-header">
              <div className="card-header-icon" style={{ background: 'rgba(245,158,11,0.15)' }}>🧱</div>
              <div className="card-header-text">
                <h3>Material Requirements</h3>
                <p>IS 456:2000 based material estimation for {form.structure_type.toLowerCase()} structure</p>
              </div>
            </div>
            <table className="data-table">
              <thead>
                <tr>
                  <th>Material</th>
                  <th>Quantity</th>
                  <th>Unit</th>
                  <th>Estimated Cost (INR)</th>
                </tr>
              </thead>
              <tbody>
                {result.material_requirements.map((m, i) => (
                  <tr key={i}>
                    <td style={{ fontWeight: 500, color: 'var(--clr-text-primary)' }}>{m.material}</td>
                    <td style={{ fontFamily: 'var(--font-mono)', color: 'var(--clr-accent-cyan)' }}>{m.quantity}</td>
                    <td style={{ color: 'var(--clr-text-muted)' }}>{m.unit}</td>
                    <td style={{ fontFamily: 'var(--font-mono)', color: 'var(--clr-accent-emerald)' }}>{m.estimated_cost_inr}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Architectural Rendering */}
          <div className="card mb-16">
            <div className="card-header">
              <div className="card-header-icon" style={{ background: 'rgba(6,182,212,0.15)' }}>🎨</div>
              <div className="card-header-text">
                <h3>Conceptual 3D Architectural Rendering</h3>
                <p>AI-generated visualization via Pollinations AI — {form.structure_type} · {form.location_tier} City</p>
              </div>
            </div>
            <div className="render-preview">
              {renderLoading && (
                <div className="flex-center" style={{ height: '100%', minHeight: '250px' }}>
                  <div style={{ textAlign: 'center' }}>
                    <div className="spinner" style={{ margin: '0 auto 12px', borderTopColor: 'var(--clr-accent-cyan)' }} />
                    <div className="text-muted" style={{ fontSize: '13px' }}>Generating architectural render...</div>
                  </div>
                </div>
              )}
              {renderImg && (
                <>
                  <img
                    src={renderImg}
                    alt="Architectural rendering"
                    id="arch-render-img"
                    onError={e => { e.target.style.display = 'none' }}
                    style={{ objectFit: 'cover' }}
                  />
                  <div className="render-overlay-badge">
                    🤖 AI Generated · Pollinations AI · Conceptual Only
                  </div>
                </>
              )}
            </div>
          </div>

          <div className="download-section">
            <button id="valuation-download-btn" className="btn btn-secondary" onClick={downloadReport}>
              ⬇️ Download Valuation Report
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
