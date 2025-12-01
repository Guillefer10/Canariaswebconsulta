from typing import Optional
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, obj_in: UserCreate) -> User:
        obj_data = obj_in.model_dump(exclude={"password"})
        db_obj = User(**obj_data, hashed_password=hash_password(obj_in.password))
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: User, obj_in: UserUpdate | dict) -> User:
        update_data = obj_in if isinstance(obj_in, dict) else obj_in.model_dump(exclude_unset=True)
        if "password" in update_data and update_data["password"]:
            update_data["hashed_password"] = hash_password(update_data.pop("password"))
        return super().update(db, db_obj, update_data)


def _get_user_crud() -> CRUDUser:
    return CRUDUser(User)


crud_user = _get_user_crud()
