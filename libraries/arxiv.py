from arxiv import Client, Search, SortCriterion # pyright: ignore[reportMissingTypeStubs]

from queries.insert_paper_async_edgeql import insert_paper, InsertPaperResult
from queries.get_paper_async_edgeql import get_paper, GetPaperResult
from queries.get_papers_async_edgeql import get_papers

from .initalizer import db, scheduler

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

@scheduler.task("daily") # pyright: ignore[reportUnknownMemberType, reportUntypedFunctionDecorator]
async def refresh_cache():
  papers = await get_papers(db)
  paper_ids = [i.paper_id for i in papers]
  slow_client = Client(num_retries=5, delay_seconds=10)
  for paper, paper_cached in zip(slow_client.results(Search(id_list=paper_ids)), papers):
    if paper_cached.modified != paper.updated:
      _ = paper.download_pdf(dirpath="./files", filename=f"{paper_cached.paper_id}.pdf")
      _ = await insert_paper(db, paper_id=paper_cached.paper_id, modified=paper.updated)

