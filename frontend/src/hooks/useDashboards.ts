import { useQuery } from '@tanstack/react-query'
import { fetchAdminDashboard, fetchClientDashboard, fetchWorkerDashboard } from '../services/dashboardService'
import { useAuth } from './useAuth'

export const useAdminDashboard = () => {
  const { token } = useAuth()
  return useQuery({
    queryKey: ['dashboard', 'admin'],
    queryFn: () => fetchAdminDashboard(token ?? undefined),
    enabled: !!token,
  })
}

export const useWorkerDashboard = () => {
  const { token } = useAuth()
  return useQuery({
    queryKey: ['dashboard', 'worker'],
    queryFn: () => fetchWorkerDashboard(token ?? undefined),
    enabled: !!token,
  })
}

export const useClientDashboard = () => {
  const { token } = useAuth()
  return useQuery({
    queryKey: ['dashboard', 'client'],
    queryFn: () => fetchClientDashboard(token ?? undefined),
    enabled: !!token,
  })
}
