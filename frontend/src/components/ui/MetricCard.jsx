export default function MetricCard({ icon, label, value, sub, accentColor = 'var(--clr-primary)' }) {
  return (
    <div className="metric-card" style={{ '--accent-color': accentColor }}>
      <span className="metric-icon">{icon}</span>
      <div className="metric-label">{label}</div>
      <div className="metric-value">{value}</div>
      {sub && <div className="metric-sub">{sub}</div>}
    </div>
  )
}
