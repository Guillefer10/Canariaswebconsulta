import Alert from '../../components/common/Alert'
import { StatusBadge } from '../../components/common/StatusBadge'
import { useClientDashboard } from '../../hooks/useDashboards'

const ClientDashboard = () => {
  const { data, isLoading, error } = useClientDashboard()

  return (
    <div className="card-grid">
      {isLoading && <div className="card">Cargando tu información...</div>}
      {error && <Alert type="error" message="No se pudo cargar tu panel" />}
      {data && (
        <>
          <div className="card">
            <h3>Tu próxima cita</h3>
            {data.next_appointment ? (
              <>
                <div className="text-strong">{new Date(data.next_appointment.start_datetime).toLocaleString()}</div>
                <StatusBadge status={data.next_appointment.status} />
              </>
            ) : (
              <p>No tienes citas programadas.</p>
            )}
          </div>
          <div className="card full-width">
            <h3>Histórico reciente</h3>
            <ul className="list">
              {data.last_visits.map((visit) => (
                <li key={visit.id} className="list-row">
                  <div>
                    <div className="text-strong">{new Date(visit.start_datetime).toLocaleDateString()}</div>
                    <StatusBadge status={visit.status} />
                  </div>
                </li>
              ))}
              {data.last_visits.length === 0 && <li className="list-row">Aún no hay historial.</li>}
            </ul>
          </div>
        </>
      )}
    </div>
  )
}

export default ClientDashboard
