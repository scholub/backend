from datetime import datetime
from os.path import getmtime
from pathlib import Path

from arxiv import (  # pyright: ignore[reportMissingTypeStubs]
  Client,
  Search,
  SortCriterion,
)

from libraries.initalizer import (
  get_data_path,
)

client = Client()
slow_client = Client(page_size=1000, num_retries=5, delay_seconds=10)

async def download_recent_posts():
  result_generator = slow_client.results(
    Search(
      query = "cat:cs.AI",
      sort_by = SortCriterion.SubmittedDate
    )
  )
  result = next(result_generator)
  now = datetime.now().date()
  while result.published < now:
    yield download_arxiv(result.entry_id)
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
  papers = list(get_data_path("cache").glob("*.pdf"))
  paper_ids = [i.stem for i in papers]
  for paper, paper_cached in zip(slow_client.results(Search(id_list=paper_ids)), papers):
    if paper.updated.timestamp() > getmtime(paper_cached):
      paper_cached.unlink()
      _ = paper.download_pdf(dirpath=get_data_path("cache").as_posix(), filename=paper_cached.name)

