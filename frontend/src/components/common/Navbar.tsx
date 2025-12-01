import { useAuth } from '../../hooks/useAuth'
import { useTheme } from '../../hooks/useTheme'

export const Navbar = ({ user }: { user: { first_name?: string; role: string } }) => {
  const { logout } = useAuth()
  const { theme, toggleTheme } = useTheme()
  return (
    <div className="navbar">
      <div className="navbar-left">
        <div className="app-brand">Beauty Clinic</div>
        <span className="muted">Panel de control</span>
      </div>
      <div className="navbar-right">
        <button className="button ghost" type="button" onClick={toggleTheme} aria-label="Cambiar modo de color">
          {theme === 'light' ? '🌙 Modo nocturno' : '☀️ Modo claro'}
        </button>
        <span className="chip">{user.first_name || 'Usuario'} · {user.role}</span>
        <button className="button secondary" onClick={logout}>Cerrar sesión</button>
      </div>
    </div>
  )
}
