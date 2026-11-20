// Turns an Axios error into a message the user can act on.
export function getErrorMessage(error) {
  // No response at all: server down, wrong address, or the browser blocked it (CORS)
  if (!error.response) {
    return 'No se pudo conectar con el servidor. Revisa que Django esté encendido y que CORS permita este origen.'
  }

  const { status, data } = error.response

  if (status === 401 || status === 403) {
    return 'No tienes permiso para esta operación. Revisa el token en .env.local.'
  }
  if (status === 404) {
    return 'El recurso solicitado no existe.'
  }
  if (status >= 500) {
    return 'El servidor falló al procesar la petición. Intenta de nuevo.'
  }

  return data?.detail ?? `La API respondió con el código ${status}.`
}