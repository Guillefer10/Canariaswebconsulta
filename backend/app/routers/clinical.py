from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.crud.appointment import crud_appointment
from app.crud.clinical_episode import crud_clinical_episode
from app.crud.clinical_note import crud_clinical_note
from app.crud.client_profile import crud_client_profile
from app.crud.treatment_type import crud_treatment_type
from app.crud.user import crud_user
from app.schemas.clinical_episode import ClinicalEpisodeCreate, ClinicalEpisodeRead, ClinicalEpisodeUpdate
from app.schemas.clinical_note import ClinicalNoteCreate, ClinicalNoteRead, ClinicalNoteUpdate
from app.utils.exceptions import bad_request, forbidden, not_found
from app.utils.validators import ensure_worker

router = APIRouter(prefix="/clinical", tags=["clinical"])


def _get_client_profile(client_id: int, db: Session, user):
    profile = crud_client_profile.get(db, client_id)
    if not profile:
        raise not_found("ClientProfile")
    if user.role == "client" and profile.user_id != user.id:
        raise forbidden("No autorizado")
    return profile


def _ensure_can_write(user):
    if user.role == "client":
        raise forbidden("No autorizado")


@router.get("/episodes/clients/{client_id}", response_model=list[ClinicalEpisodeRead])
def list_episodes(
    client_id: int,
    include_inactive: bool = Query(False),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    _get_client_profile(client_id, db, current_user)
    query = db.query(crud_clinical_episode.model).filter(crud_clinical_episode.model.client_id == client_id)
    if not include_inactive:
        query = query.filter(crud_clinical_episode.model.is_active.is_(True))
    return query.order_by(crud_clinical_episode.model.started_at.desc()).all()


@router.post("/episodes/clients/{client_id}", response_model=ClinicalEpisodeRead)
def create_episode(
    client_id: int,
    data: ClinicalEpisodeCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    _ensure_can_write(current_user)
    _get_client_profile(client_id, db, current_user)
    payload = data.model_dump()
    payload["client_id"] = client_id
    payload["created_by_user_id"] = current_user.id
    return crud_clinical_episode.create(db, ClinicalEpisodeCreate(**payload))


@router.put("/episodes/{episode_id}", response_model=ClinicalEpisodeRead)
def update_episode(
    episode_id: int,
    data: ClinicalEpisodeUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    episode = crud_clinical_episode.get(db, episode_id)
    if not episode:
        raise not_found("ClinicalEpisode")
    _get_client_profile(episode.client_id, db, current_user)
    if current_user.role == "client":
        raise forbidden("No autorizado")
    return crud_clinical_episode.update(db, episode, data)


@router.get("/notes/clients/{client_id}", response_model=list[ClinicalNoteRead])
def list_notes(
    client_id: int,
    episode_id: int | None = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    _get_client_profile(client_id, db, current_user)
    query = db.query(crud_clinical_note.model).filter(crud_clinical_note.model.client_id == client_id)
    if episode_id:
        query = query.filter(crud_clinical_note.model.episode_id == episode_id)
    return query.order_by(crud_clinical_note.model.note_date.desc()).all()


@router.post("/notes/clients/{client_id}", response_model=ClinicalNoteRead)
def create_note(
    client_id: int,
    data: ClinicalNoteCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    _ensure_can_write(current_user)
    _get_client_profile(client_id, db, current_user)

    worker = crud_user.get(db, data.worker_id)
    if not worker:
        raise not_found("Worker")
    ensure_worker(worker)
    if current_user.role == "worker" and worker.id != current_user.id:
        raise forbidden("Solo puedes registrar notas propias")

    if data.episode_id:
        episode = crud_clinical_episode.get(db, data.episode_id)
        if not episode or episode.client_id != client_id:
            raise bad_request("Episodio no valido para el paciente")

    if data.appointment_id:
        appointment = crud_appointment.get(db, data.appointment_id)
        if not appointment or appointment.client_id != client_id:
            raise bad_request("La cita no pertenece al paciente")

    if data.treatment_type_id:
        treatment = crud_treatment_type.get(db, data.treatment_type_id)
        if not treatment:
            raise bad_request("TreatmentType no existe")

    payload = data.model_dump()
    payload["client_id"] = client_id

    return crud_clinical_note.create(db, ClinicalNoteCreate(**payload))


@router.put("/notes/{note_id}", response_model=ClinicalNoteRead)
def update_note(
    note_id: int,
    data: ClinicalNoteUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    note = crud_clinical_note.get(db, note_id)
    if not note:
        raise not_found("ClinicalNote")

    _get_client_profile(note.client_id, db, current_user)

    if current_user.role == "client":
        raise forbidden("No autorizado")
    if current_user.role == "worker" and note.worker_id != current_user.id:
        raise forbidden("Solo puedes editar tus notas")

    if data.episode_id:
        episode = crud_clinical_episode.get(db, data.episode_id)
        if not episode or episode.client_id != note.client_id:
            raise bad_request("Episodio no valido para el paciente")

    if data.appointment_id:
        appointment = crud_appointment.get(db, data.appointment_id)
        if not appointment or appointment.client_id != note.client_id:
            raise bad_request("La cita no pertenece al paciente")

    if data.treatment_type_id:
        treatment = crud_treatment_type.get(db, data.treatment_type_id)
        if not treatment:
            raise bad_request("TreatmentType no existe")

    return crud_clinical_note.update(db, note, data)
