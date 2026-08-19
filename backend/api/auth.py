from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from database.crud import (
    create_user,
    get_user_by_email
)


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


# =========================================================
# REQUEST MODELS
# =========================================================

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


# =========================================================
# REGISTER
# =========================================================

@router.post("/register")
def register_user(data: RegisterRequest):

    if not data.name.strip():
        raise HTTPException(
            status_code=400,
            detail="Name is required."
        )

    if not data.email.strip():
        raise HTTPException(
            status_code=400,
            detail="Email is required."
        )

    if len(data.password) < 6:
        raise HTTPException(
            status_code=400,
            detail="Password must contain at least 6 characters."
        )

    existing_user = get_user_by_email(
        data.email
    )

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="An account with this email already exists."
        )

    user_id = create_user(
        name=data.name.strip(),
        email=data.email.strip().lower(),
        password=data.password
    )

    return {
        "success": True,
        "message": "Account created successfully.",
        "user": {
            "id": user_id,
            "name": data.name.strip(),
            "email": data.email.strip().lower()
        }
    }


# =========================================================
# LOGIN
# =========================================================

@router.post("/login")
def login_user(data: LoginRequest):

    user = get_user_by_email(
        data.email.strip().lower()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    if user["password"] != data.password:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    return {
        "success": True,
        "message": "Login successful.",
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"]
        }
    }