export type Appointment = {
  id: number
  client_id: number
  worker_id: number
  treatment_type_id: number
  start_datetime: string
  end_datetime: string
  status: AppointmentStatus
  notes?: string
  created_by_user_id: number
}

export type AppointmentStatus =
  | 'pendiente'
  | 'confirmada'
  | 'realizada'
  | 'cancelada_paciente'
  | 'cancelada_clinica'
  | 'no_show'

export type AppointmentCreatePayload = {
  client_id: number
  worker_id: number
  treatment_type_id: number
  start_datetime: string
  end_datetime?: string
  status?: AppointmentStatus
  notes?: string
  created_by_user_id?: number
}

export type AppointmentUpdatePayload = Partial<Pick<AppointmentCreatePayload, 'start_datetime' | 'end_datetime' | 'status' | 'notes'>>

export type AppointmentReschedulePayload = {
  start_datetime: string
  end_datetime?: string
}
