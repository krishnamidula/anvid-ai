import { motion } from 'framer-motion'
import { useEffect, useMemo, useState } from 'react'
import ProgressTracker from './ui/ProgressTracker'

const steps = [
  'Locating YouTube channel',
  'Fetching channel statistics',
  'Retrieving top-performing videos',
  'Running data science calculations',
  'Performing SEO pattern analysis',
  'Classifying content pillars via AI',
  'Generating channel persona',
  'Building strategic recommendations',
  'Identifying whitespace opportunities',
  'Compiling 90-day action plan',
  'Generating charts and visualisations',
  'Building PowerPoint report'
]

export default function AnalysisProgress({ request }) {
  const [activeStep, setActiveStep] = useState(0)
  const companies = useMemo(() => [request.primary_company, ...request.competitors].filter(Boolean), [request])

  useEffect(() => {
    const timings = [700, 1000, 1200, 1400, 1400, 2200, 2200, 2300, 2200, 2300, 1400, 1300]
    let step = 0
    let timer
    const tick = () => {
      step = Math.min(steps.length - 1, step + 1)
      setActiveStep(step)
      timer = setTimeout(tick, timings[step] || 1400)
    }
    timer = setTimeout(tick, timings[0])
    return () => clearTimeout(timer)
  }, [])

  const progress = Math.min(96, Math.round((activeStep / (steps.length - 1)) * 100))
  const company = companies[activeStep % companies.length]

  return (
    <motion.div initial={{ opacity: 0, y: 22 }} animate={{ opacity: 1, y: 0 }} className="relative overflow-hidden rounded-2xl border border-border bg-card p-8">
      <div className="scan-line" />
      <h2 className="mb-1 text-xl font-bold text-white">Analysing Your Competitive Landscape</h2>
      <p className="mb-8 text-sm text-muted">Processing real-time data across all channels</p>
      <div className="mb-8 h-1.5 w-full rounded-full bg-border">
        <div className="progress-fill h-1.5" style={{ width: `${progress}%` }} />
      </div>
      <ProgressTracker steps={steps} activeStep={activeStep} company={company} />
    </motion.div>
  )
}
