from libraries.initalizer import db
from libraries.arxiv import download_arxiv, refresh_cache
from queries.paper import get_cache, insert_cache

from arxiv import Client, Search # pyright: ignore[reportMissingTypeStubs]

from hashlib import sha3_512
from pathlib import Path
from shutil import rmtree

# @fixture(scope='session')
# def event_loop():
#   policy = get_event_loop_policy()
#   loop = policy.new_event_loop()
#   yield loop
#   loop.close()

client = Client()
rmtree("./files", ignore_errors=True)
Path("./files").mkdir()
_ = next(client.results(Search(id_list=["2412.19437"]))).download_pdf("./files", "2412.19437_compare.pdf")

def get_hash(path: str) -> str:
  return sha3_512(Path(path).read_bytes()).hexdigest()

async def init():
  await db.execute("DELETE Paper::Paper;") # pyright: ignore[reportUnknownMemberType]
  await db.execute("DELETE Paper::Cache;") # pyright: ignore[reportUnknownMemberType]

class TestArxivCache:
  async def test_init(self):
    await init()

  async def test_download_non_cached_pdf(self):
    assert await get_cache(db, paper_id="2412.19437") is None
    _ = await download_arxiv("2412.19437")

  async def test_download_cached_pdf(self):
    assert await get_cache(db, paper_id="2412.19437") is not None
    _ = await download_arxiv("2412.19437")
    assert get_hash("./files/2412.19437.pdf") == get_hash("./files/2412.19437_compare.pdf")


class TestArxivRefreshCache:
  async def test_refresh_cache(self):
    paper = next(client.results(Search(id_list=["2412.19437v1"])))
    _ = paper.download_pdf("./files", "2412.19437.pdf")
    result = await insert_cache(db, paper_id="2412.19437", modified=paper.updated)
    hash = get_hash("./files/2412.19437.pdf")
    await refresh_cache()
    refreshed = await get_cache(db, paper_id="2412.19437")
    if refreshed is None:
      raise ValueError("Unreachable")
    assert result.paper_id == refreshed.paper_id
    assert result.modified < refreshed.modified
    assert hash != get_hash("./files/2412.19437.pdf")

