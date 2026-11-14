import { useState } from 'react'
import { useWindowSize } from '../../hooks/useWindowSize'
import { getColumns } from '../../utils/getColumns'
import './PremiereCarousel.css'

function PremiereCarousel({ premieres }) {
  // Reuses useWindowSize to decide how many slides are visible
  const { width } = useWindowSize()
  const visible = getColumns(width)
  const [start, setStart] = useState(0)

  const maxStart = Math.max(0, premieres.length - visible)
  const safeStart = Math.min(start, maxStart)

  const goPrev = () => setStart(Math.max(0, safeStart - 1))
  const goNext = () => setStart(Math.min(maxStart, safeStart + 1))

  return (
    <div className="carousel">
      <button
        className="carousel__arrow"
        onClick={goPrev}
        disabled={safeStart === 0}
        aria-label="Anterior"
      >
        ‹
      </button>

      <div className="carousel__track" style={{ '--cols': visible }}>
        {premieres.slice(safeStart, safeStart + visible).map((movie) => (
          <article key={movie.id} className="card carousel__item">
            <img src={movie.poster} alt={movie.title} />
            <div className="carousel__info">
              <h3>{movie.title}</h3>
              <span className="muted">
                Estreno {movie.year} · {movie.genre}
              </span>
            </div>
          </article>
        ))}
      </div>

      <button
        className="carousel__arrow"
        onClick={goNext}
        disabled={safeStart === maxStart}
        aria-label="Siguiente"
      >
        ›
      </button>
    </div>
  )
}

export default PremiereCarousel