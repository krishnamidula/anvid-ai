export default function OpportunityCard({ item }) {
  return (
    <div className="rounded-lg border border-border border-l-secondary bg-card p-5 transition-transform hover:translate-x-1" style={{ borderLeftWidth: 3 }}>
      <h3 className="font-semibold text-secondary">{item.title}</h3>
      <p className="mt-2 text-sm leading-relaxed text-muted">{item.description}</p>
      <div className="mt-4 flex flex-wrap gap-2">
        <span className="rounded-full border border-secondary/30 bg-secondary/10 px-3 py-1 text-xs font-medium text-secondary">{item.format}</span>
        <span className="rounded-full border border-warm/30 bg-warm/10 px-3 py-1 text-xs font-medium text-warm">{item.potential}</span>
      </div>
    </div>
  )
}
