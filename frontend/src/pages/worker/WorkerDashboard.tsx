import Alert from '../../components/common/Alert'
import { StatusBadge } from '../../components/common/StatusBadge'
import { useWorkerDashboard } from '../../hooks/useDashboards'
import { useAuth } from '../../hooks/useAuth'

const WorkerDashboard = () => {
  const { user } = useAuth()
  const { data, isLoading, error } = useWorkerDashboard()

  return (
    <div className="card-grid">
      <div className="card">
        <h2>Agenda de hoy</h2>
        <p>
          {user?.first_name} {user?.last_name}
        </p>
      </div>
      {isLoading && <div className="card">Cargando agenda...</div>}
      {error && <Alert type="error" message="No se pudo cargar la agenda" />}
      {data && (
        <>
          <div className="card full-width">
            <h3>Próximas citas</h3>
            <ul className="list">
              {data.upcoming_appointments.map((appt) => (
                <li key={appt.id} className="list-row">
                  <div>
                    <div className="text-strong">{new Date(appt.start_datetime).toLocaleString()}</div>
                    <small>
                      Cliente #{appt.client_id} · Tratamiento #{appt.treatment_type_id}
                    </small>
                  </div>
                  <StatusBadge status={appt.status} />
                </li>
              ))}
              {data.upcoming_appointments.length === 0 && <li className="list-row">Sin próximas citas</li>}
            </ul>
          </div>
          <div className="card">
            <h3>Pacientes nuevos hoy</h3>
            <p className="metric-number">{data.new_clients_today}</p>
          </div>
        </>
      )}
    </div>
  )
}

export default WorkerDashboard
