import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { createExam } from '../../api/quizApi'
import { getErrorMessage } from '../../utils/getErrorMessage'
import './ExamFormPage.css'

function ExamFormPage() {
  const navigate = useNavigate()

  // Controlled input: React owns the value, not the DOM
  const [title, setTitle] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState(null)

  const handleSubmit = async (event) => {
    // Without this the browser would reload the page
    event.preventDefault()

    setIsSubmitting(true)
    setError(null)

    try {
      await createExam({ title })
      // The list mounts again and asks the API for fresh data
      navigate('/')
    } catch (err) {
      setError(getErrorMessage(err))
      setIsSubmitting(false)
    }
  }

  return (
    <section>
      <h2>Nuevo examen</h2>

      {/* noValidate: the browser does not block the submit, the API validates */}
      <form className="exam-form card" onSubmit={handleSubmit} noValidate>
        <label htmlFor="title">Título</label>
        <input
          id="title"
          type="text"
          value={title}
          onChange={(event) => setTitle(event.target.value)}
          placeholder="Ej. Django · Vistas"
          disabled={isSubmitting}
        />

        {error && (
          <p className="exam-form__error" role="alert">
            {error}
          </p>
        )}

        <div className="flex">
          <button type="submit" className="btn btn-primary" disabled={isSubmitting}>
            {isSubmitting ? 'Guardando…' : 'Guardar'}
          </button>
          <Link to="/" className="btn">
            Cancelar
          </Link>
        </div>
      </form>
    </section>
  )
}

export default ExamFormPage