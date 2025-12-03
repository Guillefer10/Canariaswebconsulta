import { useMemo, useState } from 'react'
import { AppointmentCreatePayload } from '../../types/appointment'
import { useAuth } from '../../hooks/useAuth'
import { CalendarView } from '../../components/calendar/CalendarView'
import { AppointmentForm } from '../../components/forms/AppointmentForm'
import EmptyState from '../../components/common/EmptyState'
import {
  useAppointments,
  useCreateAppointment,
  useChangeAppointmentStatus,
  useRescheduleAppointment,
  useCancelAppointment,
} from '../../hooks/useAppointments'
import { useClients } from '../../hooks/useClients'
import { useTreatments } from '../../hooks/useTreatments'

const WorkerAgendaPage = () => {
  const { user } = useAuth()
  const [showForm, setShowForm] = useState(false)

  const { data: appointments, isLoading: apptLoading, error: apptError } = useAppointments()
  const { data: clients, isLoading: clientsLoading, error: clientsError } = useClients()
  const { data: treatments, isLoading: treatmentsLoading, error: treatmentsError } = useTreatments()
  const createAppointment = useCreateAppointment()
  const changeStatus = useChangeAppointmentStatus()
  const reschedule = useRescheduleAppointment()
  const cancel = useCancelAppointment()

  const loading = apptLoading || clientsLoading || treatmentsLoading
  const error = apptError || clientsError || treatmentsError

  const workers = useMemo(() => (user ? [user] : []), [user])

  const handleCreate = async (payload: AppointmentCreatePayload) => {
    await createAppointment.mutateAsync(payload)
    setShowForm(false)
  }

  if (loading) return <p className="muted">Cargando agenda...</p>

  if (error) {
    return (
      <EmptyState
        title="Error al cargar la agenda"
        description="Comprueba tu conexión e inténtalo de nuevo."
        action={
          <button className="button" onClick={() => window.location.reload()}>
            Reintentar
          </button>
        }
      />
    )
  }

  return (
    <>
      <CalendarView
        appointments={appointments ?? []}
        onCreate={() => setShowForm(true)}
        onChangeStatus={(id, status) => changeStatus.mutate({ id, status })}
        onReschedule={(id, start, end) =>
          reschedule.mutate({ id, payload: { start_datetime: start, end_datetime: end ?? undefined } })
        }
        onCancel={(id) => cancel.mutate(id)}
      />

      {showForm && clients && treatments && (
        <div className="card">
          <div className="card-header">
            <div>
              <h3>Nueva cita</h3>
              <p className="muted">Completa los datos y guarda para agendar</p>
            </div>
            <button className="button ghost" onClick={() => setShowForm(false)}>
              Cerrar
            </button>
          </div>
          <AppointmentForm
            clients={clients}
            workers={workers}
            treatments={treatments}
            defaultWorkerId={user?.id}
            onSubmit={handleCreate}
            onCancel={() => setShowForm(false)}
          />
          {createAppointment.isPending && <p className="muted">Guardando cita...</p>}
          {createAppointment.isError && <p className="error">No se pudo crear la cita.</p>}
        </div>
      )}
    </>
  )
}

export default WorkerAgendaPage
