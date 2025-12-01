import { useMemo } from 'react'
import { apiClient } from '../services/apiClient'
import { useAuth } from './useAuth'

export const useApi = () => {
  const { token } = useAuth()
  return useMemo(() => apiClient(token ?? undefined), [token])
}
