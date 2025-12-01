from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import decode_token
from app.db.session import SessionLocal
from app.crud import user as crud_user
from app.schemas.user import UserInDB

security_scheme = HTTPBearer(auto_error=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security_scheme), db: Session = Depends(get_db)):
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = credentials.credentials
    user_id = decode_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    db_user = crud_user.get(db, int(user_id))
    if not db_user or not db_user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive or not found user")
    return db_user


def get_current_user(db_user=Depends(_get_current_user)):
    return db_user


def get_current_admin(db_user=Depends(_get_current_user)):
    if db_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")
    return db_user


def get_current_worker(db_user=Depends(_get_current_user)):
    if db_user.role != "worker":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Worker privileges required")
    return db_user


def get_current_client(db_user=Depends(_get_current_user)):
    if db_user.role != "client":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Client privileges required")
    return db_user
