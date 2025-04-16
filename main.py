from contextlib import asynccontextmanager

from libraries.initalizer import scheduler
from libraries.arxiv import refresh_cache

from fastapi import FastAPI
from dotenv import load_dotenv

_ = load_dotenv()

app = FastAPI()

@asynccontextmanager
async def on_start():
  _ = scheduler.add_job(refresh_cache, 'interval', days=1) # pyright: ignore[reportUnknownMemberType]
  yield
  scheduler.shutdown() # pyright: ignore[reportUnknownMemberType]

