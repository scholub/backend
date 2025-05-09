from datetime import datetime, timedelta, timezone
from sys import modules

from jwt import decode, encode
from pydantic import BaseModel, EmailStr

from libraries.initalizer import SECRET_KEY


class Data(BaseModel):
  email: EmailStr
  confirmed: bool

def register_jwt(data: Data) -> str:
  _data = data.model_dump()
  _data["exp"] = int((datetime.now(timezone.utc) + timedelta(days=30)).timestamp())
  return encode(_data, SECRET_KEY, "HS512")

def verify_jwt(token: str, require_confirm: bool = False) -> Data | None:
  try:
    _data: dict[str, str | int] = decode( # pyright: ignore[reportAny]
      token,
      SECRET_KEY,
      ["HS512"],
      options={"verify_signature": True, "verify_exp": True, "require": [
        "exp", "email", "confirmed"
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
