# AUTOGENERATED FROM 'queries/insert_paper.edgeql' WITH:
#     $ gel-py --dir queries --no-skip-pydantic-validation


from __future__ import annotations
import dataclasses
import datetime
import gel
import uuid


@dataclasses.dataclass
class InsertPaperResult:
    id: uuid.UUID


async def insert_paper(
    executor: gel.AsyncIOExecutor,
    *,
    paper_id: str,
    modified: datetime.datetime,
) -> InsertPaperResult:
    return await executor.query_single(
        """\
        insert Paper {
          paper_id := <str>$paper_id,
          modified := <datetime>$modified
        } unless conflict on .paper_id else (
          select (update Paper set {
            modified := <datetime>$modified
          })
        );\
        """,
        paper_id=paper_id,
        modified=modified,
    )
