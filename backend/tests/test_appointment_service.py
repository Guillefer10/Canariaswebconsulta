from datetime import datetime, timedelta

import pytest
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.db.base import Base
from app.models.appointment import AppointmentStatus
from app.models.client_profile import ClientProfile
from app.models.treatment_type import TreatmentType
from app.models.user import User
from app.schemas.appointment import AppointmentCreate, AppointmentReschedule, AppointmentUpdate
from app.services.appointment_service import AppointmentService


@pytest.fixture
def db() -> Session:
    engine = create_engine("sqlite:///:memory:", future=True)
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


def _seed_users_and_patient(db: Session):
    admin = User(first_name="Admin", last_name="Test", email="admin@test.com", hashed_password="x", role="admin", is_active=True)
    worker = User(first_name="Worker", last_name="Test", email="worker@test.com", hashed_password="x", role="worker", is_active=True)
    client_user = User(first_name="Client", last_name="Test", email="client@test.com", hashed_password="x", role="client", is_active=True)
    db.add_all([admin, worker, client_user])
    db.commit()
    db.refresh(admin)
    db.refresh(worker)
    db.refresh(client_user)

    profile = ClientProfile(
        user_id=client_user.id,
        phone="123",
        birth_date=datetime.utcnow().date(),
        national_id="DNI",
        address="",
        medical_notes="",
        consent_data=True,
        join_date=datetime.utcnow().date(),
    )
    db.add(profile)
    treatment = TreatmentType(name="Consulta", description="", estimated_duration_minutes=60, base_price=50)
    db.add(treatment)
    db.commit()
    db.refresh(profile)
    db.refresh(treatment)
    return admin, worker, profile, treatment


def test_client_cannot_create_for_other_client(db: Session):
    admin, worker, profile, treatment = _seed_users_and_patient(db)
    now = datetime(2024, 1, 1, 10, 0, 0)
    service = AppointmentService(now_provider=lambda: now)
    other_profile = ClientProfile(
        user_id=admin.id,
        phone="999",
        birth_date=now.date(),
        national_id="ADMIN",
        address="",
        medical_notes="",
        consent_data=True,
        join_date=now.date(),
    )
    db.add(other_profile)
    db.commit()
    with pytest.raises(HTTPException):
        service.create(
            db,
            data=AppointmentCreate(
                client_id=other_profile.id,
                worker_id=worker.id,
                treatment_type_id=treatment.id,
                start_datetime=now + timedelta(hours=1),
                end_datetime=now + timedelta(hours=2),
            ),
            current_user=profile.user,
        )


def test_create_appointment_without_overlap(db: Session):
    admin, worker, profile, treatment = _seed_users_and_patient(db)
    now = datetime(2024, 1, 1, 10, 0, 0)
    service = AppointmentService(now_provider=lambda: now)

    appt = service.create(
        db,
        data=AppointmentCreate(
            client_id=profile.id,
            worker_id=worker.id,
            treatment_type_id=treatment.id,
            start_datetime=now + timedelta(hours=1),
            end_datetime=now + timedelta(hours=2),
        ),
        current_user=admin,
    )

    assert appt.id is not None
    assert appt.status == AppointmentStatus.pending


def test_create_appointment_overlap_fails(db: Session):
    admin, worker, profile, treatment = _seed_users_and_patient(db)
    now = datetime(2024, 1, 1, 10, 0, 0)
    service = AppointmentService(now_provider=lambda: now)

    service.create(
        db,
        data=AppointmentCreate(
            client_id=profile.id,
            worker_id=worker.id,
            treatment_type_id=treatment.id,
            start_datetime=now + timedelta(hours=1),
            end_datetime=now + timedelta(hours=2),
        ),
        current_user=admin,
    )

    with pytest.raises(HTTPException):
        service.create(
            db,
            data=AppointmentCreate(
                client_id=profile.id,
                worker_id=worker.id,
                treatment_type_id=treatment.id,
                start_datetime=now + timedelta(hours=1, minutes=30),
                end_datetime=now + timedelta(hours=2, minutes=30),
            ),
            current_user=admin,
        )


def test_create_in_past_blocked_for_non_admin(db: Session):
    admin, worker, profile, treatment = _seed_users_and_patient(db)
    now = datetime(2024, 1, 1, 10, 0, 0)
    service = AppointmentService(now_provider=lambda: now)

    with pytest.raises(HTTPException):
        service.create(
            db,
            data=AppointmentCreate(
                client_id=profile.id,
                worker_id=worker.id,
                treatment_type_id=treatment.id,
                start_datetime=now - timedelta(hours=2),
                end_datetime=now - timedelta(hours=1),
            ),
            current_user=worker,
        )


def test_admin_past_requires_done_or_no_show(db: Session):
    admin, worker, profile, treatment = _seed_users_and_patient(db)
    now = datetime(2024, 1, 1, 10, 0, 0)
    service = AppointmentService(now_provider=lambda: now)

    with pytest.raises(HTTPException):
        service.create(
            db,
            data=AppointmentCreate(
                client_id=profile.id,
                worker_id=worker.id,
                treatment_type_id=treatment.id,
                start_datetime=now - timedelta(hours=2),
                end_datetime=now - timedelta(hours=1),
                status=AppointmentStatus.pending,
            ),
            current_user=admin,
        )


def test_create_outside_hours_blocked(db: Session):
    admin, worker, profile, treatment = _seed_users_and_patient(db)
    now = datetime(2024, 1, 1, 7, 0, 0)
    service = AppointmentService(now_provider=lambda: now)

    with pytest.raises(HTTPException):
        service.create(
            db,
            data=AppointmentCreate(
                client_id=profile.id,
                worker_id=worker.id,
                treatment_type_id=treatment.id,
                start_datetime=now,
                end_datetime=now + timedelta(hours=1),
            ),
            current_user=admin,
        )


