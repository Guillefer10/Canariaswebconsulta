import { useEffect, useState } from 'react'
import { fetchTreatments } from '../../services/treatmentService'
import { useAuth } from '../../hooks/useAuth'
import { TreatmentType } from '../../types/treatment'
import { DataTable } from '../../components/common/DataTable'

const TreatmentsPage = () => {
  const { token } = useAuth()
  const [treatments, setTreatments] = useState<TreatmentType[]>([])

  useEffect(() => {
    if (token) fetchTreatments(token).then(setTreatments)
  }, [token])

  return (
    <div className="card">
      <h3>Tratamientos</h3>
      <DataTable
        headers={["Nombre", "Duración (min)", "Precio", "Estado"]}
        rows={treatments.map((t) => (
          <tr key={t.id}>
            <td>{t.name}</td>
            <td>{t.estimated_duration_minutes}</td>
            <td>{t.base_price ?? '-'}</td>
            <td>{t.is_active ? 'Activo' : 'Inactivo'}</td>
          </tr>
        ))}
      />
    </div>
  )
}

export default TreatmentsPage
