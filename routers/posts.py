from datetime import datetime
from fastapi import APIRouter

from libraries.initalizer import db
from libraries.recommend import recomend_post, RecomendPostResult
from queries.posts import get_posts

from queries.posts import get_posts, get_posts_like_order


router = APIRouter(prefix="/posts", tags=["posts"])

@router.get("/posts")
async def posts():
  return await get_posts(db)


@router.get("/posts/recommend")
async def recommend_posts():


  return []

@router.get("/posts/like")
async def posts_like(
  start_date: datetime,
  end_date: datetime
):
  return await get_posts_like_order(db, start_date=start_date, end_date=end_date)


