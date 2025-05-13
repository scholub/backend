from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, HTTPException, status
from satellite_py import generate_error_responses

from libraries.initalizer import db
from queries.post import get_comment as db_get_comment
from queries.post import get_post as db_get_post

router = APIRouter(prefix="/post", tags=["post"])

@router.get("/{post_id}", responses=generate_error_responses({404}))
async def get_post(post_id: UUID):
  resp = await db_get_post(db, id=post_id)
  if resp is None:
    raise HTTPException(status.HTTP_404_NOT_FOUND)
  return resp

@router.post("/{post_id}/reaction", responses=generate_error_responses({404}))
async def reaction(
  post_id: UUID,
  like: Annotated[bool, Body(description="if true do like, else dislike")]
):
  if (await db_get_post(db, id=post_id)) is None:
    raise HTTPException(status.HTTP_404_NOT_FOUND)
  await reaction(post_id=post_id, like=like)

@router.get("/{post_id}/comment", responses=generate_error_responses({404}))
async def get_comment(post_id: UUID):
  resp = await db_get_comment(db, post_id=post_id)
  if resp is None:
    raise HTTPException(status.HTTP_404_NOT_FOUND)
  return resp

