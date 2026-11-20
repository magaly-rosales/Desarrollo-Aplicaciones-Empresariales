import { useEffect, useState } from 'react'

// Returns the value only after it stops changing for `delay` ms
export function useDebounce(value, delay = 400) {
  const [debouncedValue, setDebouncedValue] = useState(value)

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay)

    // Cancel the previous timer on every new keystroke
    return () => clearTimeout(timer)
  }, [value, delay])

  return debouncedValue
}