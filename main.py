from contextlib import asynccontextmanager

from libraries.arxiv import refresh_cache

from fastapi import FastAPI
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler # pyright: ignore[reportMissingTypeStubs]

_ = load_dotenv()

app = FastAPI()

@asynccontextmanager
async def on_start():
  scheduler = BackgroundScheduler()
  _ = scheduler.add_job(refresh_cache, 'interval', days=1) # pyright: ignore[reportUnknownMemberType]
  yield
  scheduler.shutdown() # pyright: ignore[reportUnknownMemberType]

@app.get("/")
async def root():
  return {"message": "Hello World"}

