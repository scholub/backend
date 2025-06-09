from os import getenv
from pathlib import Path

from apscheduler.schedulers.asyncio import (  # pyright: ignore[reportMissingTypeStubs]
  AsyncIOScheduler,
)
from dotenv import load_dotenv
from gel import create_async_client  # pyright: ignore[reportUnknownVariableType]

_ = load_dotenv()
scheduler = AsyncIOScheduler()
db = create_async_client()
SECRET_KEY = getenv("SECRET_KEY", "")
if SECRET_KEY == "":
  print("SECRET_KEY is none")
  exit(1)
DATA_PATH = Path(getenv("DATA_PATH", "./files"))
def get_data_path(name: str):
  CACHE_PATH = DATA_PATH / name
  if not CACHE_PATH.is_dir():
    CACHE_PATH.mkdir(parents=True)
  return CACHE_PATH

