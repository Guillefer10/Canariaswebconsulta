import { User } from './user'

export type ClientProfile = {
  id: number
  user_id: number
  phone: string
  birth_date: string
  national_id: string
  address?: string
  medical_notes?: string
  consent_data: boolean
  join_date: string
  skin_type?: string
  conditions?: string
  user?: User
}
