import MovieCard from '../MovieCard/MovieCard'

function MovieList({ movies }) {
  if (movies.length === 0) {
    return <p className="muted text-center">No se encontraron películas.</p>
  }

  return (
    <div className="grid">
      {movies.map((movie) => (
        <MovieCard key={movie.id} movie={movie} />
      ))}
    </div>
  )
}

export default MovieList