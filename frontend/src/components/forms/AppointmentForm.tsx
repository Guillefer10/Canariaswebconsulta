import { useState } from 'react'
import { Appointment } from '../../types/appointment'

export const AppointmentForm = ({ onSubmit }: { onSubmit: (payload: Partial<Appointment>) => void }) => {
  const [clientId, setClientId] = useState('')
  const [workerId, setWorkerId] = useState('')
  const [treatmentTypeId, setTreatmentTypeId] = useState('')
  const [start, setStart] = useState('')
  const [end, setEnd] = useState('')

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault()
        onSubmit({
          client_id: Number(clientId),
          worker_id: Number(workerId),
          treatment_type_id: Number(treatmentTypeId),
          start_datetime: new Date(start).toISOString(),
          end_datetime: new Date(end).toISOString(),
          status: 'pendiente',
          notes: '',
          created_by_user_id: Number(workerId),
        } as any)
      }}
    >
      <label>Cliente</label>
      <input value={clientId} onChange={(e) => setClientId(e.target.value)} required />
      <label>Trabajador</label>
      <input value={workerId} onChange={(e) => setWorkerId(e.target.value)} required />
      <label>Tratamiento</label>
      <input value={treatmentTypeId} onChange={(e) => setTreatmentTypeId(e.target.value)} required />
      <label>Inicio</label>
      <input type="datetime-local" value={start} onChange={(e) => setStart(e.target.value)} required />
      <label>Fin</label>
      <input type="datetime-local" value={end} onChange={(e) => setEnd(e.target.value)} required />
      <button className="button" type="submit">Guardar cita</button>
    </form>
  )
}
