import { PolarAngleAxis, PolarGrid, PolarRadiusAxis, Radar, RadarChart, ResponsiveContainer, Tooltip } from 'recharts'
import MetricCard from '../ui/MetricCard'
import WinnerCard from '../ui/WinnerCard'
import { COLORS, tooltipStyle } from '../ui/helpers'

const dimensions = [
  ['consistency', 'Consistency'],
  ['engagement', 'Engagement'],
  ['audience_growth', 'Growth'],
  ['content_performance', 'Performance'],
  ['activity_level', 'Activity'],
  ['overall_strength', 'Strength']
]

export default function ExecutiveSummary({ data }) {
  const winner = data.companies.find((company) => company.name === data.winner)
  const radarData = dimensions.map(([key, label]) => {
    const row = { dimension: label }
    data.companies.forEach((company) => { row[company.name] = company.radar_scores[key] })
    return row
  })
  return (
    <div className="space-y-6">
      <WinnerCard winner={winner} />
      <div className="rounded-lg border border-border bg-card p-6 text-lg leading-relaxed text-muted">{data.executive_verdict}</div>
      <div className="grid gap-4 md:grid-cols-3">
        <MetricCard label="Overall Score" value={winner?.radar_scores.overall_strength || 0} />
        <MetricCard label="Companies Analysed" value={data.companies.length} delay={0.05} />
        <MetricCard label="Videos Analysed" value={data.total_videos_analysed} delay={0.1} />
      </div>
      <div className="rounded-lg border border-border bg-card p-5">
        <div className="mb-4 text-lg font-bold text-white">Competitive Radar</div>
        <ResponsiveContainer width="100%" height={400}>
          <RadarChart data={radarData}>
            <PolarGrid stroke="#2D3250" />
            <PolarAngleAxis dataKey="dimension" tick={{ fill: '#A0A0B0', fontSize: 12 }} />
            <PolarRadiusAxis angle={90} domain={[0, 100]} tick={{ fill: '#A0A0B0', fontSize: 10 }} />
            <Tooltip contentStyle={tooltipStyle} />
            {data.companies.map((company, index) => (
              <Radar key={company.name} name={company.name} dataKey={company.name} stroke={COLORS[index % COLORS.length]} fill={COLORS[index % COLORS.length]} fillOpacity={0.16} />
            ))}
          </RadarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
