import { apiClient } from './apiClient'
import { AdminDashboardMetrics, ClientDashboardMetrics, WorkerDashboardMetrics } from '../types/dashboard'

export const fetchAdminDashboard = async (token?: string): Promise<AdminDashboardMetrics> => {
  const { data } = await apiClient(token).get<AdminDashboardMetrics>('/dashboards/admin')
  return data
}

export const fetchWorkerDashboard = async (token?: string): Promise<WorkerDashboardMetrics> => {
  const { data } = await apiClient(token).get<WorkerDashboardMetrics>('/dashboards/worker')
  return data
}

export const fetchClientDashboard = async (token?: string): Promise<ClientDashboardMetrics> => {
  const { data } = await apiClient(token).get<ClientDashboardMetrics>('/dashboards/client')
  return data
}
