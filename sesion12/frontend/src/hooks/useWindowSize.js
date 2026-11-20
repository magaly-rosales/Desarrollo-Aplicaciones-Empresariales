import { useEffect, useState } from 'react'

// Tracks the current window size and updates on resize
export function useWindowSize() {
  const [size, setSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight,
  })

  useEffect(() => {
    const handleResize = () =>
      setSize({ width: window.innerWidth, height: window.innerHeight })

    window.addEventListener('resize', handleResize)

    // Remove the listener when the component unmounts
    return () => window.removeEventListener('resize', handleResize)
  }, [])

  return size
}