import { apiClient } from './apiClient'
import { User } from '../types/user'

export const fetchUsers = async (token?: string): Promise<User[]> => {
  const { data } = await apiClient(token).get<User[]>('/users')
  return data
}
