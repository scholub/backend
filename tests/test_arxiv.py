from hashlib import sha3_512
from os import utime
from pathlib import Path
from shutil import rmtree

from arxiv import Client, Search  # pyright: ignore[reportMissingTypeStubs]

from libraries.initalizer import get_data_path
from libraries.paper import download_arxiv, refresh_cache

# @fixture(scope='session')
# def event_loop():
#   policy = get_event_loop_policy()
#   loop = policy.new_event_loop()
#   yield loop
#   loop.close()

client = Client()

rmtree(get_data_path("cache"), ignore_errors=True)
_ = next(
  client.results(Search(id_list=["2412.19437"]))
).download_pdf(
  get_data_path("cache").as_posix(),
  "2412.19437_compare.pdf"
)

def get_hash(path: Path) -> str:
  return sha3_512(path.read_bytes()).hexdigest()

async def init():
  for i in get_data_path("cache").glob("*"):
    i.unlink()

class TestArxivCache:
  async def test_init(self):
    await init()

  async def test_download_arxiv(self):
    assert not (get_data_path("cache") / "2412.19437.pdf").exists()
    _ = await download_arxiv("2412.19437")

class TestArxivRefreshCache:
  async def test_refresh_cache(self):
    paper = next(client.results(Search(id_list=["2412.19437v1"])))
    _ = paper.download_pdf(get_data_path("cache").as_posix(), "2412.19437.pdf")
    file_path = get_data_path("cache") / "2412.19437.pdf"
    utime(file_path, (0, 0))
    await refresh_cache()
    assert not file_path.exists()

