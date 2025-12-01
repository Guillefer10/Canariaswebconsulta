import { useEffect, useState } from 'react'
import { fetchClients } from '../../services/clientService'
import { useAuth } from '../../hooks/useAuth'
import { ClientProfile } from '../../types/client'

const ClientProfilePage = () => {
  const { token, user } = useAuth()
  const [profile, setProfile] = useState<ClientProfile | null>(null)

  useEffect(() => {
    if (token && user) {
      fetchClients(token).then((profiles) => {
        const match = profiles.find((p) => p.user_id === user.id)
        if (match) setProfile(match)
      })
    }
  }, [token, user])

  if (!profile) return <div className="card">Cargando perfil...</div>

  return (
    <div className="card">
      <h3>Mis datos</h3>
      <p>Teléfono: {profile.phone}</p>
      <p>DNI: {profile.national_id}</p>
      <p>Fecha de nacimiento: {profile.birth_date}</p>
      <p>Consentimiento: {profile.consent_data ? 'Sí' : 'No'}</p>
    </div>
  )
}

export default ClientProfilePage
