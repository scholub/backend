from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, HTTPException, status
from satellite_py import generate_error_responses

from libraries.auth import cookieDep
from libraries.initalizer import db
from queries.comment import delete_comment, delete_reaction, get_comment, reaction

router = APIRouter(prefix="/comment", tags=["comment"])

@router.post("/{comment_id}/reaction", responses=generate_error_responses({401, 404}))
async def reaction_comment(
  comment_id: UUID,
  like: Annotated[bool, Body(description="if true do like, else dislike")],
  user: cookieDep
):
  resp = await reaction(db, user_id=user.id, comment_id=comment_id, is_like=like)
  if resp is None:
    raise HTTPException(status.HTTP_404_NOT_FOUND)

@router.delete("/{comment_id}/reaction", responses=generate_error_responses({401, 404}))
async def reaction_delete(
  comment_id: UUID,
  user: cookieDep
):
  resp = await delete_reaction(db, user_id=user.id, comment_id=comment_id)
  if resp is None:
    raise HTTPException(status.HTTP_404_NOT_FOUND)

@router.delete("/{comment_id}", responses=generate_error_responses({401, 403, 404}))
async def delete(
  comment_id: UUID,
  user: cookieDep
):
  comment = await get_comment(db, id=comment_id)
  if comment is None:
    raise HTTPException(status.HTTP_404_NOT_FOUND)
  if comment.user.id != user.id:
    raise HTTPException(status.HTTP_403_FORBIDDEN)
  _ = await delete_comment(db, id=comment_id)

# @router.post("/{comment_id}/comment", responses=generate_error_responses({401, 404}))
# async def comment(
#   comment_id: UUID,
#   content: str,
#   user: cookieDep
# ):
#   post = await post_comment(db, content=content, comment_id=comment_id, user_id=user.id)
#   if post is None:
#     raise HTTPException(status.HTTP_404_NOT_FOUND)

