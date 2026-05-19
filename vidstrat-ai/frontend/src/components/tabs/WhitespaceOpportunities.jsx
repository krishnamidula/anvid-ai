import OpportunityCard from '../ui/OpportunityCard'
import { Fragment } from 'react'

export default function WhitespaceOpportunities({ data }) {
  const pillars = [...new Set(data.companies.flatMap((company) => Object.keys(company.content_pillars)))]
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-white">Whitespace Opportunities</h2>
        <p className="mt-2 text-muted">Topics and formats with room to build a differentiated competitive position.</p>
      </div>
      <div className="grid gap-4 md:grid-cols-2">
        {data.whitespace_opportunities.map((item) => <OpportunityCard key={item.title} item={item} />)}
      </div>
      <div className="rounded-lg border border-border bg-card p-5">
        <h3 className="mb-4 font-bold text-white">Coverage Gap Matrix</h3>
        <div className="overflow-x-auto">
          <div className="grid min-w-[760px]" style={{ gridTemplateColumns: `150px repeat(${pillars.length}, minmax(90px, 1fr))` }}>
            <div className="p-2 text-xs text-muted">Company</div>
            {pillars.map((pillar) => <div key={pillar} className="p-2 text-xs text-muted">{pillar}</div>)}
            {data.companies.map((company) => (
              <Fragment key={company.name}>
                <div key={`${company.name}-name`} className="border-t border-border p-2 text-sm font-semibold text-white">{company.name}</div>
                {pillars.map((pillar) => {
                  const covered = (company.content_pillars[pillar] || 0) > 0
                  return <div key={`${company.name}-${pillar}`} className="border-t border-border p-2"><div className={`h-6 rounded ${covered ? 'bg-primary/30' : 'bg-border'}`} /></div>
                })}
              </Fragment>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
