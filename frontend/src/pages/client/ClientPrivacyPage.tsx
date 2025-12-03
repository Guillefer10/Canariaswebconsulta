import { useEffect, useState } from 'react'
import Alert from '../../components/common/Alert'
import { Toast } from '../../components/common/Toast'
import { useAuth } from '../../hooks/useAuth'
import { useCreateConsent, useMyConsents } from '../../hooks/useConsents'
import { fetchClientMe } from '../../services/clientService'
import { ConsentType } from '../../types/consent'
import { ClientProfile } from '../../types/client'

const CONSENT_TEXT_VERSION = 'v1.0'

const ClientPrivacyPage = () => {
  const { token } = useAuth()
  const { data: consents, isLoading, error } = useMyConsents()
  const [profile, setProfile] = useState<ClientProfile | null>(null)
  const [profileError, setProfileError] = useState<string | null>(null)
  const [loadingProfile, setLoadingProfile] = useState(true)
  const [toast, setToast] = useState<{ type: 'success' | 'error' | 'info'; message: string } | null>(null)

  const createConsent = useCreateConsent(profile?.id ?? 0)

  useEffect(() => {
    if (!token) return
    setLoadingProfile(true)
    fetchClientMe(token)
      .then((p) => {
        setProfile(p)
        setProfileError(null)
      })
      .catch(() => setProfileError('No pudimos cargar tus datos'))
      .finally(() => setLoadingProfile(false))
  }, [token])

  const hasConsent = (type: ConsentType) => consents?.some((c) => c.consent_type === type)

  const registerConsent = (type: ConsentType) => {
    if (!profile) return
    createConsent.mutate(
      {
        consent_type: type,
        text_version: CONSENT_TEXT_VERSION,
        ip_address: '',
        user_agent: navigator.userAgent,
        client_id: profile.id,
      },
      {
        onSuccess: () => setToast({ type: 'success', message: 'Consentimiento registrado' }),
        onError: () => setToast({ type: 'error', message: 'No pudimos registrar tu consentimiento' }),
      },
    )
  }

  return (
    <div className="card">
      <h3>Privacidad y consentimientos</h3>
      {(error || profileError) && <Alert type="error" message="No pudimos cargar tu información de privacidad" />}
      {isLoading || loadingProfile ? (
        <p>Cargando...</p>
      ) : (
        <>
          <section className="section">
            <h4>Política de privacidad</h4>
            <p>Versión: {CONSENT_TEXT_VERSION}</p>
            <p>
              Recogemos y tratamos tus datos para la prestación del servicio clínico. Puedes solicitar la revocación en
              cualquier momento.
            </p>
            {hasConsent('privacy_policy') ? (
              <span className="badge success">Aceptado</span>
            ) : (
              <button className="button primary" disabled={createConsent.isPending} onClick={() => registerConsent('privacy_policy')}>
                Aceptar
              </button>
            )}
          </section>
          <section className="section">
            <h4>Consentimiento de datos de salud</h4>
            <p>Versión: {CONSENT_TEXT_VERSION}</p>
            <p>
              Necesitamos tu autorización para almacenar y usar datos de salud con fines asistenciales y de seguimiento clínico.
            </p>
            {hasConsent('health_data') ? (
              <span className="badge success">Aceptado</span>
            ) : (
              <button className="button primary" disabled={createConsent.isPending} onClick={() => registerConsent('health_data')}>
                Aceptar
              </button>
            )}
          </section>
          <section className="section">
            <h4>Histórico</h4>
            {consents && consents.length > 0 ? (
              <ul className="list">
                {consents.map((c) => (
                  <li key={c.id} className="list-row">
                    <div>
                      <div className="text-strong">{c.consent_type}</div>
                      <small>Versión {c.text_version}</small>
                    </div>
                    <span>{new Date(c.accepted_at).toLocaleString()}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p>Aún no has registrado consentimientos.</p>
            )}
          </section>
        </>
      )}
      {toast && <Toast type={toast.type} message={toast.message} />}
    </div>
  )
}

export default ClientPrivacyPage
