from asyncio import run

from PyPDF2 import PdfReader

from libraries.paper import download_arxiv
from libraries.paper_reviewer import Reviewer

paper_id = input()
paper_path = run(download_arxiv(paper_id))
paper_content = PdfReader(paper_path)
result = ""
for i in paper_content.pages:
  result += f"{i.extract_text()}\n"
r = Reviewer(model="o4-mini", prompts_dir="./libraries/paper_reviewer/prompts")
print(run(r.review(result, reflection=2))) # pyright: ignore[reportUnknownArgumentType, reportUnknownMemberType]
