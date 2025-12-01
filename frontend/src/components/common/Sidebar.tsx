import { NavLink } from 'react-router-dom'

const adminLinks = [
  { to: '/admin', label: 'Dashboard' },
  { to: '/admin/users', label: 'Usuarios' },
  { to: '/admin/clients', label: 'Clientes' },
  { to: '/admin/treatments', label: 'Tratamientos' },
  { to: '/admin/calendar', label: 'Calendario' },
]

const workerLinks = [
  { to: '/worker', label: 'Dashboard' },
  { to: '/worker/agenda', label: 'Mi agenda' },
]

const clientLinks = [
  { to: '/client', label: 'Dashboard' },
  { to: '/client/profile', label: 'Mis datos' },
  { to: '/client/appointments', label: 'Mis citas' },
  { to: '/client/treatments', label: 'Mis tratamientos' },
]

export const Sidebar = ({ role }: { role: string }) => {
  const links = role === 'admin' ? adminLinks : role === 'worker' ? workerLinks : clientLinks
  return (
    <aside className="sidebar">
      <div className="sidebar-heading">Navegación</div>
      <nav>
        {links.map((l) => (
          <NavLink
            key={l.to}
            to={l.to}
            className={({ isActive }) => (isActive ? 'active' : '')}
            end
          >
            {l.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  )
}
