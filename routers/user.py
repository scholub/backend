from os import getenv
from typing import Annotated

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import EmailStr
from satellite_py import generate_error_responses

from libraries.auth import Data, register_jwt, verify_jwt
from libraries.initalizer import db
from libraries.mailer import send_email
from queries.user import get_user_by_email, get_user_by_name, insert_user, update_password

router = APIRouter(prefix="/user", tags=["user"])

domain = getenv("ROOT_DOMAIN", "http://localhost:8080")
hasher = PasswordHasher()

@router.post("/register", responses=generate_error_responses({409}))
async def register(
  name: Annotated[str, Body(description="name of account")],
  email: Annotated[EmailStr, Body(description="email of account")]
):
  if (await get_user_by_email(db, email=email)) is not None:
    raise HTTPException(
      status.HTTP_409_CONFLICT,
      "email must be unique."
    )
  send_email(
    "Verification request from Scholub",
    f"{domain}/confirm?email={email}&jwt={register_jwt(Data(
      name=name,
      email=email,
      confirmed=False
    ))}",
    [email]
  )

@router.post("/confirm", responses=generate_error_responses({401, 400, 409}))
async def confirm(
  token: Annotated[str, Body(description="jwt token")],
  password: Annotated[str, Body(description="password of account")]
):
  data = verify_jwt(token, False)
  if data is None:
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, "token expired or invalid")
  if len(password) < 8:
    raise HTTPException(
      status.HTTP_400_BAD_REQUEST,
      "password must be at least 8 characters"
    )
  if (await get_user_by_name(db, name=data.name)) is not None:
    raise HTTPException(
      status.HTTP_409_CONFLICT,
      "name must be unique."
    )
  if (await get_user_by_email(db, email=data.email)) is not None:
    raise HTTPException(
      status.HTTP_409_CONFLICT,
      "email must be unique."
    )
  _ = await insert_user(db, name=data.name, email=data.email, password=hasher.hash(password))
  return register_jwt(Data(
    name=data.name,
    email=data.email,
    confirmed=True
  ))

@router.post("/login", responses=generate_error_responses({401}))
async def login(
  email: Annotated[EmailStr, Body(description="email of account")],
  password: Annotated[str, Body(description="password of account")]
):
  user = await get_user_by_email(db, email=email)
  if user is None:
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, "login failed")
  try:
    _ = hasher.verify(user.password, password)
    if hasher.check_needs_rehash(user.password):
      _ = update_password(db, email=email, password=hasher.hash(password))
  except VerifyMismatchError:
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, "login failed")
  return register_jwt(Data(name=user.name, email=email, confirmed=True))
