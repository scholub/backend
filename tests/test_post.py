from typing import final

from fastapi import HTTPException
from pytest import raises

from libraries.auth import Data, login_dep, register_jwt, verify_jwt
from libraries.initalizer import db
from queries.post import insert_post
from queries.tests import get_reaction
from queries.user import GetUserByEmailResult
from routers.post import get_post, reaction_post
from routers.user import confirm


async def query(command: str):
  return await db.execute(command) # pyright: ignore[reportUnknownMemberType]

class TestGet:
  async def test_init(self):
    await query("delete Paper::Post;")
    _ = await insert_post(
      db,
      title="A",
      description="A",
      paper_id="A",
      category="A",
      tag="A"
    )
  
  async def test_get(self):
    with raises(HTTPException):
      _ = await get_post("B")
    resp = await get_post("A")
    assert resp.title == "A"
    assert resp.description == "A"
    assert resp.paper_id == "A"
    assert resp.category == "A"
    assert resp.tag == "A"

@final
class TestReaction:
  def __init__(self):
    self.user: GetUserByEmailResult
    self.user2: GetUserByEmailResult
  
  async def TestInit(self):
    await query("delete Paper::Reaction;")
    await query("delete User;")
    _ = verify_jwt(await confirm(
      register_jwt(Data(
        name="test",
        email="test@example.com",
        confirmed=False
      )),
      "12345678"
    ), True)
    _ = verify_jwt(await confirm(
      register_jwt(Data(
        name="test2",
        email="test2@example.com",
        confirmed=False
      )),
      "12345678"
    ), True)
  
  async def TestLoginDep(self):
    with raises(HTTPException):
      _ = await login_dep(None)
    with raises(HTTPException):
      _ = await login_dep(register_jwt(Data(
        name="test2",
        email="test2@example.com",
        confirmed=False
      )))
    with raises(HTTPException):
      _ = await login_dep(register_jwt(Data(
        name="test3",
        email="test3@example.com",
        confirmed=True
      )))
    self.user = await login_dep(register_jwt(Data(
      name="test",
      email="test@example.com",
      confirmed=True
    )))
    assert self.user.name == "test"
    assert self.user.email == "test2example.com"
    self.user2 = await login_dep(register_jwt(Data(
      name="test2",
      email="test2@example.com",
      confirmed=True
    )))
    assert self.user2.name == "test2"
    assert self.user2.email == "test2@example.com"

  async def TestReactionNormalSingle(self):
    with raises(HTTPException):
      await reaction_post(
        paper_id="B",
        like=False,
        user=self.user
      )
    await reaction_post(
      paper_id="A",
      like=False,
      user=self.user
    )
    react = await get_reaction(db, paper_id="A")
    assert react is not None
    assert react.dislike_count == 1
    with raises(HTTPException):
      await reaction_post(
        paper_id="B",
        like=True,
        user=self.user
      )
    await reaction_post(
      paper_id="A",
      like=True,
      user=self.user
    )
    react = await get_reaction(db, paper_id="A")
    assert react is not None
    assert react.like_count == 1
    assert react.dislike_count == 0
