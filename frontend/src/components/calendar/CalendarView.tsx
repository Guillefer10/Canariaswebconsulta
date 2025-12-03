import EmptyState from '../common/EmptyState'
import { Appointment } from '../../types/appointment'

const formatDay = (date: Date) =>
  date.toLocaleDateString('es-ES', { weekday: 'short', day: 'numeric', month: 'short' })

const formatTime = (iso: string) =>
  new Date(iso).toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })

export const CalendarView = ({ appointments, onCreate }: { appointments: Appointment[]; onCreate: () => void }) => {
  const today = new Date()
  const startOfWeek = new Date(today)
  const day = startOfWeek.getDay()
  const diff = day === 0 ? -6 : 1 - day
  startOfWeek.setDate(startOfWeek.getDate() + diff)
  startOfWeek.setHours(0, 0, 0, 0)

  const weekDays = Array.from({ length: 7 }).map((_, idx) => {
    const d = new Date(startOfWeek)
    d.setDate(startOfWeek.getDate() + idx)
    return d
  })

  const hasAppointments = appointments.length > 0

  return (
    <div className="card">
      <div className="card-header">
        <div>
          <h3>Calendario semanal</h3>
          <p className="muted">Vista de los proximos 7 dias</p>
        </div>
        <button className="button" onClick={onCreate}>Nueva cita</button>
      </div>

      {!hasAppointments && (
        <EmptyState
          title="Sin citas programadas"
          description="Crea una nueva cita para verla en la agenda semanal."
          action={<button className="button" onClick={onCreate}>Crear cita</button>}
        />
      )}

      {hasAppointments && (
        <div className="calendar-grid">
          {weekDays.map((dayDate) => {
            const slots = appointments
              .filter((a) => {
                const date = new Date(a.start_datetime)
                return (
                  date.getFullYear() === dayDate.getFullYear() &&
                  date.getMonth() === dayDate.getMonth() &&
                  date.getDate() === dayDate.getDate()
                )
              })
              .sort(
                (a, b) =>
                  new Date(a.start_datetime).getTime() - new Date(b.start_datetime).getTime()
              )

            return (
              <div className="calendar-day" key={dayDate.toISOString()}>
                <div className="calendar-day-header">
                  <span>{formatDay(dayDate)}</span>
                  <span className="pill">{slots.length} citas</span>
                </div>
                {slots.length === 0 && <p className="muted">Sin citas</p>}
                {slots.map((slot) => (
                  <div className="calendar-slot" key={slot.id}>
                    <div>
                      <div className="calendar-slot-time">{formatTime(slot.start_datetime)}</div>
                      <div className="muted">Cliente #{slot.client_id} / Trabajador #{slot.worker_id}</div>
                    </div>
                    <span className={`badge ${slot.status}`}>{slot.status}</span>
                  </div>
                ))}
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
