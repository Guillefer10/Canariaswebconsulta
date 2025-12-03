import { useEffect, useState } from 'react'
import { fetchClientMe } from '../../services/clientService'
import { useAuth } from '../../hooks/useAuth'
import { ClientProfile } from '../../types/client'
import Alert from '../../components/common/Alert'

const ClientProfilePage = () => {
  const { token } = useAuth()
  const [profile, setProfile] = useState<ClientProfile | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const loadProfile = () => {
    if (!token) return
    setLoading(true)
    fetchClientMe(token)
      .then((p) => {
        setProfile(p)
        setError(null)
      })
      .catch(() => setError('No pudimos cargar tu perfil'))
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    loadProfile()
  }, [token])

  if (loading) return <div className="card">Cargando perfil...</div>

  if (error) {
    return (
      <div className="card">
        <div className="card-header">
          <h3>Mis datos</h3>
        </div>
        <Alert type="error" message={error} />
        <button className="button secondary" onClick={loadProfile}>Reintentar</button>
      </div>
    )
  }

  if (!profile) return null

  return (
    <div className="card">
      <h3>Mis datos</h3>
      <p>Telefono: {profile.phone}</p>
      <p>DNI: {profile.national_id}</p>
      <p>Fecha de nacimiento: {profile.birth_date}</p>
      <p>Consentimiento: {profile.consent_data ? 'Si' : 'No'}</p>
    </div>
  )
}

export default ClientProfilePage
