import './Banner.css'

// Doesn't own the filter: it shows it and asks App to clear it
function Banner({ activeFilter, resultsCount, onClearFilter }) {
  const hasFilter = activeFilter.trim() !== ''

  return (
    <section className="banner">
      <div>
        <h2>¿Qué vemos hoy?</h2>
        {hasFilter ? (
          <p>
            Filtro activo: <strong>«{activeFilter}»</strong> · {resultsCount} resultados
          </p>
        ) : (
          <p>Explora las {resultsCount} películas de la cartelera</p>
        )}
      </div>

      {hasFilter && (
        <button className="btn btn-primary" onClick={onClearFilter}>
          ✕ Limpiar filtro
        </button>
      )}
    </section>
  )
}

export default Banner