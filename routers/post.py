from typing import Annotated

from fastapi import APIRouter, Header, HTTPException, status
from satellite_py import generate_error_responses

from libraries.auth import cookieDep
from libraries.initalizer import db
from queries.comment import post_comment
from queries.post import (
  GetCommentResultCommentsItem,
  GetPostListResult,
  GetPostResult,
  delete_reaction,
  insert_bookmark,
  reaction,
  select_reaction,
)
from queries.post import delete_bookmark as db_delete_bookmark
from queries.post import get_comment as db_get_comment
from queries.post import get_post as db_get_post
from queries.post import get_post_list as db_get_post_list

router = APIRouter(prefix="/post", tags=["post"])

@router.get("", responses=generate_error_responses({404}))
async def get_post_list() -> list[GetPostListResult]:
  return await db_get_post_list(db)

@router.get("/{paper_id}", responses=generate_error_responses({404}))
async def get_post(paper_id: str) -> GetPostResult:
  resp = await db_get_post(db, paper_id=paper_id)
  if resp is None:
    raise HTTPException(status.HTTP_404_NOT_FOUND)
  return resp

@router.get("/{paper_id}/reaction", responses=generate_error_responses({401, 404}))
async def reaction_get(
  paper_id: str,
  user: cookieDep
):
  resp = await select_reaction(db, paper_id=paper_id, user_id=user.id)
  if resp is None:
    return None
  return resp.is_like

@router.post("/{paper_id}/reaction", responses=generate_error_responses({401, 404}))
async def reaction_post(
  paper_id: str,
  like: Annotated[bool, Header(description="if true do like, else dislike")],
  user: cookieDep
):
  resp = await reaction(db, user_id=user.id, paper_id=paper_id, is_like=like)
  if resp is None:
    raise HTTPException(status.HTTP_404_NOT_FOUND)

@router.delete("/{paper_id}/reaction", responses=generate_error_responses({401, 404}))
async def reaction_delete(
  paper_id: str,
  user: cookieDep
):
  resp = await delete_reaction(db, user_id=user.id, paper_id=paper_id)
  if resp is None:
    raise HTTPException(status.HTTP_404_NOT_FOUND)

@router.get("/{paper_id}/comment", responses=generate_error_responses({404}))
async def get_comment(paper_id: str) -> list[GetCommentResultCommentsItem]:
  resp = await db_get_comment(db, paper_id=paper_id)
  if resp is None:
    raise HTTPException(status.HTTP_404_NOT_FOUND)
  return resp.comments

@router.post("/{paper_id}/comment", responses=generate_error_responses({401, 404}))
async def comment(
  paper_id: str,
  content: str,
  user: cookieDep
):
  post = await post_comment(db, content=content, paper_id=paper_id, user_id=user.id)
  if post is None:
    raise HTTPException(status.HTTP_404_NOT_FOUND)

@router.post("/{paper_id}/bookmark", responses=generate_error_responses({401, 404}))
async def bookmark(user: cookieDep, paper_id: str):
  resp = await insert_bookmark(db, paper_id=paper_id, email=user.email)
  if resp is None:
    raise HTTPException(status.HTTP_404_NOT_FOUND)
  return resp

@router.delete("/{paper_id}/bookmark", responses=generate_error_responses({401, 404}))
async def delete_bookmark(user: cookieDep, paper_id: str):
  _ = await db_delete_bookmark(db, paper_id=paper_id, email=user.email)

