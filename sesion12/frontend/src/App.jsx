import { Route, Routes } from 'react-router-dom'
import ExamListPage from './pages/ExamListPage/ExamListPage'
import ExamFormPage from './pages/ExamFormPage/ExamFormPage'

function App() {
  return (
    <main className="container section">
      <h1>Quiz Lab 12</h1>
      <p className="muted" style={{ marginBottom: '2rem' }}>
        Servicios web: React + Axios consumiendo la API de Django
      </p>

      <Routes>
        <Route path="/" element={<ExamListPage />} />
        <Route path="/exams/new" element={<ExamFormPage />} />
      </Routes>
    </main>
  )
}

export default App