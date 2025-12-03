import { useState } from 'react'
import { AppointmentCreatePayload } from '../../types/appointment'
import { ClientProfile } from '../../types/client'
import { TreatmentType } from '../../types/treatment'
import { User } from '../../types/user'

type AppointmentFormProps = {
  clients: ClientProfile[]
  workers: User[]
  treatments: TreatmentType[]
  defaultClientId?: number
  defaultWorkerId?: number
  onSubmit: (payload: AppointmentCreatePayload) => void
  onCancel?: () => void
}

export const AppointmentForm = ({
  clients,
  workers,
  treatments,
  defaultClientId,
  defaultWorkerId,
  onSubmit,
  onCancel,
}: AppointmentFormProps) => {
  const [clientId, setClientId] = useState(defaultClientId ? String(defaultClientId) : '')
  const [workerId, setWorkerId] = useState(defaultWorkerId ? String(defaultWorkerId) : '')
  const [treatmentTypeId, setTreatmentTypeId] = useState('')
  const [start, setStart] = useState('')
  const [end, setEnd] = useState('')
  const [notes, setNotes] = useState('')

  const handleSubmit = () => {
    if (!clientId || !workerId || !treatmentTypeId || !start) return
    const payload: AppointmentCreatePayload = {
      client_id: Number(clientId),
      worker_id: Number(workerId),
      treatment_type_id: Number(treatmentTypeId),
      start_datetime: new Date(start).toISOString(),
      status: 'pendiente',
    }
    if (end) payload.end_datetime = new Date(end).toISOString()
    if (notes) payload.notes = notes
    onSubmit(payload)
  }

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault()
        handleSubmit()
      }}
    >
      <label>Cliente</label>
      <select value={clientId} onChange={(e) => setClientId(e.target.value)} required>
        <option value="">Selecciona un cliente</option>
        {clients.map((c) => (
          <option key={c.id} value={c.id}>
            {c.user?.first_name} {c.user?.last_name}
          </option>
        ))}
      </select>

      <label>Trabajador</label>
      <select value={workerId} onChange={(e) => setWorkerId(e.target.value)} required>
        <option value="">Selecciona un profesional</option>
        {workers.map((w) => (
          <option key={w.id} value={w.id}>
            {w.first_name} {w.last_name}
          </option>
        ))}
      </select>

      <label>Tratamiento</label>
      <select value={treatmentTypeId} onChange={(e) => setTreatmentTypeId(e.target.value)} required>
        <option value="">Selecciona un tratamiento</option>
        {treatments.map((t) => (
          <option key={t.id} value={t.id}>
            {t.name} - {t.estimated_duration_minutes} min
          </option>
        ))}
      </select>

      <label>Inicio</label>
      <input type="datetime-local" value={start} onChange={(e) => setStart(e.target.value)} required />

      <label>Fin (opcional)</label>
      <input type="datetime-local" value={end} onChange={(e) => setEnd(e.target.value)} />

      <label>Notas</label>
      <textarea value={notes} onChange={(e) => setNotes(e.target.value)} placeholder="Notas para la cita (opcional)" />

      <div className="form-actions">
        {onCancel && <button className="button ghost" type="button" onClick={onCancel}>Cancelar</button>}
        <button className="button" type="submit">Guardar cita</button>
      </div>
    </form>
  )
}
