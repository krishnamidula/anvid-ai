import { motion } from 'framer-motion'

const badges = ['YouTube Intelligence', 'Data Science', 'SEO Analysis', 'AI Strategy', 'PowerPoint Export']

export default function Hero({ compact = false }) {
  return (
    <section className={`hero-gradient relative overflow-hidden border-b border-border ${compact ? 'py-10' : 'py-16'}`}>
      <div className="ambient-field" />
      <div className="relative z-10 mx-auto max-w-6xl px-6 text-center">
        <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="text-xs font-bold uppercase tracking-[0.35em] text-muted">
          Video Marketing Intelligence
        </motion.div>
        <motion.h1 initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.08 }} className={`${compact ? 'text-4xl' : 'text-6xl'} mt-4 font-black text-shimmer`}>
          anvidAI
        </motion.h1>
        <motion.p initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.14 }} className="mt-3 text-xl text-muted">
          Real Data. Deep Strategy. Agency-Grade Insights.
        </motion.p>
        {!compact && (
          <div className="mt-6 flex flex-wrap justify-center gap-3">
            {badges.map((badge, index) => (
              <motion.span
                key={badge}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 + index * 0.1 }}
                className="rounded-full border border-primary/30 bg-primary/10 px-4 py-1.5 text-xs font-medium text-primary/80"
              >
                {badge}
              </motion.span>
            ))}
          </div>
        )}
      </div>
    </section>
  )
}
