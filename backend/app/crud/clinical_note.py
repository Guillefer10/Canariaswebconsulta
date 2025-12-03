from app.crud.base import CRUDBase
from app.models.clinical_note import ClinicalNote
from app.schemas.clinical_note import ClinicalNoteCreate, ClinicalNoteUpdate


class CRUDClinicalNote(CRUDBase[ClinicalNote, ClinicalNoteCreate, ClinicalNoteUpdate]):
    pass


def _get_crud():
    return CRUDClinicalNote(ClinicalNote)


crud_clinical_note = _get_crud()
