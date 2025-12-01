export type Appointment = {
  id: number
  client_id: number
  worker_id: number
  treatment_type_id: number
  start_datetime: string
  end_datetime: string
  status: string
  notes?: string
  created_by_user_id: number
}
