import { useAuth } from './useAuth'

export const useRoleGuard = (roles: string[]) => {
  const { user } = useAuth()
  if (!user) return { user: null, allowed: false }
  return { user, allowed: roles.includes(user.role) }
}
