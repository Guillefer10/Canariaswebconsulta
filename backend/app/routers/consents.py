from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.crud.client_profile import crud_client_profile
from app.crud.consent_record import crud_consent_record
from app.schemas.consent_record import ConsentRecordCreate, ConsentRecordRead
from app.utils.exceptions import forbidden, not_found

router = APIRouter(prefix="/consents", tags=["consents"])


def _get_profile_or_403(client_id: int, db: Session, user):
    profile = crud_client_profile.get(db, client_id)
    if not profile:
        raise not_found("ClientProfile")
    if user.role == "client" and profile.user_id != user.id:
        raise forbidden("No autorizado")
    return profile


@router.get("/clients/{client_id}", response_model=list[ConsentRecordRead])
def list_consents(client_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _get_profile_or_403(client_id, db, current_user)
    return (
        db.query(crud_consent_record.model)
        .filter(crud_consent_record.model.client_id == client_id)
        .order_by(crud_consent_record.model.accepted_at.desc())
        .all()
    )


@router.post("/clients/{client_id}", response_model=ConsentRecordRead)
def register_consent(
    client_id: int,
    data: ConsentRecordCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    # Clients can only register their own; admins can register on behalf
    profile = _get_profile_or_403(client_id, db, current_user)
    if current_user.role not in ("client", "admin"):
        raise forbidden("No autorizado")
    payload = data.model_dump()
    payload["client_id"] = profile.id
    payload["accepted_by_user_id"] = current_user.id
    return crud_consent_record.create(db, ConsentRecordCreate(**payload))


@router.get("/me", response_model=list[ConsentRecordRead])
def my_consents(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role != "client":
        raise forbidden("Solo clientes")
    profile = crud_client_profile.get_by_user(db, current_user.id)
    if not profile:
        return []
    return (
        db.query(crud_consent_record.model)
        .filter(crud_consent_record.model.client_id == profile.id)
        .order_by(crud_consent_record.model.accepted_at.desc())
        .all()
    )
