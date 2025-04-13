from gel import create_async_client # pyright: ignore[reportUnknownVariableType]
from rocketry import Rocketry # pyright: ignore[reportMissingTypeStubs]

db = create_async_client()
scheduler = Rocketry(execution="asyncio")

