export type User = {
  id: number
  first_name: string
  last_name: string
  email: string
  role: 'admin' | 'worker' | 'client'
  is_active: boolean
}
