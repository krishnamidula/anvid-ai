import { formatNumber } from './helpers'

export default function VideoCard({ company, video }) {
  return (
    <div className="card-hover rounded-lg border border-border bg-card overflow-hidden">
      <div className="p-5">
        <div className="text-xs font-bold uppercase tracking-widest text-primary">{company}</div>
        <h3 className="mt-3 line-clamp-2 min-h-[3rem] text-base font-semibold text-white">{video.title}</h3>
        <div className="mt-4 grid grid-cols-2 gap-3 text-sm">
          <div>
            <div className="text-lg font-bold text-white">{formatNumber(video.views)}</div>
            <div className="text-xs text-muted">Views</div>
          </div>
          <div>
            <div className="text-lg font-bold text-secondary">{Number(video.engagement_rate || 0).toFixed(2)}%</div>
            <div className="text-xs text-muted">Engagement</div>
          </div>
        </div>
        <div className="my-4 h-px bg-border" />
        <div className="text-sm italic text-secondary">{video.why_it_worked}</div>
      </div>
    </div>
  )
}
