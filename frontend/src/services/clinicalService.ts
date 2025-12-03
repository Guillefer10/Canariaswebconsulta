import { apiClient } from './apiClient'
import {
  ClinicalEpisode,
  ClinicalEpisodeCreate,
  ClinicalEpisodeUpdate,
  ClinicalNote,
  ClinicalNoteCreate,
  ClinicalNoteUpdate,
} from '../types/clinical'

export const fetchEpisodes = async (clientId: number, token?: string): Promise<ClinicalEpisode[]> => {
  const { data } = await apiClient(token).get<ClinicalEpisode[]>(`/clinical/episodes/clients/${clientId}`)
  return data
}

export const createEpisode = async (
  clientId: number,
  payload: ClinicalEpisodeCreate,
  token?: string,
): Promise<ClinicalEpisode> => {
  const { data } = await apiClient(token).post<ClinicalEpisode>(`/clinical/episodes/clients/${clientId}`, payload)
  return data
}

export const updateEpisode = async (
  episodeId: number,
  payload: ClinicalEpisodeUpdate,
  token?: string,
): Promise<ClinicalEpisode> => {
  const { data } = await apiClient(token).put<ClinicalEpisode>(`/clinical/episodes/${episodeId}`, payload)
  return data
}

export const fetchNotes = async (clientId: number, episodeId?: number, token?: string): Promise<ClinicalNote[]> => {
  const params = episodeId ? { episode_id: episodeId } : undefined
  const { data } = await apiClient(token).get<ClinicalNote[]>(`/clinical/notes/clients/${clientId}`, { params })
  return data
}

export const createNote = async (
  clientId: number,
  payload: ClinicalNoteCreate,
  token?: string,
): Promise<ClinicalNote> => {
  const { data } = await apiClient(token).post<ClinicalNote>(`/clinical/notes/clients/${clientId}`, payload)
  return data
}

export const updateNote = async (noteId: number, payload: ClinicalNoteUpdate, token?: string): Promise<ClinicalNote> => {
  const { data } = await apiClient(token).put<ClinicalNote>(`/clinical/notes/${noteId}`, payload)
  return data
}