def test_create_on_weekend_blocked(db: Session):
    admin, worker, profile, treatment = _seed_users_and_patient(db)
    saturday = datetime(2024, 1, 6, 10, 0, 0)
    service = AppointmentService(now_provider=lambda: saturday - timedelta(days=1))

    with pytest.raises(HTTPException):
        service.create(
            db,
            data=AppointmentCreate(
                client_id=profile.id,
                worker_id=worker.id,
                treatment_type_id=treatment.id,
                start_datetime=saturday,
                end_datetime=saturday + timedelta(hours=1),
            ),
            current_user=admin,
        )


def test_worker_cannot_mark_future_as_done(db: Session):
    admin, worker, profile, treatment = _seed_users_and_patient(db)
    now = datetime(2024, 1, 1, 10, 0, 0)
    service = AppointmentService(now_provider=lambda: now)

    appt = service.create(
        db,
        data=AppointmentCreate(
            client_id=profile.id,
            worker_id=worker.id,
            treatment_type_id=treatment.id,
            start_datetime=now + timedelta(hours=2),
            end_datetime=now + timedelta(hours=3),
        ),
        current_user=admin,
    )

    with pytest.raises(HTTPException):
        service.change_status(db, appt.id, data=AppointmentUpdate(status=AppointmentStatus.done), current_user=worker)


def test_worker_can_confirm_pending(db: Session):
    admin, worker, profile, treatment = _seed_users_and_patient(db)
    now = datetime(2024, 1, 1, 10, 0, 0)
    service = AppointmentService(now_provider=lambda: now)

    appt = service.create(
        db,
        data=AppointmentCreate(
            client_id=profile.id,
            worker_id=worker.id,
            treatment_type_id=treatment.id,
            start_datetime=now + timedelta(hours=1),
            end_datetime=now + timedelta(hours=2),
        ),
        current_user=admin,
    )

    updated = service.change_status(
        db,
        appt.id,
        data=AppointmentUpdate(status=AppointmentStatus.confirmed),
        current_user=worker,
    )
    assert updated.status == AppointmentStatus.confirmed


def test_client_can_cancel_own_future_pending(db: Session):
    admin, worker, profile, treatment = _seed_users_and_patient(db)
    now = datetime(2024, 1, 1, 10, 0, 0)
    service = AppointmentService(now_provider=lambda: now)

    appt = service.create(
        db,
        data=AppointmentCreate(
            client_id=profile.id,
            worker_id=worker.id,
            treatment_type_id=treatment.id,
            start_datetime=now + timedelta(hours=2),
            end_datetime=now + timedelta(hours=3),
        ),
        current_user=admin,
    )

    updated = service.change_status(
        db,
        appt.id,
        data=AppointmentUpdate(status=AppointmentStatus.cancelled_by_client),
        current_user=profile.user,
    )
    assert updated.status == AppointmentStatus.cancelled_by_client


def test_client_cannot_confirm_pending(db: Session):
    admin, worker, profile, treatment = _seed_users_and_patient(db)
    now = datetime(2024, 1, 1, 10, 0, 0)
    service = AppointmentService(now_provider=lambda: now)

    appt = service.create(
        db,
        data=AppointmentCreate(
            client_id=profile.id,
            worker_id=worker.id,
            treatment_type_id=treatment.id,
            start_datetime=now + timedelta(hours=1),
            end_datetime=now + timedelta(hours=2),
        ),
        current_user=admin,
    )

    with pytest.raises(HTTPException):
        service.change_status(
            db,
            appt.id,
            data=AppointmentUpdate(status=AppointmentStatus.confirmed),
            current_user=profile.user,
        )


def test_client_cannot_change_status_of_other(db: Session):
    admin, worker, profile, treatment = _seed_users_and_patient(db)
    now = datetime(2024, 1, 1, 10, 0, 0)
    service = AppointmentService(now_provider=lambda: now)

    other_client_user = User(first_name="Other", last_name="Client", email="other@test.com", hashed_password="x", role="client", is_active=True)
    db.add(other_client_user)
    db.commit()
    db.refresh(other_client_user)

    appt = service.create(
        db,
        data=AppointmentCreate(
            client_id=profile.id,
            worker_id=worker.id,
            treatment_type_id=treatment.id,
            start_datetime=now + timedelta(hours=2),
            end_datetime=now + timedelta(hours=3),
        ),
        current_user=admin,
    )

    with pytest.raises(HTTPException):
        service.change_status(
            db,
            appt.id,
            data=AppointmentUpdate(status=AppointmentStatus.cancelled_by_client),
            current_user=other_client_user,
        )


def test_reschedule_past_appointment_blocked_for_worker(db: Session):
    admin, worker, profile, treatment = _seed_users_and_patient(db)
    now = datetime(2024, 1, 2, 10, 0, 0)
    service = AppointmentService(now_provider=lambda: now)

    appt = service.create(
        db,
        data=AppointmentCreate(
            client_id=profile.id,
            worker_id=worker.id,
            treatment_type_id=treatment.id,
            start_datetime=now - timedelta(hours=2),
            end_datetime=now - timedelta(hours=1),
            status=AppointmentStatus.done,
        ),
        current_user=admin,
    )

    with pytest.raises(HTTPException):
        service.reschedule(
            db,
            appointment_id=appt.id,
            data=AppointmentReschedule(start_datetime=now, end_datetime=now + timedelta(hours=1)),
            current_user=worker,
        )
