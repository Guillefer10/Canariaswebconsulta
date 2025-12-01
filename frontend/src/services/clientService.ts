import { apiClient } from './apiClient'
import { ClientProfile } from '../types/client'

export const fetchClients = async (token?: string): Promise<ClientProfile[]> => {
  const { data } = await apiClient(token).get<ClientProfile[]>('/clients')
  return data
}

export const fetchClient = async (id: number, token?: string): Promise<ClientProfile> => {
  const { data } = await apiClient(token).get<ClientProfile>(`/clients/${id}`)
  return data
}
