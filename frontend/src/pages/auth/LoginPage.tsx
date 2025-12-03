import { useState } from 'react'
import { useAuth } from '../../hooks/useAuth'
import { useNavigate } from 'react-router-dom'
import Alert from '../../components/common/Alert'

const LoginPage = () => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const { login } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await login({ email, password })
      navigate('/')
    } catch (err) {
      setError('Credenciales invalidas')
    }
  }

  return (
    <div className="auth-wrapper">
      <div className="auth-card">
        <h2>Bienvenido a Beauty Clinic</h2>
        <p className="helper-text">Accede con tu correo y contrasena para continuar.</p>
        <form onSubmit={handleSubmit}>
          <label>Email</label>
          <input
            type="email"
            value={email}
            placeholder="ejemplo@correo.com"
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <label>Contrasena</label>
          <input
            type="password"
            value={password}
            placeholder="********"
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          {error && <Alert type="error" message={error} />}
          <button className="button" type="submit">Entrar</button>
        </form>
        <p className="helper-text mt-1">
          Necesitas una cuenta? Pide acceso al administrador de la clinica.
        </p>
      </div>
    </div>
  )
}

export default LoginPage
