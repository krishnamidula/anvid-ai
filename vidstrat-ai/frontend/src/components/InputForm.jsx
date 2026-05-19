import { motion } from 'framer-motion'
import { useState } from 'react'

const example = {
  primary_company: 'Amul',
  competitors: ['Mother Dairy', 'Nestle India', 'Britannia', 'Nandini']
}

export default function InputForm({ onSubmit }) {
  const [primary, setPrimary] = useState('')
  const [competitors, setCompetitors] = useState(['', '', '', ''])

  function loadExample() {
    setPrimary(example.primary_company)
    setCompetitors(example.competitors)
  }

  function updateCompetitor(index, value) {
    setCompetitors((current) => current.map((item, itemIndex) => itemIndex === index ? value : item))
  }

  function submit(event) {
    event.preventDefault()
    onSubmit({ primary_company: primary, competitors: competitors.filter(Boolean) })
  }

  return (
    <motion.form initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }} onSubmit={submit} className="rounded-2xl border border-border bg-card p-8">
      <div className="mb-2 text-xs font-bold uppercase tracking-widest text-primary">Define Your Competitive Landscape</div>
      <h2 className="mb-8 text-2xl font-bold text-white">Who are you up against?</h2>
      <div className="grid gap-4">
        <motion.input initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} value={primary} onChange={(event) => setPrimary(event.target.value)} placeholder="Primary company" className="w-full rounded-xl border border-border bg-surface px-4 py-3 text-sm text-white transition-all placeholder:text-faint focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20" />
        <div className="grid gap-4 md:grid-cols-2">
          {competitors.map((value, index) => (
            <motion.input
              key={index}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.05 * index }}
              value={value}
              onChange={(event) => updateCompetitor(index, event.target.value)}
              placeholder={`Competitor ${index + 1}`}
              className="w-full rounded-xl border border-border bg-surface px-4 py-3 text-sm text-white transition-all placeholder:text-faint focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20"
            />
          ))}
        </div>
      </div>
      <div className="mt-8 flex flex-wrap justify-between gap-4">
        <button type="button" onClick={loadExample} className="rounded-xl border border-border bg-transparent px-6 py-3 text-sm text-muted transition-all hover:border-primary hover:text-primary">
          Load Example: Dairy Brands
        </button>
        <button type="submit" className="rounded-xl bg-primary px-8 py-3 text-sm font-semibold text-white shadow-lg shadow-primary/30 transition-all hover:-translate-y-0.5 hover:bg-primary/90 hover:shadow-xl hover:shadow-primary/40">
          Generate Intelligence Report
        </button>
      </div>
    </motion.form>
  )
}
