from fastapi import HTTPException, status

from app.models.user import User


def ensure_worker(user: User):
    if user.role != "worker":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Assigned user must be a worker")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Assigned worker must be active")
