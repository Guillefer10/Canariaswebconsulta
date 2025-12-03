import { useEffect, useState } from 'react'
import { fetchUsers } from '../../services/userService'
import { useAuth } from '../../hooks/useAuth'
import { DataTable } from '../../components/common/DataTable'
import EmptyState from '../../components/common/EmptyState'
import { User } from '../../types/user'

const UsersPage = () => {
  const { token } = useAuth()
  const [users, setUsers] = useState<User[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const loadUsers = () => {
    if (!token) return
    setLoading(true)
    fetchUsers(token)
      .then((data) => {
        setUsers(data)
        setError(null)
      })
      .catch(() => setError('No se pudieron cargar los usuarios'))
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    loadUsers()
  }, [token])

  return (
    <div className="card">
      <div className="card-header">
        <div>
          <h3>Usuarios</h3>
          <p className="muted">Gestiona los accesos del equipo</p>
        </div>
        <button className="button">Crear usuario</button>
      </div>

      {loading && <p className="muted">Cargando usuarios...</p>}

      {!loading && error && (
        <EmptyState
          title="No se pudo cargar la lista"
          description={error}
          action={<button className="button secondary" onClick={loadUsers}>Reintentar</button>}
        />
      )}

      {!loading && !error && users.length === 0 && (
        <EmptyState
          title="Aun no hay usuarios"
          description="Crea la primera cuenta para tu equipo."
          action={<button className="button">Crear usuario</button>}
        />
      )}

      {!loading && !error && users.length > 0 && (
        <DataTable
          headers={["Nombre", "Email", "Rol", "Estado", "Acciones"]}
          rows={users.map((u) => (
            <tr key={u.id}>
              <td>{u.first_name} {u.last_name}</td>
              <td>{u.email}</td>
              <td className="pill">{u.role}</td>
              <td>
                <span className={`badge ${u.is_active ? 'confirmed' : 'cancelled'}`}>
                  {u.is_active ? 'Activo' : 'Inactivo'}
                </span>
              </td>
              <td>
                <div className="table-actions">
                  <button className="button ghost small" type="button">Editar</button>
                  <button className="button ghost small" type="button">{u.is_active ? 'Desactivar' : 'Activar'}</button>
                  <button className="button ghost small danger" type="button">Resetear password</button>
                </div>
              </td>
            </tr>
          ))}
        />
      )}
    </div>
  )
}

export default UsersPage
