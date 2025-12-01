import { useAuth } from '../../hooks/useAuth'

const WorkerDashboard = () => {
  const { user } = useAuth()
  return (
    <div className="card-grid">
      <div className="card">Agenda del día para {user?.first_name}</div>
      <div className="card">Accesos rápidos a clientes y sesiones.</div>
    </div>
  )
}

export default WorkerDashboard
