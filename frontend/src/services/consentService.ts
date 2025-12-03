import { apiClient } from './apiClient'
import { ConsentRecord, ConsentRecordCreate } from '../types/consent'

export const fetchClientConsents = async (clientId: number, token?: string): Promise<ConsentRecord[]> => {
  const { data } = await apiClient(token).get<ConsentRecord[]>(`/consents/clients/${clientId}`)
  return data
}

export const fetchMyConsents = async (token?: string): Promise<ConsentRecord[]> => {
  const { data } = await apiClient(token).get<ConsentRecord[]>('/consents/me')
  return data
}

export const createConsent = async (
  clientId: number,
  payload: ConsentRecordCreate,
  token?: string,
): Promise<ConsentRecord> => {
  const { data } = await apiClient(token).post<ConsentRecord>(`/consents/clients/${clientId}`, payload)
  return data
}
