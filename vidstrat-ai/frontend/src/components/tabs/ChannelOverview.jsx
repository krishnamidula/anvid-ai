import { Bar, BarChart, CartesianGrid, Legend, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import StyledTable from '../ui/StyledTable'
import { COLORS, formatNumber, tooltipStyle } from '../ui/helpers'

export default function ChannelOverview({ data }) {
  const subscribers = data.companies.map((company) => ({ name: company.name, subscribers: company.subscribers }))
  const timeline = []
  data.companies.forEach((company) => company.videos_over_time.forEach((point, index) => {
    timeline[index] = { ...(timeline[index] || { index }), [company.name]: point.views }
  }))
  const rows = data.companies.map((company) => ({
    company: company.name,
    subscribers: formatNumber(company.subscribers),
    total_views: formatNumber(company.total_views),
    avg_views: formatNumber(company.avg_views),
    engagement: `${company.avg_engagement_rate}%`,
    consistency: company.consistency_score
  }))
  return (
    <div className="space-y-6">
      <div className="grid gap-4 md:grid-cols-5">
        {data.companies.map((company) => (
          <div key={company.name} className="rounded-lg border border-border bg-card overflow-hidden">
            <div className="p-4">
              <div className="text-base font-semibold text-white">{company.name}</div>
              <div className="mt-2 text-xl font-black text-white">{formatNumber(company.subscribers)}</div>
              <div className="mt-1 text-xs text-muted">Subscribers</div>
            </div>
          </div>
        ))}
      </div>
      <div className="rounded-lg border border-border bg-card p-5">
        <ResponsiveContainer width="100%" height={320}>
          <BarChart data={subscribers} layout="vertical">
            <CartesianGrid stroke="#2D3250" />
            <XAxis type="number" tick={{ fill: '#A0A0B0' }} />
            <YAxis type="category" dataKey="name" tick={{ fill: '#A0A0B0' }} width={120} />
            <Tooltip contentStyle={tooltipStyle} formatter={(value) => formatNumber(value)} />
            <Bar dataKey="subscribers" fill="#6C63FF" radius={[0, 6, 6, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
      <StyledTable columns={[
        { key: 'company', label: 'Company' },
        { key: 'subscribers', label: 'Subscribers' },
        { key: 'total_views', label: 'Total Views' },
        { key: 'avg_views', label: 'Avg Views' },
        { key: 'engagement', label: 'Engagement Rate' },
        { key: 'consistency', label: 'Consistency Score' }
      ]} rows={rows} scoreKeys={['consistency']} winner={data.winner} />
      <div className="rounded-lg border border-border bg-card p-5">
        <div className="mb-4 text-lg font-bold text-white">Recent View Momentum</div>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={timeline}>
            <CartesianGrid stroke="#2D3250" />
            <XAxis dataKey="index" tick={{ fill: '#A0A0B0' }} />
            <YAxis tick={{ fill: '#A0A0B0' }} tickFormatter={formatNumber} />
            <Tooltip contentStyle={tooltipStyle} formatter={(value) => formatNumber(value)} />
            <Legend wrapperStyle={{ color: '#A0A0B0' }} />
            {data.companies.map((company, index) => <Line key={company.name} type="monotone" dataKey={company.name} stroke={COLORS[index % COLORS.length]} strokeWidth={2} dot={false} />)}
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
