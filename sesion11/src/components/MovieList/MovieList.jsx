import { useState } from 'react'
import toast from 'react-hot-toast'
import { useWindowSize } from '../../hooks/useWindowSize'
import MovieCard from '../MovieCard/MovieCard'

// Decides how many cards fit per row based on the window width
function getColumns(width) {
  if (width < 500) return 1
  if (width < 768) return 2
  if (width < 1024) return 3
  return 4
}

function MovieList({ movies }) {
  // Temporary: favorites live here for now (lifted to App in step 9)
  const [favoriteIds, setFavoriteIds] = useState([])
  const { width } = useWindowSize()
  const columns = getColumns(width)

  const handleToggleFavorite = (movie) => {
    const isFavorite = favoriteIds.includes(movie.id)

    setFavoriteIds((prev) =>
      isFavorite ? prev.filter((id) => id !== movie.id) : [...prev, movie.id]
    )

    // The parent decides how to notify the user
    if (isFavorite) {
      toast(`${movie.title} se quitó de favoritas`, { icon: '💔' })
    } else {
      toast.success(`${movie.title} se agregó a favoritas`)
    }
  }

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
            onToggleFavorite={handleToggleFavorite}
          />
        ))}
      </div>
    </>
  )
}

export default MovieList