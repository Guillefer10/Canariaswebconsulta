import { useEffect, useState } from 'react'
import { fetchUsers } from '../../services/userService'
import { useAuth } from '../../hooks/useAuth'
import { DataTable } from '../../components/common/DataTable'
import { User } from '../../types/user'

const UsersPage = () => {
  const { token } = useAuth()
  const [users, setUsers] = useState<User[]>([])

  useEffect(() => {
    if (token) {
      fetchUsers(token).then(setUsers)
    }
  }, [token])

  return (
    <div className="card">
      <h3>Usuarios</h3>
      <DataTable
        headers={["Nombre", "Email", "Rol", "Estado"]}
        rows={users.map((u) => (
          <tr key={u.id}>
            <td>{u.first_name} {u.last_name}</td>
            <td>{u.email}</td>
            <td>{u.role}</td>
            <td>{u.is_active ? 'Activo' : 'Inactivo'}</td>
          </tr>
        ))}
      />
    </div>
  )
}

export default UsersPage
