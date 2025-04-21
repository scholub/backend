from contextlib import asynccontextmanager
from os import getenv

from libraries.initalizer import scheduler
from libraries.arxiv import refresh_cache

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv

_ = load_dotenv()
SECRET_KEY = getenv("SECRET_KEY")
if SECRET_KEY is None:
  print("SECRET_KEY is none")
  exit(1)

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

@asynccontextmanager
async def on_start():
  _ = scheduler.add_job(refresh_cache, 'interval', days=1) # pyright: ignore[reportUnknownMemberType]
  yield
  scheduler.shutdown() # pyright: ignore[reportUnknownMemberType]

