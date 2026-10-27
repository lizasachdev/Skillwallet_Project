import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import axios from 'axios'
import MetricCard from '../ui/MetricCard'
import StatusPill from '../ui/StatusPill'
import { apiUrl } from '../../api'

const CRACK_TYPE_CONFIG = {
  'Hairline': { icon: '〰️', color: 'var(--clr-severity-low)', desc: 'Very fine cracks < 0.1mm width' },
  'Settlement': { icon: '⬇️', color: 'var(--clr-severity-medium)', desc: 'Caused by differential foundation settlement' },
  'Structural Shear': { icon: '⚡', color: 'var(--clr-severity-critical)', desc: 'Diagonal crack from shear stress — critical' },
  'Thermal Expansion': { icon: '🌡️', color: 'var(--clr-severity-medium)', desc: 'Temperature-induced expansion/contraction' },
  'Spalling': { icon: '💥', color: 'var(--clr-severity-high)', desc: 'Concrete surface flaking with rebar exposure' },
  'Unknown': { icon: '❓', color: 'var(--clr-text-muted)', desc: 'Requires further investigation' },
}

function RiskGauge({ score }) {
  const color = score < 35 ? '#10b981' : score < 60 ? '#f59e0b' : score < 80 ? '#f97316' : '#f43f5e'

  return (
    <div style={{ textAlign: 'center', padding: '24px 16px' }}>
      <div style={{ position: 'relative', width: '160px', height: '90px', margin: '0 auto' }}>
        <svg viewBox="0 0 160 90" width="160" height="90">
          {/* Track arc */}
          <path d="M 10 80 A 70 70 0 0 1 150 80" fill="none" stroke="rgba(255,255,255,0.08)" strokeWidth="12" strokeLinecap="round" />
          {/* Filled arc */}
          <path
            d="M 10 80 A 70 70 0 0 1 150 80"
            fill="none"
            stroke={color}
            strokeWidth="12"
            strokeLinecap="round"
            strokeDasharray="220"
            strokeDashoffset={220 - (score / 100) * 220}
            style={{ filter: `drop-shadow(0 0 6px ${color})`, transition: 'all 1s ease' }}
          />
          {/* Zone labels */}
          <text x="8" y="88" fontSize="8" fill="#10b981" fontFamily="Inter">Safe</text>
          <text x="68" y="18" fontSize="8" fill="#f59e0b" fontFamily="Inter" textAnchor="middle">Moderate</text>
          <text x="138" y="88" fontSize="8" fill="#f43f5e" fontFamily="Inter" textAnchor="end">Critical</text>
        </svg>
      </div>
      <div style={{ fontSize: '36px', fontWeight: 800, color, lineHeight: 1, marginTop: '8px' }}>{score}</div>
      <div style={{ fontSize: '12px', color: 'var(--clr-text-muted)' }}>Structural Risk Score</div>
    </div>
  )
}

