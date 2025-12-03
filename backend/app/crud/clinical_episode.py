from app.crud.base import CRUDBase
from app.models.clinical_episode import ClinicalEpisode
from app.schemas.clinical_episode import ClinicalEpisodeCreate, ClinicalEpisodeUpdate


class CRUDClinicalEpisode(CRUDBase[ClinicalEpisode, ClinicalEpisodeCreate, ClinicalEpisodeUpdate]):
    pass


def _get_crud():
    return CRUDClinicalEpisode(ClinicalEpisode)


crud_clinical_episode = _get_crud()
