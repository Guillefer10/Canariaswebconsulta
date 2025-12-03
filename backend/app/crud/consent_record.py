from app.crud.base import CRUDBase
from app.models.consent_record import ConsentRecord
from app.schemas.consent_record import ConsentRecordCreate


class CRUDConsentRecord(CRUDBase[ConsentRecord, ConsentRecordCreate, ConsentRecordCreate]):
    pass


def _get_crud():
    return CRUDConsentRecord(ConsentRecord)


crud_consent_record = _get_crud()
