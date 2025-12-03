from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.main import app
from app.core.dependencies import get_db


def _get_test_db():
    engine = create_engine("sqlite:///:memory:", future=True)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db: Session = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_health_check():
    app.dependency_overrides[get_db] = _get_test_db
    client = TestClient(app)
    resp = client.get("/api/v1/health")
    app.dependency_overrides.clear()
    assert resp.status_code == 200
    data = resp.json()
    assert "status" in data
    assert "db" in data
