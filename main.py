from contextlib import asynccontextmanager

from libraries.initalizer import scheduler
from libraries.arxiv import refresh_cache

from routers.oauth import router as oauth_router
from routers.user import router as user_router

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:5173"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"]
)
app.include_router(oauth_router)
app.include_router(user_router)

@asynccontextmanager
async def on_start():
  _ = scheduler.add_job(refresh_cache, 'interval', days=1) # pyright: ignore[reportUnknownMemberType]
  yield
  scheduler.shutdown() # pyright: ignore[reportUnknownMemberType]

