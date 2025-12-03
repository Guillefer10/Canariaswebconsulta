import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import {
  cancelAppointment,
  changeAppointmentStatus,
  createAppointment,
  fetchAppointments,
  rescheduleAppointment,
  updateAppointment,
} from '../services/appointmentService'
import {
  Appointment,
  AppointmentCreatePayload,
  AppointmentReschedulePayload,
  AppointmentStatus,
  AppointmentUpdatePayload,
} from '../types/appointment'
import { useAuth } from './useAuth'

const queryKey = ['appointments']

export const useAppointments = () => {
  const { token } = useAuth()
  return useQuery<Appointment[]>({
    queryKey,
    queryFn: () => fetchAppointments(token ?? undefined),
    enabled: !!token,
  })
}

export const useCreateAppointment = () => {
  const { token } = useAuth()
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: AppointmentCreatePayload) => createAppointment(payload, token ?? undefined),
    onSuccess: () => queryClient.invalidateQueries({ queryKey }),
  })
}

export const useUpdateAppointment = () => {
  const { token } = useAuth()
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ id, payload }: { id: number; payload: AppointmentUpdatePayload }) =>
      updateAppointment(id, payload, token ?? undefined),
    onSuccess: () => queryClient.invalidateQueries({ queryKey }),
  })
}

export const useChangeAppointmentStatus = () => {
  const { token } = useAuth()
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ id, status }: { id: number; status: AppointmentStatus }) =>
      changeAppointmentStatus(id, status, token ?? undefined),
    onSuccess: () => queryClient.invalidateQueries({ queryKey }),
  })
}

export const useRescheduleAppointment = () => {
  const { token } = useAuth()
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ id, payload }: { id: number; payload: AppointmentReschedulePayload }) =>
      rescheduleAppointment(id, payload, token ?? undefined),
    onSuccess: () => queryClient.invalidateQueries({ queryKey }),
  })
}

export const useCancelAppointment = () => {
  const { token } = useAuth()
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (id: number) => cancelAppointment(id, token ?? undefined),
    onSuccess: () => queryClient.invalidateQueries({ queryKey }),
  })
}
