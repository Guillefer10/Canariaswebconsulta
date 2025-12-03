export type ClinicalEpisode = {
  id: number
  client_id: number
  title: string
  description?: string
  started_at: string
  closed_at?: string
  is_active: boolean
  created_at?: string
  updated_at?: string
}

export type ClinicalNote = {
  id: number
  client_id: number
  worker_id: number
  episode_id?: number
  appointment_id?: number
  treatment_type_id?: number
  note_date?: string
  motive?: string
  observations?: string
  plan?: string
  attachments?: string
  created_at?: string
  updated_at?: string
}

export type ClinicalEpisodeCreate = Omit<ClinicalEpisode, 'id' | 'created_at' | 'updated_at'>
export type ClinicalEpisodeUpdate = Partial<ClinicalEpisodeCreate>

export type ClinicalNoteCreate = Omit<ClinicalNote, 'id' | 'created_at' | 'updated_at'>
export type ClinicalNoteUpdate = Partial<ClinicalNoteCreate>
