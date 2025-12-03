import { Appointment } from './appointment'

export type AdminDashboardMetrics = {
  appointments_today: number
  cancelled_today: number
  occupancy_by_worker: {
    worker_id: number
    worker_name: string
    appointments_today: number
  }[]
}

export type WorkerDashboardMetrics = {
  upcoming_appointments: Appointment[]
  new_clients_today: number
}

export type ClientDashboardMetrics = {
  next_appointment: Appointment | null
  last_visits: Appointment[]
}
