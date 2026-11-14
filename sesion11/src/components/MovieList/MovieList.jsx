import { useState } from 'react'
import toast from 'react-hot-toast'
import MovieCard from '../MovieCard/MovieCard'

function MovieList({ movies }) {
  // Temporary: favorites live here for now (lifted to App in step 9)
  const [favoriteIds, setFavoriteIds] = useState([])

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
    <div className="grid">
      {movies.map((movie) => (
        <MovieCard
          key={movie.id}
          movie={movie}
          isFavorite={favoriteIds.includes(movie.id)}
          onToggleFavorite={handleToggleFavorite}
        />
      ))}
    </div>
  )
}

export default MovieList