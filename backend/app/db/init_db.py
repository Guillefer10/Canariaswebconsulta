from app.db.session import engine
from app.db import base  # noqa: F401
from app.models import (  # noqa: F401
    user,
    client_profile,
    treatment_type,
    treatment_session,
    appointment,
    clinical_episode,
    clinical_note,
    consent_record,
)


def init_db():
    base.Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
