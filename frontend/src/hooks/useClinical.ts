import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import {
  fetchEpisodes,
  createEpisode,
  updateEpisode,
  fetchNotes,
  createNote,
  updateNote,
} from '../services/clinicalService'
import { ClinicalEpisodeCreate, ClinicalEpisodeUpdate, ClinicalNoteCreate, ClinicalNoteUpdate } from '../types/clinical'
import { useAuth } from './useAuth'

export const useEpisodes = (clientId: number) => {
  const { token } = useAuth()
  return useQuery({
    queryKey: ['clinical', 'episodes', clientId],
    queryFn: () => fetchEpisodes(clientId, token ?? undefined),
    enabled: !!clientId && !!token,
  })
}

export const useCreateEpisode = (clientId: number) => {
  const { token } = useAuth()
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: ClinicalEpisodeCreate) => createEpisode(clientId, payload, token ?? undefined),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['clinical', 'episodes', clientId] }),
  })
}

export const useUpdateEpisode = (clientId: number, episodeId: number) => {
  const { token } = useAuth()
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: ClinicalEpisodeUpdate) => updateEpisode(episodeId, payload, token ?? undefined),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['clinical', 'episodes', clientId] }),
  })
}

export const useNotes = (clientId: number, episodeId?: number) => {
  const { token } = useAuth()
  return useQuery({
    queryKey: ['clinical', 'notes', clientId, episodeId ?? 'all'],
    queryFn: () => fetchNotes(clientId, episodeId, token ?? undefined),
    enabled: !!clientId && !!token,
  })
}

export const useCreateNote = (clientId: number, episodeId?: number) => {
  const { token } = useAuth()
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: ClinicalNoteCreate) => createNote(clientId, payload, token ?? undefined),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['clinical', 'notes', clientId, episodeId ?? 'all'] })
      queryClient.invalidateQueries({ queryKey: ['clinical', 'episodes', clientId] })
    },
  })
}

export const useUpdateNote = (clientId: number, noteId: number, episodeId?: number) => {
  const { token } = useAuth()
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: ClinicalNoteUpdate) => updateNote(noteId, payload, token ?? undefined),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['clinical', 'notes', clientId, episodeId ?? 'all'] })
      queryClient.invalidateQueries({ queryKey: ['clinical', 'episodes', clientId] })
    },
  })
}
