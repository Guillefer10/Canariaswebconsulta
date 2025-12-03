import { AppointmentStatus } from '../../types/appointment'

const statusCopy: Record<AppointmentStatus, string> = {
  pendiente: 'Pendiente',
  confirmada: 'Confirmada',
  realizada: 'Realizada',
  cancelada_paciente: 'Cancelada paciente',
  cancelada_clinica: 'Cancelada clínica',
  no_show: 'No show',
}

const statusClass: Record<AppointmentStatus, string> = {
  pendiente: 'warning',
  confirmada: 'info',
  realizada: 'success',
  cancelada_paciente: 'neutral',
  cancelada_clinica: 'neutral',
  no_show: 'error',
}

type Props = {
  status: AppointmentStatus
}

export const StatusBadge = ({ status }: Props) => {
  const label = statusCopy[status] ?? status
  const variant = statusClass[status] ?? 'info'
  return <span className={`badge ${variant}`}>{label}</span>
}
