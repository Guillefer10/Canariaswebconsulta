import { useEffect, useMemo, useState } from 'react'
import { Appointment, AppointmentCreatePayload } from '../../types/appointment'
import { ClientProfile } from '../../types/client'
import { TreatmentType } from '../../types/treatment'
import { useAuth } from '../../hooks/useAuth'
import { CalendarView } from '../../components/calendar/CalendarView'
import { AppointmentForm } from '../../components/forms/AppointmentForm'
import { createAppointment, fetchAppointments } from '../../services/appointmentService'
import { fetchClients } from '../../services/clientService'
import { fetchTreatments } from '../../services/treatmentService'
import EmptyState from '../../components/common/EmptyState'
import { User } from '../../types/user'

const WorkerAgendaPage = () => {
  const { token, user } = useAuth()
  const [appointments, setAppointments] = useState<Appointment[]>([])
  const [clients, setClients] = useState<ClientProfile[]>([])
  const [treatments, setTreatments] = useState<TreatmentType[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [showForm, setShowForm] = useState(false)
  const [saving, setSaving] = useState(false)

  const workers: User[] = useMemo(() => (user ? [user] : []), [user])

  const loadData = () => {
    if (!token) return
    setLoading(true)
    Promise.all([fetchAppointments(token), fetchClients(token), fetchTreatments(token)])
      .then(([apts, clientList, treatmentList]) => {
        setAppointments(apts)
        setClients(clientList)
        setTreatments(treatmentList)
        setError(null)
      })
      .catch(() => setError('No se pudo cargar la agenda'))
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
      setError(null)
    } catch (err) {
      setError('No se pudo crear la cita')
    } finally {
      setSaving(false)
    }
  }

  if (loading) return <p className="muted">Cargando agenda...</p>

  if (error) {
    return (
      <EmptyState
        title="Error al cargar la agenda"
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
              <h3>Nueva cita</h3>
              <p className="muted">Completa los datos y guarda para agendar</p>
            </div>
            <button className="button ghost" onClick={() => setShowForm(false)}>Cerrar</button>
          </div>
          <AppointmentForm
            clients={clients}
            workers={workers}
            treatments={treatments}
            defaultWorkerId={user?.id}
            onSubmit={handleCreate}
            onCancel={() => setShowForm(false)}
          />
          {saving && <p className="muted">Guardando cita...</p>}
        </div>
      )}
    </>
  )
}

export default WorkerAgendaPage
