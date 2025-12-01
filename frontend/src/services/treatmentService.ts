import { apiClient } from './apiClient'
import { TreatmentType } from '../types/treatment'

export const fetchTreatments = async (token?: string): Promise<TreatmentType[]> => {
  const { data } = await apiClient(token).get<TreatmentType[]>('/treatments')
  return data
}
