import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import axios from 'axios'
import MetricCard from '../ui/MetricCard'
import StatusPill from '../ui/StatusPill'
import { apiUrl } from '../../api'

function ScoreRing({ score }) {
  const radius = 54
  const circumference = 2 * Math.PI * radius
  const offset = circumference - (score / 100) * circumference

  const color = score >= 75 ? '#10b981' : score >= 50 ? '#f59e0b' : '#f43f5e'

  return (
    <div className="score-ring">
      <svg width="140" height="140" viewBox="0 0 140 140">
        <circle cx="70" cy="70" r={radius} fill="none" stroke="rgba(255,255,255,0.06)" strokeWidth="12" />
        <circle
          cx="70" cy="70" r={radius}
          fill="none"
          stroke={color}
          strokeWidth="12"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          style={{ filter: `drop-shadow(0 0 8px ${color})`, transition: 'stroke-dashoffset 1s ease' }}
        />
      </svg>
      <div className="score-ring-text">
        <span className="score-number" style={{ color }}>{score}</span>
        <span className="score-label">/ 100</span>
      </div>
    </div>
  )
}

export default function PPESafety() {
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
      const res = await axios.post(apiUrl('/api/ppe-safety/analyze'), form, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      setResult(res.data)
    } catch {
      // Fallback to demo endpoint
      try {
        const res = await axios.get(apiUrl('/api/ppe-safety/demo'))
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
      const res = await axios.get('/api/ppe-safety/demo')
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
    a.download = `ppe_safety_report_${Date.now()}.json`
    a.click()
    URL.revokeObjectURL(url)
  }


  return (
    <div className="fade-in">
      {/* Upload Section */}
      <div className="card mb-24">
        <div className="card-header">
          <div className="card-header-icon" style={{ background: 'rgba(59,130,246,0.15)' }}>🦺</div>
          <div className="card-header-text">
            <h3>Upload Construction Site Photo</h3>
            <p>JPG / PNG / WebP · Max 10MB · OSHA 29 CFR 1926 + IS 456:2000 analysis</p>
          </div>
        </div>

        <div {...getRootProps()} className={`dropzone ${isDragActive ? 'active' : ''}`}>
          <input {...getInputProps()} id="ppe-file-input" />
          {preview ? (
            <div className="image-preview-container">
              <img src={preview} alt="Site preview" />
            </div>
          ) : (
            <>
              <span className="dropzone-icon">📷</span>
              <h3>{isDragActive ? 'Drop it here!' : 'Drag & drop site photo'}</h3>
              <p>or click to browse files</p>
              <div className="format-tags">
                {['JPG', 'PNG', 'WebP'].map(f => <span key={f} className="format-tag">{f}</span>)}
              </div>
            </>
          )}
        </div>

        <div className="flex gap-8 mt-16">
          <button
            id="ppe-analyze-btn"
            className="btn btn-primary"
            onClick={analyze}
            disabled={!file || loading}
          >
            {loading ? '⏳ Analyzing...' : '🔬 Analyze PPE Compliance'}
          </button>
          <button
            id="ppe-demo-btn"
            className="btn btn-secondary"
            onClick={loadDemo}
            disabled={loading}
          >
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
              <div className="alert-card-title">Analysis Error</div>
              <div className="alert-card-text">{error}</div>
            </div>
          </div>
        )}
      </div>

      {/* Loading */}
      {loading && (
        <div className="card">
          <div className="loading-overlay">
            <div className="spinner" />
            <div className="loading-text">Analyzing with Gemini Vision AI...</div>
            <div className="text-muted" style={{ fontSize: '12px' }}>Checking PPE compliance against OSHA and IS 456:2000 standards</div>
          </div>
        </div>
      )}

      {/* Results */}
      {result && !loading && (
        <div className="fade-in">
          {/* Score + Status */}
          <div className="grid-2 mb-24">
            <div className="card flex-center" style={{ flexDirection: 'column', gap: '12px' }}>
              <ScoreRing score={result.safety_score} />
              <StatusPill status={result.overall_status} />
              <div style={{ fontSize: '12px', color: 'var(--clr-text-muted)', textAlign: 'center' }}>
                {result.standard_reference}
              </div>
            </div>
            <div className="card">
              <div className="card-header" style={{ marginBottom: '12px', paddingBottom: '12px' }}>
                <div className="card-header-text">
                  <h3>Summary</h3>
                </div>
              </div>
              <p style={{ fontSize: '13px', color: 'var(--clr-text-secondary)', lineHeight: '1.6', marginBottom: '12px' }}>
                {result.summary}
              </p>
              <div className="info-box">
                <span className="info-box-icon">💡</span>
                <span>{result.recommendation}</span>
              </div>
            </div>
          </div>

          {/* Metric Cards */}
          <div className="metrics-grid mb-24">
            <MetricCard icon="🛡️" label="Safety Score" value={result.safety_score} sub="out of 100" accentColor="var(--clr-primary)" />
            <MetricCard
              icon="✅"
              label="PPE Compliant"
              value={result.ppe_detection_checklist.filter(p => p.compliant).length}
              sub={`of ${result.ppe_detection_checklist.length} items`}
              accentColor="var(--clr-accent-emerald)"
            />
            <MetricCard
              icon="⚠️"
              label="Hazards Found"
              value={result.site_hazards.length}
              sub="requiring action"
              accentColor="var(--clr-accent-amber)"
            />
            <MetricCard
              icon="🚨"
              label="Critical Hazards"
              value={result.site_hazards.filter(h => h.severity === 'Critical').length}
              sub="immediate action"
              accentColor="var(--clr-accent-rose)"
            />
          </div>

          {/* PPE Checklist */}
          <div className="card mb-24">
            <div className="card-header">
              <div className="card-header-icon" style={{ background: 'rgba(16,185,129,0.15)' }}>📋</div>
              <div className="card-header-text">
                <h3>PPE Detection Checklist</h3>
                <p>Worker personal protective equipment compliance status</p>
              </div>
            </div>
            <ul className="checklist">
              {result.ppe_detection_checklist.map((item, i) => (
                <li key={i} className={`checklist-item ${item.compliant ? 'pass' : 'fail'}`}>
                  <span className="check-icon">{item.detected ? (item.compliant ? '✅' : '⚠️') : '❌'}</span>
                  <div className="check-item-text">
                    <div className="check-item-name">{item.item}</div>
                    {item.notes && <div className="check-item-notes">{item.notes}</div>}
                  </div>
                  <span className={`severity-badge ${item.compliant ? 'low' : 'high'}`}>
                    {item.compliant ? 'Compliant' : item.detected ? 'Non-Compliant' : 'Not Detected'}
                  </span>
                </li>
              ))}
            </ul>
          </div>

          {/* Hazards Table */}
          <div className="card mb-16">
            <div className="card-header">
              <div className="card-header-icon" style={{ background: 'rgba(244,63,94,0.15)' }}>🚨</div>
              <div className="card-header-text">
                <h3>Site Hazards & Corrective Remedies</h3>
                <p>Identified safety violations with recommended actions</p>
              </div>
            </div>
            {result.site_hazards.map((h, i) => (
              <div key={i} className={`alert-card ${h.severity.toLowerCase()} mb-16`} style={{ marginBottom: '10px' }}>
                <span className="alert-card-icon">
                  {h.severity === 'Critical' ? '🔴' : h.severity === 'High' ? '🟠' : h.severity === 'Medium' ? '🟡' : '🟢'}
                </span>
                <div className="alert-card-body">
                  <div className="flex items-center gap-8" style={{ marginBottom: '4px' }}>
                    <div className="alert-card-title">{h.hazard}</div>
                    <span className={`severity-badge ${h.severity.toLowerCase()}`}>{h.severity}</span>
                  </div>
                  <div className="alert-card-text">
                    <strong style={{ color: 'var(--clr-accent-cyan)' }}>Remedy: </strong>{h.corrective_remedy}
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Download */}
          <div className="download-section">
            <button id="ppe-download-btn" className="btn btn-secondary" onClick={downloadReport}>
              ⬇️ Download JSON Report
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
