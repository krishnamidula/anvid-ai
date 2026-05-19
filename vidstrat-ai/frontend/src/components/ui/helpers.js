export const COLORS = ['#6C63FF', '#43B89C', '#FF6584', '#FFB347', '#A78BFA']

export function formatNumber(value = 0) {
  const number = Number(value) || 0
  if (number >= 1000000) return `${(number / 1000000).toFixed(1)}M`
  if (number >= 1000) return `${(number / 1000).toFixed(1)}K`
  return Math.round(number).toLocaleString()
}

export function scoreColor(score = 0) {
  if (score >= 70) return 'score-high'
  if (score >= 40) return 'score-medium'
  return 'score-low'
}

export const tooltipStyle = {
  background: '#1E2130',
  border: '1px solid #2D3250',
  borderRadius: 8,
  color: '#FFFFFF'
}
