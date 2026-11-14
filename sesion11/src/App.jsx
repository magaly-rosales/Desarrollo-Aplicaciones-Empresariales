import { Toaster } from 'react-hot-toast'
import { rawMovies } from './data/rawMovies'
import { adaptMovies } from './utils/movieAdapter'
import MovieList from './components/MovieList/MovieList'

// Every movie goes through the adapter before reaching the UI
const movies = adaptMovies(rawMovies)

function App() {
  return (
    <main className="container section">
      <h1>Cartelera Lab 11</h1>
      <p className="muted" style={{ marginBottom: '1.5rem' }}>
        Comunicación entre componentes en React
      </p>

      <h2>Cartelera</h2>
      <MovieList movies={movies} />

      {/* Global toast container */}
      <Toaster
        position="bottom-right"
        toastOptions={{ style: { background: '#252533', color: '#f1f1f5' } }}
      />
    </main>
  )
}

export default App