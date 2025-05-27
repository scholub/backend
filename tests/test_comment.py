from typing import final
from uuid import UUID

from fastapi import HTTPException
from gel import AsyncIOExecutor
from pytest import raises

from libraries.auth import Data, login_dep, register_jwt, verify_jwt
from libraries.initalizer import db
from queries.comment import reaction
from queries.post import insert_post
from queries.tests import get_comment_reaction as db_get_reaction
from queries.user import GetUserByEmailResult
from routers.user import confirm
from routers.post import get_comment, comment as post_comment


async def get_reaction(db: AsyncIOExecutor, id: UUID):
  react = await db_get_reaction(db, id=id)
  assert react is not None
  return react

async def query(command: str):
  return await db.execute(command) # pyright: ignore[reportUnknownMemberType]

class TestBasic:
  def __init__(self):
    self.user: GetUserByEmailResult

  async def test_init(self):
    await query("delete Comment::Comment")
    _ = await insert_post(
      db,
      title="A",
      description="A",
      paper_id="A",
      category="A",
      tag="A"
    )
    self.user = await login_dep(register_jwt(Data(
      name="test",
      email="test@example.com",
      confirmed=True
    )))

  async def test_comment(self):
    with raises(HTTPException):
      await post_comment(
        paper_id="B",
        content="A",
        user=self.user
      )
    await post_comment(
      paper_id="A",
      content="A",
      user=self.user
    )
    comments = await get_comment("A")
    assert len(comments) == 1
    assert comments[0].content == "A"
    assert comments[0].user.email == self.user.email

@final
class TestReaction:
  def __init__(self):
    self.user: GetUserByEmailResult
    self.user2: GetUserByEmailResult
  
  async def TestInit(self):
    await query("delete Comment::Reaction;")
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
    assert (await get_reaction(db, paper_id="A")).dislike_count == 1
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
    assert react.like_count == 1
    assert react.dislike_count == 0

  async def TestDuplicatedReaction(self):
    await reaction_post(
      paper_id="A",
      like=True,
      user=self.user
    )
    react = await get_reaction(db, paper_id="A")
    assert react.like_count == 1
    assert react.dislike_count == 0

  async def TestReactionMultiple(self):
    await reaction_post(paper_id="A", like=True, user=self.user2)
    assert (await get_reaction(db, paper_id="A")).like_count == 2
    await reaction_post(paper_id="A", like=False, user=self.user)
    react = await get_reaction(db, paper_id="A")
    assert react.dislike_count == 1
    assert react.like_count == 1
