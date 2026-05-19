import StyledTable from '../ui/StyledTable'

export default function ActionPlan({ data }) {
  const months = [
    ['month_1', 'Month 1', 'text-primary', 'border-primary/50'],
    ['month_2', 'Month 2', 'text-secondary', 'border-secondary/50'],
    ['month_3', 'Month 3', 'text-warm', 'border-warm/50']
  ]

  function download() {
    const binary = atob(data.pptx_base64)
    const bytes = new Uint8Array(binary.length)
    for (let index = 0; index < binary.length; index += 1) bytes[index] = binary.charCodeAt(index)
    const blob = new Blob([bytes], { type: 'application/vnd.openxmlformats-officedocument.presentationml.presentation' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `anvidAI-report-${Date.now()}.pptx`
    link.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="space-y-6">
      <div className="grid gap-6 lg:grid-cols-3">
        {months.map(([key, label, textColor, borderColor]) => {
          const month = data.action_plan[key]
          return (
            <div key={key} className={`rounded-lg border ${borderColor} bg-card p-5`}>
              <div className={`text-xs font-bold uppercase tracking-widest ${textColor}`}>{label}</div>
              <h3 className="mt-2 text-lg font-bold text-white">{month.title}</h3>
              <div className="my-4 h-px bg-border" />
              <div className="space-y-3">
                {month.actions.map((action) => <div key={action} className="flex gap-3 text-sm text-muted"><span className="mt-2 h-1.5 w-1.5 rounded-full bg-current" /><span>{action}</span></div>)}
              </div>
            </div>
          )
        })}
      </div>
      <StyledTable columns={[
        { key: 'rank', label: 'Rank' },
        { key: 'company', label: 'Company' },
        { key: 'overall_score', label: 'Score' },
        { key: 'key_strength', label: 'Key Strength' },
        { key: 'biggest_opportunity', label: 'Biggest Opportunity' }
      ]} rows={data.final_ranking} scoreKeys={['overall_score']} winner={data.winner} />
      <div className="rounded-lg border border-primary/50 bg-gradient-to-br from-card to-surface p-7">
        <h3 className="text-2xl font-bold text-white">Your Intelligence Report is Ready</h3>
        <p className="mt-2 text-muted">Professional 12-slide PowerPoint with embedded charts and AI-generated strategic insights</p>
        <button onClick={download} className="mt-6 rounded-xl bg-gradient-to-r from-primary to-secondary px-10 py-4 font-semibold text-white shadow-lg shadow-primary/30 transition-all hover:scale-105 hover:shadow-xl">
          Download PowerPoint Report
        </button>
      </div>
    </div>
  )
}
