import { motion } from 'framer-motion'

export default function MetricCard({ label, value, delay = 0 }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 14 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay }}
      className="card-hover rounded-lg border border-border bg-card p-5"
    >
      <div className="text-3xl font-black text-shimmer">{value}</div>
      <div className="mt-2 text-sm text-muted">{label}</div>
    </motion.div>
  )
}
