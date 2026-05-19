import VideoCard from '../ui/VideoCard'

export default function TopVideos({ data }) {
  return (
    <div className="space-y-8">
      <div className="grid gap-4 lg:grid-cols-3">
        {data.companies.flatMap((company) => company.top_videos.slice(0, 2).map((video) => <VideoCard key={`${company.name}-${video.title}`} company={company.name} video={video} />))}
      </div>
      <div>
        <h2 className="mb-4 text-xl font-bold text-white">Steal This Strategy</h2>
        <div className="grid gap-4 md:grid-cols-2">
          {data.companies.map((company) => (
            <div key={company.name} className="rounded-lg border border-border bg-card p-5">
              <div className="mb-4 text-sm font-bold uppercase tracking-widest text-primary">{company.name}</div>
              <div className="space-y-3">
                {company.steal_strategy.map((point) => (
                  <div key={point} className="flex gap-3 text-sm text-muted">
                    <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-primary" />
                    <span>{point}</span>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
