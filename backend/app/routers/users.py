from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_admin, get_db
from app.crud.user import crud_user
from app.crud.client_profile import crud_client_profile
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.schemas.client_profile import ClientProfileCreate, ClientProfileRead
from app.utils.exceptions import not_found, bad_request

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserRead])
def list_users(db: Session = Depends(get_db), _: None = Depends(get_current_admin)):
    return crud_user.get_multi(db)


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, db: Session = Depends(get_db), _: None = Depends(get_current_admin)):
    if crud_user.get_by_email(db, user_in.email):
        raise bad_request("Email ya registrado")
    user = crud_user.create(db, user_in)
    if user.role == "client":
        # basic profile placeholder
        raise bad_request("Perfil de cliente requerido; crea uno via /clients")
    return user


@router.put("/{user_id}", response_model=UserRead)
def update_user(user_id: int, user_in: UserUpdate, db: Session = Depends(get_db), _: None = Depends(get_current_admin)):
    db_user = crud_user.get(db, user_id)
    if not db_user:
        raise not_found("User")
    return crud_user.update(db, db_user, user_in)


@router.patch("/{user_id}/activate", response_model=UserRead)
def activate_user(user_id: int, db: Session = Depends(get_db), _: None = Depends(get_current_admin)):
    db_user = crud_user.get(db, user_id)
    if not db_user:
        raise not_found("User")
    return crud_user.update(db, db_user, {"is_active": True})


@router.patch("/{user_id}/deactivate", response_model=UserRead)
def deactivate_user(user_id: int, db: Session = Depends(get_db), _: None = Depends(get_current_admin)):
    db_user = crud_user.get(db, user_id)
    if not db_user:
        raise not_found("User")
    return crud_user.update(db, db_user, {"is_active": False})
