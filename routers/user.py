import re
from asyncio import sleep
from os import getenv
from typing import Annotated

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import APIRouter, Body, HTTPException, WebSocket, status
from pydantic import BaseModel, EmailStr
from satellite_py import generate_error_responses

from libraries.auth import Data, cookieDep, register_jwt, verify_jwt
from libraries.initalizer import db
from libraries.mailer import send_email
from queries.user import (
  get_user_by_email,
  get_user_by_name,
  insert_user,
  update_password,
)

router = APIRouter(prefix="/user", tags=["user"])

domain = getenv("ROOT_DOMAIN", "http://localhost:8080")
hasher = PasswordHasher()
confirmed: set[str] = set()

class VerifyReturn(BaseModel):
  name: str
  email: EmailStr
  bookmarks: list[str]

@router.websocket("/register")
async def register(ws: WebSocket):
  await ws.accept()
  email = await ws.receive_text()
  email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
  if not re.match(email_regex, email):
    await ws.send_json({"status": 400, "data": "email isn't valid"})
    await ws.close()
    return
  if (await get_user_by_email(db, email=email)) is not None:
    await ws.send_json({"status": 409, "data": "user already exist"})
    await ws.close()
    return
  send_email(
    "Verification request from Scholub",
    f"{domain}/user/confirm?token={register_jwt(Data(
      name='',
      email=email,
      confirmed=False
    ))}",
    [email]
  )
  while True:
    if email in confirmed:
      confirmed.remove(email)
      await ws.send_json({"status": 200, "data": register_jwt(Data(
        name='',
        email=email,
        confirmed=True
      ))})
      await ws.close()
    await sleep(1)

@router.get("/confirm", responses=generate_error_responses({401}))
async def confirm(
  token: str
):
  data = verify_jwt(token, False)
  if data is None:
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, "token expired or invalid")
  confirmed.add(data.email)

@router.post("/register", responses=generate_error_responses({401, 400, 409}))
async def register_final(
  token: Annotated[str, Body(description="jwt token")],
  name: Annotated[str, Body(description="name")],
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
  if (await get_user_by_name(db, name=name)) is not None:
    raise HTTPException(
      status.HTTP_409_CONFLICT,
      "name must be unique."
    )
  if (await get_user_by_email(db, email=data.email)) is not None:
    raise HTTPException(
      status.HTTP_409_CONFLICT,
      "email must be unique."
    )
  _ = await insert_user(db, name=name, email=data.email, password=hasher.hash(password))
  return register_jwt(Data(
    name=name,
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

@router.get("/verify", responses=generate_error_responses({401}))
async def verify(
  user: cookieDep
) -> VerifyReturn:
  return VerifyReturn(
    name=user.name,
    email=user.email,
    bookmarks=[i.paper_id for i in user.bookmarks]
  )
