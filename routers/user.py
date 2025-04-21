from collections import defaultdict
from typing import Annotated
from uuid import UUID, uuid4
from datetime import datetime
from os import getenv

from libraries.initalizer import db, scheduler
from libraries.email import send_email

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
sessions: defaultdict[str, set[UUID]] = defaultdict(lambda: set())
emails: defaultdict[str, set[UUID]] = defaultdict(lambda: set())

def issue_session(name: str, sessions: defaultdict[str, set[UUID]]) -> UUID:
  session = uuid4()
  sessions[name].add(session)
  _ = scheduler.add_job( # pyright: ignore[reportUnknownMemberType]
    lambda: sessions[name].remove(session) if len(sessions[name]) != 1 else sessions.__delitem__(name),
    "date",
    run_date=datetime.now().isoformat()
  )
  return session

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
    f"{domain}/confirm?email={email}&session={issue_session(email, emails)}",
    [email]
  )

@router.post("/confirm")
async def confirm(
  email: Annotated[str, Header(description="email of account")],
  password: Annotated[str, Header(description="password of account")],
  session: Annotated[str, Header(description="session of email verification request")]
):
  if len(password) < 8:
    raise HTTPException(
      status.HTTP_400_BAD_REQUEST,
      "password must be at least 8 characters"
    )
  if (await get_user(db, email=email)) is not None:
    raise HTTPException(
      status.HTTP_409_CONFLICT,
      "email must be unique."
    )
  if session not in emails[email]:
    raise HTTPException(
      status.HTTP_400_BAD_REQUEST,
      "link doesn't exist"
    )
  _ = await insert_user(db, email=email, password=hasher.hash(password))

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
  return JSONResponse({"session": str(issue_session(email, sessions))})
