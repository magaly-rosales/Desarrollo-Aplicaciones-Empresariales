import { useMemo, useState } from 'react'
import { Toaster } from 'react-hot-toast'
import { rawMovies } from './data/rawMovies'
import { adaptMovies } from './utils/movieAdapter'
import { useDebounce } from './hooks/useDebounce'
import SearchBar from './components/SearchBar/SearchBar'
import MovieList from './components/MovieList/MovieList'

// Every movie goes through the adapter before reaching the UI
const movies = adaptMovies(rawMovies)

function App() {
  // Shared by SearchBar and MovieList (siblings) -> lives in their common ancestor
  const [query, setQuery] = useState('')
  const debouncedQuery = useDebounce(query, 400)

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
    <main className="container section">
      <h1>Cartelera Lab 11</h1>
      <p className="muted" style={{ marginBottom: '1.5rem' }}>
        Comunicación entre componentes en React
      </p>

      <SearchBar
        value={query}
        onChange={setQuery}
        isSearching={query !== debouncedQuery}
      />

      <div className="flex between" style={{ marginBottom: '1rem' }}>
        <h2>Cartelera</h2>
        <span className="muted">{filteredMovies.length} películas</span>
      </div>

      <MovieList movies={filteredMovies} />

      {/* Global toast container */}
      <Toaster
        position="bottom-right"
        toastOptions={{ style: { background: '#252533', color: '#f1f1f5' } }}
      />
    </main>
  )
}

export default App