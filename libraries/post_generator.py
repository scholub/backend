import asyncio
import base64
import json
import os
from pathlib import Path

import PyPDF2
from openai import OpenAI
from pydantic import BaseModel

from .initalizer import get_data_path
from .paper import download_arxiv

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
    reader = PyPDF2.PdfReader(file)
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
    _ = (get_data_path("post") / f"{paper_id}/{i.id}.png").write_bytes(image_bytes)
    completion.content = completion.content.replace(
      i.id,
      (get_data_path("post").relative_to(os.getcwd()) / f"{paper_id}/{i.id}.png").as_uri()
    )

  _ = (get_data_path("post") / f"{paper_id}/post.md").write_text(
    json.dumps(completion.content, ensure_ascii=False, indent=4
  ))

  return completion.content

if __name__ == "__main__":
  print(asyncio.run(generate_post("2501.12948")))
