import { useEffect, useState } from 'react'
import Skeleton, { SkeletonTheme } from 'react-loading-skeleton'
import 'react-loading-skeleton/dist/skeleton.css'
import { listExams } from '../../api/quizApi'
import { getErrorMessage } from '../../utils/getErrorMessage'
import './ExamListPage.css'

const SKELETON_ROWS = 5

function ExamListPage() {
  // The three states of a request: data, loading and error
  const [exams, setExams] = useState([])
  const [total, setTotal] = useState(0)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState(null)

  // Changing this number launches the request again (used by the retry button)
  const [attempt, setAttempt] = useState(0)

  // GET on mount (and on every retry). The initial state is already
  // "loading", so nothing needs to be reset here.
  useEffect(() => {
    // Avoids using the answer of a request that is no longer current
    let ignore = false

    listExams()
      .then((data) => {
        if (ignore) return
        setExams(data.results)
        setTotal(data.count)
      })
      .catch((err) => {
        if (!ignore) setError(getErrorMessage(err))
      })
      .finally(() => {
        if (!ignore) setIsLoading(false)
      })

    return () => {
      ignore = true
    }
  }, [attempt])

  const handleRetry = () => {
    setIsLoading(true)
    setError(null)
    setAttempt((current) => current + 1)
  }
    return (
    <section>
      <div className="flex between exam-page__header">
        <h2>Exámenes</h2>
        {!isLoading && !error && (
          <span className="muted">
            {exams.length} de {total} exámenes
          </span>
        )}
      </div>

      {/* State 1: loading */}
      {isLoading && (
        <SkeletonTheme baseColor="#1a1a24" highlightColor="#2f2f40">
          <div className="exam-table" aria-busy="true" aria-label="Cargando exámenes">
            {Array.from({ length: SKELETON_ROWS }, (_, index) => (
              <Skeleton key={index} height={44} borderRadius={8} />
            ))}
          </div>
        </SkeletonTheme>
      )}

      {/* State 2: error, with a way out */}
      {!isLoading && error && (
        <div className="exam-error" role="alert">
          <p>{error}</p>
          <button type="button" className="btn btn-primary" onClick={handleRetry}>
            Reintentar
          </button>
        </div>
      )}

      {/* State 3: data */}
      {!isLoading && !error && exams.length === 0 && (
        <p className="muted text-center">Todavía no hay exámenes.</p>
      )}

      {!isLoading && !error && exams.length > 0 && (
        <table className="exam-table card">
          <thead>
            <tr>
              <th>ID</th>
              <th>Título</th>
              <th>Preguntas</th>
              <th>Creado</th>
            </tr>
          </thead>
          <tbody>
            {exams.map((exam) => (
              <tr key={exam.id}>
                <td>{exam.id}</td>
                <td>{exam.title}</td>
                <td>{exam.question_count}</td>
                <td>{new Date(exam.created_at).toLocaleDateString('es-PE')}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  )
}

export default ExamListPage