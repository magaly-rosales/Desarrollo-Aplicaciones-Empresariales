import { useMemo, useState } from 'react'
import toast, { Toaster } from 'react-hot-toast'
import { rawMovies } from './data/rawMovies'
import { adaptMovies } from './utils/movieAdapter'
import { useDebounce } from './hooks/useDebounce'
import Header from './components/Header/Header'
import PremieresSection from './components/PremieresSection/PremieresSection'
import SearchBar from './components/SearchBar/SearchBar'
import MovieList from './components/MovieList/MovieList'

// Every movie goes through the adapter before reaching the UI
const movies = adaptMovies(rawMovies)

function App() {
  // Shared by SearchBar and MovieList (siblings) -> lives in their common ancestor
  const [query, setQuery] = useState('')
  const debouncedQuery = useDebounce(query, 400)

  // Lifted state: Header (count) and MovieList (hearts) are siblings
  const [favoriteIds, setFavoriteIds] = useState([])

  const handleToggleFavorite = (movie) => {
    const isFavorite = favoriteIds.includes(movie.id)

    setFavoriteIds((prev) =>
      isFavorite ? prev.filter((id) => id !== movie.id) : [...prev, movie.id]
    )

    // App decides how to notify; the card only reports the click
    if (isFavorite) {
      toast(`${movie.title} se quitó de favoritas`, { icon: '💔' })
    } else {
      toast.success(`${movie.title} se agregó a favoritas`)
    }
  }

  const filteredMovies = useMemo(() => {
    const term = debouncedQuery.trim().toLowerCase()
    if (!term) return movies

    return movies.filter(
      (movie) =>
        movie.title.toLowerCase().includes(term) ||
        movie.genre.toLowerCase().includes(term)
    )
  }, [debouncedQuery])

  return (
    <>
      {/* Header only receives the number, not the whole list */}
      <Header favoritesCount={favoriteIds.length} />

      <main className="container section">
        <PremieresSection />

        <SearchBar
          value={query}
          onChange={setQuery}
          isSearching={query !== debouncedQuery}
        />

        <div className="flex between" style={{ marginBottom: '1rem' }}>
          <h2>Cartelera</h2>
          <span className="muted">{filteredMovies.length} películas</span>
        </div>

        <MovieList
          movies={filteredMovies}
          favoriteIds={favoriteIds}
          onToggleFavorite={handleToggleFavorite}
        />
      </main>

      {/* Global toast container */}
      <Toaster
        position="bottom-right"
        toastOptions={{ style: { background: '#252533', color: '#f1f1f5' } }}
      />
    </>
  )
}

export default App