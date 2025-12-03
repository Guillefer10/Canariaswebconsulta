import { apiClient } from './apiClient'
import { Appointment, AppointmentCreatePayload } from '../types/appointment'

export const fetchAppointments = async (token?: string): Promise<Appointment[]> => {
  const { data } = await apiClient(token).get<Appointment[]>('/appointments')
  return data
}

export const createAppointment = async (payload: AppointmentCreatePayload, token?: string): Promise<Appointment> => {
  const { data } = await apiClient(token).post<Appointment>('/appointments', payload)
  return data
}
