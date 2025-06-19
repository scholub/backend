from fastapi import HTTPException
from jwt import DecodeError
from pytest import raises

from libraries.auth import Data, register_jwt, verify_jwt
from libraries.initalizer import db
from routers.user import confirm, login


class TestInvalid:
  async def test_init(self):
    await db.execute("delete User;") # pyright: ignore[reportUnknownMemberType]

  async def test_invalid_login(self):
    with raises(HTTPException):
      _ = await login("invalid", "invalid")
    with raises(HTTPException):
      _ = await login("invalid@gmail.com", "invalid")

  async def test_invalid_confirm(self):
    with raises(DecodeError):
      _ = await confirm("invalid", "invalid")
    with raises(HTTPException):
      _ = await confirm(register_jwt(
        Data(
          name="test",
          email="test@example.com",
          confirmed=False
        )
      ), "123456")


class TestValidAndPartiallyValid:
  async def test_confirm(self):
    data = verify_jwt(await confirm(
      register_jwt(Data(
        name="test",
        email="test@example.com",
        confirmed=False
      )),
      "12345678"
    ), True)
    assert data is not None
    assert data.email == "test@example.com"
    assert data.confirmed is True
    with raises(HTTPException):
      _ = await confirm(
        register_jwt(Data(
          name="test",
          email="test@example.com",
          confirmed=False
        )),
        "12345678"
      )
    with raises(HTTPException):
      _ = await confirm(
        register_jwt(Data(
          name="test",
          email="test2@example.com",
          confirmed=False
        )),
        "12345678"
      )
    with raises(HTTPException):
      _ = await confirm(
        register_jwt(Data(
          name="test2",
          email="test@example.com",
          confirmed=False
        )),
        "12345678"
      )
  
  async def test_login(self):
    with raises(HTTPException):
      _ = await login("test@example.com", "1234567")
    data = verify_jwt(
      await login("test@example.com", "12345678"),
      True
    )
    assert data is not None
    assert data.email == "test@example.com"
    assert data.confirmed is True

