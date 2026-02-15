from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.ext.asyncio import AsyncSession
from .. import crud, schemas, auth
from ..db import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=schemas.UserRead)
async def register(user_in: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await crud.get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = auth.get_password_hash(user_in.password)
    user = await crud.create_user(db, user_in.email, hashed, user_in.full_name)
    return user


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    username: str = Form(...), password: str = Form(...), db: AsyncSession = Depends(get_db)
):
    user = await crud.get_user_by_email(db, username)
    if not user or not auth.verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password")
    access = auth.create_access_token(user.email)
    refresh = auth.create_refresh_token(user.email)
    return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}


@router.post("/refresh", response_model=schemas.Token)
async def refresh_token(refresh_token: str, db: AsyncSession = Depends(get_db)):
    try:
        payload = auth.jwt.decode(
            refresh_token, auth.settings.SECRET_KEY, algorithms=["HS256"])
        sub = payload.get("sub")
        if sub is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except auth.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = await crud.get_user_by_email(db, sub)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    access = auth.create_access_token(user.email)
    refresh = auth.create_refresh_token(user.email)
    return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}
