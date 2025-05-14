from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Cookie, HTTPException, status
from satellite_py import generate_error_responses

from libraries.auth import verify_jwt
from libraries.initalizer import db
from queries.post import get_comment as db_get_comment
from queries.post import get_post as db_get_post
from queries.post import reaction
from queries.user import get_user_by_email

router = APIRouter(prefix="/post", tags=["post"])

@router.get("/{post_id}", responses=generate_error_responses({404}))
async def get_post(post_id: UUID):
  resp = await db_get_post(db, id=post_id)
  if resp is None:
    raise HTTPException(status.HTTP_404_NOT_FOUND)
  return resp

@router.post("/{post_id}/reaction", responses=generate_error_responses({404}))
async def reaction_post(
  post_id: UUID,
  like: Annotated[bool, Body(description="if true do like, else dislike")],
  auth: Annotated[str | None, Cookie()]
):
  if auth is None:
    raise HTTPException(status.HTTP_400_BAD_REQUEST)
  data = verify_jwt(auth)
  if data is None:
    raise HTTPException(status.HTTP_400_BAD_REQUEST)
  user = await get_user_by_email(db, email=data.email)
  if user is None:
    raise HTTPException(status.HTTP_400_BAD_REQUEST)
  if (await db_get_post(db, id=post_id)) is None:
    raise HTTPException(status.HTTP_404_NOT_FOUND)
  _ = await reaction(db, user_id=user.id, post_id=post_id, is_like=like)

@router.get("/{post_id}/comment", responses=generate_error_responses({404}))
async def get_comment(post_id: UUID):
  resp = await db_get_comment(db, post_id=post_id)
  if resp is None:
    raise HTTPException(status.HTTP_404_NOT_FOUND)
  return resp

