import asyncio
import base64
import os
from contextlib import suppress
from pathlib import Path

import pypdf
from gel.errors import ConstraintViolationError
from openai import OpenAI
from pydantic import BaseModel
from pypdf.errors import PdfStreamError

from queries.cache import get_cache, insert_cache
from queries.post import insert_post

from .initalizer import db, get_data_path
from .paper import download_arxiv, get_recent_posts
from .paper_reviewer.reviewer import Reviewer

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class PaperInfo(BaseModel):
  title: str
  author: str

class ImageInfo(BaseModel):
  id: str
  prompt: str

class Article(BaseModel):
  title: str
  subtitle: str
  summary: str
  paper_info: PaperInfo
  content: str
  images: list[ImageInfo]

async def generate_post(paper_id: str):
  paper_path = await download_arxiv(paper_id)
  prompt = Path("./prompts/post.txt").read_text()

  with open(paper_path, "rb") as file:
    reader = pypdf.PdfReader(file)
    text = ""
    for page in reader.pages:
      text += page.extract_text() or ""
  text = text.replace("\n", "")
  prompt += text

  completion = client.beta.chat.completions.parse(
    model="o4-mini",
    messages=[
      {"role": "system", "content": "You are a helpful AI assistant"},
      {"role": "user", "content": prompt}
    ],
    response_format=Article
  ).choices[0].message.parsed

  if completion is None:
    raise ValueError("completion failed")

  for i in completion.images:
    result = client.images.generate(
      model="dall-e-3",
      prompt=i.prompt,
      response_format="b64_json"
    )

    data = result.data
    if data is None:
      raise ValueError("Image generation failed")
    image_base64 = data[0].b64_json
    if image_base64 is None:
      raise ValueError("Image generation succeed, but doesn't have image data")
    image_bytes = base64.b64decode(image_base64)
    post_path = get_data_path(f"post/{paper_id}")
    _ = (post_path / f"{i.id}.png").write_bytes(image_bytes)
    completion.content = completion.content.replace(
      i.id,
      f"/{str(post_path)}/{i.id}.png"
    )

  _ = (get_data_path("post") / f"{paper_id}/post.md").write_text(completion.content)
  _ = await insert_post(
    db,
    title=completion.title,
    description=completion.summary,
    paper_id=paper_id,
    category="",
    tag="",
    embedding=client.embeddings.create(
      input=completion.content,
      model="text-embedding-3-small"
    ).data[0].embedding
  )

  return completion.content


async def refresh_paper():
  print("start summarize paper")
  async for paper_id in get_recent_posts():
    if await get_cache(db, paper_id=paper_id) is not None:
      print(paper_id, "already summarized")
      continue
    print(paper_id, "summarizing")
    paper_path = await download_arxiv(paper_id)
    with suppress(PdfStreamError):
      paper_content = pypdf.PdfReader(paper_path)
      result = ""
      for i in paper_content.pages:
        result += f"{i.extract_text()}\n"
      
      r = Reviewer(model="o4-mini", prompts_dir="./libraries/paper_reviewer/prompts/paper_review")
      _ = await r.review(result, reflection=2) # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]
      _ = await r.review_ensembling() # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]
      if r.is_review_strong_enough():
        print(paper_id, "has strong potential")
        _ = await generate_post(paper_id=paper_id)
      with suppress(ConstraintViolationError):
        _ = await insert_cache(db, paper_id=paper_id)

if __name__ == "__main__":
  print(asyncio.run(generate_post("2501.12948")))
