export default function WinnerCard({ winner }) {
  if (!winner) return null
  const reasons = [
    `Overall strength score of ${winner.radar_scores.overall_strength}`,
    `Engagement score of ${winner.radar_scores.engagement}`,
    `Content performance score of ${winner.radar_scores.content_performance}`
  ]
  return (
    <div className="rounded-lg border border-warm/50 bg-gradient-to-br from-card to-surface p-7 shadow-lg shadow-warm/10">
      <div className="text-xs font-bold uppercase tracking-widest text-warm">Intelligence Winner</div>
      <div className="mt-2 flex flex-wrap items-end justify-between gap-4">
        <h2 className="text-4xl font-black text-white">{winner.name}</h2>
        <span className="rounded-full border border-secondary/40 bg-secondary/10 px-4 py-1.5 text-sm font-bold text-secondary">
          {winner.radar_scores.overall_strength} overall
        </span>
      </div>
      <div className="mt-5 grid gap-3 md:grid-cols-3">
        {reasons.map((reason) => (
          <div key={reason} className="flex gap-2 text-sm text-muted">
            <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-secondary" />
            <span>{reason}</span>
          </div>
        ))}
      </div>
    </div>
  )
}
