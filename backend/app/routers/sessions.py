from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.crud.treatment_session import crud_treatment_session
from app.crud.client_profile import crud_client_profile
from app.crud.user import crud_user
from app.schemas.treatment_session import TreatmentSessionCreate, TreatmentSessionRead, TreatmentSessionUpdate
from app.utils.exceptions import not_found
from app.utils.validators import ensure_worker

router = APIRouter(prefix="/sessions", tags=["sessions"])


def _can_manage(user, client_id: int, db: Session):
    profile = crud_client_profile.get(db, client_id)
    if not profile:
        raise not_found("ClientProfile")
    if user.role == "client" and profile.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return profile


@router.get("/clients/{client_id}", response_model=list[TreatmentSessionRead])
def list_sessions(client_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _can_manage(current_user, client_id, db)
    return db.query(crud_treatment_session.model).filter(crud_treatment_session.model.client_id == client_id).all()


@router.post("/clients/{client_id}", response_model=TreatmentSessionRead)
def create_session(
    client_id: int,
    data: TreatmentSessionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if current_user.role == "client":
        raise HTTPException(status_code=403, detail="Clients cannot register treatment sessions")
    _can_manage(current_user, client_id, db)
    worker = crud_user.get(db, data.worker_id)
    if not worker:
        raise not_found("Worker")
    ensure_worker(worker)
    return crud_treatment_session.create(db, data)


@router.put("/{session_id}", response_model=TreatmentSessionRead)
def update_session(session_id: int, data: TreatmentSessionUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    session = crud_treatment_session.get(db, session_id)
    if not session:
        raise not_found("TreatmentSession")
    _can_manage(current_user, session.client_id, db)
    return crud_treatment_session.update(db, session, data)
