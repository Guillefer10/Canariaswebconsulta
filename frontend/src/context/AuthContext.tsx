import React, { createContext, useEffect, useState } from 'react'
import { login as loginService, getMe } from '../services/authService'
import { AuthContextType, AuthUser, LoginPayload } from '../types/auth'

export const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<AuthUser | null>(null)
  const [token, setToken] = useState<string | null>(() => localStorage.getItem('token'))

  useEffect(() => {
    if (token) {
      localStorage.setItem('token', token)
      getMe(token)
        .then(setUser)
        .catch(() => logout())
    }
  }, [token])

  const login = async (payload: LoginPayload) => {
    const data = await loginService(payload)
    setToken(data.access_token)
    setUser(data.user)
  }

  const logout = () => {
    setToken(null)
    setUser(null)
    localStorage.removeItem('token')
  }

  return (
    <AuthContext.Provider value={{ user, token, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}
