import { useQuery } from '@tanstack/react-query'
import { fetchClients } from '../services/clientService'
import { ClientProfile } from '../types/client'
import { useAuth } from './useAuth'

export const useClients = () => {
  const { token } = useAuth()
  return useQuery<ClientProfile[]>({
    queryKey: ['clients'],
    queryFn: () => fetchClients(token ?? undefined),
    enabled: !!token,
  })
}
