import { User } from './user'

export type LoginPayload = { email: string; password: string }

export type AuthUser = User

export type AuthResponse = {
  access_token: string
  token_type: string
  user: AuthUser
}

export type AuthContextType = {
  user: AuthUser | null
  token: string | null
  login: (payload: LoginPayload) => Promise<void>
  logout: () => void
}
