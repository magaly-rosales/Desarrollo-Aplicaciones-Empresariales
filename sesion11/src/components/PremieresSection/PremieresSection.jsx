import { useState } from 'react'
import { usePremieres } from '../../hooks/usePremieres'
import { useWindowSize } from '../../hooks/useWindowSize'
import { getColumns } from '../../utils/getColumns'
import SkeletonCard from '../SkeletonCard/SkeletonCard'
import PremiereCarousel from '../PremiereCarousel/PremiereCarousel'
import './PremieresSection.css'

function PremieresSection() {
  // Only this section needs it, so the state lives here
  const [simulateError, setSimulateError] = useState(false)
  const { premieres, status, error, reload } = usePremieres(simulateError)
  const { width } = useWindowSize()
  const columns = getColumns(width)

  return (
    <section className="premieres">
      <div className="flex between premieres__header">
        <h2>Próximos estrenos</h2>

        <div className="flex">
          <label className="premieres__toggle">
            <input
              type="checkbox"
              checked={simulateError}
              onChange={(e) => setSimulateError(e.target.checked)}
            />
            Simular error
          </label>
          <button className="btn" onClick={reload} disabled={status === 'loading'}>
            Recargar
          </button>
        </div>
      </div>

      {/* State 1: loading */}
      {status === 'loading' && (
        <div className="grid" style={{ '--cols': columns }}>
          {Array.from({ length: columns }).map((_, i) => (
            <SkeletonCard key={i} />
          ))}
        </div>
      )}

      {/* State 2: error with a clear explanation */}
      {status === 'error' && (
        <div className="error-box">
          <span className="error-box__icon">⚠️</span>
          <div>
            <h3>No pudimos cargar los estrenos</h3>
            <p>{error}</p>
          </div>
          <button className="btn btn-primary" onClick={reload}>
            Reintentar
          </button>
        </div>
      )}

      {/* State 3: data */}
      {status === 'success' && <PremiereCarousel premieres={premieres} />}
    </section>
  )
}

export default PremieresSection