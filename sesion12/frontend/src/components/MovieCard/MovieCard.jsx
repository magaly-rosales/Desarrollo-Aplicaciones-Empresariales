import './MovieCard.css'

// The card only notifies the parent; it doesn't know how the message is shown
function MovieCard({ movie, isFavorite, onToggleFavorite }) {
  return (
    <article className="card movie-card">
      <div className="movie-card__poster">
        <img src={movie.poster} alt={movie.title} loading="lazy" />
        <button
          className={`fav-btn ${isFavorite ? 'fav-btn--active' : ''}`}
          onClick={() => onToggleFavorite(movie)}
          aria-label={isFavorite ? 'Quitar de favoritas' : 'Agregar a favoritas'}
        >
          {isFavorite ? '♥' : '♡'}
        </button>
      </div>

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