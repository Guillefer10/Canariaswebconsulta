import { useEffect, useState } from 'react'
import { fetchClients } from '../../services/clientService'
import { useAuth } from '../../hooks/useAuth'
import { DataTable } from '../../components/common/DataTable'
import EmptyState from '../../components/common/EmptyState'
import { ClientProfile } from '../../types/client'

const ClientsPage = () => {
  const { token } = useAuth()
  const [clients, setClients] = useState<ClientProfile[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const loadClients = () => {
    if (!token) return
    setLoading(true)
    fetchClients(token)
      .then((data) => {
        setClients(data)
        setError(null)
      })
      .catch(() => setError('No se pudieron cargar los clientes'))
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    loadClients()
  }, [token])

  return (
    <div className="card">
      <div className="card-header">
        <div>
          <h3>Clientes</h3>
          <p className="muted">Crea y edita perfiles desde aqui</p>
        </div>
        <button className="button">Crear cliente</button>
      </div>

      {loading && <p className="muted">Cargando clientes...</p>}

      {!loading && error && (
        <EmptyState
          title="No se pudo cargar la lista"
          description={error}
          action={<button className="button secondary" onClick={loadClients}>Reintentar</button>}
        />
      )}

      {!loading && !error && clients.length === 0 && (
        <EmptyState
          title="No hay clientes aun"
          description="Cuando crees uno veras aqui su perfil y contacto."
          action={<button className="button">Crear cliente</button>}
        />
      )}

      {!loading && !error && clients.length > 0 && (
        <DataTable
          headers={["Nombre", "Telefono", "DNI", "Alta", "Acciones"]}
          rows={clients.map((c) => (
            <tr key={c.id}>
              <td>{c.user?.first_name} {c.user?.last_name}</td>
              <td>{c.phone}</td>
              <td>{c.national_id}</td>
              <td>{c.join_date}</td>
              <td>
                <div className="table-actions">
                  <button className="button ghost small" type="button">Editar</button>
                  <button className="button ghost small" type="button">Ver perfil</button>
                </div>
              </td>
            </tr>
          ))}
        />
      )}
    </div>
  )
}

export default ClientsPage
