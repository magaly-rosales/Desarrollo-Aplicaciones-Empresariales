import { useCallback, useEffect, useState } from 'react'
import { rawPremieres } from '../data/rawPremieres'
import { adaptMovies } from '../utils/movieAdapter'

const FAKE_DELAY = 2000

// Simulates a network request that can succeed or fail
function fakeFetchPremieres(shouldFail) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (shouldFail) {
        reject(
          new Error(
            'No se pudo conectar con el servidor de estrenos (error 503). Intenta nuevamente en unos segundos.'
          )
        )
      } else {
        resolve(rawPremieres)
      }
    }, FAKE_DELAY)
  })
}

// Three states: 'loading' | 'success' | 'error'
export function usePremieres(shouldFail = false) {
  const [premieres, setPremieres] = useState([])
  const [status, setStatus] = useState('loading')
  const [error, setError] = useState(null)
  const [attempt, setAttempt] = useState(0)

  useEffect(() => {
    // Prevents updating state if the request is outdated
    let ignore = false

    setStatus('loading')
    setError(null)

    fakeFetchPremieres(shouldFail)
      .then((data) => {
        if (ignore) return
        setPremieres(adaptMovies(data)) // reuses the adapter
        setStatus('success')
      })
      .catch((err) => {
        if (ignore) return
        setError(err.message)
        setStatus('error')
      })

    return () => {
      ignore = true
    }
  }, [shouldFail, attempt])

  // Forces a new request
  const reload = useCallback(() => setAttempt((n) => n + 1), [])

  return { premieres, status, error, reload }
}