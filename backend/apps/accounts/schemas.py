from typing import Optional
from django.forms import ValidationError
from pydantic import BaseModel, EmailStr, field_validator
from apps.accounts.models import User, UserRole


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class RefreshSchema(BaseModel):
    refresh: str


class TokenResponse(BaseModel):
    access: str
    refresh: str
    user: dict


class UserSchema(BaseModel):
    id: str
    email: str
    role: str
    is_active: bool
    created_at: str
    
    class Config:
        from_attributes = True


class PasswordChangeSchema(BaseModel):
    old_password: str
    new_password: str
    
    @field_validator('new_password')
    def password_min_length(cls, v):
        if len(v) < 8:
            raise ValidationError('Password must be at least 8 characters')
        return v