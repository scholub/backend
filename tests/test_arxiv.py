from hashlib import sha3_512
from os import utime
from os.path import getctime, getmtime
from pathlib import Path
from shutil import rmtree

from arxiv import Client, Search  # pyright: ignore[reportMissingTypeStubs]

from libraries.initalizer import db
from libraries.paper import download_arxiv, refresh_cache

# @fixture(scope='session')
# def event_loop():
#   policy = get_event_loop_policy()
#   loop = policy.new_event_loop()
#   yield loop
#   loop.close()

client = Client()
rmtree("./files/cache", ignore_errors=True)
_ = next(client.results(Search(id_list=["2412.19437"]))).download_pdf("./files", "2412.19437_compare.pdf")

def get_hash(path: str) -> str:
  return sha3_512(Path(path).read_bytes()).hexdigest()

async def init():
  await db.execute("DELETE Paper::Paper;") # pyright: ignore[reportUnknownMemberType]
  for i in Path("./files").glob("*"):
    i.unlink()

class TestArxivCache:
  async def test_init(self):
    await init()

  async def test_download_arxiv(self):
    assert not Path("./files/2412.19437.pdf").exists()
    _ = await download_arxiv("2412.19437")

class TestArxivRefreshCache:
  async def test_refresh_cache(self):
    paper = next(client.results(Search(id_list=["2412.19437v1"])))
    _ = paper.download_pdf("./files", "2412.19437.pdf")
    utime(Path("./files/2412.19437.pdf"), (0, 0))
    hash = get_hash("./files/2412.19437.pdf")
    modified = getmtime("./files/2412.19437.pdf")
    created = getctime("./files/2412.19437.pdf")
    await refresh_cache()
    refreshed = Path("./files/2412.19437.pdf")
    assert modified < getmtime(refreshed)
    assert created < getctime(refreshed)
    assert hash != get_hash("./files/2412.19437.pdf")

