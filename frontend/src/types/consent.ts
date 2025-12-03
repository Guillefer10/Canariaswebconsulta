export type ConsentType = 'privacy_policy' | 'health_data'

export type ConsentRecord = {
  id: number
  client_id: number
  consent_type: ConsentType
  text_version: string
  accepted_at: string
  ip_address?: string
  user_agent?: string
  accepted_by_user_id?: number
  created_at?: string
  updated_at?: string
}

export type ConsentRecordCreate = Omit<ConsentRecord, 'id' | 'accepted_at' | 'created_at' | 'updated_at'>
