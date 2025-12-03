import { useEffect, useState } from 'react'
import { fetchAppointments } from '../../services/appointmentService'
import { useAuth } from '../../hooks/useAuth'
import { Appointment } from '../../types/appointment'
import EmptyState from '../../components/common/EmptyState'

const ClientAppointmentsPage = () => {
  const { token } = useAuth()
  const [appointments, setAppointments] = useState<Appointment[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const loadAppointments = () => {
    if (!token) return
    setLoading(true)
    fetchAppointments(token)
      .then((data) => {
        setAppointments(data)
        setError(null)
      })
      .catch(() => setError('No se pudieron cargar tus citas'))
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    loadAppointments()
  }, [token])

  return (
    <div className="card">
      <div className="card-header">
        <div>
          <h3>Mis citas</h3>
          <p className="muted">Consulta el estado de tus citas programadas</p>
        </div>
        <button className="button ghost" type="button" onClick={() => alert('Solicitar nueva cita')}>
          Pedir cita
        </button>
      </div>

      {loading && <p className="muted">Cargando citas...</p>}

      {!loading && error && (
        <EmptyState
          title="No pudimos cargar tus citas"
          description={error}
          action={<button className="button" onClick={loadAppointments}>Reintentar</button>}
        />
      )}

      {!loading && !error && appointments.length === 0 && (
        <EmptyState
          title="No tienes citas aun"
          description="Cuando reserves una cita aparecera aqui."
          action={<button className="button ghost" onClick={() => alert('Solicitar nueva cita')}>Pedir cita</button>}
        />
      )}

      {!loading && !error && appointments.length > 0 && (
        <div className="list-block">
          {appointments.map((a) => (
            <div className="list-card" key={a.id}>
              <div>
                <div className="calendar-slot-time">{new Date(a.start_datetime).toLocaleString()}</div>
                <div className="muted">Tratamiento #{a.treatment_type_id}</div>
              </div>
              <span className={`badge ${a.status}`}>{a.status}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default ClientAppointmentsPage
