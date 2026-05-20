import axios from 'axios'
import { AnimatePresence, motion } from 'framer-motion'
import { useEffect, useState } from 'react'
import AnalysisProgress from './components/AnalysisProgress'
import Hero from './components/Hero'
import InputForm from './components/InputForm'
import ResultsDashboard from './components/ResultsDashboard'

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api/analyse';
console.log('Using API_URL:', API_URL)

export default function App() {
  const [state, setState] = useState('input')
  const [request, setRequest] = useState(null)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    if (state !== 'analysing' || !request) return
    let cancelled = false
    axios
  .post(API_URL, request, {
    timeout: 120000,
  })
  .then((response) => {
    console.log("SUCCESS:", response.data)

    if (cancelled) return

    setResult(response.data)
    setState('results')
  })
  .catch((err) => {
    console.log("FULL ERROR:", err)

    if (cancelled) return

    const message =
      err.response?.data?.detail ||
      err.message ||
      'Connection failed. Please check your connection and try again.'

    setError(
      Array.isArray(message)
        ? 'Please check the submitted company names and try again.'
        : message
    )

    setState('error')
  })
    return () => { cancelled = true }
  }, [state, request])

  function submit(payload) {
    if (!payload.primary_company?.trim() || payload.competitors.length < 1) {
      setError('Enter a primary company and at least one competitor.')
      setState('error')
      return
    }
    setRequest(payload)
    setState('analysing')
  }

  useEffect(() => {
    if (state === 'input' || state === 'results') {
      const scrollTop = () => {
        window.scrollTo({ top: 0, left: 0, behavior: 'smooth' })
        if (document.scrollingElement) document.scrollingElement.scrollTop = 0
        if (document.body) document.body.scrollTop = 0
      }
      window.requestAnimationFrame(() => setTimeout(scrollTop, 50))
    }
  }, [state])

  return (
    <div className="min-h-screen bg-surface">
      <AnimatePresence mode="sync">
        {state === 'input' && (
          <motion.main key="input" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
            <Hero />
            <div className="mx-auto max-w-4xl px-6 py-10"><InputForm onSubmit={submit} /></div>
          </motion.main>
        )}
        {state === 'analysing' && (
          <motion.main key="analysing" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
            <Hero compact />
            <div className="mx-auto max-w-4xl px-6 py-10"><AnalysisProgress request={request} /></div>
          </motion.main>
        )}
        {state === 'results' && result && (
          <motion.main key="results" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
            <ResultsDashboard
              data={result}
              onNew={() => {
                setState('input')
                setResult(null)
                setRequest(null)
                setError('')
                window.scrollTo({ top: 0, behavior: 'smooth' })
              }}
            />
          </motion.main>
        )}
        {state === 'error' && (
          <motion.main key="error" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
            <Hero compact />
            <div className="mx-auto max-w-3xl px-6 py-10">
              <div className="rounded-2xl border border-accent/40 bg-card p-8">
                <div className="text-xs font-bold uppercase tracking-widest text-accent">Analysis Error</div>
                <h2 className="mt-2 text-2xl font-bold text-white">The report could not be generated</h2>
                <p className="mt-4 text-muted">{error}</p>
                <button onClick={() => setState('input')} className="mt-6 rounded-xl bg-primary px-6 py-3 text-sm font-semibold text-white transition-colors hover:bg-primary/90">
                  Try Again
                </button>
              </div>
            </div>
          </motion.main>
        )}
      </AnimatePresence>
    </div>
  )
}
