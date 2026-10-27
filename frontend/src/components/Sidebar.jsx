export default function Sidebar({ tabs, activeTab, onTabChange, apiKey, onApiKeyChange, isDemo, backendStatus }) {
  return (
    <aside className="sidebar">
      {/* Brand */}
      <div className="sidebar-brand">
        <div className="brand-logo">
          <div className="brand-icon">🏗️</div>
          <div className="brand-text">
            <h1>Construction<br />Intelligence</h1>
            <p>Skill Wallet · Project 1</p>
          </div>
        </div>
        <div className="platform-id">ID: 6ac4c98d1dcde6d7857c1642</div>
        <span className={`mode-badge ${isDemo ? 'demo' : 'live'}`}>
          <span className="dot" />
          {isDemo ? '🔶 Demo Mode — No API Key' : '✅ Live — Gemini AI Connected'}
        </span>
      </div>

      {/* API Key */}
      <div className="api-key-section">
        <label htmlFor="api-key-input">🔑 Gemini API Key</label>
        <input
          id="api-key-input"
          type="password"
          className="api-key-input"
          placeholder="AIza..."
          value={apiKey}
          onChange={e => onApiKeyChange(e.target.value)}
          autoComplete="off"
        />
        <p className="api-key-hint">
          {isDemo
            ? '⚡ Running in demo mode with realistic mock data. Add your Gemini API key for live AI analysis.'
            : '✅ API key configured. Live multimodal AI analysis enabled.'}
        </p>
        {!apiKey && (
          <a
            href="https://aistudio.google.com/app/apikey"
            target="_blank"
            rel="noopener noreferrer"
            style={{ fontSize: '10px', color: 'var(--clr-accent-cyan)', display: 'block', marginTop: '4px' }}
          >
            → Get free API key at Google AI Studio
          </a>
        )}
      </div>

      {/* Navigation */}
      <nav className="sidebar-nav">
        <div className="nav-section-label">Modules</div>
        {tabs.map(tab => (
          <div
            key={tab.id}
            role="button"
            tabIndex={0}
            className={`nav-item ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => onTabChange(tab.id)}
            onKeyDown={e => e.key === 'Enter' && onTabChange(tab.id)}
            id={`nav-${tab.id}`}
            aria-label={tab.label}
          >
            <div className="nav-item-icon">{tab.icon}</div>
            <div className="nav-item-text">
              <span>{tab.label}</span>
              <small>{tab.subtitle}</small>
            </div>
            <span className="nav-epic-badge">{tab.epic}</span>
          </div>
        ))}
      </nav>

      {/* Architecture Overview */}
      <div className="api-key-section" style={{ borderTop: '1px solid var(--clr-border)', borderBottom: 'none' }}>
        <label>⚙️ Architecture</label>
        <div style={{ fontSize: '11px', color: 'var(--clr-text-muted)', lineHeight: '1.6' }}>
          <div>Frontend: React 18 + Vite</div>
          <div>Backend: FastAPI (Python 3.9+)</div>
          <div>AI: Google Gemini 1.5 Flash</div>
          <div>Status:
            <span style={{
              marginLeft: '4px',
              color: backendStatus === 'online' ? 'var(--clr-accent-emerald)' : 'var(--clr-accent-amber)',
              fontWeight: 600
            }}>
              {backendStatus === 'online' ? '● Online' : '● Offline'}
            </span>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="sidebar-footer">
        <div className="sidebar-footer-info">
          <div style={{ fontWeight: 600, color: 'var(--clr-text-secondary)', marginBottom: '6px' }}>
            Compliance Standards
          </div>
          <div className="standards-tags">
            {['OSHA 29 CFR 1926', 'IS 456:2000', 'IS 3696', 'IS 1786', 'IS 2925', 'RERA'].map(s => (
              <span key={s} className="std-tag">{s}</span>
            ))}
          </div>
          <div style={{ marginTop: '12px', color: 'var(--clr-text-muted)', fontSize: '10px' }}>
            © 2024 Skill Wallet · Multimodal Construction Intelligence Platform
          </div>
        </div>
      </div>
    </aside>
  )
}
