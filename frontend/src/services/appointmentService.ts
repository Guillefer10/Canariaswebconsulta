import { apiClient } from './apiClient'
import {
  Appointment,
  AppointmentCreatePayload,
  AppointmentReschedulePayload,
  AppointmentStatus,
  AppointmentUpdatePayload,
} from '../types/appointment'

export const fetchAppointments = async (token?: string): Promise<Appointment[]> => {
  const { data } = await apiClient(token).get<Appointment[]>('/appointments')
  return data
}

export const createAppointment = async (payload: AppointmentCreatePayload, token?: string): Promise<Appointment> => {
  const { data } = await apiClient(token).post<Appointment>('/appointments', payload)
  return data
}

export const updateAppointment = async (
  appointmentId: number,
  payload: AppointmentUpdatePayload,
  token?: string,
): Promise<Appointment> => {
  const { data } = await apiClient(token).put<Appointment>(`/appointments/${appointmentId}`, payload)
  return data
}

export const changeAppointmentStatus = async (
  appointmentId: number,
  status: AppointmentStatus,
  token?: string,
): Promise<Appointment> => {
  const { data } = await apiClient(token).patch<Appointment>(`/appointments/${appointmentId}/status`, { status })
  return data
}

export const rescheduleAppointment = async (
  appointmentId: number,
  payload: AppointmentReschedulePayload,
  token?: string,
): Promise<Appointment> => {
  const { data } = await apiClient(token).patch<Appointment>(`/appointments/${appointmentId}/reschedule`, payload)
  return data
}

export const cancelAppointment = async (appointmentId: number, token?: string): Promise<Appointment> => {
  const { data } = await apiClient(token).patch<Appointment>(`/appointments/${appointmentId}/cancel`)
  return data
}
