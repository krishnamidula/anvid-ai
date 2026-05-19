import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import ConsistencyBadge from '../ui/ConsistencyBadge'
import OpportunityCard from '../ui/OpportunityCard'
import StyledTable from '../ui/StyledTable'
import { tooltipStyle } from '../ui/helpers'

export default function CadenceAndSEO({ data }) {
  const seoRows = data.companies.map((company) => ({
    company: company.name,
    overall: company.seo_scores.overall,
    title_score: company.seo_scores.title_score,
    description_score: company.seo_scores.description_score,
    best_upload_day: company.seo_scores.best_upload_day,
    timing_score: company.seo_scores.timing_score
  }))
  return (
    <div className="space-y-6">
      <div className="grid gap-4 lg:grid-cols-2">
        {data.companies.map((company) => (
          <div key={company.name} className="rounded-lg border border-border bg-card p-5">
            <h3 className="mb-3 font-bold text-white">{company.name}</h3>
            <ResponsiveContainer width="100%" height={190}>
              <BarChart data={Object.entries(company.upload_day_distribution).map(([day, count]) => ({ day: day.slice(0, 3), count }))}>
                <CartesianGrid stroke="#2D3250" />
                <XAxis dataKey="day" tick={{ fill: '#A0A0B0' }} />
                <YAxis tick={{ fill: '#A0A0B0' }} />
                <Tooltip contentStyle={tooltipStyle} />
                <Bar dataKey="count" fill="#43B89C" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        ))}
      </div>
      <div className="grid gap-4 md:grid-cols-3">
        {data.companies.map((company) => (
          <div key={company.name} className="rounded-lg border border-border bg-card p-5">
            <div className="text-sm font-bold text-white">{company.name}</div>
            <div className="mt-3 text-4xl font-black text-shimmer">{company.consistency_score}</div>
            <div className="mt-3"><ConsistencyBadge value={company.consistency_classification} /></div>
            <div className="mt-3 text-sm text-muted">Average interval: {company.avg_interval_days} days</div>
          </div>
        ))}
      </div>
      <StyledTable columns={[
        { key: 'company', label: 'Company' },
        { key: 'overall', label: 'SEO Score' },
        { key: 'title_score', label: 'Title Score' },
        { key: 'description_score', label: 'Description Score' },
        { key: 'best_upload_day', label: 'Best Day' },
        { key: 'timing_score', label: 'Timing Score' }
      ]} rows={seoRows} scoreKeys={['overall', 'title_score', 'description_score', 'timing_score']} />
      <div className="grid gap-4 md:grid-cols-2">
        <OpportunityCard item={{ title: 'Metadata Depth Advantage', description: 'Descriptions with links, hashtags, chapter-like structure, and conversion paths can immediately improve discoverability against thin competitor uploads.', format: 'Description system', potential: 'High' }} />
        <OpportunityCard item={{ title: 'Intent-Led Title System', description: 'The strongest opportunity is to title around viewer jobs, comparisons, and outcomes instead of broad brand announcements.', format: 'Search title framework', potential: 'High' }} />
      </div>
    </div>
  )
}
