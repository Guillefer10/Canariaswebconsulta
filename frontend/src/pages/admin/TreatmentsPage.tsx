import { useEffect, useState } from 'react'
import { fetchTreatments } from '../../services/treatmentService'
import { useAuth } from '../../hooks/useAuth'
import { TreatmentType } from '../../types/treatment'
import { DataTable } from '../../components/common/DataTable'
import EmptyState from '../../components/common/EmptyState'

const TreatmentsPage = () => {
  const { token } = useAuth()
  const [treatments, setTreatments] = useState<TreatmentType[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const loadTreatments = () => {
    if (!token) return
    setLoading(true)
    fetchTreatments(token)
      .then((data) => {
        setTreatments(data)
        setError(null)
      })
      .catch(() => setError('No se pudieron cargar los tratamientos'))
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    loadTreatments()
  }, [token])

  return (
    <div className="card">
      <div className="card-header">
        <div>
          <h3>Tratamientos</h3>
          <p className="muted">Define catalogo, duracion y disponibilidad</p>
        </div>
        <div className="table-actions">
          <button className="button">Nuevo tratamiento</button>
        </div>
      </div>

      {loading && <p className="muted">Cargando tratamientos...</p>}

      {!loading && error && (
        <EmptyState
          title="No se pudo cargar la lista"
          description={error}
          action={<button className="button secondary" onClick={loadTreatments}>Reintentar</button>}
        />
      )}

      {!loading && !error && treatments.length === 0 && (
        <EmptyState
          title="Aun no hay tratamientos"
          description="Crea tu catalogo con nombre, duracion y precio."
          action={<button className="button">Nuevo tratamiento</button>}
        />
      )}

      {!loading && !error && treatments.length > 0 && (
        <DataTable
          headers={["Nombre", "Duracion (min)", "Precio", "Estado", "Acciones"]}
          rows={treatments.map((t) => (
            <tr key={t.id}>
              <td>{t.name}</td>
              <td>{t.estimated_duration_minutes}</td>
              <td>{t.base_price ?? '-'}</td>
              <td>
                <span className={`badge ${t.is_active ? 'confirmed' : 'cancelled'}`}>
                  {t.is_active ? 'Activo' : 'Inactivo'}
                </span>
              </td>
              <td>
                <div className="table-actions">
                  <button className="button ghost small" type="button">Editar</button>
                  <button className="button ghost small" type="button">{t.is_active ? 'Desactivar' : 'Activar'}</button>
                </div>
              </td>
            </tr>
          ))}
        />
      )}
    </div>
  )
}

export default TreatmentsPage
