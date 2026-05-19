import { CartesianGrid, Scatter, ScatterChart, ResponsiveContainer, Tooltip, XAxis, YAxis, ZAxis } from 'recharts'
import StyledTable from '../ui/StyledTable'
import { COLORS, formatNumber, tooltipStyle } from '../ui/helpers'

export default function EngagementAnalysis({ data }) {
  const scatterData = data.companies.map((company) => ({
    name: company.name,
    avg_views: company.avg_views,
    engagement: company.avg_engagement_rate,
    subscribers: company.subscribers
  }))
  const rows = data.companies.map((company) => ({
    company: company.name,
    avg_views: formatNumber(company.avg_views),
    avg_likes: formatNumber(company.avg_likes),
    avg_comments: formatNumber(company.avg_comments),
    engagement: `${company.avg_engagement_rate}%`
  }))
  return (
    <div className="space-y-6">
      <div className="rounded-lg border border-border bg-card p-5">
        <ResponsiveContainer width="100%" height={420}>
          <ScatterChart>
            <CartesianGrid stroke="#2D3250" />
            <XAxis type="number" dataKey="avg_views" name="Avg Views" tick={{ fill: '#A0A0B0' }} tickFormatter={formatNumber} />
            <YAxis type="number" dataKey="engagement" name="Engagement" tick={{ fill: '#A0A0B0' }} />
            <ZAxis type="number" dataKey="subscribers" range={[120, 850]} />
            <Tooltip contentStyle={tooltipStyle} cursor={{ strokeDasharray: '3 3' }} formatter={(value, name) => name === 'Avg Views' ? formatNumber(value) : value} />
            {scatterData.map((company, index) => <Scatter key={company.name} name={company.name} data={[company]} fill={COLORS[index % COLORS.length]} />)}
          </ScatterChart>
        </ResponsiveContainer>
        <div className="grid gap-2 text-xs text-muted md:grid-cols-4">
          <span>Hidden Gems: high engagement, lower scale</span>
          <span>Stars: high engagement and high scale</span>
          <span>Under-Leveraged: low scale and low engagement</span>
          <span>Scale Without Depth: reach that can be converted</span>
        </div>
      </div>
      <StyledTable columns={[
        { key: 'company', label: 'Company' },
        { key: 'avg_views', label: 'Avg Views' },
        { key: 'avg_likes', label: 'Avg Likes' },
        { key: 'avg_comments', label: 'Avg Comments' },
        { key: 'engagement', label: 'Engagement Rate' }
      ]} rows={rows} />
      <div>
        <h2 className="mb-4 text-xl font-bold text-white">Outlier Performers</h2>
        <div className="grid gap-4 md:grid-cols-2">
          {data.companies.flatMap((company) => company.outlier_videos.slice(0, 2).map((video) => (
            <div key={`${company.name}-${video.video_id}`} className="rounded-lg border border-border bg-card p-5">
              <div className="text-xs font-bold uppercase tracking-widest text-primary">{company.name}</div>
              <div className="mt-2 font-semibold text-white">{video.title}</div>
              <div className="mt-3 flex gap-3 text-sm text-muted"><span>{formatNumber(video.views)} views</span><span className="text-warm">Z-score {video.z_score}</span></div>
            </div>
          )))}
        </div>
      </div>
    </div>
  )
}
