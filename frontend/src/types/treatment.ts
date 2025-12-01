export type TreatmentType = {
  id: number
  name: string
  description?: string
  estimated_duration_minutes: number
  base_price?: number
  is_active: boolean
}
