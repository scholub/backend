# AUTOGENERATED FROM 'queries/post/get_post.edgeql' WITH:
#     $ gel-py --dir queries


from __future__ import annotations
import dataclasses
import datetime
import gel
import uuid


class NoPydanticValidation:
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler):
        # Pydantic 2.x
        from pydantic_core.core_schema import any_schema
        return any_schema()

    @classmethod
    def __get_validators__(cls):
        # Pydantic 1.x
        from pydantic.dataclasses import dataclass as pydantic_dataclass
        _ = pydantic_dataclass(cls)
        cls.__pydantic_model__.__get_validators__ = lambda: []
        return []


@dataclasses.dataclass
class GetPostResult(NoPydanticValidation):
    id: uuid.UUID
    title: str
    description: str
    paper_id: str
    category: str
    tag: str
    created: datetime.datetime
    modified: datetime.datetime
    like_count: int
    dislike_count: int


async def get_post(
    executor: gel.AsyncIOExecutor,
    *,
    paper_id: str,
) -> GetPostResult | None:
    return await executor.query_single(
        """\
        select Paper::Post {
          title,
          description,
          paper_id,
          category,
          tag,
          created,
          modified,
          like_count,
          dislike_count
        } filter .paper_id = <str>$paper_id;\
        """,
        paper_id=paper_id,
    )
