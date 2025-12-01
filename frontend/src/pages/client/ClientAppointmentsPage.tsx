import { useEffect, useState } from 'react'
import { fetchAppointments } from '../../services/appointmentService'
import { useAuth } from '../../hooks/useAuth'
import { Appointment } from '../../types/appointment'

const ClientAppointmentsPage = () => {
  const { token } = useAuth()
  const [appointments, setAppointments] = useState<Appointment[]>([])

  useEffect(() => {
    if (token) fetchAppointments(token).then(setAppointments)
  }, [token])

  return (
    <div className="card">
      <h3>Mis citas</h3>
      <ul>
        {appointments.map((a) => (
          <li key={a.id}>{new Date(a.start_datetime).toLocaleString()} - {a.status}</li>
        ))}
      </ul>
    </div>
  )
}

export default ClientAppointmentsPage
