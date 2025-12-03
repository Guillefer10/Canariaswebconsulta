import { useEffect, useMemo, useState } from 'react'
import Alert from '../../components/common/Alert'
import { Toast } from '../../components/common/Toast'
import { useAuth } from '../../hooks/useAuth'
import {
  useClients,
} from '../../hooks/useClients'
import {
  useEpisodes,
  useCreateEpisode,
  useNotes,
  useCreateNote,
} from '../../hooks/useClinical'
import { ClientProfile } from '../../types/client'
import { ClinicalEpisodeCreate, ClinicalNoteCreate } from '../../types/clinical'

const WorkerClinicalPage = () => {
  const { user } = useAuth()
  const { data: clients, isLoading: clientsLoading, error: clientsError } = useClients()
  const [selectedClient, setSelectedClient] = useState<ClientProfile | null>(null)

  const clientId = selectedClient?.id ?? 0
  const { data: episodes, isLoading: episodesLoading, error: episodesError } = useEpisodes(clientId)
  const { data: notes, isLoading: notesLoading, error: notesError } = useNotes(clientId, undefined)

  const createEpisode = useCreateEpisode(clientId)
  const createNote = useCreateNote(clientId)

  const [toast, setToast] = useState<{ type: 'success' | 'error' | 'info'; message: string } | null>(null)
  const [episodeTitle, setEpisodeTitle] = useState('')
  const [episodeDescription, setEpisodeDescription] = useState('')
  const [noteMotive, setNoteMotive] = useState('')
  const [noteObservations, setNoteObservations] = useState('')
  const [notePlan, setNotePlan] = useState('')
  const [noteEpisodeId, setNoteEpisodeId] = useState<string>('')

  useEffect(() => {
    if (clients && clients.length > 0 && !selectedClient) {
      setSelectedClient(clients[0])
    }
  }, [clients, selectedClient])

  const handleCreateEpisode = () => {
    if (!clientId || !episodeTitle) return
    const payload: ClinicalEpisodeCreate = {
      client_id: clientId,
      title: episodeTitle,
      description: episodeDescription || undefined,
      is_active: true,
    }
    createEpisode.mutate(payload, {
      onSuccess: () => {
        setEpisodeTitle('')
        setEpisodeDescription('')
        setToast({ type: 'success', message: 'Episodio creado' })
      },
      onError: () => setToast({ type: 'error', message: 'No se pudo crear el episodio' }),
    })
  }

  const handleCreateNote = () => {
    if (!clientId || !noteMotive) return
    const payload: ClinicalNoteCreate = {
      client_id: clientId,
      worker_id: user?.id ?? 0,
      motive: noteMotive,
      observations: noteObservations || undefined,
      plan: notePlan || undefined,
      episode_id: noteEpisodeId ? Number(noteEpisodeId) : undefined,
    }
    createNote.mutate(payload, {
      onSuccess: () => {
        setNoteMotive('')
        setNoteObservations('')
        setNotePlan('')
        setNoteEpisodeId('')
        setToast({ type: 'success', message: 'Nota creada' })
      },
      onError: () => setToast({ type: 'error', message: 'No se pudo crear la nota' }),
    })
  }

  const loading = clientsLoading || episodesLoading || notesLoading
  const error = clientsError || episodesError || notesError

  return (
    <div className="card-grid">
      <div className="card">
        <h3>Paciente</h3>
        {clientsLoading && <p className="muted">Cargando pacientes...</p>}
        {clientsError && <Alert type="error" message="No se pudo cargar pacientes" />}
        {clients && clients.length > 0 && (
          <select
            value={selectedClient?.id ?? ''}
            onChange={(e) => {
              const id = Number(e.target.value)
              const found = clients.find((c) => c.id === id)
              setSelectedClient(found || null)
            }}
          >
            {clients.map((c) => (
              <option key={c.id} value={c.id}>
                {c.user?.first_name} {c.user?.last_name}
              </option>
            ))}
          </select>
        )}
      </div>

      <div className="card">
        <h3>Nuevo episodio</h3>
        <input
          type="text"
          placeholder="Título del episodio"
          value={episodeTitle}
          onChange={(e) => setEpisodeTitle(e.target.value)}
        />
        <textarea
          placeholder="Descripción"
          value={episodeDescription}
          onChange={(e) => setEpisodeDescription(e.target.value)}
        />
        <button className="button" onClick={handleCreateEpisode} disabled={createEpisode.isPending || !episodeTitle || !clientId}>
          Crear episodio
        </button>
      </div>

      <div className="card full-width">
        <h3>Episodios</h3>
        {loading && <p className="muted">Cargando episodios...</p>}
        {error && <Alert type="error" message="No se pudieron cargar episodios/notas" />}
        <div className="list-block">
          {episodes?.map((ep) => (
            <div key={ep.id} className="list-card">
              <div>
                <div className="text-strong">{ep.title}</div>
                <small>{ep.description}</small>
              </div>
              <div className="badge">{ep.is_active ? 'Activo' : 'Cerrado'}</div>
            </div>
          ))}
          {episodes && episodes.length === 0 && <p className="muted">Sin episodios</p>}
        </div>
      </div>

      <div className="card full-width">
        <h3>Nueva nota</h3>
        <select value={noteEpisodeId} onChange={(e) => setNoteEpisodeId(e.target.value)}>
          <option value="">Nota sin episodio</option>
          {episodes?.map((ep) => (
            <option key={ep.id} value={ep.id}>
              {ep.title}
            </option>
          ))}
        </select>
        <input
          type="text"
          placeholder="Motivo"
          value={noteMotive}
          onChange={(e) => setNoteMotive(e.target.value)}
        />
        <textarea
          placeholder="Observaciones"
          value={noteObservations}
          onChange={(e) => setNoteObservations(e.target.value)}
        />
        <textarea placeholder="Plan" value={notePlan} onChange={(e) => setNotePlan(e.target.value)} />
        <button
          className="button"
          onClick={handleCreateNote}
          disabled={createNote.isPending || !noteMotive || !clientId || !user}
        >
          Crear nota
        </button>
      </div>

      <div className="card full-width">
        <h3>Notas</h3>
        {notesLoading && <p className="muted">Cargando notas...</p>}
        <div className="list-block">
          {notes?.map((note) => (
            <div key={note.id} className="list-card">
              <div>
                <div className="text-strong">{note.motive}</div>
                <small>{note.observations}</small>
              </div>
              <div className="badge">{new Date(note.note_date ?? note.created_at ?? '').toLocaleString()}</div>
            </div>
          ))}
          {notes && notes.length === 0 && <p className="muted">Sin notas</p>}
        </div>
      </div>

      {toast && <Toast type={toast.type} message={toast.message} />}
    </div>
  )
}

export default WorkerClinicalPage
