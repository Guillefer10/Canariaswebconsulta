import axios from 'axios'

const baseURL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api/v1'

export const apiClient = (token?: string) => {
  const instance = axios.create({
    baseURL,
  })
  instance.interceptors.request.use((config) => {
    if (token) {
      config.headers = config.headers ?? {}
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  })
  instance.interceptors.response.use(
    (response) => response,
    (error) => {
      if (error.response?.status === 401) {
        error.message = 'Sesión caducada o credenciales inválidas'
      }
      return Promise.reject(error)
    },
  )
  return instance
}
