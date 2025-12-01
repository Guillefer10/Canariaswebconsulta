import { ReactNode } from 'react'
import { Sidebar } from '../common/Sidebar'
import { Navbar } from '../common/Navbar'
import { useAuth } from '../../hooks/useAuth'

export const MainLayout = ({ children }: { children: ReactNode }) => {
  const { user } = useAuth()
  if (!user) return <>{children}</>
  return (
    <div className="app-shell">
      <Sidebar role={user.role} />
      <div className="main-panel">
        <Navbar user={user} />
        <div className="content">{children}</div>
      </div>
    </div>
  )
}
