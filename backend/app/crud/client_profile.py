from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.client_profile import ClientProfile
from app.schemas.client_profile import ClientProfileCreate, ClientProfileUpdate


class CRUDClientProfile(CRUDBase[ClientProfile, ClientProfileCreate, ClientProfileUpdate]):
    def get_by_user(self, db: Session, user_id: int):
        return db.query(ClientProfile).filter(ClientProfile.user_id == user_id).first()


def _get_crud():
    return CRUDClientProfile(ClientProfile)


crud_client_profile = _get_crud()
