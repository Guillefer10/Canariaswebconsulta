from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.treatment_session import TreatmentSession
from app.schemas.treatment_session import TreatmentSessionCreate, TreatmentSessionUpdate


def _get_crud():
    return CRUDBase[TreatmentSession, TreatmentSessionCreate, TreatmentSessionUpdate](TreatmentSession)


crud_treatment_session = _get_crud()
