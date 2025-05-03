from dotenv import load_dotenv
from gel import create_async_client # pyright: ignore[reportUnknownVariableType]
from apscheduler.schedulers.background import BackgroundScheduler # pyright: ignore[reportMissingTypeStubs]

from os import getenv

_ = load_dotenv()
scheduler = BackgroundScheduler()
db = create_async_client()
SECRET_KEY = getenv("SECRET_KEY", "")
if SECRET_KEY == "":
  print("SECRET_KEY is none")
  exit(1)

