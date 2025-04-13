from arxiv import Client, Search, SortCriterion # pyright: ignore[reportMissingTypeStubs]

from .db import db
from queries.insert_paper_async_edgeql import insert_paper, InsertPaperResult
from queries.get_paper_async_edgeql import get_paper, GetPaperResult

client = Client()

async def download_arxiv(paper_id: str, force: bool = False) -> InsertPaperResult | GetPaperResult:
  paper = next(client.results(
    Search(id_list=[paper_id])
  ))
  if not force:
    paper_cached = await get_paper(db, paper_id=paper_id)
    if paper_cached:
      return paper_cached
  _ = paper.download_pdf(dirpath="./files", filename=f"{paper_id}.pdf")
  return await insert_paper(
    db,
    paper_id=paper_id,
    modified=paper.updated
  )

async def refresh_paper(paper_id: str):
  paper_cached = await get_paper(db, paper_id=paper_id)
  paper = next(client.results(
    Search(id_list=[paper_id])
  ))
  if paper_cached is None:
    raise ValueError("Unreachable")
  if paper_cached.modified != paper.updated:
    _ = paper.download_pdf(dirpath="./files", filename=f"{paper_id}.pdf")
    _ = await insert_paper(db, paper_id=paper_id, modified=paper.updated)

