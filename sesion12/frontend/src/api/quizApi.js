import axios from 'axios'

// The only place that knows the API address and the credentials:
// no component writes a URL by hand.
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api',
  headers: { Authorization: `Token ${import.meta.env.VITE_API_TOKEN}` },
})

// The API is paginated: the response is { count, next, previous, results }
export const listExams = () => api.get('/exams/').then((response) => response.data)

export const createExam = (exam) =>
  api.post('/exams/', exam).then((response) => response.data)

export const deleteExam = (id) => api.delete(`/exams/${id}/`)