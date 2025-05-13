import asyncio
import os
from pathlib import Path
import json
import base64


import PyPDF2
from openai import OpenAI

from .paper import download_arxiv

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def generate_post(paper_id: str):
    paper_path = await download_arxiv(paper_id)
    prompt = Path("./prompts/post.txt").read_text()
    
    with open(paper_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
    text = text.replace("\n", "")
    prompt+=text
    

    completion = client.chat.completions.create(
        model="o4-mini",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant"},
            {"role": "user", "content": prompt}
        ]
    )
    print(completion.choices[0].message.content)
    post_data = json.loads(completion.choices[0].message.content)
    post_data.json.save(f"./files/post/{paper_id}.json")

    for i in post_data["images"]:
        result = client.images.generate(
            model="dall-e-3",
            prompt= i["prompt"],
            response_format="b64_json" 
        )

        image_base64 = result.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)

        # Save the image to a file
        with open(f"./files/post/{i["id"].png}", "wb") as f:
            f.write(image_bytes)
        



    return post_data

if __name__ == "__main__":
    asyncio.run(generate_post("2501.12948"))
