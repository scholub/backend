from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Cookie, Depends, HTTPException, status
from satellite_py import generate_error_responses

from libraries.auth import verify_jwt
from libraries.initalizer import db
from queries.post import get_comment as db_get_comment
from queries.post import get_post as db_get_post
from queries.post import post_comment, reaction
from queries.user import GetUserByEmailResult, get_user_by_email

router = APIRouter(prefix="/post", tags=["post"])

async def login_dep(auth: Annotated[str | None, Cookie()] = None):
  if auth is None:
    raise HTTPException(status.HTTP_401_UNAUTHORIZED)
  data = verify_jwt(auth)
  if data is None:
    raise HTTPException(status.HTTP_401_UNAUTHORIZED)
  user = await get_user_by_email(db, email=data.email)
  if user is None:
    raise HTTPException(status.HTTP_401_UNAUTHORIZED)
  return user
cookieDep = Annotated[GetUserByEmailResult, Depends(login_dep)]

@router.get("/{post_id}", responses=generate_error_responses({404}))
async def get_post(post_id: UUID):
  resp = await db_get_post(db, id=post_id)
  if resp is None:
    raise HTTPException(status.HTTP_404_NOT_FOUND)
  return resp

@router.post("/{post_id}/reaction", responses=generate_error_responses({401, 404}))
async def reaction_post(
  post_id: UUID,
  like: Annotated[bool, Body(description="if true do like, else dislike")],
  user: cookieDep
):
  resp = await reaction(db, user_id=user.id, post_id=post_id, is_like=like)
  if resp is None:
    raise HTTPException(status.HTTP_404_NOT_FOUND)

@router.delete("/{post_id}/reaction", responses=generate_error_responses({401, 404}))
async def reaction_delete(
  post_id: UUID,
  user: cookieDep
):
  resp = await delete_reaction(db, user_id=user.id, post_id=post_id)
  if resp is None:
    raise HTTPException(status.HTTP_404_NOT_FOUND)

@router.get("/{post_id}/comment", responses=generate_error_responses({404}))
async def get_comment(post_id: UUID):
  resp = await db_get_comment(db, post_id=post_id)
  if resp is None:
    raise HTTPException(status.HTTP_404_NOT_FOUND)
  return resp

@router.post("/{post_id}/comment", responses=generate_error_responses({401, 404}))
async def comment(
  post_id: UUID,
  content: str,
  user: cookieDep
):
  post = await post_comment(db, content=content, post_id=post_id, user_id=user.id)
  if post is None:
    raise HTTPException(status.HTTP_404_NOT_FOUND)

