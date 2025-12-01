import { useEffect, useState } from 'react'
import { fetchClients } from '../../services/clientService'
import { useAuth } from '../../hooks/useAuth'
import { DataTable } from '../../components/common/DataTable'
import { ClientProfile } from '../../types/client'

const ClientsPage = () => {
  const { token } = useAuth()
  const [clients, setClients] = useState<ClientProfile[]>([])

  useEffect(() => {
    if (token) fetchClients(token).then(setClients)
  }, [token])

  return (
    <div className="card">
      <h3>Clientes</h3>
      <DataTable
        headers={["Nombre", "Teléfono", "DNI", "Alta"]}
        rows={clients.map((c) => (
          <tr key={c.id}>
            <td>{c.user?.first_name} {c.user?.last_name}</td>
            <td>{c.phone}</td>
            <td>{c.national_id}</td>
            <td>{c.join_date}</td>
          </tr>
        ))}
      />
    </div>
  )
}

export default ClientsPage
