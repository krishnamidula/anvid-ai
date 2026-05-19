export default function PersonaCard({ company }) {
  return (
    <div className="rounded-lg border border-border bg-card p-5">
      <div className="flex items-center justify-between gap-3">
        <h3 className="font-bold text-white">{company.name}</h3>
        <span className="rounded-full bg-primary/10 px-3 py-1 text-xs font-bold text-primary">{company.radar_scores.overall_strength}</span>
      </div>
      <p className="mt-4 text-sm italic leading-relaxed text-muted">{company.persona}</p>
    </div>
  )
}
