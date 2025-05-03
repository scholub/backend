from typing import Annotated
from os import getenv

from libraries.initalizer import db
from libraries.email import send_email

from libraries.jwt import Data, register_jwt, verify_jwt
from queries.get_user_async_edgeql import get_user
from queries.insert_user_async_edgeql import insert_user
from queries.update_hash_async_edgeql import update_hash

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import APIRouter, HTTPException, Header, status
from fastapi.responses import JSONResponse
from pydantic import EmailStr

router = APIRouter(prefix="/user", tags=["user"])

domain = getenv("ROOT_DOMAIN", "http://localhost:8080")
hasher = PasswordHasher()

@router.post("/register")
async def register(
  email: Annotated[EmailStr, Header(description="email of account")]
):
  if (await get_user(db, email=email)) is not None:
    raise HTTPException(
      status.HTTP_409_CONFLICT,
      "email must be unique."
    )
  send_email(
    "Verification request from Scholub",
    f"{domain}/confirm?email={email}&jwt={register_jwt(Data(email=email))}",
    [email]
  )

@router.post("/confirm")
async def confirm(
  token: Annotated[str, Header(description="jwt token")],
  password: Annotated[str, Header(description="password of account")]
):
  data = verify_jwt(token)
  if data is None:
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, "token expired or invalid")
  if len(password) < 8:
    raise HTTPException(
      status.HTTP_400_BAD_REQUEST,
      "password must be at least 8 characters"
    )
  if (await get_user(db, email=data.email)) is not None:
    raise HTTPException(
      status.HTTP_409_CONFLICT,
      "email must be unique."
    )
  _ = await insert_user(db, email=data.email, password=hasher.hash(password))

@router.post("/login")
async def login(
  email: Annotated[EmailStr, Header(description="email of account")],
  password: Annotated[str, Header(description="password of account")]
):
  user = await get_user(db, email=email)
  if user is None:
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, "login failed")
  try:
    _ = hasher.verify(user.password, password)
    if hasher.check_needs_rehash(user.password):
      _ = update_hash(db, email=email, password=hasher.hash(password))
  except VerifyMismatchError:
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, "login failed")
  return register_jwt(Data(email=email))
