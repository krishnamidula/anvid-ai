import { AnimatePresence, motion } from 'framer-motion'
import { useEffect, useRef, useState } from 'react'
import ActionPlan from './tabs/ActionPlan'
import CadenceAndSEO from './tabs/CadenceAndSEO'
import ChannelOverview from './tabs/ChannelOverview'
import ContentStrategy from './tabs/ContentStrategy'
import EngagementAnalysis from './tabs/EngagementAnalysis'
import ExecutiveSummary from './tabs/ExecutiveSummary'
import TopVideos from './tabs/TopVideos'
import WhitespaceOpportunities from './tabs/WhitespaceOpportunities'

const tabs = [
  ['Executive Summary', ExecutiveSummary],
  ['Channel Overview', ChannelOverview],
  ['Content Strategy', ContentStrategy],
  ['Top Videos', TopVideos],
  ['Cadence and SEO', CadenceAndSEO],
  ['Engagement Analysis', EngagementAnalysis],
  ['Whitespace Opportunities', WhitespaceOpportunities],
  ['90-Day Action Plan', ActionPlan]
]

export default function ResultsDashboard({ data, onNew }) {
  const wrapperRef = useRef(null)

  function downloadPpt() {
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
  const [active, setActive] = useState(0)
  const ActiveComponent = tabs[active][1]

  useEffect(() => {
    if (wrapperRef.current) {
      wrapperRef.current.scrollIntoView({ behavior: 'smooth', block: 'start' })
    } else {
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }
  }, [active])

  return (
    <motion.div ref={wrapperRef} initial={{ opacity: 0, y: 22 }} animate={{ opacity: 1, y: 0 }} className="mx-auto max-w-7xl px-6 py-8">
      <div className="mb-6 flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="text-xs font-bold uppercase tracking-widest text-primary">anvidAI Report</div>
          <h1 className="mt-2 text-3xl font-black text-white">{data.winner} leads this comparison</h1>
          {data.excluded_companies?.length > 0 && <p className="mt-2 text-sm text-warm">{data.excluded_companies.map((item) => item.error).join(' ')}</p>}
          {data.ai_message && <p className="mt-2 text-sm text-warm">{data.ai_message}</p>}
        </div>
        <div className="flex flex-wrap gap-3">
          <button onClick={downloadPpt} className="rounded-xl bg-gradient-to-r from-primary to-secondary px-5 py-3 text-sm font-semibold text-white shadow-lg shadow-primary/30 transition-all hover:scale-105 hover:shadow-xl">
            Download PPT
          </button>
          <button onClick={onNew} className="rounded-xl border border-border px-5 py-3 text-sm font-semibold text-muted transition-colors hover:border-primary hover:text-primary">
            Analyse New Companies
          </button>
        </div>
      </div>
      <div className="rounded-xl border border-border bg-card p-1">
        <div className="flex gap-1 overflow-x-auto">
          {tabs.map(([label], index) => (
            <button key={label} onClick={() => setActive(index)} className={`relative whitespace-nowrap rounded-lg px-5 py-2.5 text-sm font-medium transition-all ${active === index ? 'text-white' : 'text-muted hover:bg-white/5 hover:text-white'}`}>
              {active === index && <motion.span layoutId="active-tab" className="absolute inset-0 rounded-lg bg-primary shadow-lg shadow-primary/30" />}
              <span className="relative z-10">{label}</span>
            </button>
          ))}
        </div>
      </div>
      <div className="mt-6">
        <AnimatePresence mode="wait">
          <motion.div key={active} initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} transition={{ duration: 0.3 }}>
            <ActiveComponent data={data} />
          </motion.div>
        </AnimatePresence>
      </div>
    </motion.div>
  )
}
