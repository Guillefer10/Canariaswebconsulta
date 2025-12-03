import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { createConsent, fetchClientConsents, fetchMyConsents } from '../services/consentService'
import { ConsentRecordCreate } from '../types/consent'
import { useAuth } from './useAuth'

export const useClientConsents = (clientId: number) => {
  const { token } = useAuth()
  return useQuery({
    queryKey: ['consents', 'client', clientId],
    queryFn: () => fetchClientConsents(clientId, token ?? undefined),
    enabled: !!clientId && !!token,
  })
}

export const useMyConsents = () => {
  const { token } = useAuth()
  return useQuery({
    queryKey: ['consents', 'me'],
    queryFn: () => fetchMyConsents(token ?? undefined),
    enabled: !!token,
  })
}

export const useCreateConsent = (clientId: number) => {
  const { token } = useAuth()
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: ConsentRecordCreate) => createConsent(clientId, payload, token ?? undefined),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['consents', 'client', clientId] })
      queryClient.invalidateQueries({ queryKey: ['consents', 'me'] })
    },
  })
}
