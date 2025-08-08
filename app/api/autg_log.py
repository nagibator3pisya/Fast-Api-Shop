from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import JSONResponse

from app.api.auth import create_access_token, get_current_user, get_password_hash, authenticate_user, SECRET_KEY, \
    ALGORITHM
from app.deps.dependes import get_db
from app.model.models import User

from app.schemas.Token import Token
from app.schemas.User import UserCreate, UserOut
from app.services.service_auth import filter_user_to_db

aut_log = APIRouter(prefix="/auth", tags=["auth"])




@aut_log.post("/register", response_model=UserOut)
async def register(user: UserCreate, session: AsyncSession = Depends(get_db)):
    db_users = await filter_user_to_db(user=user, session=session)
    if db_users:
        if db_users.email == user.email:
            raise HTTPException(status_code=400, detail="Email уже зарегистрирован")
        if db_users.name == user.name:
            raise HTTPException(status_code=400, detail="Имя пользователя уже занято")

    hashed_password = get_password_hash(user.password)
    session_users = User(
        email=user.email,
        name=user.name,
        hashed_password=hashed_password
    )
    session.add(session_users)
    await session.commit()
    await session.refresh(session_users)
    return session_users


@aut_log.post("/login/", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_db)):
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(minutes=15))
    refresh_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(days=7))

    response = JSONResponse(content={"access_token": access_token, "token_type": "bearer"})
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=7 * 24 * 60 * 60,
        secure=False,  # True на проде
        samesite="lax",

    )
    return response



@aut_log.post('/refresh', response_model=Token)
async def refresh_token(refresh_token: str = Cookie(None)):
    print("Получен refresh_token:", refresh_token)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if refresh_token is None:
        raise credentials_exception

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    access_token = create_access_token(data={"sub": email})
    return {"access_token": access_token, "token_type": "bearer"}


# @aut_log.post("/login/", response_model=Token)
# async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_db)):
#     user = await authenticate_user(session, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#     access_token = create_access_token(data={"sub": user.email})
#     return {"access_token": access_token, "token_type": "bearer"}






@aut_log.get("/me", response_model=UserOut)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@aut_log.post("/logout")
async def logout():
    response = JSONResponse(content={"detail": "Logged out"})
    response.delete_cookie("refresh_token", path="/")  # удалит куку
    return response
