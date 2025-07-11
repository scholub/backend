# AUTOGENERATED FROM 'queries/posts/get_posts.edgeql' WITH:
#     $ gel-py --dir queries


from __future__ import annotations
import dataclasses
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
class GetPostsResult(NoPydanticValidation):
    id: uuid.UUID
    title: str
    description: str
    paper_id: str


async def get_posts(
    executor: gel.AsyncIOExecutor,
) -> list[GetPostsResult]:
    return await executor.query(
        """\
        select Paper::Post {
          title,
          description,
          paper_id
        } order by (.like_count - .dislike_count) desc;\
        """,
    )
