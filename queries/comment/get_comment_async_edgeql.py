# AUTOGENERATED FROM 'queries/comment/get_comment.edgeql' WITH:
#     $ gel-py --dir queries --no-skip-pydantic-validation


from __future__ import annotations
import dataclasses
import gel
import uuid


@dataclasses.dataclass
class GetCommentResult:
    id: uuid.UUID
    user: GetCommentResultUser


@dataclasses.dataclass
class GetCommentResultUser:
    id: uuid.UUID


async def get_comment(
    executor: gel.AsyncIOExecutor,
    *,
    id: uuid.UUID,
) -> GetCommentResult | None:
    return await executor.query_single(
        """\
        select Comment::Comment { user } filter .id = <uuid>$id;\
        """,
        id=id,
    )
