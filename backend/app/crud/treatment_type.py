from app.crud.base import CRUDBase
from app.models.treatment_type import TreatmentType
from app.schemas.treatment_type import TreatmentTypeCreate, TreatmentTypeUpdate


def _get_crud():
    return CRUDBase[TreatmentType, TreatmentTypeCreate, TreatmentTypeUpdate](TreatmentType)


crud_treatment_type = _get_crud()
