import { Appointment } from '../../types/appointment'

export const CalendarView = ({ appointments, onCreate }: { appointments: Appointment[]; onCreate: () => void }) => {
  return (
    <div className="card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h3>Calendario</h3>
        <button className="button" onClick={onCreate}>Nueva cita</button>
      </div>
      <ul>
        {appointments.map((a) => (
          <li key={a.id}>
            {new Date(a.start_datetime).toLocaleString()} - {a.status} (Cliente {a.client_id} / Trabajador {a.worker_id})
          </li>
        ))}
      </ul>
    </div>
  )
}
