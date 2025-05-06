from arxiv import Client, Search  # pyright: ignore[reportMissingTypeStubs]

from queries.paper import (
  GetCacheResult,
  InsertCacheResult,
  get_cache,
  get_caches,
  insert_cache,
)

from .initalizer import db

client = Client()

async def download_arxiv(paper_id: str, force: bool = False) -> InsertCacheResult | GetCacheResult:
  paper = next(client.results(
    Search(id_list=[paper_id])
  ))
  if not force:
    paper_cached = await get_cache(db, paper_id=paper_id)
    if paper_cached:
      return paper_cached
  _ = paper.download_pdf(dirpath="./files", filename=f"{paper_id}.pdf")
  return await insert_cache(
    db,
    paper_id=paper_id,
    modified=paper.updated
  )

async def refresh_cache():
  papers = await get_caches(db)
  paper_ids = [i.paper_id for i in papers]
  slow_client = Client(num_retries=5, delay_seconds=10)
  for paper, paper_cached in zip(slow_client.results(Search(id_list=paper_ids)), papers):
    if paper_cached.modified != paper.updated:
      _ = paper.download_pdf(dirpath="./files", filename=f"{paper_cached.paper_id}.pdf")
      _ = await insert_cache(db, paper_id=paper_cached.paper_id, modified=paper.updated)

