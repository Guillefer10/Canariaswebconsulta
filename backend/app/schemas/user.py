from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime

from app.models.user import UserRole


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    role: UserRole
    is_active: bool = True

    @field_validator("first_name", "last_name")
    @classmethod
    def validate_names(cls, v: str) -> str:
        cleaned = v.strip()
        if not cleaned:
            raise ValueError("Name fields cannot be empty")
        return cleaned

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: EmailStr) -> EmailStr:
        return EmailStr(str(v).lower())


class UserCreate(UserBase):
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if v.isdigit() or v.isalpha():
            raise ValueError("Password must include letters and numbers or symbols")
        return v


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None


class UserRead(UserBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserInDB(UserRead):
    hashed_password: str
