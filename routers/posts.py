from datetime import datetime

from fastapi import APIRouter

from libraries.auth import cookieDep
from libraries.initalizer import db
from queries.posts import get_posts, get_posts_like_order
from queries.user import GetRecommendsResultRecommendsItem, get_recommends

router = APIRouter(prefix="/posts", tags=["posts"])

@router.get("/")
async def posts():
  return await get_posts(db)


@router.get("/recommend")
async def recommend_posts(user: cookieDep) -> list[GetRecommendsResultRecommendsItem]:
  resp = await get_recommends(db, email=user.email)
  if resp is not None:
    return resp.recommends
  return []

@router.get("/like")
async def posts_like(
  start_date: datetime,
  end_date: datetime
):
  return await get_posts_like_order(db, start_date=start_date, end_date=end_date)


