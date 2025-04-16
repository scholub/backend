from gel import create_async_client # pyright: ignore[reportUnknownVariableType]
from apscheduler.schedulers.background import BackgroundScheduler # pyright: ignore[reportMissingTypeStubs]

scheduler = BackgroundScheduler()
db = create_async_client()

