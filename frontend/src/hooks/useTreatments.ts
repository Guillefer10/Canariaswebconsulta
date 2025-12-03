import { useQuery } from '@tanstack/react-query'
import { fetchTreatments } from '../services/treatmentService'
import { TreatmentType } from '../types/treatment'
import { useAuth } from './useAuth'

export const useTreatments = () => {
  const { token } = useAuth()
  return useQuery<TreatmentType[]>({
    queryKey: ['treatments'],
    queryFn: () => fetchTreatments(token ?? undefined),
    enabled: !!token,
  })
}
