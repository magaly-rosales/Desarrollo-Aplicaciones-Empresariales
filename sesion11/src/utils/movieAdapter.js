const FALLBACK_POSTER = 'https://placehold.co/300x450/1a1a24/9a9ab0?text=No+Image'

// Adapter pattern: converts the API shape into the app model
export function adaptMovie(raw) {
  return {
    id: raw.id,
    title: raw.original_title ?? 'Untitled',
    poster: raw.poster_path || FALLBACK_POSTER,
    rating: Number(raw.vote_average ?? 0).toFixed(1),
    year: raw.release_date ? raw.release_date.slice(0, 4) : 'N/A',
    genre: raw.genre ?? 'Unknown',
  }
}

export const adaptMovies = (list = []) => list.map(adaptMovie)