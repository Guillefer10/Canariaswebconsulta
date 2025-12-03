from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.crud.client_profile import crud_client_profile
from app.crud.user import crud_user
from app.schemas.client_profile import ClientProfileCreate, ClientProfileRead, ClientProfileUpdate
from app.utils.exceptions import not_found, bad_request, forbidden

router = APIRouter(prefix="/clients", tags=["clients"])


def _authorize(user):
    if user.role not in ("admin", "worker"):
        raise forbidden("Permisos insuficientes")


@router.get("/", response_model=list[ClientProfileRead])
def list_clients(
    name: str | None = Query(None),
    national_id: str | None = Query(None),
    phone: str | None = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    _authorize(current_user)
    query = db.query(crud_client_profile.model)
    if name:
        query = query.join(crud_client_profile.model.user).filter(
            (crud_user.model.first_name + " " + crud_user.model.last_name).ilike(f"%{name}%")  # type: ignore
        )
    if national_id:
        query = query.filter(crud_client_profile.model.national_id == national_id)
    if phone:
        query = query.filter(crud_client_profile.model.phone == phone)
    return query.all()


@router.post("/", response_model=ClientProfileRead)
def create_client(profile_in: ClientProfileCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _authorize(current_user)
    user = crud_user.get(db, profile_in.user_id)
    if not user:
        raise not_found("User")
    if user.role != "client":
        raise bad_request("Associated user must have client role")
    if crud_client_profile.get_by_user(db, user.id):
        raise bad_request("Profile already exists for this user")
    return crud_client_profile.create(db, profile_in)


@router.get("/me", response_model=ClientProfileRead)
def get_my_profile(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    profile = crud_client_profile.get_by_user(db, current_user.id)
    if not profile:
        raise not_found("ClientProfile")
    return profile


@router.get("/{profile_id}", response_model=ClientProfileRead)
def get_client(profile_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    profile = crud_client_profile.get(db, profile_id)
    if not profile:
        raise not_found("ClientProfile")
    if current_user.role == "client" and profile.user_id != current_user.id:
        raise forbidden("No autorizado")
    return profile


@router.put("/{profile_id}", response_model=ClientProfileRead)
def update_client(profile_id: int, profile_in: ClientProfileUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    profile = crud_client_profile.get(db, profile_id)
    if not profile:
        raise not_found("ClientProfile")
    if current_user.role == "client" and profile.user_id != current_user.id:
        raise forbidden("No autorizado")
    return crud_client_profile.update(db, profile, profile_in)
