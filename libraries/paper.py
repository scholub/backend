from os.path import getmtime
from pathlib import Path

from arxiv import Client, Search  # pyright: ignore[reportMissingTypeStubs]

client = Client()

async def download_arxiv(paper_id: str, force: bool = False) -> Path:
  paper = next(client.results(
    Search(id_list=[paper_id])
  ))
  cache = Path(f"./files/{paper_id}.pdf")
  if not force:
    if cache.exists():
      return Path("./files") / f"{paper_id}.pdf"
  _ = paper.download_pdf(dirpath="./files", filename=f"{paper_id}.pdf")
  return Path("./files") / f"{paper_id}.pdf"

async def refresh_cache():
  papers = list(Path("./files").glob("*.pdf"))
  paper_ids = [i.stem for i in papers]
  slow_client = Client(num_retries=5, delay_seconds=10)
  for paper, paper_cached in zip(slow_client.results(Search(id_list=paper_ids)), papers):
    if paper.updated.timestamp() > getmtime(paper_cached):
      paper_cached.unlink()
      _ = paper.download_pdf(dirpath="./files", filename=paper_cached.name)

