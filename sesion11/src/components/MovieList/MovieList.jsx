import { useWindowSize } from '../../hooks/useWindowSize'
import { getColumns } from '../../utils/getColumns'
import MovieCard from '../MovieCard/MovieCard'

// Stateless for favorites: receives them from App and reports changes up
function MovieList({ movies, favoriteIds, onToggleFavorite }) {
  const { width } = useWindowSize()
  const columns = getColumns(width)

  if (movies.length === 0) {
    return <p className="muted text-center">No se encontraron películas.</p>
  }

  return (
    <>
      <p className="muted" style={{ fontSize: '0.8rem', marginBottom: '0.8rem' }}>
        Ancho: {width}px · {columns} por fila
      </p>

      {/* --cols feeds the .grid utility from index.css */}
      <div className="grid" style={{ '--cols': columns }}>
        {movies.map((movie) => (
          <MovieCard
            key={movie.id}
            movie={movie}
            isFavorite={favoriteIds.includes(movie.id)}
            onToggleFavorite={onToggleFavorite}
          />
        ))}
      </div>
    </>
  )
}

export default MovieList