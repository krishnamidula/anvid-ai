export default function ProgressTracker({ steps, activeStep, company }) {
  return (
    <div>
      {steps.map((step, index) => {
        const state = index < activeStep ? 'done' : index === activeStep ? 'active' : 'waiting'
        return (
          <div key={step} className="flex items-center gap-3 border-b border-border/50 py-2.5 last:border-b-0">
            <span className={`h-2 w-2 rounded-full ${state === 'done' ? 'bg-secondary' : state === 'active' ? 'pulse-dot bg-primary' : 'bg-border'}`} />
            <div>
              <div className={`text-sm ${state === 'done' ? 'text-secondary' : state === 'active' ? 'font-medium text-white' : 'text-faint'}`}>{step}</div>
              {state === 'active' && company && <div className="mt-1 text-xs text-muted">Current company: {company}</div>}
            </div>
          </div>
        )
      })}
    </div>
  )
}
