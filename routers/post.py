from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from libraries.initalizer import db
from queries.post import get_post as db_get_post

router = APIRouter(prefix="/post", tags=["post"])

@router.get("/{post_id}")
async def get_post(post_id: UUID):
  resp = await db_get_post(db, id=post_id)
  if resp is None:
    raise HTTPException(status.HTTP_404_NOT_FOUND)
  return resp
