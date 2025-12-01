import { useAuth } from './useAuth'

export const useRoleGuard = (roles: string[]) => {
  const { user } = useAuth()
  if (!user) return { user: null }
  return { user: roles.includes(user.role) ? user : user }
}
