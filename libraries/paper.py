from arxiv import Client, Search  # pyright: ignore[reportMissingTypeStubs]

from .initalizer import db
from queries.paper import (
  get_cache,
  get_caches,
  insert_cache,
)

from pathlib import Path

client = Client()

async def download_arxiv(paper_id: str, force: bool = False) -> Path:
  paper = next(client.results(
    Search(id_list=[paper_id])
  ))
  if not force:
    if await get_cache(db, paper_id=paper_id):
      return Path("./files") / f"{paper_id}.pdf"
  _ = paper.download_pdf(dirpath="./files", filename=f"{paper_id}.pdf")
  _ = await insert_cache(
    db,
    paper_id=paper_id,
    modified=paper.updated
  )
  return Path("./files") / f"{paper_id}.pdf"

async def refresh_cache():
  papers = await get_caches(db)
  paper_ids = [i.paper_id for i in papers]
  slow_client = Client(num_retries=5, delay_seconds=10)
  for paper, paper_cached in zip(slow_client.results(Search(id_list=paper_ids)), papers):
    if paper_cached.modified != paper.updated:
      _ = paper.download_pdf(dirpath="./files", filename=f"{paper_cached.paper_id}.pdf")
      _ = await insert_cache(db, paper_id=paper_cached.paper_id, modified=paper.updated)

