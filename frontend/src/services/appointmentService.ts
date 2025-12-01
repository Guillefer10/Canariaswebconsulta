import { apiClient } from './apiClient'
import { Appointment } from '../types/appointment'

export const fetchAppointments = async (token?: string): Promise<Appointment[]> => {
  const { data } = await apiClient(token).get<Appointment[]>('/appointments')
  return data
}
