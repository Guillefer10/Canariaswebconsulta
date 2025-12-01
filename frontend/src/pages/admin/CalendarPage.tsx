import { useEffect, useState } from 'react'
import { fetchAppointments } from '../../services/appointmentService'
import { useAuth } from '../../hooks/useAuth'
import { Appointment } from '../../types/appointment'
import { CalendarView } from '../../components/calendar/CalendarView'

const CalendarPage = () => {
  const { token } = useAuth()
  const [appointments, setAppointments] = useState<Appointment[]>([])

  useEffect(() => {
    if (token) fetchAppointments(token).then(setAppointments)
  }, [token])

  return <CalendarView appointments={appointments} onCreate={() => alert('Abrir formulario de cita')} />
}

export default CalendarPage
