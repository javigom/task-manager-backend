from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List, Optional
from datetime import datetime
import re


class UserCreate(BaseModel):
    email: EmailStr
    # bcrypt has a 72-byte input limit; validate against UTF-8 byte length.
    password: str = Field(..., min_length=8, max_length=72)
    full_name: Optional[str] = None

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password strength."""
        # enforce bcrypt byte-length limit
        try:
            byte_len = len(v.encode('utf-8'))
        except Exception:
            raise ValueError('Invalid password encoding')
        if byte_len > 72:
            raise ValueError(
                'Password is too long (max 72 bytes when UTF-8 encoded)')
        if not re.search(r'[A-Z]', v):
            raise ValueError(
                'Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError(
                'Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        return v


class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None


class TaskRead(BaseModel):
    id: int
    title: str
    description: Optional[str]
    owner_id: int
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}
