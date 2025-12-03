import { useEffect, useState } from 'react'
import { Appointment, AppointmentCreatePayload } from '../../types/appointment'
import { ClientProfile } from '../../types/client'
import { TreatmentType } from '../../types/treatment'
import { User } from '../../types/user'
import { useAuth } from '../../hooks/useAuth'
import { CalendarView } from '../../components/calendar/CalendarView'
import { AppointmentForm } from '../../components/forms/AppointmentForm'
import { createAppointment, fetchAppointments } from '../../services/appointmentService'
import { fetchClients } from '../../services/clientService'
import { fetchTreatments } from '../../services/treatmentService'
import { fetchUsers } from '../../services/userService'
import EmptyState from '../../components/common/EmptyState'

const CalendarPage = () => {
  const { token } = useAuth()
  const [appointments, setAppointments] = useState<Appointment[]>([])
  const [clients, setClients] = useState<ClientProfile[]>([])
  const [treatments, setTreatments] = useState<TreatmentType[]>([])
  const [workers, setWorkers] = useState<User[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [showForm, setShowForm] = useState(false)
  const [saving, setSaving] = useState(false)

  const loadData = () => {
    if (!token) return
    setLoading(true)
    Promise.all([fetchAppointments(token), fetchClients(token), fetchTreatments(token), fetchUsers(token)])
      .then(([apts, clientList, treatmentList, users]) => {
        setAppointments(apts)
        setClients(clientList)
        setTreatments(treatmentList)
        setWorkers(users.filter((u) => u.role === 'worker'))
        setError(null)
      })
      .catch(() => setError('No se pudo cargar el calendario'))
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    loadData()
  }, [token])

  const handleCreate = async (payload: AppointmentCreatePayload) => {
    if (!token) return
    try {
      setSaving(true)
      const newAppointment = await createAppointment(payload, token)
      setAppointments((prev) => [...prev, newAppointment])
      setShowForm(false)
    } catch (err) {
      setError('No se pudo crear la cita')
    } finally {
      setSaving(false)
    }
  }

  if (loading) return <p className="muted">Cargando calendario...</p>

  if (error) {
    return (
      <EmptyState
        title="Error al cargar el calendario"
        description={error}
        action={<button className="button" onClick={loadData}>Reintentar</button>}
      />
    )
  }

  return (
    <>
      <CalendarView appointments={appointments} onCreate={() => setShowForm(true)} />

      {showForm && (
        <div className="card">
          <div className="card-header">
            <div>
              <h3>Crear cita</h3>
              <p className="muted">Rellena los datos para agendar al cliente</p>
            </div>
            <button className="button ghost" onClick={() => setShowForm(false)}>Cerrar</button>
          </div>
          <AppointmentForm
            clients={clients}
            workers={workers}
            treatments={treatments}
            onSubmit={handleCreate}
            onCancel={() => setShowForm(false)}
          />
          {saving && <p className="muted">Guardando cita...</p>}
        </div>
      )}
    </>
  )
}

export default CalendarPage
