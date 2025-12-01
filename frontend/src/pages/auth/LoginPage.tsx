import { useState } from 'react'
import { useAuth } from '../../hooks/useAuth'
import { useNavigate } from 'react-router-dom'

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
      setError('Credenciales inválidas')
    }
  }

  return (
    <div className="auth-wrapper">
      <div className="auth-card">
        <h2>Bienvenido a Beauty Clinic</h2>
        <p className="helper-text">Accede con tu correo y contraseña para continuar.</p>
        <form onSubmit={handleSubmit}>
          <label>Email</label>
          <input
            type="email"
            value={email}
            placeholder="ejemplo@correo.com"
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <label>Contraseña</label>
          <input
            type="password"
            value={password}
            placeholder="••••••••"
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          {error && <p style={{ color: '#dc2626', marginTop: 0 }}>{error}</p>}
          <button className="button" type="submit">Entrar</button>
        </form>
        <p className="helper-text" style={{ marginTop: '1rem' }}>
          ¿Necesitas una cuenta? Pide acceso al administrador de la clínica.
        </p>
      </div>
    </div>
  )
}

export default LoginPage
