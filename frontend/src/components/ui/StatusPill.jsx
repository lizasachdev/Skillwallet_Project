export default function StatusPill({ status }) {
  const statusMap = {
    'Compliant': { cls: 'compliant', icon: '✅' },
    'Non-Compliant': { cls: 'non-compliant', icon: '❌' },
    'Partial Compliance': { cls: 'partial', icon: '⚠️' },
    'Safe': { cls: 'safe', icon: '✅' },
    'Unsafe': { cls: 'unsafe', icon: '🚨' },
    'Warning': { cls: 'warning', icon: '⚠️' },
    'Low': { cls: 'compliant', icon: '🟢' },
    'Medium': { cls: 'partial', icon: '🟡' },
    'High': { cls: 'warning', icon: '🟠' },
    'Critical': { cls: 'non-compliant', icon: '🔴' },
  }

  const { cls, icon } = statusMap[status] || { cls: 'partial', icon: '•' }

  return (
    <span className={`status-pill ${cls}`}>
      {icon} {status}
    </span>
  )
}
