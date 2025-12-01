import { useAuth } from '../../hooks/useAuth'

const AdminDashboard = () => {
  const { user } = useAuth()
  return (
    <div className="card-grid">
      <div className="card">Bienvenido, {user?.first_name || 'Admin'}</div>
      <div className="card">Métricas rápidas: citas, clientes, tratamientos.</div>
    </div>
  )
}

export default AdminDashboard