export default function CrackDiagnostics() {
  const [file, setFile] = useState(null)
  const [preview, setPreview] = useState(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const onDrop = useCallback(accepted => {
    const f = accepted[0]
    if (!f) return
    setFile(f)
    setPreview(URL.createObjectURL(f))
    setResult(null)
    setError(null)
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'image/*': ['.jpg', '.jpeg', '.png', '.webp'] },
    maxFiles: 1,
  })

  async function analyze() {
    if (!file) return
    setLoading(true)
    setError(null)
    try {
      const form = new FormData()
      form.append('file', file)
      const res = await axios.post(apiUrl('/api/crack-analysis/analyze'), form, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      setResult(res.data)
    } catch {
      try {
        const res = await axios.get(apiUrl('/api/crack-analysis/demo'))
        setResult(res.data)
      } catch {
        setError('Failed to analyze image. Please check backend connection.')
      }
    } finally {
      setLoading(false)
    }
  }

  async function loadDemo() {
    setLoading(true)
    setError(null)
    try {
      const res = await axios.get(apiUrl('/api/crack-analysis/demo'))
      setResult(res.data)
    } catch {
      setError('Backend not running. Please start the FastAPI server.')
    } finally {
      setLoading(false)
    }
  }

  function downloadReport() {
    if (!result) return
    const blob = new Blob([JSON.stringify(result, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `crack_diagnostics_${Date.now()}.json`
    a.click()
    URL.revokeObjectURL(url)
  }

  const crackConfig = result ? (CRACK_TYPE_CONFIG[result.crack_type] || CRACK_TYPE_CONFIG['Unknown']) : null

  return (
    <div className="fade-in">
      {/* Upload */}
      <div className="card mb-24">
        <div className="card-header">
          <div className="card-header-icon" style={{ background: 'rgba(139,92,246,0.15)' }}>🔍</div>
          <div className="card-header-text">
            <h3>Upload Concrete / Wall Surface Photo</h3>
            <p>AI classifies crack type, estimates width, and recommends repairs per IS 456:2000</p>
          </div>
        </div>

        <div {...getRootProps()} className={`dropzone ${isDragActive ? 'active' : ''}`}
          style={{ borderColor: 'rgba(139,92,246,0.35)', background: 'rgba(139,92,246,0.03)' }}>
          <input {...getInputProps()} id="crack-file-input" />
          {preview ? (
            <div className="image-preview-container">
              <img src={preview} alt="Crack surface preview" />
            </div>
          ) : (
            <>
              <span className="dropzone-icon">🧱</span>
              <h3>{isDragActive ? 'Drop it here!' : 'Drag & drop concrete/wall photo'}</h3>
              <p>or click to browse files</p>
              <div className="format-tags">
                {['JPG', 'PNG', 'WebP'].map(f => <span key={f} className="format-tag">{f}</span>)}
              </div>
            </>
          )}
        </div>

        <div className="flex gap-8 mt-16">
          <button
            id="crack-analyze-btn"
            className="btn btn-primary"
            onClick={analyze}
            disabled={!file || loading}
            style={{ background: 'linear-gradient(135deg, var(--clr-accent-violet), #6d28d9)' }}
          >
            {loading ? '⏳ Analyzing...' : '🔬 Analyze Crack Structure'}
          </button>
          <button id="crack-demo-btn" className="btn btn-secondary" onClick={loadDemo} disabled={loading}>
            ⚡ Load Demo Analysis
          </button>
          {file && (
            <button className="btn btn-danger" onClick={() => { setFile(null); setPreview(null); setResult(null) }}>
              🗑 Clear
            </button>
          )}
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
      </div>

      {loading && (
        <div className="card">
          <div className="loading-overlay">
            <div className="spinner" style={{ borderTopColor: 'var(--clr-accent-violet)' }} />
            <div className="loading-text">Running structural crack analysis...</div>
            <div className="text-muted" style={{ fontSize: '12px' }}>Classifying defect type and calculating repair recommendations</div>
          </div>
        </div>
      )}

      {result && !loading && (
        <div className="fade-in">
          {/* Overview */}
          <div className="grid-2 mb-24">
            {/* Crack Type Card */}
            <div className="card" style={{
              borderColor: crackConfig.color.replace('var(--clr-severity-', 'rgba(').replace(')', ', 0.3)').replace('low', '16,185,129').replace('medium', '245,158,11').replace('high', '249,115,22').replace('critical', '244,63,94'),
              background: `linear-gradient(135deg, var(--clr-bg-card), rgba(0,0,0,0.2))`
            }}>
              <div style={{ textAlign: 'center', padding: '24px 16px' }}>
                <div style={{ fontSize: '48px', marginBottom: '12px' }}>{crackConfig.icon}</div>
                <div style={{ fontSize: '22px', fontWeight: 700, color: crackConfig.color, marginBottom: '4px' }}>
                  {result.crack_type}
                </div>
                <div style={{ fontSize: '12px', color: 'var(--clr-text-muted)', marginBottom: '16px' }}>
                  {crackConfig.desc}
                </div>
                <StatusPill status={result.severity} />
                <div style={{ marginTop: '12px', fontSize: '13px', color: 'var(--clr-text-secondary)' }}>
                  🕐 Urgency: <strong style={{ color: 'var(--clr-text-primary)' }}>{result.urgency}</strong>
                </div>
              </div>
            </div>

            {/* Risk Gauge */}
            <div className="card">
              <RiskGauge score={result.structural_risk_score} />
              <div className="info-box mt-12">
                <span className="info-box-icon">⚡</span>
                <span>{result.immediate_action}</span>
              </div>
            </div>
          </div>

          {/* Metric Cards */}
          <div className="metrics-grid mb-24">
            <MetricCard
              icon="📏"
              label="Crack Width"
              value={`${result.estimated_crack_width_mm}mm`}
              sub="estimated width"
              accentColor={crackConfig.color}
            />
            <MetricCard
              icon="⚠️"
              label="Severity"
              value={result.severity}
              sub="structural assessment"
              accentColor="var(--clr-accent-amber)"
            />
            <MetricCard
              icon="🔧"
              label="Repair Methods"
              value={result.repair_recommendations.length}
              sub="recommended"
              accentColor="var(--clr-accent-cyan)"
            />
            <MetricCard
              icon="🏗️"
              label="Risk Score"
              value={result.structural_risk_score}
              sub="out of 100"
              accentColor="var(--clr-accent-violet)"
            />
          </div>

          {/* Summary */}
          <div className="card mb-24">
            <div className="card-header">
              <div className="card-header-text"><h3>Engineering Assessment</h3></div>
            </div>
            <p style={{ fontSize: '13px', color: 'var(--clr-text-secondary)', lineHeight: '1.7' }}>
              {result.summary}
            </p>

            <div className="section-divider">
              <span className="section-divider-text">Root Causes</span>
            </div>
            <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {result.root_causes.map((c, i) => (
                <li key={i} style={{
                  display: 'flex', gap: '10px', fontSize: '13px',
                  color: 'var(--clr-text-secondary)', padding: '8px 12px',
                  background: 'var(--clr-bg-surface)', borderRadius: '8px',
                  border: '1px solid var(--clr-border)'
                }}>
                  <span style={{ color: 'var(--clr-accent-amber)', flexShrink: 0 }}>▸</span>
                  {c}
                </li>
              ))}
            </ul>
          </div>

          {/* Repair Recommendations */}
          <div className="card mb-16">
            <div className="card-header">
              <div className="card-header-icon" style={{ background: 'rgba(6,182,212,0.15)' }}>🔧</div>
              <div className="card-header-text">
                <h3>Repair Recommendations</h3>
                <p>Engineering repair methods with cost estimates</p>
              </div>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {result.repair_recommendations.map((r, i) => (
                <div key={i} style={{
                  background: 'var(--clr-bg-surface)',
                  border: '1px solid var(--clr-border)',
                  borderRadius: '10px',
                  padding: '16px',
                  borderLeft: '3px solid var(--clr-accent-cyan)'
                }}>
                  <div className="flex items-center justify-between mb-8">
                    <div style={{ fontWeight: 600, color: 'var(--clr-text-primary)', fontSize: '14px' }}>
                      🔧 {r.method}
                    </div>
                    <div style={{
                      fontSize: '12px', fontFamily: 'var(--font-mono)',
                      color: 'var(--clr-accent-emerald)',
                      background: 'rgba(16,185,129,0.1)',
                      padding: '2px 8px', borderRadius: '4px',
                      border: '1px solid rgba(16,185,129,0.2)'
                    }}>
                      {r.estimated_cost_inr}
                    </div>
                  </div>
                  <p style={{ fontSize: '13px', color: 'var(--clr-text-secondary)', lineHeight: '1.5' }}>
                    {r.description}
                  </p>
                </div>
              ))}
            </div>
          </div>

          <div className="download-section">
            <button id="crack-download-btn" className="btn btn-secondary" onClick={downloadReport}>
              ⬇️ Download Diagnostics Report
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
