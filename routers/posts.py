from datetime import datetime, time

from fastapi import APIRouter

from libraries.auth import cookieDep
from libraries.initalizer import db
from queries.posts import (
  GetPostsLikeOrderResult,
  GetPostsResult,
  get_posts,
  get_posts_like_order,
)
from queries.user import GetRecommendsResultRecommendsItem, get_recommends

router = APIRouter(prefix="/posts", tags=["posts"])

@router.get("/")
async def posts() -> list[GetPostsResult]:
  return await get_posts(db)


@router.get("/recommend")
async def recommend_posts(user: cookieDep) -> list[GetRecommendsResultRecommendsItem]:
  resp = await get_recommends(db, email=user.email)
  if resp is not None:
    return resp.recommends
  return []

@router.get("/like")
async def posts_like(
  start_date: datetime | None = None,
  end_date: datetime | None = None
) -> list[GetPostsLikeOrderResult]:
  if start_date is None:
    today = datetime.now().date()
    start_date = datetime.combine(today, time.min).replace(tzinfo=datetime.now().astimezone().tzinfo)
  if end_date is None:
    today = datetime.now().date()
    end_date = datetime.combine(today, time.max).replace(tzinfo=datetime.now().astimezone().tzinfo)
  return await get_posts_like_order(db, start_date=start_date, end_date=end_date)


