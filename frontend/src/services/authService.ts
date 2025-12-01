import { apiClient } from './apiClient'
import { AuthResponse, LoginPayload } from '../types/auth'

export const login = async (payload: LoginPayload): Promise<AuthResponse> => {
  const { data } = await apiClient().post<AuthResponse>('/auth/login', payload)
  return data
}

export const getMe = async (token: string) => {
  const { data } = await apiClient(token).get<AuthResponse['user']>('/auth/me')
  return data
}
