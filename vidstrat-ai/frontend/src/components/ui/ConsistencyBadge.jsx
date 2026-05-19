export default function ConsistencyBadge({ value }) {
  const tone = value === 'Very Consistent' || value === 'Consistent' ? 'text-secondary border-secondary/40 bg-secondary/10' : value === 'Irregular' ? 'text-warm border-warm/40 bg-warm/10' : 'text-accent border-accent/40 bg-accent/10'
  return <span className={`rounded-full border px-3 py-1 text-xs font-bold ${tone}`}>{value}</span>
}
