from os import getenv

from apscheduler.schedulers.background import (
  BackgroundScheduler,  # pyright: ignore[reportMissingTypeStubs]
)
from dotenv import load_dotenv
from gel import create_async_client  # pyright: ignore[reportUnknownVariableType]

_ = load_dotenv()
scheduler = BackgroundScheduler()
db = create_async_client()
SECRET_KEY = getenv("SECRET_KEY", "")
if SECRET_KEY == "":
  print("SECRET_KEY is none")
  exit(1)

