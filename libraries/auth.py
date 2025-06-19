from datetime import datetime, timedelta, timezone
from sys import modules
from typing import Annotated

from fastapi import Depends, Header, HTTPException
from jwt import decode, encode
from pydantic import BaseModel, EmailStr
from starlette import status

from libraries.initalizer import SECRET_KEY, db
from queries.user import GetUserByEmailResult, get_user_by_email


class Data(BaseModel):
  name: str
  email: EmailStr
  confirmed: bool

def register_jwt(data: Data) -> str:
  _data = data.model_dump()
  _data["exp"] = int((datetime.now(timezone.utc) + timedelta(days=30)).timestamp())
  return encode(_data, SECRET_KEY, "HS512")

def verify_jwt(token: str, require_confirm: bool = True) -> Data | None:
  try:
    _data: dict[str, str | int] = decode( # pyright: ignore[reportAny]
      token,
      SECRET_KEY,
      ["HS512"],
      options={"verify_signature": True, "verify_exp": True, "require": [
        "exp", "email", "name", "confirmed"
      ]},
    )
    data = Data.model_validate(_data)
    if require_confirm and not data.confirmed:
      return None
    return data
  except Exception as e:
    if "pytest" in modules:
      raise e
    return None

async def login_dep(token: Annotated[str | None, Header(description="jwt token")] = None):
  if token is None:
    raise HTTPException(status.HTTP_401_UNAUTHORIZED)
  data = verify_jwt(token)
  if data is None:
    raise HTTPException(status.HTTP_401_UNAUTHORIZED)
  user = await get_user_by_email(db, email=data.email)
  if user is None:
    raise HTTPException(status.HTTP_401_UNAUTHORIZED)
  return user
cookieDep = Annotated[GetUserByEmailResult, Depends(login_dep)]

