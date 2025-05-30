from fastapi import APIRouter

from libraries.initalizer import db
from queries.posts import get_posts

router = APIRouter(prefix="/posts", tags=["posts"])

@router.get("/posts")
async def posts():
  return await get_posts(db)

