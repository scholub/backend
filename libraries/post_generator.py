import asyncio
import os

import PyPDF2
from openai import OpenAI

from .paper import download_arxiv

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def generate_post(paper_id: str):
    paper = await download_arxiv(paper_id)
    

    with open(paper, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()

    text = text.replace("\n", "")

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role":"system","content":"You are a helpful AI assistant"},
            {"role":"user","content":f"논문 요약을 뉴스 형태로 생성해 주세요. 당신은 이 논문을 처음 보았다고 가정합니다. 한국어로 생성해야합니다. \n\n{text}"}
        ]
    )

    print(completion.choices[0].message.content)


if __name__ == "__main__":
    asyncio.run(generate_post("1706.03762v7"))

