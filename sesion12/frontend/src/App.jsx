import ExamListPage from './pages/ExamListPage/ExamListPage'

function App() {
  return (
    <main className="container section">
      <h1>Quiz Lab 12</h1>
      <p className="muted" style={{ marginBottom: '2rem' }}>
        Servicios web: React + Axios consumiendo la API de Django
      </p>
      <ExamListPage />
    </main>
  )
}

export default App