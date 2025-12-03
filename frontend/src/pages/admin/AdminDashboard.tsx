import Alert from '../../components/common/Alert'
import { useAdminDashboard } from '../../hooks/useDashboards'
import { useAuth } from '../../hooks/useAuth'

const AdminDashboard = () => {
  const { user } = useAuth()
  const { data, isLoading, error } = useAdminDashboard()

  return (
    <div className="card-grid">
      <div className="card">
        <h2>Hola, {user?.first_name || 'Admin'}</h2>
        <p>Resumen operativo del día</p>
      </div>
      {isLoading && <div className="card">Cargando métricas...</div>}
      {error && <Alert type="error" message="No se pudieron cargar las métricas" />}
      {data && (
        <>
          <div className="card">
            <h3>Citas hoy</h3>
            <p className="metric-number">{data.appointments_today}</p>
            <small>Total de citas programadas para hoy</small>
          </div>
          <div className="card">
            <h3>Cancelaciones hoy</h3>
            <p className="metric-number">{data.cancelled_today}</p>
            <small>Incluye cancelación paciente/clinica</small>
          </div>
          <div className="card full-width">
            <h3>Ocupación por profesional</h3>
            <ul className="list">
              {data.occupancy_by_worker.map((item) => (
                <li key={item.worker_id} className="list-row">
                  <span>{item.worker_name}</span>
                  <span className="badge">{item.appointments_today} citas</span>
                </li>
              ))}
            </ul>
          </div>
        </>
      )}
    </div>
  )
}

export default AdminDashboard
