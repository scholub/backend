from collections.abc import AsyncGenerator
from datetime import UTC, datetime, timedelta
from os.path import getmtime
from pathlib import Path

from arxiv import (  # pyright: ignore[reportMissingTypeStubs]
  Client,
  Search,
  SortCriterion,
)

from libraries.initalizer import db, get_data_path
from queries.cache import gc_cache

client = Client()
slow_client = Client(page_size=1000, num_retries=5, delay_seconds=10)

async def get_recent_posts() -> AsyncGenerator[str, None]:
  result_generator = slow_client.results(
    Search(
      query = "cat:cs.AI",
      sort_by = SortCriterion.SubmittedDate
    )
  )
  result = next(result_generator)
  now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
  while result.published < now:
    yield result.entry_id
    result = next(result_generator)

async def download_arxiv(paper_id: str, force: bool = False) -> Path:
  paper = next(client.results(
    Search(id_list=[paper_id])
  ))
  cache = get_data_path("cache") / f"{paper_id}.pdf"
  if not force:
    if cache.exists():
      return cache
  _ = paper.download_pdf(dirpath=get_data_path("cache").as_posix(), filename=f"{paper_id}.pdf")
  return cache

async def refresh_cache():
  print("starting refresh of arxiv cache")
  yesterday = datetime.now() - timedelta(days=1)
  yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0).replace(tzinfo=UTC)
  papers = list(get_data_path("cache").glob("*.pdf"))
  for paper_cached in papers:
    if yesterday.timestamp() > getmtime(paper_cached):
      paper_cached.unlink()
  print("starting garbage collection of summarize cache")
  gc_cached = await gc_cache(db, datetime=yesterday)
  print("garbage collected summarize cache length:", gc_cached)

