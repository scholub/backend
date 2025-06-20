from fastapi import APIRouter

from libraries.initalizer import db
from libraries.recommend import recomend_post, RecomendPostResult
from queries.posts import get_posts

router = APIRouter(prefix="/posts", tags=["posts"])

@router.get("/posts")
async def posts():
  return await get_posts(db)

@router.get("/posts/recommend")
async def recommend_posts():


  return []