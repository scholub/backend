from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from libraries.initalizer import scheduler
from libraries.paper import refresh_cache
from libraries.post_generator import refresh_paper
from routers.comment import router as comment_router
from routers.oauth import router as oauth_router
from routers.post import router as post_router
from routers.user import router as user_router


@asynccontextmanager
async def on_start(app: FastAPI): # pyright: ignore[reportUnusedParameter]
  _ = scheduler.add_job(refresh_cache, 'interval', days=1) # pyright: ignore[reportUnknownMemberType]
  _ = scheduler.add_job(refresh_paper, 'interval', days=1) # pyright: ignore[reportUnknownMemberType]
  _ = scheduler.start()
  yield
  scheduler.shutdown()

app = FastAPI(lifespan=on_start)
app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:5173"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"]
)
app.include_router(oauth_router)
app.include_router(user_router)
app.include_router(post_router)
app.include_router(comment_router)


