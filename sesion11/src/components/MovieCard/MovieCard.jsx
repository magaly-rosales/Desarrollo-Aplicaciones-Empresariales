import './MovieCard.css'

function MovieCard({ movie }) {
  return (
    <article className="card movie-card">
      <img src={movie.poster} alt={movie.title} loading="lazy" />
      <div className="movie-card__body">
        <h3>{movie.title}</h3>
        <div className="flex between">
          <span className="muted">
            {movie.year} · {movie.genre}
          </span>
          <span className="badge">★ {movie.rating}</span>
        </div>
      </div>
    </article>
  )
}

export default MovieCard