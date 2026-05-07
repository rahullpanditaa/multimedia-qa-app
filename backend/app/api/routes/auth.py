from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.models.user import User

from app.schemas.auth import (
    UserLogin,
    UserRegister,
)

from app.services.auth_service import (
    create_access_token,
    hash_password,
    verify_password,
)

router = APIRouter(prefix="/auth", tags=["auth"])

# register
@router.post("/register")
def register(payload: UserRegister, db: Session = Depends(get_db)):
    existing_user = (
        db.query(User)
        .filter(User.username == payload.username
        ).first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists.",
        )

    user = User(
        username=payload.username,
        hashed_password=
            hash_password(
                payload.password
            ),
    )

    db.add(user)

    db.commit()

    return {"message": "User created successfully."}

# login
@router.post("/login")
def login(payload: UserLogin, db: Session = Depends(get_db),):
    user = (
        db.query(User)
        .filter(User.username == payload.username
        ).first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials.",
        )

    if not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials.",
        )

    token = create_access_token(
        {
            "sub": user.username
        }
    )

    return {
        "access_token": token
    }