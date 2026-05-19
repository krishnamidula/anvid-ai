import { Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import PersonaCard from '../ui/PersonaCard'
import { COLORS, tooltipStyle } from '../ui/helpers'

export default function ContentStrategy({ data }) {
  const pillars = [...new Set(data.companies.flatMap((company) => Object.keys(company.content_pillars)))]
  const chartData = data.companies.map((company) => {
    const total = Object.values(company.content_pillars).reduce((sum, value) => sum + value, 0) || 1
    const row = { name: company.name }
    pillars.forEach((pillar) => { row[pillar] = Math.round((company.content_pillars[pillar] || 0) / total * 100) })
    return row
  })
  return (
    <div className="space-y-6">
      <div className="rounded-lg border border-border bg-card p-5">
        <ResponsiveContainer width="100%" height={360}>
          <BarChart data={chartData} layout="vertical">
            <CartesianGrid stroke="#2D3250" />
            <XAxis type="number" tick={{ fill: '#A0A0B0' }} />
            <YAxis type="category" dataKey="name" tick={{ fill: '#A0A0B0' }} width={120} />
            <Tooltip contentStyle={tooltipStyle} />
            <Legend wrapperStyle={{ color: '#A0A0B0' }} />
            {pillars.map((pillar, index) => <Bar key={pillar} dataKey={pillar} stackId="a" fill={COLORS[index % COLORS.length]} />)}
          </BarChart>
        </ResponsiveContainer>
      </div>
      <div className="grid gap-4 md:grid-cols-2">
        {data.companies.map((company) => <PersonaCard key={company.name} company={company} />)}
      </div>
      <div className="grid gap-4 md:grid-cols-3">
        {data.companies.map((company) => {
          const total = Object.values(company.format_distribution).reduce((sum, value) => sum + value, 0) || 1
          return (
            <div key={company.name} className="rounded-lg border border-border bg-card p-5">
              <h3 className="font-bold text-white">{company.name}</h3>
              {Object.entries(company.format_distribution).map(([format, count]) => (
                <div key={format} className="mt-4">
                  <div className="mb-1 flex justify-between text-xs text-muted"><span>{format}</span><span>{Math.round(count / total * 100)}%</span></div>
                  <div className="h-2 rounded-full bg-border"><div className="h-2 rounded-full bg-primary" style={{ width: `${count / total * 100}%` }} /></div>
                </div>
              ))}
            </div>
          )
        })}
      </div>
    </div>
  )
}
